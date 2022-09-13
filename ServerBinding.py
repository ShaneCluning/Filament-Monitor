class ServerBinding:
    def __init__(self, url: str, handler: object) -> None:
        self.url = url
        self.handler = handler
