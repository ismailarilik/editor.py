class Store:
    def __init__(self):
        self._application_name = 'Editor'

    @property
    def application_name(self):
        return self._application_name
