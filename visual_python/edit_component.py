class EditComponent(object):
    def __init__(self, find_callback):
        self.__find_callback = find_callback

    def find(self, event=None):
        self.__find_callback(event)
