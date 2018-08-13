from collections import namedtuple
from tracker.track_buffer import TrackBuffer

Instance = namedtuple('Instance', 'id pose')

class GraphTracks:
    '''Graph symbolizing the tracking information for each tracked peron

    Attributes
    ----------
    slot_count : int
        Size of the track (track history). All tracks have the same size.
    '''

    def __init__(self, slot_count):
        self.slot_count = slot_count
        self.graph = {} # a graph is a dictionary of tracks, with the key being the track id

    def get_last_valid_poses(self):
        '''Gets the last valid pose (non-None pose) for each track.

        Returns
        -------
            A list containing the last valid pose of each track.
        '''
        #TODO rename and comprehension (either list of dict)
        poses = []
        for id, track in self.graph.items():
            poses.append(Instance(id, track.get_last_valid_pose()))
            
        return poses
    
    def get_last_poses(self):
        '''Gets the last pose at current timestep for each track

        Returns
        -------
            A dictionary containing the track id as key and the last pose of the track as value.
            Note that tracks may be missing if their last pose is None
        '''
        return {id:track.get_last_pose() for id, track in self.graph.items() if track.get_last_pose() is not None}
        #poses = [Instance(id, track.get_last_pose()) for id, track in self.graph.items() if track.get_last_pose() is not None]

    def add_instances(self, instances):
        '''Adds new instances (track id and pose) for a new timestep.

        Parameters
        ----------
        instances : list
            A list of Instance representing the new pose for the new timestep
        '''
        #TODO instances as dict ?
        ids = []
        for instance in instances:
            ids.append(instance.id) 
            if instance.id not in self.graph: # new id so create new track
                self.graph[instance.id] = TrackBuffer(self.slot_count)
            self.graph[instance.id].append(instance.pose)
        
        # Find the existing track with no new pose 
        remaining_ids = set(self.graph.keys()).symmetric_difference(set(ids))
        for id in remaining_ids: # add none pose to other existing tracks
            self.graph[id].append(None)
            if self.graph[id].is_untracked(): # Prune the graph when a track expired
                self.graph.pop(id)