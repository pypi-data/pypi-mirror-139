class GeneralException(Exception):
    code: int
    Detail: str
    Id: str
    Status: str


class UnknownError(Exception):
    pass
