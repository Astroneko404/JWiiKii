from PseudoRFSearch.PseudoRFRetrievalModel import PseudoRFRetrievalModel
from Search.QueryRetrievalModel import QueryRetrievalModel


class ProportionalScore:
    # query_list should contain two queries:
    #   (1) the original query
    #   (2) the hiragana version of the original query
    def __init__(self, query_list, idxReader):
        self.origin_query = query_list[0]
        self.kana_query = query_list[1]
        print(self.origin_query.get_content())
        self.model = QueryRetrievalModel(idxReader)
        self.list_size = 150

    def get_n(self, top_n):
        list_1 = self.model.retrieve_query(self.origin_query, self.list_size)
        list_2 = self.model.retrieve_query(self.kana_query, self.list_size)
        result_dict = {}
        p = 0.7

        for doc in list_1:
            result_dict[doc.get_id()] = doc.get_score() * p
        for doc in list_2:
            if doc.get_id in result_dict:
                result_dict[doc.get_id()] += doc.get_score() * (1-p)
            else:
                result_dict[doc.get_id()] = doc.get_score() * p

        result = sorted(result_dict.items(), key=lambda kv: kv[1], reverse=True)
        result = result[0:top_n]
        # print(result)

        return result
