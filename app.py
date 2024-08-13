from urllib.parse import urljoin
from bs4 import BeautifulSoup
from flask import Flask, request, Response
import json
import Levenshtein
import pykakasi
import itertools
import requests

app = Flask(__name__)

# JSONファイルからデータを読み込む
with open('allwords.json', 'r', encoding='utf-8') as jsonfile:
    japanese_words = json.load(jsonfile)

# kakasiの新しいAPIを使用して初期化
kks = pykakasi.kakasi()

def convert_to_hiragana(text):
    result = kks.convert(text)
    return "".join([entry['hira'] for entry in result])


def convert_to_romaji(text):
    hiragana_text = convert_to_hiragana(text)
    romaji = ""
    i = 0
    while i < len(hiragana_text):
        char = hiragana_text[i]
        
        # 「ん」の場合は「nn」とする
        if char == 'ん':
            romaji += 'nn'
            i += 1
        # 「つ」の場合は、"tu"にする
        elif char == 'つ':
            romaji += 'tu'
            i += 1
        elif char == 'し' and i < len(hiragana_text) - 1 and hiragana_text[i + 1] in ['ゃ', 'ゅ', 'ょ']:
            result = kks.convert(hiragana_text[i+1])
            romaji += 's' + "".join([entry['hepburn'] for entry in result])
            i += 2
        elif char == 'し':
            romaji += 'si'
            i += 1
        elif char == 'ち' and i < len(hiragana_text) - 1 and hiragana_text[i + 1] in ['ゃ', 'ゅ', 'ょ']:
            result = kks.convert(hiragana_text[i+1])
            romaji += 't' + "".join([entry['hepburn'] for entry in result])
            i += 2
        elif char == 'ち':
            romaji += 'ti'
            i += 1
        # 「っ」が続く場合、次の文字の最初の子音を重ねる
        elif char == 'っ' and i < len(hiragana_text) - 1:
            next_char_romaji = kks.convert(hiragana_text[i+1])[0]['hepburn']
            if next_char_romaji:
                romaji += next_char_romaji[0]
            i += 1
        # 小さい「や」「ゆ」「よ」が続く場合
        elif i < len(hiragana_text) - 1 and hiragana_text[i + 1] in ['ゃ', 'ゅ', 'ょ']:
            result = kks.convert(hiragana_text[i:i+2])
            romaji += "".join([entry['hepburn'] for entry in result])
            i += 2
        else:
            result = kks.convert(char)
            romaji += "".join([entry['hepburn'] for entry in result])
            i += 1

    return romaji

#言いづらさを評価する評価関数
def evaluate_word(word):
    # wordのローマ字を取得
    romaji = convert_to_romaji(word)
    # ローマ字を特定のセットに分割する
    parts = split_into_parts(romaji)
    # ま行が多く含まれているとポイントゲット
    points = sum(part in ['ma', 'mi', 'mu', 'me', 'mo'] for part in parts)


def get_youon(word):
    #もし、 wordが「か行、さ行、た行、な行、は行、ま行、ら行」の文字を含む場合、その行の拗音を早口言葉のワード候補に入れる
    youon_list = []
    # 各行の文字と対応する拗音
    rows = {
        "ま行": (["ま", "み", "む", "め", "も","ば", "び", "ぶ", "べ", "ぼ","ぱ", "ぴ", "ぷ", "ぺ", "ぽ"], ["みゃ","みゅ","みょ","びゃ","びゅ","びょ","ぴゃ","ぴゅ","ぴょ"]),
        "か行": (["か", "き", "く", "け", "こ","が", "ぎ", "ぐ", "げ", "ご"], ["きゃ","きゅ","きょ","ぎゃ","ぎゅ","ぎょ"]),
        "な行": (["な", "に", "ぬ", "ね", "の"], ["にゃ","にゅ","にょ"]),
        "ら行": (["ら", "り", "る", "れ", "ろ"], ["りゃ","りゅ","りょ"]),
        "さ行": (["さ", "し", "す", "せ", "そ","ざ", "じ", "ず", "ぜ", "ぞ"], ["しゃ","しゅ","しょ","じゃ","じゅ","じょ","ぢゃ","ぢゅ","ぢょ"]),
        "た行": (["た", "ち", "つ", "て", "と"], ["ちゃ","ちゅ","ちょ"]),
    }

    # Count the occurrences of each group's characters in the word
    # 各行の文字が単語に何回出現するかをカウントする
    counts = {}
    for row, (chars, youon) in rows.items():
        # 単語内の各文字の出現回数をカウントし、その合計を取得
        counts[row] = sum(word.count(char) for char in chars)
 # 最大のカウントを持つ行を見つける
    max_row = max(counts, key=counts.get)

    # 最大のカウントを持つ行の拗音を返す
    for row, (chars, youon) in rows.items():
        if row == max_row:
            return youon


    return youon_list

def get_youon_word(youon_list):
    # 早口言葉のワード候補を作成する
    youon_word_list = []
    for youon in youon_list:
        # youonを含む単語をjaonese_wordsから探す
        for word, romaji in japanese_words.items():
            for part in split_into_parts(romaji):
                if convert_to_romaji(youon) == part:
                    youon_word_list.append(word)
                    break
    return youon_word_list

# アナグラムを生成
def generate_anagrams(word):
    romaji_word = convert_to_romaji(word)
    return generate_anagram_with_romaji_word(romaji_word)

def generate_anagram_with_romaji_word(romaji_word):
    parts = split_into_parts(romaji_word)
    anagrams = set([''.join(p) for p in itertools.permutations(parts)])

    # 一致する日本語の単語を見つける
    matching_words = []
    for anagram in anagrams:
        if anagram in japanese_words.values():
            # 対応する日本語の単語を追加
            matching_words.extend([jap_word for jap_word, romaji in japanese_words.items() if romaji == anagram])

    return matching_words  # 重複を除かずにリストを返す


# ローマ字を特定のセットに分割するロジックを実装する
def split_into_parts(romaji_word):
    parts = []
    i = 0
    while i < len(romaji_word):
        # nの処理 - 「ん」または「なにぬねの」
        if romaji_word[i] == 'n' and i < len(romaji_word) - 1 and romaji_word[i + 1]  in "naiueo":
            # "n"は独立した発音単位
            parts.append('n' + romaji_word[i + 1])
            i += 2
        elif romaji_word[i] == '-':
            # "-"は独立した発音単位
            parts.append('-')
            i += 1
        elif romaji_word[i] in "kstnhmrpbg" and i < len(romaji_word) - 2 and romaji_word[i + 1] == 'y':
            # 「にゃ」「にゅ」「にょ」の処理
            parts.append(romaji_word[i:i + 3])
            i += 3
        elif romaji_word[i] in "aiueo":
            # あいうえおの処理
            parts.append(romaji_word[i])
            i += 1
        elif romaji_word[i] not in "aiueo" and i < len(romaji_word) - 1 and romaji_word[i + 1] in "aiueo":
            # それ以外の場合、1文字を単位とする
            parts.append(romaji_word[i:i + 2])
            i += 2
        elif romaji_word[i] not in "aiueo" and i < len(romaji_word) - 2 and romaji_word[i+1] == romaji_word[i]:
            # 小さい「つ」
            parts.append(romaji_word[i])
            i += 1
        else:
            # それ以外の場合、1文字を単位とする
            parts.append(romaji_word[i])
            i += 1
    return parts

def replace_youon_with_normal(romaji):
    replacements = {
        'kya': 'ki', 'kyu': 'ki', 'kyo': 'ki',
        'sya': 'si', 'syu': 'si', 'syo': 'si',
        'tya': 'ti', 'tyu': 'ti', 'tyo': 'ti',
        'nya': 'ni', 'nyu': 'ni', 'nyo': 'ni',
        'hya': 'hi', 'hyu': 'hi', 'hyo': 'hi',
        'mya': 'mi', 'myu': 'mi', 'myo': 'mi',
        'rya': 'ri', 'ryu': 'ri', 'ryo': 'ri',
        'gya': 'gi', 'gyu': 'gi', 'gyo': 'gi',
        'ja': 'ji', 'ju': 'ji', 'jo': 'ji',
        'bya': 'bi', 'byu': 'bi', 'byo': 'bi',
        'pya': 'pi', 'pyu': 'pi', 'pyo': 'pi'
    }
    for youon, normal in replacements.items():
        romaji = romaji.replace(youon, normal)
    return romaji

def replace_normal_with_youon(romaji):
    replacements = {
        'ki': ['kya', 'kyu', 'kyo'],
        'si': ['sya', 'syu', 'syo'],
        'ti': ['tya', 'tyu', 'tyo'],
        'ni': ['nya', 'nyu', 'nyo'],
        'hi': ['hya', 'hyu', 'hyo'],
        'mi': ['mya', 'myu', 'myo'],
        'ri': ['rya', 'ryu', 'ryo'],
        'gi': ['gya', 'gyu', 'gyo'],
        'ji': ['ja', 'ju', 'jo'],
        'bi': ['bya', 'byu', 'byo'],
        'pi': ['pya', 'pyu', 'pyo']
    }
    youon_variants = [romaji]
    for normal, youons in replacements.items():
        if normal in romaji:
            for youon in youons:
                youon_variants.append(romaji.replace(normal, youon))
    return youon_variants

def generate_romaji_variants(romaji_word):
    romaji_variants = [romaji_word, replace_youon_with_normal(romaji_word)] + replace_normal_with_youon(romaji_word)
    return romaji_variants

def three_letters_romaji_variants(romaji_word):
    romaji_variants = []
    # 最初の3文字と最後の3文字を追加
    parts = split_into_parts(romaji_word)
    if len(parts) >= 3:
        prefix = ''.join(parts[:3])
        suffix = ''.join(parts[-3:])
        romaji_variants.append(prefix)
        romaji_variants.append(suffix)
        romaji_variants.append(replace_youon_with_normal(prefix))
        romaji_variants.append(replace_youon_with_normal(suffix))
        romaji_variants.append(generate_anagram_with_romaji_word(prefix))
        romaji_variants.append(generate_anagram_with_romaji_word(suffix))
        romaji_variants += replace_normal_with_youon(prefix)
        romaji_variants += replace_normal_with_youon(suffix)
    
    
    return romaji_variants

def two_letters_romaji_variants(romaji_word):
    romaji_variants = []
    # 最初の2文字と最後の2文字を追加
    parts = split_into_parts(romaji_word)
    if len(parts) >= 2:
        prefix = ''.join(parts[:2])
        suffix = ''.join(parts[-2:])
        romaji_variants.append(prefix)
        romaji_variants.append(suffix)
        romaji_variants.append(replace_youon_with_normal(prefix))
        romaji_variants.append(replace_youon_with_normal(suffix))
        romaji_variants.append(generate_anagram_with_romaji_word(prefix))
        romaji_variants.append(generate_anagram_with_romaji_word(suffix))
        romaji_variants += replace_normal_with_youon(prefix)
        romaji_variants += replace_normal_with_youon(suffix)
    
    return romaji_variants

@app.route('/get_youon_words', methods=['POST'])
def get_youon_words():
    data = request.json
    word = data.get('word')
    youon_list = get_youon(word)
    youon_word_list = get_youon_word(youon_list)
    # JSONレスポンスを生成して返す
    return Response(json.dumps(youon_word_list, ensure_ascii=False),
                    mimetype='application/json')

# アナグラムを見つけるAPIルート
@app.route('/find_anagrams', methods=['POST'])
def find_anagrams():
    data = request.json
    word = data.get('word')
    anagrams = generate_anagrams(word)

    # JSONレスポンスを生成して返す
    return Response(json.dumps(list(anagrams), ensure_ascii=False),
                    mimetype='application/json')


@app.route('/find_similar_words', methods=['POST'])
def find_similar_words():
    data = request.json
    word = data.get('word')

    # ローマ字に変換
    romaji_word = convert_to_romaji(word)

    # 閾値を設定（入力単語の長さの1/3）
    threshold = len(romaji_word) // 3
    # Levenshtein距離を計算して似ている単語を見つける
    similar_words = []
    romaji_variants = generate_romaji_variants(romaji_word)
    for variant in romaji_variants:
        for jap_word, romaji in japanese_words.items():
            # Levenshtein距離を計算
            if Levenshtein.distance(variant, romaji) <= threshold:
                similar_words.append(jap_word)
            # wordとおなじ言葉を含んでいる単語を見つける
            # 例: momo => sumomo
            elif variant in romaji:
                similar_words.append(jap_word)

    # JSONレスポンスを生成して返す
    return Response(json.dumps(list(set(similar_words)), ensure_ascii=False),
                    mimetype='application/json')


@app.route('/find_similar_and_anagrams', methods=['POST'])
def find_similar_and_anagrams():
    data = request.json
    word = data.get('word')

    # ローマ字に変換
    romaji_word = convert_to_romaji(word)
    two_letter_variants = two_letters_romaji_variants(romaji_word)
    three_letter_variants = three_letters_romaji_variants(romaji_word)

    # 初期の閾値を設定（入力単語の長さの1/5）
    threshold = len(romaji_word) // 5
    two_letters_threshold = len(4) // 5
    three_letters_threshold = len(6) // 5

    similar_words = []
    while len(similar_words) <= 5:
        # 音が似ている単語を見つける
        similar_words = []
        romaji_variants = generate_romaji_variants(romaji_word)
        for variant in romaji_variants:
            for jap_word, romaji in japanese_words.items():
                if Levenshtein.distance(variant, romaji) <= threshold:
                    similar_words.append(jap_word)
                # wordとおなじ言葉を含んでいる単語を見つける
                # 例: momo => sumomo
                elif variant in romaji:
                    similar_words.append(jap_word)

        for variant in three_letter_variants:
            for jap_word, romaji in japanese_words.items():
                if Levenshtein.distance(variant, romaji) <= three_letters_threshold:
                    similar_words.append(jap_word)

        for variant in two_letter_variants:
            for jap_word, romaji in japanese_words.items():
                if Levenshtein.distance(variant, romaji) <= two_letters_threshold:
                    similar_words.append(jap_word)

        # アナグラムを生成
        anagrams = generate_anagrams(word)

        # アナグラムに似ている単語も追加
        for anagram in anagrams:
            anagram_romaji = convert_to_romaji(anagram)
            anagram_variants = generate_romaji_variants(romaji_word)
            for variant in anagram_variants:
                for jap_word, romaji in japanese_words.items():
                    if Levenshtein.distance(anagram_romaji, romaji) <= threshold and jap_word not in similar_words:
                        similar_words.append(jap_word)
                    # wordとおなじ言葉を含んでいる単語を見つける
                    # 例: momo => sumomo
                    elif anagram_romaji in romaji:
                        similar_words.append(jap_word)

        # similar_wordsの重複を削除
        similar_words = list(set(similar_words))

        # 閾値を増加させる
        threshold += 1

        # しきい値が単語の長さを超えた場合はループを終了
        if threshold > len(romaji_word):
            break

    # JSONレスポンスを生成して返す
    return Response(json.dumps(similar_words, ensure_ascii=False),
                    mimetype='application/json')





if __name__ == '__main__':
    app.run(debug=True)
