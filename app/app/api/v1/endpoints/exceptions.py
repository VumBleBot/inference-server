class NoAdequateSearchResultException(Exception):
    msg: str

    def __init__(self, msg: str = "Related search result not exist."):
        self.msg = msg

    def __str__(self):
        return self.msg
