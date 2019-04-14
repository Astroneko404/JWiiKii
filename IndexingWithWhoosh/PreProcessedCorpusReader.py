import Classes.Path as Path


class PreprocessedCorpusReader:

    corpus = 0

    def __init__(self, num):
        self.corpus = open(Path.PreprocessResult + num, "r", encoding="utf8")

    def nextDocument(self):
        docNo = self.corpus.readline().strip()
        docNo = docNo[0:docNo.find(" ")]
        if docNo=="":
            self.corpus.close()
            return
        content=self.corpus.readline().strip()
        return [docNo, content]

# test = "1226 chinese"
# test = test[0:test.find(" ")]
# print(test)
