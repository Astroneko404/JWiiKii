from datetime import datetime
from IndexingWithWhoosh.MyIndexReader import MyIndexReader
import PseudoRFSearch.ProportionalScore as ProportionalScore
print(datetime.now())
from SearchWithWhoosh.ExtractQuery import ExtractQuery
print(datetime.now())

startTime = datetime.now()

print('Start index reading')
index = MyIndexReader()
print('Finish index reading')

s = '東京'
extractor = ExtractQuery(s)
q = extractor.get_query()
search = ProportionalScore.ProportionalScore(q, index)

print(q.get_content())
results = search.get_n(20)
rank = 1
for result in results:
    print(q, ' ', result.get_id(), ' ', rank, ' ', result.get_score())
    rank += 1

endTime = datetime.now()
print("query search time: ", endTime - startTime)
