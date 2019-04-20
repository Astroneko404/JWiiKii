from Classes import Path
import datetime
from IndexingWithWhoosh.PreProcessedCorpusReader import PreprocessedCorpusReader
from IndexingWithWhoosh.MyIndexWriter import MyIndexWriter
from IndexingWithWhoosh.MyIndexReader import MyIndexReader
import os


def WriteIndex():
    count = 0
    # num = 0
    file_list = os.listdir(Path.PreprocessResult)

    # Initiate the index writer.
    index_writer = MyIndexWriter()

    for file in file_list:
        path = Path.PreprocessResult + file
        corpus = PreprocessedCorpusReader(path)

        while True:
            doc = corpus.next_document()
            if not doc:
                break
            index_writer.index(doc[0], doc[1])
            count += 1
            if count % 10000 == 0:
                print('finish ', count, ' docs')

    # Build index of corpus document by document.
    # while True:
    #     doc = corpus.nextDocument()
    #     if not doc:
    #         if num == 9:
    #             #print("2")
    #             break
    #         else:
    #             num += 1
    #             #print(num)
    #             corpus = PreprocessedCorpusReader.PreprocessedCorpusReader(str(num))
    #             doc = corpus.nextDocument()
    #     #print(doc[0])
    #     indexWriter.index(doc[0], doc[1])
    #     count+=1
    #     if count%30000==0:
    #         print("finish ", count," docs")

    print("totally finish ", count, " docs")
    index_writer.close()
    return


def ReadIndex(token):
    # Initiate the index file reader.
    index = MyIndexReader()
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
print ("index writing finished")
endTime = datetime.datetime.now()
print("index web corpus running time: ", endTime - startTime)
