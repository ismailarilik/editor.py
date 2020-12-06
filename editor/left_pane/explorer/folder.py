'''
class Folder
'''

import os.path

class Folder:
    '''
    class Folder
    '''
    def __init__(self, path):
        self.path = path
        self.name = os.path.basename(self.path)
