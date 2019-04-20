import SearchWithWhoosh.QueryRetrievalModel as QueryRetrievalModel


class PseudoRFRetrievalModel:
    indexReader = []
    collectionLength = 0
    qrmodel = []

    def __init__(self, ixReader):
        self.indexReader = ixReader
        self.collectionLength = ixReader.getCollLength()
        self.model = QueryRetrievalModel(ixReader)
        return

    def retrieveQuery(self, query, topN, topK, alpha):
        # get P(token|feedback documents)
        TokenRFScore = self.GetTokenRFScore(query, topK)

        # sort all retrieved documents from most relevant to least, and return TopN
        results = []
        return results

    def GetTokenRFScore(self, query, topK):
        TokenRFScore = {}
        return TokenRFScore
