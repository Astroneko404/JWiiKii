import Classes.Path as Path
from whoosh import index
from whoosh.fields import Schema, TEXT, KEYWORD, ID, STORED
from whoosh.analysis import RegexTokenizer


# Efficiency and memory cost should be paid with extra attention.
class MyIndexWriter:

    writer = []

    def __init__(self):
        path_dir = Path.IndexDir

        schema = Schema(doc_no=ID(stored=True),
                        doc_content=TEXT(analyzer=RegexTokenizer(), stored=True))
        indexing = index.create_in(path_dir, schema)
        self.writer = indexing.writer()
        return

    def index(self, docNo, content):
        self.writer.add_document(doc_no=docNo, doc_content=content)
        return

    def close(self):
        self.writer.commit()
        return
