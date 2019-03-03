class Token(object):
    def __init__(self, _type, exact_type, name, string, start_row, start_column, end_row, end_column, line):
        self.type = _type
        self.exact_type = exact_type
        self.name = name
        self.string = string
        self.start_row = start_row
        self.start_column = start_column
        self.end_row = end_row
        self.end_column = end_column
        self.line = line
