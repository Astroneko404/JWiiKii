class PreprocessedCorpusReader:

    corpus = 0

    def __init__(self, file):
        self.corpus = open(file, "r", encoding="utf8")

    def next_document(self):
        line = self.corpus.readline().strip()
        if not line:
            self.corpus.close()
            return

        # Get docNo
        line = line.split()
        doc_no = line[0]

        # Get doc content
        content = self.corpus.readline().strip()
        if not content:
            raise Exception('Document ' + str(doc_no) + ' has no content')

        # print(doc_no)
        # print(content)
        return doc_no, content
