import tokenize
import keyword
from .token import Token

class Tokenizer(object):
    # Initialize keyword token type and name
    KEYWORD = 1000
    _KEYWORD_NAME = 'KEYWORD'

    def __init__(self):
        self._keywords = keyword.kwlist

    def get_token_name(self, token_type):
        if token_type == self.KEYWORD:
            return self._KEYWORD_NAME
        return tokenize.tok_name[token_type]

    def tokenize(self, readline):
        tokens = tokenize.tokenize(readline)
        for _token in tokens:
            token = Token(
                _token.type,
                _token.exact_type,
                tokenize.tok_name[_token.exact_type],
                _token.string,
                _token.start[0],
                _token.start[1],
                _token.end[0],
                _token.end[1],
                _token.line
            )
            # Check for keyword token
            if token.exact_type == tokenize.NAME and token.string in self._keywords:
                token.type = self.KEYWORD
                token.exact_type = token.type
                token.name = self._KEYWORD_NAME
            yield token
