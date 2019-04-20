import Classes.Path as Path
import re


class returnOriginContent:

    writer=[]

    def __init__(self):
        def __init__(self, num):
            self.corpus = open(Path.origin + num, "r", encoding="utf8")

    def readDocument(self,docno):
        for x in range(docno):
            doc = self.corpus.readline().strip()

        title = re.search(r'(?<=\\).*?(?=\?)',doc)
        content = re.search(r'(?<=").*?(?=")',doc)

        url = "http://ja.wikipedia.org/wiki/" + title.group()
        return [title, url, content.group()]

# doc = "i hace \ a111 dog ? lalala  "
# title = re.search(r'(?<=\\).*?(?=\?)',doc)
# #content = "haha" + content
# new = "hahah"+ title.group()
# print(new)
