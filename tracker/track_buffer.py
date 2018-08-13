from tracker.ring_buffer import RingBuffer

class TrackBuffer:
    ''' Buffer representing a temporal sequence of poses (i.e track)
    
    The buffer may contain None element, in the case where no pose was
    added in the instant t.

    Attributes
    ----------
    pose_count : int
        The size of the buffer (i.e. number of poses)
    '''
    #TODO Why store None in buffer ?
    def __init__(self, pose_count):
        self.pose_count = pose_count
        self.buffer = RingBuffer(pose_count) # Buffer represented as a circular buffer
        self.cur_valid = -1 # Index of the last non-None element
        self.counter_none = 0 # Counter of successive None element
        self.untracked = False # Flag if track is only None pose (i.e. no new pose in `pose_count` timestep)

    def append(self, pose = None):
        '''Adds a new pose for the timestep t

        Parameters
        ----------
        pose
            The new element to add
        '''

        #TODO throw exception if untracked and try to append something not null
        self.buffer.append(pose)
        if pose is None:
            self.counter_none += 1
            if self.counter_none == self.pose_count:
                self.untracked = True
        else:
            #TODO safer to just get the current index from the underlaying buffer ?
            self.cur_valid = (self.cur_valid + self.counter_none + 1) % self.pose_count
            self.counter_none = 0 # Reset the none counter
    
    def get_last_valid_pose(self):
        '''Gets the last valid (non-None) element added to the buffer
        
        Returns
        -------
            The last valid element
        '''
        #TODO rename and add exeception
        return self.buffer.get(self.cur_valid)
    
    def get_last_pose(self):
        '''Gets the last element of the buffer

        Returns
        -------
            The last element
        '''
        #TODO rename 
        return self.buffer.get()
    
    def is_untracked(self):
        '''Checks if the track is only composed of None element

        Returns
        -------
        bool
            True if untracked, False otherwise
        '''
        return self.untracked
