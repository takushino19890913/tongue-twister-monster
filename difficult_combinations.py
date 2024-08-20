# 組み合わせルール
# リスト[]の中は、この中の組み合わせいずれかが連続したらポイントゲット。タプル()の中は、この中の順番通りに連続したらポイントゲット。
# xは、すべての子音音素のうちいずれかを表す - k,s,t,n,h,m,y,r,w,g,z,d,b,p,j,ty,py,hy,by,my,ry,ky,gy,sh,ny
# lは、すべての母音音素のうちいずれかを表す - a,i,u,e,o
# ? は、すべての文字のうちいずれかを表す

from itertools import product

combination = {
    "xa": ["a", "ka", "sa", "ta", "na", "ha", "ma", "ya", "ra", "wa", "ga", "za", "da", "ba", "pa", "ja", "tya", "pya", "hya", "bya", "mya", "rya", "kya", "gya", "sya", "nya"],
    "xi": ["i", "ki", "si", "ti", "ni", "hi", "mi", "ri", "gi", "zi", "di", "bi", "pi", "ji", "tyi", "pyi", "hyi", "byi", "myi", "ryi", "kyi", "gyi", "syi", "nyi"],
    "xu": ["u", "ku", "su", "tu", "nu", "hu", "mu", "yu", "ru", "gu", "zu", "du", "bu", "pu", "ju", "tyu", "pyu", "hyu", "byu", "myu", "ryu", "kyu", "gyu", "syu", "nyu"],
    "xe": ["e", "ke", "se", "te", "ne", "he", "me", "re", "ge", "ze", "de", "be", "pe", "je", "tye", "pye", "hye", "bye", "mye", "rye", "kye", "gye", "sye", "nye"],
    "xo": ["o", "ko", "so", "to", "no", "ho", "mo", "yo", "ro", "go", "zo", "do", "bo", "po", "jo", "tyo", "pyo", "hyo", "byo", "myo", "ryo", "kyo", "gyo", "syo", "nyo"],
    "kl": ["ka", "ki", "ku", "ke", "ko"],
    "sl": ["sa", "si", "su", "se", "so"],
    "tl": ["ta", "ti", "tu", "te", "to"],
    "nl": ["na", "ni", "nu", "ne", "no"],
    "hl": ["ha", "hi", "hu", "he", "ho"],
    "ml": ["ma", "mi", "mu", "me", "mo"],
    "rl": ["ra", "ri", "ru", "re", "ro"],
    "gl": ["ga", "gi", "gu", "ge", "go"],
    "zl": ["za", "zi", "zu", "ze", "zo"],
    "dl": ["da", "di", "du", "de", "do"],
    "bl": ["ba", "bi", "bu", "be", "bo"],
    "pl": ["pa", "pi", "pu", "pe", "po"],
    "jl": ["ja", "ji", "ju", "je", "jo"],
    "tyl": ["tya", "tyi", "tyu", "tye", "tyo"],
    "pyl": ["pya", "pyi", "pyu", "pye", "pyo"],
    "hyl": ["hya", "hyi", "hyu", "hye", "hyo"],
    "byl": ["bya", "byi", "byu", "bye", "byo"],
    "myl": ["mya", "myi", "myu", "mye", "myo"],
    "ryl": ["rya", "ryi", "ryu", "rye", "ryo"],
    "kyl": ["kya", "kyi", "kyu", "kye", "kyo"],
    "gyl": ["gya", "gyi", "gyu", "gye", "gyo"],
    "syl": ["sya", "syi", "syu", "sye", "syo"],
    "nyl": ["nya", "nyi", "nyu", "nye", "nyo"],
    "?": [  'a', 'i', 'u', 'e', 'o',
            'ka', 'ki', 'ku', 'ke', 'ko',
            'sa', 'si', 'su', 'se', 'so',
            'ta', 'ti', 'tu', 'te', 'to',
            'na', 'ni', 'nu', 'ne', 'no',
            'ha', 'hi', 'fu', 'he', 'ho',
            'ma', 'mi', 'mu', 'me', 'mo',
            'ya', 'yu', 'yo',
            'ra', 'ri', 'ru', 're', 'ro',
            'wa', 'wo', 'nn',
            'ga', 'gi', 'gu', 'ge', 'go',
            'za', 'ji', 'zu', 'ze', 'zo',
            'da', 'ji', 'zu', 'de', 'do',
            'ba', 'bi', 'bu', 'be', 'bo',
            'pa', 'pi', 'pu', 'pe', 'po',
            'kya', 'kyu', 'kyo',
            'sya', 'syu', 'syo',
            'tya', 'tyu', 'tyo',
            'nya', 'nyu', 'nyo',
            'hya', 'hyu', 'hyo',
            'mya', 'myu', 'myo',
            'rya', 'ryu', 'ryo',
            'gya', 'gyu', 'gyo',
            'ja', 'ju', 'jo',
            'bya', 'byu', 'byo',
            'pya', 'pyu', 'pyo']
}


rules = {
    # 連続する母音音素 
    # 条件: 完全に連続　＝　3要素で1ポイント。
    "母音音素／i／または/u／_3-1": [["i", "xi"], ["u", "xu"]],
    "母音音素／a／_3-1": [["a", "xa"]],
    # kya, kyu, kyo, sya, syu, syo, tya, tyu, tyo, nya, nyu, nyo, hya, hyu, hyo, mya, myu, myo, rya, ryu, ryo, gya, gyu, gyo, ja, ju, jo, bya, byu, byo, pya, pyu, pyo
    # 条件: 拗音の連続は特に難しい。拗音の連続＝2要素で2ポイント。拗音と、拗音とおなじ子音音素を持っている音素の連続＝2要素で1ポイント。
    "拗音の連続_2-3": [["kya", "kyu", "kyo", "sya", "syu", "syo", "tya", "tyu", "tyo", "nya", "nyu", "nyo", "hya", "hyu", "hyo", "mya", "myu", "myo", "rya", "ryu", "ryo", "gya", "gyu", "gyo", "ja", "ju", "jo", "bya", "byu", "byo", "pya", "pyu", "pyo"]],
    "拗音と、拗音とおなじ子音音素を持っている音素の連続_2": [("kya", "kl"), ("kyu", "kl"), ("kyo", "kl"), ("sya", "sl"), ("syu", "sl"), ("syo", "sl"), ("tya", "tl"), ("tyu", "tl"), ("tyo", "tl"), ("nya", "nl"), ("nyu", "nl"), ("nyo", "nl"), ("hya", "hl"), ("hyu", "hl"), ("hyo", "hl"), ("mya", "ml"), ("myu", "ml"), ("myo", "ml"), ("rya", "rl"), ("ryu", "rl"), ("ryo", "rl"), ("gya", "gl"), ("gyu", "gl"), ("gyo", "gl"), ("ja", "zl"), ("ju", "zl"), ("jo", "zl"), ("bya", "bl"), ("byu", "bl"), ("byo", "bl"), ("pya", "pl"), ("pyu", "pl"), ("pyo", "pl"), ("kl", "kya"), ("kl", "kyu"), ("kl", "kyo"), ("sl", "sya"), ("sl", "syu"), ("sl", "syo"), ("tl", "tya"), ("tl", "tyu"), ("tl", "tyo"), ("nl", "nya"), ("nl", "nyu"), ("nl", "nyo"), ("hl", "hya"), ("hl", "hyu"), ("hl", "hyo"), ("ml", "mya"), ("ml", "myu"), ("ml", "myo"), ("rl", "rya"), ("rl", "ryu"), ("rl", "ryo"), ("gl", "gya"), ("gl", "gyu"), ("gl", "gyo"), ("zl", "ja"), ("zl", "ju"), ("zl", "jo"), ("bl", "bya"), ("bl", "byu"), ("bl", "byo"), ("pl", "pya"), ("pl", "pyu"), ("pl", "pyo")],
    # 同じ母音音素の間に半母音音素がある場合ーex: ayamaru
    # 条件: 母音音素の間に半母音音素がある＝3要素で1ポイント。ayamaで1ポイント、"国有": "kokuyuu"の"kuyuu"
    # (a,ya,a), (a,ya,ka), (a,ya,sa), 
    # "半母音音素と母音_1": [("xa","ya", "xa"), ("xu", "yu", "xu"), ("xo","yo","xo")],
    # # 「ん」が続く＝一文字おきに「ん」がある場合
    # # 条件: 一文字おきに「ん」がある＝2要素で1ポイント。
    # "モーラ音素/NI_1": [("nn","?", "nn")],
    # 同じ行の子音の連続 ka,ki,ku,ke,ko - sa,si su,se, so - ta,ti, tu, te, to - na,ni, nu, ne, no - ha,hi, hu, he, ho - ma,mi, mu, me, mo - ya, yu, yo - ra,ri, ru, re, ro - wa, wo - ga, gi, gu, ge, go - za, zi, zu, ze, zo - da, di, du, de, do - ba, bi, bu, be, bo - pa, pi, pu, pe, po
    # 条件: 同じ行の子音の連続＝3要素で1ポイント。
    "硬音的な無声子音音素_3-1": [["ka", "ki", "ku", "ke", "ko"], ["sa", "si", "su", "se", "so"], ["ta", "ti", "tu", "te", "to"], ["na", "ni", "nu", "ne", "no"], ["ha", "hi", "hu", "he", "ho"], ["ma", "mi", "mu", "me", "mo"], ["ya", "yu", "yo"], ["ra", "ri", "ru", "re", "ro"], ["wa", "wo"]],
}

# タプルから特定の要素を削除
def remove_from_tuple(tup, element):
    return tuple(x for x in tup if x != element)


#["i", "xi"]  => ["i", "ki", "si", "ti", "ni", "hi", "mi", "ri", "gi", "zi", "di", "bi", "pi", "ji", "tyi", "pyi", "hyi", "byi", "myi", "ryi", "kyi", "gyi", "syi", "nyi"]
#["kya", "kyu", "kyo", "kl"] => ["kya", "kyu", "kyo", "ka", "ki", "ku", "ke", "ko"]
def decode_set(set):
    for index, character in enumerate(set):
        if 'x' in character:
            set.extend(combination[set[index]])
            set.remove(set[index])
            
        if 'l' in character:
            vowels = ['a', 'i', 'u', 'e', 'o']
            set.extend([set[index].replace('l', vowel) for vowel in vowels])
            set.remove(set[index])
        if '?' in set:
            characters = [
                'a', 'i', 'u', 'e', 'o',
                'ka', 'ki', 'ku', 'ke', 'ko',
                'sa', 'si', 'su', 'se', 'so',
                'ta', 'ti', 'tu', 'te', 'to',
                'na', 'ni', 'nu', 'ne', 'no',
                'ha', 'hi', 'fu', 'he', 'ho',
                'ma', 'mi', 'mu', 'me', 'mo',
                'ya', 'yu', 'yo',
                'ra', 'ri', 'ru', 're', 'ro',
                'wa', 'wo', 'nn',
                'ga', 'gi', 'gu', 'ge', 'go',
                'za', 'ji', 'zu', 'ze', 'zo',
                'da', 'ji', 'zu', 'de', 'do',
                'ba', 'bi', 'bu', 'be', 'bo',
                'pa', 'pi', 'pu', 'pe', 'po',
                'kya', 'kyu', 'kyo',
                'sya', 'syu', 'syo',
                'tya', 'tyu', 'tyo',
                'nya', 'nyu', 'nyo',
                'hya', 'hyu', 'hyo',
                'mya', 'myu', 'myo',
                'rya', 'ryu', 'ryo',
                'gya', 'gyu', 'gyo',
                'ja', 'ju', 'jo',
                'bya', 'byu', 'byo',
                'pya', 'pyu', 'pyo'
            ]
            set.extend([set.replace('?', character) for character in characters])
            #setがリストの場合
            if isinstance(set, list):
                set.remove('?')
            #setがタプルの場合
            elif isinstance(set, tuple):
                set = remove_from_tuple(set, '?')
    return set

def decode_tuple(tup):
    decoded = [combination.get(item, [item]) for item in tup]
    return [tuple(item) for item in product(*decoded)]

def evaluate_word(word):
    from app import convert_to_romaji, split_into_parts
    # wordのローマ字を取得
    romaji = convert_to_romaji(word)
    # ローマ字を特定のセットに分割する
    parts = split_into_parts(romaji)
    
    points = 0
    # 組み合わせルール
    #"モーラ音素/NI_1": [("nn","?", "nn")],
    for rule_name, rule in rules.items():
        # ルールに一致するかどうかをチェック
        # conditionには、ルールの条件、つまり、rule_nameの後ろの_の後の文字列が入る
        condition = rule_name.split("_")[1]
        if isinstance(rule[0], list):  # ルールがリストの場合
            rows = int(condition.split("-")[0])
            point = int(condition.split("-")[1])
            for set in rule:
                
                #仮に、decode_set内でruleに変更があって、要素が増えた場合も、オリジナルの要素のみでループする
                count = 0
                for part in parts:
                    decoded_set = decode_set(set)
                    if part in decoded_set:
                        count += 1
                    else:
                        count = 0

                    if count >=rows:
                        points += point + (count - rows)

        elif isinstance(rule[0], tuple):  # ルールがタプルの場合
            point = int(condition)
            # tupleをcombinationに応じて変換したい。
            #　例えば、ruleが[(xa, ya, xa), (xu, yu, xu), (xo, yo, xo)]の場合、[(a,ya,a), (a,ya,ka), (a,ya,sa),....(ka,ya,a),(ka,ya,ka),....(ko,yo,ko)]に変換したい。
            decoded_rule = [decode_tuple(tup) for tup in rule]
            decoded_rule = [tup for sublist in decoded_rule for tup in sublist]
            
            point_count = 0
            for set in decoded_rule:
                count = 0
                for j in range(len(parts)):
                    for i in range(len(set)):
                        if parts[j] == set[i]:
                            count += 1
                            if count == len(set):
                                points += point
                                point_count += len(set)
                        else:
                            count = 0
            
            points += point_count/len(parts) * 30 * point
                    
                        
    # 2文字ごとに同じ母音のパターンが出てくる場合にポイントを追加
    consecutive_counter = 0
    point_count = 0
    last_vowel_pair = None
    for i in range(len(parts) - 3):
        if len(parts[i]) > 1 and len(parts[i+2]) > 1 and parts[i][1] == parts[i+2][1] and len(parts[i+1]) > 1 and len(parts[i+3]) > 1 and parts[i+1][1] == parts[i+3][1] and parts[i] != parts[i+1]:
            current_vowel_pair = (parts[i][-1], parts[i+1][-1])
            # ("a", "e")からインデックスが1だけずれるので、("e", "a")になる
            if last_vowel_pair == current_vowel_pair or last_vowel_pair == current_vowel_pair[::-1]:
                consecutive_counter += 1
                points += 1
                point_count +=1
                # 子音が微妙に違う場合にポイントを追加
                if parts[i][0] != parts[i+2][0] or parts[i+1][0] != parts[i+3][0]:
                    points += 1
                #子音が拗音の場合はさらにポイントを追加
                if len(parts[i]) > 2 or len(parts[i+1]) > 2 or parts[i] in ["ja","ju","jo"] or parts[i+1] in ["ja","ju","jo"]:
                    points += 1
            else:
                consecutive_counter = 1
            last_vowel_pair = current_vowel_pair
            points += consecutive_counter
        else:
            consecutive_counter = 0
    
    points += point_count/len(parts) * 60

    # 2文字ごとに同じ文字のパターンがでてきた場合にポイントを追加
    consecutive_counter = 0
    last_character_pair = None
    for i in range(len(parts) - 2):
        current_character_pair = (parts[i], parts[i+1])
        #last_character_pairはインデックスが一個ずれるので逆にする
        if parts[i] != parts[i+1] and (last_character_pair == current_character_pair or last_character_pair == current_character_pair[::-1]):
            consecutive_counter += 1
            points += 1
            if(consecutive_counter >= 2):
                points += 1
        else:
            consecutive_counter = 0

        last_character_pair = current_character_pair
    
    #単純な拗音の数を数える
    youon_count = 0
    for part in parts:
        if len(part) > 2 or part in ["ja","ju","jo"]:
            youon_count += 1
    
    if youon_count > 1:
        points += youon_count/len(parts) * 80

    #ま行、ば行、パ行のカウント
    ma_count = 0
    ba_count = 0
    pa_count = 0
    for part in parts:
        if part[0] == "m":
            ma_count += 1
        elif part[0] == "b":
            ba_count += 1
        elif part[0] == "p":
            pa_count += 1

    if ma_count > 1:
        points += ma_count/len(parts) * 40
    if ba_count > 1:
        points += ba_count/len(parts) * 40
    if pa_count > 1:
        points += pa_count/len(parts) * 40

    return points

if __name__ == "__main__":
    print("すももももももももうのち: ",evaluate_word("すもももももももものうち"))
    print("隣の客はよく柿くう客だ: ",evaluate_word("隣の客はよく柿くう客だ"))
    print("赤巻紙青巻紙黄巻紙: ",evaluate_word("赤巻紙青巻紙黄巻紙"))
    print("東京特許許可局: ",evaluate_word("東京特許許可局"))
    print("坊主が屏風に上手に坊主の絵を描いた: ",evaluate_word("坊主が屏風に上手に坊主の絵を描いた"))
    print("バスガス爆発: ",evaluate_word("バスガス爆発"))
    print("この竹藪に竹立てかけたのは竹立てかけたかったから竹立てかけた: ",evaluate_word("この竹藪に竹立てかけたのは竹立てかけたかったから竹立てかけた"))
    print("かえるぴょこぴょこみぴょこぴょこ、あわせてぴょこぴょこむぴょこぴょこ",evaluate_word("かえるぴょこぴょこみぴょこぴょこ、あわせてぴょこぴょこむぴょこぴょこ"))
    print("管轄",evaluate_word("管轄"))
    print("みんな三日三晩みかん食べる",evaluate_word("みんな三日三晩みかん食べる"))

