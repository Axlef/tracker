import networkx as nx
import tracker.distance as distance
from tracker.graph_tracks import GraphTracks, Instance

import time

class PoseTracker:

    TRACK_SIZE = 100
    CONFIDENCE_THRESHOLD = 0.5

    def __init__(self):
        self.trackID = 0
        self.tracks = GraphTracks(self.TRACK_SIZE)

    class __Internal:

        def __compute_similarity(self, instances, new_poses, distance, *args):
            #TODO embedded the track_id as attribute, cf complete_bipartite_graph method source code
            bigraph = nx.complete_bipartite_graph(len(instances), len(new_poses))
            offset = len(instances)
            node_to_remove = set()
            for u,v in bigraph.edges():
                dist = distance(instances[u].pose, new_poses[v-offset], *args)
                if dist is None:
                    bigraph.remove_edge(u,v)
                    node_to_remove.add(v-offset)
                else:
                    bigraph[u][v]["weight"] = dist
            
            #TODO remove node in the graph ?
            new_poses = [pose for idx, pose in enumerate(new_poses) if idx not in node_to_remove]
            return bigraph, new_poses

        def __matching(self, bigraph, instances, new_poses):
            matching = nx.max_weight_matching(bigraph)
            new_instances = []
            new_matched_poses_idx = []
            offset = len(instances)
            #print('len of new_poses: {}'.format(len(new_poses)))
            #print('len of instances: {}'.format(len(instances)))
            #print('edges: {}'.format(bigraph.edges()))
            #print('matching: {}'.format(list(matching)))
            for u,v in matching:
                #print('u: {}, v: {}'.format(u,v))
                left = min(u,v)
                right = max(u-offset, v-offset)
                #TODO threshold if weight too low then initiate new track ?
                new_instances.append(Instance(instances[left].id, new_poses[right]))
                new_matched_poses_idx.append(right)
            
            unmatched_new_poses_gen = (unmatched_new_pose for unmatched_new_pose_idx, unmatched_new_pose in enumerate(new_poses) if unmatched_new_pose_idx not in new_matched_poses_idx)
            for pose in unmatched_new_poses_gen:
                new_instances.append(Instance(self.trackID, pose))
                # print('track_id: {}'.format(self.trackID))
                self.trackID += 1
            
            return new_instances

        def update(self, new_poses):
            instances = self.tracks.get_last_valid_poses()

            bigraph, new_poses = self.__compute_similarity(instances, new_poses, distance.skeleton_iou, PoseTracker.CONFIDENCE_THRESHOLD)

            new_instances = self.__matching(bigraph, instances, new_poses)

            self.tracks.add_instances(new_instances)

        def get_current_poses(self):
            return self.tracks.get_last_poses()
    
    def update(self, new_poses):
        #TODO check if pose valid, i.e. remove outlier
        new_instances = []
        for pose in new_poses:
            if distance.check_skeleton_bb(pose, PoseTracker.CONFIDENCE_THRESHOLD) is None:
                continue
            new_instances.append(Instance(self.trackID, pose))
            # print('track_id: {}'.format(self.trackID))
            self.trackID += 1
        
        self.tracks.add_instances(new_instances)

        self.__class__ = self.__Internal

    def get_current_poses(self):
        return self.tracks.get_last_poses()