import abc

class ListensModifiedEventMixin(abc.ABC):
    '''
    Listens modified event for Tkinter Text widget and call modified method when it occurred.
    '''
    def __init__(self):
        # Listen modified event occurrence
        self.bind('<<Modified>>', self.modified_event_occurred)
        # Set a flag to ensure modified callback being called only by a change
        self.modified_event_occurred_by_change = True

    def modified_event_occurred(self, event):
        if self.modified_event_occurred_by_change:
            self.modified(event)
            # Call this method to set modified flag to False so following modification may cause modified event occurred
            self.edit_modified(False)
        # Switch this flag, because changing modified flag above cause modified event occurred
        self.modified_event_occurred_by_change = not self.modified_event_occurred_by_change

    @abc.abstractmethod
    def modified(self, event):
        '''
        Called when a modification made to the widget
        event: the event object passed by Tkinter
        Returns nothing
        '''
        pass
