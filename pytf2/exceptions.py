class Error(Exception):
    pass


class BadStatusError(Error):
    def __init__(self, url, status, response):
        super().__init__("{} returned the bad status code {}".format(url, status))

        self.url = url
        self.status = status
        self.response = response


class BadResponseError(Error):
    def __init__(self, url, response):
        super().__init__("{} gave a bad response (see BadResponseError.response - type varies)".format(url))

        self.response = response


class KeyNotSetError(Error):
    def __init__(self, var):
        super().__init__("{} not set".format(var))

        self.var = var


class RateLimited(Error):
    def __init__(self):
        super().__init__("You have made 120 requests in the past 60 seconds. This many requests could leave your ip"
                         "liable to getting temporarily banned from backpack.tf. Read the docs to disable this error.")
