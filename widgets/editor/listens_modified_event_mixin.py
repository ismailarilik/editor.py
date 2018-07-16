import abc

class ListensModifiedEventMixin(abc.ABC):
    def __init__(self):
        # Listen modified event occurrence
        self.bind('<<Modified>>', self.modified_event_occurred)
        # Set a flag to ensure modified callback being called only by a change
        self.modified_event_occurred_by_change = True
        self.modified_programmatically = False

    def modified_event_occurred(self, event):
        if self.modified_event_occurred_by_change:
            if self.modified_programmatically:
                self.modified(event, True)
                # Switch off modified programmatically flag
                # to avoid this method from thinking every modification made programmatically
                self.modified_programmatically = False
            else:
                self.modified(event, False)
            # Call this method to set modified flag to False so following modification may cause modified event occurred
            self.edit_modified(False)
        # Switch this flag, because changing modified flag above cause modified event occurred
        self.modified_event_occurred_by_change = not self.modified_event_occurred_by_change

    @abc.abstractmethod
    def modified(self, event, programmatically):
        '''
        Called when a modification made to the widget

        event: the event object passed by Tkinter
        programmatically: `True` if modification made programmatically, `False` otherwise.

        Returns nothing
        '''
        pass

    @staticmethod
    def modifies_programmatically(function):
        '''
        A decorator which is used to specify a function modifies the widget programmatically
        '''
        def function_wrapper(self, *args, **kwargs):
            self.modified_programmatically = True
            return function(self, *args, **kwargs)

        return function_wrapper
