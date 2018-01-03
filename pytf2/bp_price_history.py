class PriceHistory:
    def __init__(self, data):
        self.value = data.get("value")
        self.value_high = data.get("value_high", self.value)
        self.currency = data.get("currency")
        self.timestamp = data.get("timestamp")
