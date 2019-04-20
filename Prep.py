from bs4 import BeautifulSoup
from Classes import Path
import Mykytea
from os import listdir
import re
import string

input_path = Path.Origin
file_list = listdir(input_path)

opt = "-model model/full_svm.mod"
mk = Mykytea.Mykytea(opt)


def show_tags(t):
    for word in t:
        out = word.surface + "\t"
        for t1 in word.tag:
            for t2 in t1:
                for t3 in t2:
                    out = out + "/" + str(t3)
                out += "\t"
            out += "\t"
        print(out + '\n')


def has_letters(s):
    result = False
    if re.search('[a-zA-Z]', s):
        result = True
    return result


def parse_line(tag):
    result_origin = []
    result_kana = []

    for i in range(len(tag)):
        word = tag[i]
        term = word.surface.lower()
        prop = word.tag[0][0][0]
        kana = word.tag[1][0][0]
        # print(term, prop, kana)

        has_num = any(char.isdigit() for char in term)
        if has_num:
            continue

        if prop == '名詞' and term != 'こと':
            if i - 1 >= 0 and tag[i-1].tag[0][0][0] == '接頭辞':
                term = tag[i-1].surface + term
                kana = tag[i-1].tag[1][0][0] + kana
            if i + 1 <= len(tag) - 1 and tag[i+1].tag[0][0][0] == '接尾辞':
                term = term + tag[i + 1].surface
                kana = kana + tag[i+1].tag[1][0][0]
            term = term.strip()
            if len(term) > 1:
                result_origin.append(term.strip())
                if not has_letters(term):
                    result_kana.append(kana)

        if prop == '動詞' or prop == '形容詞':
            term = term.strip()
            if len(term) > 1 and term != 'する':
                result_origin.append(term.strip())
                if not has_letters(term):
                    result_kana.append(kana)

    return result_origin, result_kana


# for i in range(len(file_list)):
i = 0
doc_id = 50000 * i
output_path = Path.PreprocessResult
file = open(input_path + file_list[i], 'r', encoding='utf-8')
outfile = open(output_path + 'idx_' + str(i), 'w+', encoding='utf-8')

file.seek(0)

while True:
    line = file.readline()
    if not line:
        break

    doc_id += 1

    # Search for the term and combine it with docNo
    term = re.search('http://ja.dbpedia.org/resource/(.*)\?dbpv', line).group(1).strip()
    term = re.sub(r' ', '_', term)
    s = str(doc_id) + ' ' + term
    outfile.write(s+'\n')
    # print(s)

    # Remove html tags
    bs = BeautifulSoup(line, "html.parser")
    line = bs.get_text()

    # Delete weird characters in content
    content = re.sub(r'\\n\*|\\n|\"|。|、|•|→|／|＼|（|）', '', line)
    content = content.translate(str.maketrans('', '', string.punctuation))

    # Tokenize content
    tag = mk.getTags(content)
    result = parse_line(tag)
    r = result[0] + result[1]
    result = ' '.join(r)
    result += '\n'
    outfile.write(result)

file.close()
print('idx_' + str(i) + ' finished.')
outfile.close()
