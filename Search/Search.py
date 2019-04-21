from datetime import datetime
from IndexingWithWhoosh.MyIndexReader import MyIndexReader
import PseudoRFSearch.ProportionalScore as ProportionalScore
from Search.ExtractQuery import ExtractQuery


def get_result(s):
    start_time = datetime.now()
    index = MyIndexReader()

    extractor = ExtractQuery(s)
    q_origin, q_kana = extractor.get_query()
    content_list = [q_origin, q_kana]
    search = ProportionalScore.ProportionalScore(content_list, index)

    results = search.get_n(50)
    rank = 1
    r_list = []
    for result in results:
        doc_id = int(result[0]) + 1
        r_list.append(doc_id)
        print(result[0], ' ', rank, ' ', result[1])
        rank += 1

    print("query search time: ", datetime.now() - start_time)
    return r_list
