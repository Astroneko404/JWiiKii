from Classes.Document import Document
from SearchWithWhoosh.QueryRetrievalModel import QueryRetrievalModel


class PseudoRFRetrievalModel:
    indexReader = []
    collectionLength = 0
    qrmodel = []

    def __init__(self, ixReader):
        self.indexReader = ixReader
        self.collection_length = ixReader.getCollLength()
        self.model = QueryRetrievalModel(ixReader)
        return

    def retrieve_query(self, query, topN, topK, alpha):
        # sort all retrieved documents from most relevant to least, and return TopN
        results = []
        mu = 2000

        # Get topK feedback documents
        feedback_doc_list = self.model.retrieve_query(query, topK)
        feedback_doc_list = [x.getDocId() for x in feedback_doc_list]

        # get P(token|feedback documents)
        TokenRFScore = self.GetTokenRFScore(query, topK, feedback_doc_list)

        # Calculate the final score
        ranking = {}
        for token in TokenRFScore:
            dirchlet_ranking = {}
            pos_list = self.indexReader.getPostingList(token)
            feedback_score = TokenRFScore[token]

            # Calculate P(w | REF)
            collection_freq = self.indexReader.CollectionFreq(token)
            if collection_freq == 0:
                continue
            collection_score = collection_freq / self.collection_length

            # Calculate P(q_i | M_D) using dirichlet smoothing
            for doc_id in feedback_doc_list:
                doc_length = self.indexReader.getDocLength(doc_id)
                doc_freq = 0
                if doc_id in pos_list:
                    doc_freq = pos_list[doc_id]
                dirichlet = (doc_freq + mu * collection_score) / (doc_length + mu)

                if doc_id in dirchlet_ranking:
                    dirchlet_ranking[doc_id] *= dirichlet
                else:
                    dirchlet_ranking[doc_id] = dirichlet

            # P(q_i | M_D') = alpha * P(q_i | M_D) + (1 - alpha) * P(q_i | F)
            for doc_id, model_score in dirchlet_ranking.items():
                final_score = alpha * model_score + (1 - alpha) * feedback_score
                if doc_id in ranking:
                    ranking[doc_id] *= final_score
                else:
                    ranking[doc_id] = final_score

        # sort all retrieved documents from most relevant to least, and return TopN
        ranking_sorted = sorted(ranking.items(), key=lambda x: x[1], reverse=True)
        result = []
        for i in range(topN):
            doc = Document()
            doc.setDocId(ranking_sorted[i][0])
            doc.setDocNo(self.indexReader.getDocNo(ranking_sorted[i][0]))
            doc.setScore(ranking_sorted[i][1])
            result.append(doc)

        return results

    def GetTokenRFScore(self, query, topK, feedback_doc_list):
        # for each token in the query, you should calculate token's score in feedback documents:
        #   P(token|feedback documents)
        # use Dirichlet smoothing
        # save {token: score} in dictionary TokenRFScore, and return it
        TokenRFScore = {}
        mu = 2000

        token_list = query.getQueryContent().split()
        token_list = [x for x in token_list if x != 'OR']
        for token in token_list:
            feedback_score = self.feedback_score(token, feedback_doc_list, mu)
            TokenRFScore[token] = feedback_score

        return TokenRFScore

    # A helper method that calculates P(q_i | F)
    def feedback_score(self, token, feedback_doc_list, mu):
        pos_list = self.indexReader.getPostingList(token)

        # Calculate c(q_i in F)
        feedback_count = 0
        for doc_id in feedback_doc_list:
            fdbk_freq = 0
            if doc_id in pos_list:
                fdbk_freq = pos_list[doc_id]
            feedback_count += fdbk_freq

        # Get P(q_i | collection)
        coll_count = self.indexReader.CollectionFreq(token)

        # Calculate P(q_i | F)
        feedback_score = (feedback_count + mu * coll_count) / (len(feedback_doc_list) + mu)

        return feedback_score
