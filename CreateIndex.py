import datetime
from IndexingWithWhoosh.PreProcessedCorpusReader import PreprocessedCorpusReader
from IndexingWithWhoosh.MyIndexWriter import MyIndexWriter
from IndexingWithWhoosh.MyIndexReader import MyIndexReader
from os import listdir


def WriteIndex():
    count = 0
    num = 0
    # Initiate pre-processed collection file reader.
    corpus = PreprocessedCorpusReader(str(num))
    # print("1")
    # Initiate the index writer.
    indexWriter = MyIndexWriter.MyIndexWriter()
    # Build index of corpus document by document.
    while True:
        doc = corpus.nextDocument()
        if not doc:
            if num == 9:
                #print("2")
                break
            else:
                num += 1
                #print(num)
                corpus = PreprocessedCorpusReader.PreprocessedCorpusReader(str(num))
                doc = corpus.nextDocument()
        #print(doc[0])
        indexWriter.index(doc[0], doc[1])
        count+=1
        if count%30000==0:
            print("finish ", count," docs")
    print("totally finish ", count, " docs")
    indexWriter.close()
    return


def ReadIndex(type, token):
    # Initiate the index file reader.
    index = MyIndexReader.MyIndexReader(type)
    # retrieve the token.
    df = index.DocFreq(token)
    ctf = index.CollectionFreq(token)
    result = '>> [' + token + '] has appeared in ' + str(df) + " documents and " + str(ctf) + " times in total"
    print(result)
    if df > 0:
        posting = index.getPostingList(token)
        for docId in posting:
            docNo = index.getDocNo(docId)
            print(docNo+"\t"+str(docId)+"\t"+str(posting[docId]))


startTime = datetime.datetime.now()
print ("index start", startTime)
WriteIndex()
print ("indexover")
endTime = datetime.datetime.now()
print("index web corpus running time: ", endTime - startTime)

# startTime = datetime.datetime.now()
# ReadIndex("trecweb", "acow")
# endTime = datetime.datetime.now()
# print ("load index & retrieve the token running time: ", endTime - startTime)

# startTime = datetime.datetime.now()
# WriteIndex("trectext")
# endTime = datetime.datetime.now()
# print ("index web corpus running time: ", endTime - startTime)
# startTime = datetime.datetime.now()
# ReadIndex("trectext", "normal")
# endTime = datetime.datetime.now()
# print ("load index & retrieve the token running time: ", endTime - startTime)
