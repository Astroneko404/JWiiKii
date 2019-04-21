import Indexing.MyIndexReader as MyIndexReader
import Search.QueryRetrievalModel as QueryRetreivalModel
from Search.ExtractQuery import ExtractQuery
from PseudoRFSearch.PseudoRFRetrievalModel import PseudoRFRetrievalModel
import datetime


startTime = datetime.datetime.now()
index = MyIndexReader.MyIndexReader()
pseudo_search = PseudoRFRetrievalModel(index)
extractor = ExtractQuery()
queries = extractor.get_query()
for query in queries:
    print(query.topicId,"\t",query.queryContent)
    results = pseudo_search.retrieveQuery(query, 20, 100, 0.4)
    rank = 1
    for result in results:
        print(query.getTopicId()," Q0 ",result.getDocNo(),' ',rank," ",result.getScore()," MYRUN",)
        rank += 1

endTime = datetime.datetime.now()
print("query search time: ", endTime - startTime)
