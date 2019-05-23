import tkinter as tk
import tkinter.filedialog as tk_filedialog
import tkinter.messagebox as tk_messagebox
import os

class File(object):
    def __init__(self, path):
        self.path = path
        self.is_modified = False

    @property
    def name(self):
        if self.path:
            return os.path.basename(self.path)

class Folder(object):
    def __init__(self, path=None):
        self._path = path
        self._name = None
        if self.path:
            self._name = os.path.basename(self.path)

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, newPath):
        self._path = newPath
        self._name = os.path.basename(self.path)

    @property
    def name(self):
        return self._name

class FileComponent(object):
    def __init__(self, open_file_callback, open_folder_callback, save_file_callback, save_file_as_callback):
        self.__open_file_callback = open_file_callback
        self.__open_folder_callback = open_folder_callback
        self.__save_file_callback = save_file_callback
        self.__save_file_as_callback = save_file_as_callback
        self.file = File(None)
        self.folder = Folder()

    def open_file(self, event=None):
        '''
        Return True if a file was opened
        Return False otherwise
        '''
        if self.save_unsaved_changes():
            file_path = tk_filedialog.askopenfilename(filetypes=[('Python Files', '.py')])
            if file_path:
                return self.__open_file_callback(file_path)
            else:
                return False
        else:
            return False

    def open_folder(self, event=None):
        self.folder.path = tk_filedialog.askdirectory()
        if self.folder.path:
            # Create folder
            try:
                os.mkdir(self.folder.path)
            except FileExistsError as error:
                print('An error occurred while opening a folder:')
                print(error)
            # Call callback function
            self.__open_folder_callback(self.folder)

    def save_file(self, event=None):
        '''
        Return True if the file was saved
        Return False otherwise
        '''
        # If there is not any opened file, call save_file_as method
        # Else, write editor text to the file
        if not self.file.path:
            return self.save_file_as(event)
        else:
            return self.__save_file_callback(self.file)

    def save_file_as(self, event=None):
        '''
        Return True if the specified file was saved
        Return False otherwise
        '''
        file_path = tk_filedialog.asksaveasfilename(defaultextension='.py', filetypes=[('Python Files', '.py')])
        if file_path:
            self.file.path = file_path
            self.file.is_modified = False
            return self.__save_file_as_callback(self.file)
        else:
            return False

    def save_unsaved_changes(self):
        '''
        Return True if unsaved changes were saved
        Return False otherwise
        '''
        if self.file.is_modified:
            reply = tk_messagebox.askyesnocancel('Unsaved Changes', 'There are unsaved changes, would you like to save them?')
            if reply:
                return self.save_file()
            elif reply == False:
                return True
            else:
                return False
        else:
            return True
