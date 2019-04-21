from datetime import datetime
from IndexingWithWhoosh.MyIndexReader import MyIndexReader
import PseudoRFSearch.ProportionalScore as ProportionalScore
from SearchWithWhoosh.ExtractQuery import ExtractQuery

startTime = datetime.now()

index = MyIndexReader()
print('Finish index reading in', datetime.now() - startTime)

s = '東京テレビ'
extractor = ExtractQuery(s)
q_origin, q_kana = extractor.get_query()
content_list = [q_origin, q_kana]
search = ProportionalScore.ProportionalScore(content_list, index)

results = search.get_n(20)
rank = 1
for result in results:
    print(q_origin, ' ', result.get_id(), ' ', rank, ' ', result.get_score())
    rank += 1

endTime = datetime.now()
print("query search time: ", endTime - startTime)
