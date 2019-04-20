from Classes.Query import Query
import Mykytea
from Prep import parse_line
import re
import string

opt = "-model model/full_svm.mod"
mk = Mykytea.Mykytea(opt)


class ExtractQuery:

    def __init__(self, s):
        self.s = s
        return

    # Return extracted queries with class Query in a list.
    # The content of this query should be preprocessed
    def get_query(self):
        q = Query()

        # Process the query content
        content = re.sub(r'\\n\*|\\n|\"|。|、|•|→|／|＼', '', self.s)
        content = content.translate(str.maketrans('', '', string.punctuation))
        tag = mk.getTags(content)
        result = parse_line(tag)
        result = ' '.join(result)

        # Set query
        q.set_content(result)
        return q

