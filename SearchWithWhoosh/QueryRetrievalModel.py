from Classes.Document import Document
import Classes.Path as Path
import whoosh.index as index
from whoosh.qparser import QueryParser
from whoosh import scoring


class QueryRetrievalModel:
    indexReader = []
    query_parser = []
    searcher = []

    def __init__(self, ixReader):
        path_dir = Path.IndexDir
        self.searcher = index.open_dir(path_dir).searcher(weighting=scoring.BM25F(B=0.75, content_B=1.0, K1=1.5))
        self.query_parser = QueryParser("doc_content", self.searcher.schema)
        return

    def retrieve_query(self, query, top_n):
        query_input = self.query_parser.parse(query.getQueryContent())
        search_results = self.searcher.search(query_input, limit=top_n)
        return_docs = []
        for result in search_results:
            # print(self.searcher.stored_fields(result.docnum))
            a_doc = Document()
            a_doc.setDocId(result.docnum)
            a_doc.setDocNo(self.searcher.stored_fields(result.docnum)["doc_no"])
            a_doc.setScore(result.score)
            return_docs.append(a_doc)
        return return_docs
