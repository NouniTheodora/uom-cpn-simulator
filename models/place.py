class Place:
    def __init__(self, name: str, tokens: int = 0):
        self.name = name
        self.tokens = tokens

    def add_tokens(self, count: int):
        self.tokens += count

    def remove_tokens(self, count: int):
        if self.tokens >= count:
            self.tokens -= count
        else:
            raise ValueError(f"Not any further tokens in place {self.name}")

    def __str__(self):
        return f"{self.name}: {self.tokens} tokens"
