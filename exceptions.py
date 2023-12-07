class PrintfulException(Exception):
    """Printful exception returned from the API."""
    
    def __init__(self, message: str, code: str) -> None:
        self.code = code
        self.message = message

    def __str__(self):
        return '{} - {}'.format(self.code, self.message)

class PrintfulApiKeyException(PrintfulException):
    """API Key Exception Class"""

    def __init__(self, message: str, code: str):
        super().__init__(message, code)
        

    
    
class PrintfulApiFailException(PrintfulException):
    """API Fail Exception Class"""

    def __init__(self, message: str, code: str) -> None:
        super().__init__(message, code)