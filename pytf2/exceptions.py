class Error(Exception):
    pass


class BadStatusError(Error):
    def __init__(self, url, status):
        super().__init__("{} returned the bad status code {}".format(url, status))

        self.url = url
        self.status = status


class BadResponseError(Error):
    def __init__(self, url, response):
        super().__init__("{} gave a bad response (see BadResponseError.response - type varies)".format(url))

        self.response = response


class KeyNotSetError(Error):
    def __init__(self, var):
        super().__init__("{} not set".format(var))

        self.var = var
