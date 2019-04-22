from bs4 import BeautifulSoup
from Classes import Path
import Mykytea
from os import listdir
from Prep.KyteaHelper import parse_line, show_tags
import re
import string

input_path = Path.Origin
file_list = listdir(input_path)
print(file_list)

opt = "-model model/full_svm.mod"
mk = Mykytea.Mykytea(opt)

# # For testing purpose
# s = "美術 （びじゅつ）とは芸術の分野のひとつ。視覚によってとらえることを目的として表現された視覚芸術の総称。"\
#     "英語では art（アート）、fine arts（ファインアート）、あるいは visual " \
#     "arts（ビジュアルアート）がこれに相当しうる。 "
# content = re.sub(r'\\n\*|\\n|\"|。|、|•|→|／|＼|（|）', '', s)
# content = content.translate(str.maketrans('', '', string.punctuation))
# # print(content)
# tag = mk.getTags(content)
# show_tags(tag)

for i in range(0, 10):
    # i = 0
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
        print(s)

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
    print('\nidx_' + str(i) + ' finished.\n')
    outfile.close()
