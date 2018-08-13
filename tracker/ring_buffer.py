class RingBuffer:
    '''Fixed size buffer seemingly connected end-to-end
    
    When not full, the ring buffer (also called circular buffer)
    acts like a regular buffer. When full, adding another element
    overwrites the oldest one that was still being kept, in a circular
    way (hence the name).

    Note
    ----
    see https://www.safaribooksonline.com/library/view/python-cookbook/0596001673/ch05s19.html

    Attributes
    ----------
    slot_count : int
        Size of the buffer
    '''

    def __init__(self, slot_count):
        self.slot_count = slot_count
        self.data = []

    class __InternalFull:
        '''Internal class representing a full buffer'''

        def append(self, element):
            self.cur = (self.cur + 1) % self.slot_count
            self.data[self.cur] = element

        def get(self, idx = None):
            if idx is None:
                return self.data[self.cur]
            else:
                return self.data[idx]


    def append(self, element):
        '''Adds an element to the buffer
        
        Parameters
        ----------
        element
            The new element to add in the buffer
        '''
        self.data.append(element)

        # When buffer is first fulled, change behavior to actual ring buffer implementation
        if len(self.data) == self.slot_count:
            self.cur = len(self.data) - 1 # index of the newest element
            self.__class__ = self.__InternalFull

    def get(self, idx = None):
        '''Gets an element by index

        Parameters
        ----------
        idx : int 
            The index in the buffer of the element to retrieve.
            If None, then retrieves the last added element.
        
        Returns
        -------
            The element a the index
        '''
        #TODO move to __getitem__ ?
        if idx is None:
            return self.data[-1]
        else:
            return self.data[idx]

