class Query:
    # the content of query should be two lists
    def __init__(self):
        self.queryContent = []
        return

    def get_content(self):
        return self.queryContent

    def set_content(self, content):
        self.queryContent = content
