from Classes.Query import Query
from Mykytea import Mykytea
import re
import string


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


class ExtractQuery:

    def __init__(self, s):
        self.s = s
        self.mk = Mykytea("-model ../model/full_svm.mod")

    # Return extracted queries with class Query in a list.
    # The content of this query should be preprocessed
    def get_query(self):
        q = Query()

        # Process the query content
        content = re.sub(r'\\n\*|\\n|\"|。|、|•|→|／|＼', '', self.s)
        content = content.translate(str.maketrans('', '', string.punctuation))
        tag = self.mk.getTags(content)
        result = parse_line(tag)
        # print(result)

        # Set query
        q.set_content(result)
        return q
