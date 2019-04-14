import SearchWithWhoosh.QueryRetreivalModel as QueryRetreivalModel


class PseudoRFRetreivalModel:
    indexReader = []
    collectionLength = 0
    qrmodel = []

    def __init__(self, ixReader):
        self.indexReader = ixReader
        self.collectionLength = ixReader.getCollLength()
        self.model = QueryRetreivalModel.QueryRetreivalModel(ixReader)
        return

    # Search for the topic with pseudo relevance feedback.
    # The returned results (retrieved documents) should be ranked by the score (from the most relevant to the least).
    # query: The query to be searched for.
    # TopN: The maximum number of returned document
    # TopK: The count of feedback documents
    # alpha: parameter of relevance feedback model
    # return TopN most relevant document, in List structure

    def retrieveQuery(self, query, topN, topK, alpha):
        # get P(token|feedback documents)
        TokenRFScore = self.GetTokenRFScore(query, topK)

        # sort all retrieved documents from most relevant to least, and return TopN
        results = []
        return results

    def GetTokenRFScore(self, query, topK):
        TokenRFScore = {}
        return TokenRFScore
