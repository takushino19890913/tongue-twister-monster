from flask import Flask, request, Response
import json
import Levenshtein
import pykakasi
import itertools

app = Flask(__name__)

# JSONファイルからデータを読み込む
with open('japanese_words.json', 'r', encoding='utf-8') as jsonfile:
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


# アナグラムを生成
def generate_anagrams(word):
    romaji_word = convert_to_romaji(word)
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
        elif romaji_word[i] in "kstnhmr" and i < len(romaji_word) - 2 and romaji_word[i + 1] == 'y':
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

    # 閾値を設定（入力単語の長さの半分）
    threshold = len(romaji_word) // 4

    # Levenshtein距離を計算して似ている単語を見つける
    similar_words = []
    for jap_word, romaji in japanese_words.items():
        if Levenshtein.distance(romaji_word, romaji) <= threshold:
            similar_words.append(jap_word)

     # JSONレスポンスを生成して返す
    return Response(json.dumps(similar_words, ensure_ascii=False),
                    mimetype='application/json')

@app.route('/find_similar_and_anagrams', methods=['POST'])
def find_similar_and_anagrams():
    data = request.json
    word = data.get('word')

    # ローマ字に変換
    romaji_word = convert_to_romaji(word)

    # 閾値を設定（入力単語の長さの半分）
    threshold = len(romaji_word) // 4

    # 音が似ている単語を見つける
    similar_words = []
    for jap_word, romaji in japanese_words.items():
        if Levenshtein.distance(romaji_word, romaji) <= threshold:
            similar_words.append(jap_word)

    # アナグラムを生成
    anagrams = generate_anagrams(word)

    # アナグラムに似ている単語も追加
    for anagram in anagrams:
        anagram_romaji = convert_to_romaji(anagram)
        for jap_word, romaji in japanese_words.items():
            if Levenshtein.distance(anagram_romaji, romaji) <= threshold and jap_word not in similar_words:
                similar_words.append(jap_word)

    # JSONレスポンスを生成して返す
    return Response(json.dumps(similar_words, ensure_ascii=False),
                    mimetype='application/json')




if __name__ == '__main__':
    app.run(debug=True)
