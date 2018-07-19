import tkinter as tk
import abc
import tokenize
import io
from .tokenizer import Tokenizer

class ColorizableMixin(abc.ABC):
    def __init__(self):
        self.tokenizer = Tokenizer()
        self.token_type_color_map = {
            self.tokenizer.KEYWORD: '#FF0000',
            tokenize.STRING: '#00C000',
            tokenize.NUMBER: '#0000FF',
            tokenize.COMMENT: '#808080',
            tokenize.LPAR: '#FFC000',
            tokenize.RPAR: '#FFC000',
            tokenize.LSQB: '#FF00FF',
            tokenize.RSQB: '#FF00FF',
            tokenize.LBRACE: '#00C0C0',
            tokenize.RBRACE: '#00C0C0',
            tokenize.EQUAL: '#800000',
            tokenize.PLUSEQUAL: '#800000',
            tokenize.MINEQUAL: '#800000',
            tokenize.STAREQUAL: '#800000',
            tokenize.DOUBLESTAREQUAL: '#800000',
            tokenize.SLASHEQUAL: '#800000',
            tokenize.DOUBLESLASHEQUAL: '#800000',
            tokenize.PERCENTEQUAL: '#800000',
            tokenize.ATEQUAL: '#800000',
            tokenize.VBAREQUAL: '#800000',
            tokenize.AMPEREQUAL: '#800000',
            tokenize.CIRCUMFLEXEQUAL: '#800000',
            tokenize.LEFTSHIFTEQUAL: '#800000',
            tokenize.RIGHTSHIFTEQUAL: '#800000',
            tokenize.PLUS: '#000080',
            tokenize.MINUS: '#000080',
            tokenize.STAR: '#000080',
            tokenize.DOUBLESTAR: '#000080',
            tokenize.SLASH: '#000080',
            tokenize.DOUBLESLASH: '#000080',
            tokenize.PERCENT: '#000080',
            tokenize.AT: '#000080',
            tokenize.VBAR: '#000080',
            tokenize.AMPER: '#000080',
            tokenize.TILDE: '#000080',
            tokenize.CIRCUMFLEX: '#000080',
            tokenize.LEFTSHIFT: '#000080',
            tokenize.RIGHTSHIFT: '#000080',
            tokenize.LESS: '#808000',
            tokenize.GREATER: '#808000',
            tokenize.EQEQUAL: '#808000',
            tokenize.NOTEQUAL: '#808000',
            tokenize.LESSEQUAL: '#808000',
            tokenize.GREATEREQUAL: '#808000',
            tokenize.DOT: '#800080',
            tokenize.COMMA: '#8000FF',
            tokenize.COLON: '#8080FF',
            tokenize.SEMI: '#FF0080',
            tokenize.RARROW: '#FF8080',
            tokenize.ELLIPSIS: '#FF80FF'
        }

    def colorize(self):
        # Remove previous tags, otherwise they will conflict with new ones
        self.tag_delete(*self.tag_names())
        # Configure tag colors
        for token_type, token_color in self.token_type_color_map.items():
            self.tag_config(self.tokenizer.get_token_name(token_type), foreground=token_color)
        text = self.get(1.0, tk.END)
        try:
            tokens = self.tokenizer.tokenize(io.BytesIO(text.encode('UTF-8')).readline)
            for token in tokens:
                # If there is a configured tag for this token, add it to the widget
                color = self.token_type_color_map.get(token.exact_type)
                if color:
                    start_index = f'{token.start_row}.{token.start_column}'
                    end_index = f'{token.end_row}.{token.end_column}'
                    self.tag_add(token.name, start_index, end_index)
        except:
            pass
