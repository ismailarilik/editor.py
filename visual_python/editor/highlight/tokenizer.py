import keyword
import tokenize
from .token import Token

class Tokenizer:
    # Initialize keyword token type and name
    KEYWORD = 1000
    KEYWORD_NAME = 'KEYWORD'

    def __init__(self):
        self.keywords = keyword.kwlist

    def get_token_name(self, token_type, event=None):
        if token_type == self.KEYWORD:
            return self.KEYWORD_NAME
        return tokenize.tok_name[token_type]

    def tokenize(self, readline, event=None):
        tokens = tokenize.tokenize(readline)
        for token in tokens:
            token_type = token.type
            if token.exact_type == tokenize.NAME and token.string in self.keywords:
                exact_token_type = self.KEYWORD
                token_name = self.KEYWORD_NAME
            else:
                exact_token_type = token.exact_type
                token_name = tokenize.tok_name[exact_token_type]
            token_string = token.string
            token_start_row = token.start[0]
            token_start_column = token.start[1]
            token_end_row = token.end[0]
            token_end_column = token.end[1]
            token_line = token.line
            my_token = Token(token_type, exact_token_type, token_name, token_string, token_start_row, token_start_column, token_end_row, token_end_column, token_line)

            yield my_token
