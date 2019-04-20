from IndexingWithWhoosh.MyIndexReader import MyIndexReader
from SearchWithWhoosh.QueryRetrievalModel import QueryRetrievalModel
import SearchWithWhoosh.ExtractQuery as ExtractQuery
import datetime

startTime = datetime.datetime.now()
index = MyIndexReader()
search = QueryRetrievalModel(index)
extractor = ExtractQuery.ExtractQuery()
queries = extractor.get_query()
for query in queries:
    print(query.topicId,"\t",query.queryContent)
    results = search.retrieve_query(query, 20)
    rank = 1
    for result in results:
        print(query.getTopicId()," Q0 ",result.getDocNo(),' ',rank," ",result.getScore()," MYRUN",)
        rank +=1

endTime = datetime.datetime.now()
print ("query search time: ", endTime - startTime)