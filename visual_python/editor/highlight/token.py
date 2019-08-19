class Token:
    def __init__(self, token_type, exact_token_type, name, string, start_row, start_column, end_row, end_column, line):
        self.type = token_type
        self.exact_type = exact_token_type
        self.name = name
        self.string = string
        self.start_row = start_row
        self.start_column = start_column
        self.end_row = end_row
        self.end_column = end_column
        self.line = line
