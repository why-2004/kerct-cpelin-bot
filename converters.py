import re, ast

from dragonmapper import hanzi

from wiktionaryparser import WiktionaryParser

from eng_to_ipa import jonvert as convert_to_ipa

import time

kerst = {'m': 'm', 'n': 'n', 'ñ': 'ŋ', 'p': 'p', 't': 't', 'q': 'ʧ', 'k': 'k', 'b': 'b', 'd': 'd', 'j': 'ʤ', 'g': 'g',
         'f': 'f', 'č': 'θ', 'c': 's', 's': 'ʃ', 'h': 'h', 'v': 'v', 'ž': 'ð', 'z': 'z', 'x': 'ʒ', 'l': 'l', 'r': 'r',
         'y': 'j', 'w': 'w', 'a': 'a', 'ä': 'æ', 'e': 'ə', 'ë': 'ɛ', 'ē': 'ɜː', 'o': 'ɒ', 'i': 'ɪ', 'ī': 'iː',
         'u': 'ʊ', 'ū': 'uː', 'ö': 'ˈəʊ'}
ipa = {'m': 'm', 'n': 'n', 'ŋ': 'ñ', 'p': 'p', 't': 't', 'ʧ': 'q', 'k': 'k', 'b': 'b', 'd': 'd', 'ʤ': 'j', 'g': 'g',
       'f': 'f', 'h': 'h', 'v': 'v', 'ð': 'ž', 'z': 'z', 'ʒ': 'x', 'l': 'l', 'r': 'r',
       'j': 'y', 'w': 'w', 'a': 'a', 'æ': 'ä', 'ə': 'e', 'ɛ': 'ë', 'ɜ': 'ē', 'ɒ': 'o', 'ɪ': 'i', 'i': 'ī', 'ʊ': 'u',
       'u': 'ū', 'ö': 'ö', 'ː': '', 'ˈ': '', 'ˌ': '', 'ɹ': 'r', 'ɚ': 'e', 'ʌ': 'a', 'ɑ': 'a', 'ɔ': 'o',
       'e': 'ë', 'x': 'h', 'ʍ': 'hw', "ʉ": "", "̯": "", 'ɡ': 'g', '.': '', 'ɝ': 'er'
       # , 's': 'c', 'ʃ': 's', 'θ': 'č'  # old kerct, i.e. s represents sh and c represents s
    , 's': 's', 'ʃ': 'š', 'θ': 'c'  # new kerst, i.e. c represents sh and s represents s
       }  # must replace "ˈəʊ" with ö


def kerst_to_kerct(text):
    text = re.sub('c', 'č', text)
    text = re.sub('s', 'c', text)
    text = re.sub('š', 's', text)
    return text


def kerct_to_kerst(text):
    text = re.sub('s', 'š', text)
    text = re.sub('c', 's', text)
    text = re.sub('č', 'c', text)
    return text


def ipa_to_kerst(text):
    output = ""
    arg = re.sub("ˈəʊ", 'ö', text)
    arg = re.sub("[(].[)]", "", arg)
    arg = re.sub("t͡ʃ", "ʧ", arg)
    arg = re.sub("tʃ", "ʧ", arg)
    arg = re.sub("d͡ʒ", "ʤ", arg)
    arg = re.sub("dʒ", "ʤ", arg)
    arg = re.sub("[.] ", "․ ", arg)
    for i in arg.split(" "):
        word = re.findall(r'[^,;:"\'!@#$%^&*()—\-=_+<>?\[\]{}\\|~`“”\n]+', i)
        if len(word) > 0:
            word = word[0]
        else:
            output += i + " "
            continue
        puncs = re.split(r'[^.,;:"\'!@#$%^&*()—\-=_+<>?\[\]{}\\|~`“”\n]+', i)
        output += puncs[0]
        print(puncs[0] + word + puncs[-1])
        for j in word:
            if j in ipa:
                output += ipa[j]
            else:
                output += j
        output += puncs[-1]
        output += " "
    output = re.sub("․ ", ". ", output)
    return output


def ipa_to_kerct(text):
    return kerst_to_kerct(ipa_to_kerst(text))


def kerst_to_ipa(text):
    output = ""
    for i in text.split(" "):
        for j in i:
            if j in kerst:
                output += kerst[j]
            else:
                output += j
        output += " "
    return output


def kerct_to_ipa(text):
    return kerst_to_ipa(kerct_to_kerst(text))


eng2ipa_shortcut_dict = {'a': 'eɪ'}


def update_dict_from_file():
    global eng2ipa_shortcut_dict
    try:
        with open('dictionary.kerst', 'r', encoding='utf-8') as f:
            eng2ipa_shortcut_dict = ast.literal_eval(f.read())
    except:
        update_dict_to_file()


def update_dict_to_file():
    global eng2ipa_shortcut_dict
    with open('dictionary.kerst', 'w', encoding='utf-8') as f: f.write(repr(eng2ipa_shortcut_dict))


def eng_to_ipa(text):
    '''
    if len(text.split(" ")) > 20:
        return convert_to_ipa(text)
    '''
    text = re.sub("-", ' ', text)
    text = re.sub("—", " ", text)
    output = ""
    for i in text.split(" "):
        j = re.findall(r'[\w\'’]+', i)
        if len(j) > 0:
            j = j[0]
        else:
            output += i + " "
            continue
        puncs = re.split(r'[\w\'’]+', i)
        j = j.lower()
        if j in eng2ipa_shortcut_dict and eng2ipa_shortcut_dict[j] != '':
            output += puncs[0] + eng2ipa_shortcut_dict[j] + puncs[-1] + " "
            print(i+' '+output)
            continue
        t = time.time()
        word = word_to_ipa(j, 'english')
        t = time.time() - t
        print(t)
        print(word)
        if word == "":
            k = convert_to_ipa(j)
            if k != "" and k[0] != "_":
                eng2ipa_shortcut_dict[j] = k
                output += puncs[0] + k + puncs[-1]
        else:
            eng2ipa_shortcut_dict[j] = word
            output += puncs[0] + word + puncs[-1]
        output += " "
        print(i + ' ' + output)
    print(output)
    return output[:-1]





def lang_to_ipa(text, language):
    output = ""
    for i in text.split(" "):
        word = re.findall(r'[\w\'-^\n]+', i)
        if len(word) > 0:
            word = word[0]
        else:
            output += " " + i
            continue
        puncs = re.split(r'[\w\'-^\n]+', i)
        word = word_to_ipa(word, language)
        print(word)
        if word == "":
            output += puncs[0] + "__" + i + "__" + puncs[-1]
        else:
            output += puncs[0] + word + puncs[-1]
        output += " "
    return output[:-1]


def word_to_ipa(word, language):
    print(word)
    parser = WiktionaryParser()
    parser.set_default_language(language)
    word = parser.fetch(word)
    if word:
        # print(word)
        print(word[0]['pronunciations']['text'])
        for j in word[0]['pronunciations']['text']:
            # match=re.search("^((?![(]US[)] IPA: ).)*[/][^/]+/", j)
            match = re.search("[/][^/]+/", j)
            if match:
                return match[0][1:-1].replace(" ", "")
    return ""


def eng_to_kerst(text):
    return ipa_to_kerst(eng_to_ipa(text))


def eng_to_kerct(text):
    return kerst_to_kerct(eng_to_kerst(text))


def remove_vowels(text):
    output = ""
    for i in text.split(" "):
        for j in i:
            if not re.match('[aeiouAEIOU]', j):
                output += j
        output += " "
    return


def han_to_ipa(text):
    return hanzi.to_ipa(text)


def han_to_zhu(text):
    return hanzi.to_zhuyin(text)


def han_to_pin(text):
    return hanzi.to_pinyin(text)
