class Document:

    def __init__(self):
        return

    docid = ""
    score = 0.0

    def get_id(self):
        return self.docid

    def get_score(self):
        return self.score

    def set_id(self, docid):
        self.docid = docid

    def set_score(self, the_score):
        self.score = the_score
