# This py file is for test purpose

from datetime import datetime
from Indexing.MyIndexReader import MyIndexReader
import PseudoRFSearch.ProportionalScore as ProportionalScore
from Search.ExtractQuery import ExtractQuery

startTime = datetime.now()

index = MyIndexReader()
print('Finish index reading in', datetime.now() - startTime)

s = 'スポーツ番組'
extractor = ExtractQuery(s)
q_origin, q_kana = extractor.get_query()
content_list = [q_origin, q_kana]
search = ProportionalScore.ProportionalScore(content_list, index)

results = search.get_n(20)
rank = 1
for result in results:
    doc_id = int(result[0]) + 1
    print(doc_id, ' ', rank, ' ', result[1])
    rank += 1

endTime = datetime.now()
print("query search time: ", endTime - startTime)
