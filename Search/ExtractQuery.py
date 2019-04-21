from Classes import Path
from Classes.Query import Query
from Mykytea import Mykytea
from Prep.KyteaHelper import parse_line
import re
import string


class ExtractQuery:

    def __init__(self, s):
        self.s = s
        self.mk = Mykytea("-model " + Path.KTmodel)

    # Return extracted queries with class Query in a list.
    # The content of this query should be preprocessed
    def get_query(self):
        q_origin = Query()
        q_kana = Query()

        # Process the query content
        content = re.sub(r'\\n\*|\\n|\"|。|、|•|→|／|＼', '', self.s)
        content = content.translate(str.maketrans('', '', string.punctuation))
        tag = self.mk.getTags(content)
        result = parse_line(tag)

        # Set query
        q_origin.set_content(' OR '.join(result[0]))
        q_kana.set_content(' OR '.join(result[1]))
        return q_origin, q_kana
