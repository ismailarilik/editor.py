import keyword
import tokenize
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
        for token in tokens:
            token2 = Token(token.type, token.exact_type, tokenize.tok_name[token.exact_type], token.string, token.start[0], token.start[1], token.end[0], token.end[1], token.line)
            # Check for keyword token
            if token2.exact_type == tokenize.NAME and token2.string in self._keywords:
                token2.exact_type = token2.type = self.KEYWORD
                token2.name = self._KEYWORD_NAME
            yield token2
