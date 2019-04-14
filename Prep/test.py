import Mykytea
from os import listdir
import re
import string

path = 'data/text_rip/'
file_list = listdir(path)

opt = "-model model/full_svm.mod"
mk = Mykytea.Mykytea(opt)

doc_id = 0


def showTags(t):
    for word in t:
        out = word.surface + "\t"
        for t1 in word.tag:
            for t2 in t1:
                for t3 in t2:
                    out = out + "/" + str(t3)
                out += "\t"
            out += "\t"
        print(out+'\n')


def parse_line(tag):
    result = []
    for i in range(len(tag)):
        word = tag[i]
        term = word.surface
        prop = word.tag[0][0][0]
        #print(term, prop)

        has_num = any(char.isdigit() for char in term)
        if has_num:
            continue

        if prop == '名詞' and term != 'こと':
            if i-1 >= 0 and tag[i-1].tag[0][0][0] == '接頭辞':
                term = tag[i-1].surface + term
            if i+1 <= len(tag)-1 and tag[i+1].tag[0][0][0] == '接尾辞':
                term = term + tag[i+1].surface
            term = term.strip()
            if len(term) > 1:
                result.append(term.strip())

        if prop == '動詞' or prop == '形容詞':
            term = term.strip()
            if len(term) > 1 and term != 'する':
                result.append(term.strip())

    return result


for i in range(len(file_list)):
    file = open(path + file_list[i], 'r', encoding='utf-8')
    outfile = open(path + 'idx_' + str(i), 'w+', encoding='utf-8')

    file.seek(0)

    while True:
        line = file.readline()
        if not line:
            break

        doc_id += 1
        print(doc_id)

        # Remove strange strings
        line = re.split('<|>', line)
        line = [x for x in line if x.strip()]
        line.remove(line[1])
        line.remove(line[2])
        line.remove(line[2])

        term = re.search('http://ja.dbpedia.org/resource/(.*)\?dbpv', line[0]).group(1)
        term = re.sub(r'\ ', '_', term)
        s = str(doc_id) + ' ' + term + '\n'
        outfile.write(s)

        content = re.sub(r'\\n\*|\\n|\"|。|、|•|→|／|＼', '', line[1])
        content = content.translate(str.maketrans('', '', string.punctuation))
        # content = line[1].replace('\\n* ', '')
        # content = content.replace('\\n ', '')
        # content = content.replace('\"', '')

        tag = mk.getTags(content)
        #showTags(tag)
        result = parse_line(tag)
        result = ' '.join(result)
        result += '\n'
        outfile.write(result)

    file.close()
    print(file_list[i] + ' finished.')
    outfile.close()
