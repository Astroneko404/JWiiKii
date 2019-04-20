from Classes.Query import Query
from Mykytea import Mykytea
from Prep import parse_line
import re
import string


class ExtractQuery:

    def __init__(self, s):
        self.s = s
        self.mk = Mykytea("-model model/full_svm.mod")

    # Return extracted queries with class Query in a list.
    # The content of this query should be preprocessed
    def get_query(self):
        q = Query()

        # Process the query content
        content = re.sub(r'\\n\*|\\n|\"|。|、|•|→|／|＼', '', self.s)
        content = content.translate(str.maketrans('', '', string.punctuation))
        tag = self.mk.getTags(content)
        result = parse_line(tag)
        print(result)

        # Set query
        q.set_content(result)
        return q

