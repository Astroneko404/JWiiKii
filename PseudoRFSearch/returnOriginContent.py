from bs4 import BeautifulSoup
import Classes.Path as Path
import re
from test import searchResult


class returnOriginContent:

    writer=[]

    def __init__(self, num):
        self.file_idx = num // 50000
        self.doc_pos = num % 50000
        print(self.file_idx, self.doc_pos)
        self.corpus = open(Path.Origin + "part_" + str(self.file_idx) + ".txt", "r", encoding="utf8")

    def readDocument(self):
        for x in range(self.doc_pos):
            doc = self.corpus.readline().strip()

        title = re.search('http://ja.dbpedia.org/resource/(.*)\?dbpv', doc).group(1).strip()
        bs = BeautifulSoup(doc, "html.parser")
        content = bs.get_text()
        content = content[1:]
        content = content[:-1]

        url = "http://ja.wikipedia.org/wiki/" + title
        out = searchResult(title, url, content)
        return out

# doc = "i hace \ a111 dog ? lalala  "
# title = re.search(r'(?<=\\).*?(?=\?)',doc)
# #content = "haha" + content
# new = "hahah"+ title.group()
# print(new)
