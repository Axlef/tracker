import pytest
from tracker.tracker import PoseTracker
from tracker.graph_tracks import Instance
import tracker.distance as distance
import networkx as nx

@pytest.fixture
def tracker():
    PoseTracker.TRACK_SIZE = 3
    return PoseTracker._PoseTracker__Internal()

def check_bigraph(bigraph, expected_bigraph):
    assert len(bigraph) == len(expected_bigraph)

    for expected_edge in expected_bigraph:
        expected_node1 = expected_edge[0]
        expected_node2 = expected_edge[1]
        edge_found = False
        for edge in bigraph:
            node1 = edge[0]
            node2 = edge[1]
            if node1 == expected_node1 and node2 == expected_node2:
                edge_found = True
                assert edge[2] == pytest.approx(expected_edge[2], 0.001)
                break
        assert edge_found

def check_matching(new_instances, expected_instances):
    assert len(new_instances) == len(expected_instances)

    for expected_instance in expected_instances:
        expected_id = expected_instance.id
        expected_pose = expected_instance.pose
        instance_found = False
        for new_instance in new_instances:
            id = new_instance.id
            pose = new_instance.pose
            if expected_id == id:
                instance_found = True
                assert set(expected_pose) == set(pose)
                break
        assert instance_found

def test_compute_similarity(tracker):
    pose1_time1 = [4.0, 5.0, 1.0, 2.0, 6.0, 1.0, 6.0, 6.0, 1.0, 1.0, 8.0, 1.0, 7.0, 8.0, 1.0, 3.0, 9.0, 1.0, 5.0, 9.0, 1.0, 2.0, 13.0, 1.0, 5.0, 13.0, 1.0]
    pose2_time1 = [4.0, 15.0, 1.0, 2.0, 16.0, 1.0, 6.0, 16.0, 1.0, 1.0, 18.0, 1.0, 7.0, 18.0, 1.0, 3.0, 19.0, 1.0, 5.0, 19.0, 1.0, 2.0, 23.0, 1.0, 5.0, 23.0, 1.0]

    pose1_time2 = [5.0, 4.0, 1.0, 3.0, 5.0, 1.0, 7.0, 5.0, 1.0, 2.0, 7.0, 1.0, 8.0, 7.0, 1.0, 4.0, 8.0, 1.0, 6.0, 8.0, 1.0, 3.0, 12.0, 1.0, 6.0, 12.0, 1.0]
    pose2_time2 = [5.0, 16.0, 1.0, 3.0, 17.0, 1.0, 7.0, 17.0, 1.0, 2.0, 19.0, 1.0, 8.0, 19.0, 1.0, 4.0, 20.0, 1.0, 6.0, 20.0, 1.0, 3.0, 24.0, 1.0, 6.0, 24.0, 1.0]
    
    expected_bigraph = [(0, 2, 0.6153), (1, 3, 0.6153), (0, 3, 0.0), (1, 2, 0.0)]

    instances = [Instance(0, pose1_time1), Instance(1, pose2_time1)]
    new_poses = [pose1_time2, pose2_time2]

    bigraph, _ = tracker._Internal__compute_similarity(instances, new_poses, distance.skeleton_iou, 0.5)

    check_bigraph(list(bigraph.edges.data('weight')), expected_bigraph)

    pose1_time1 = [4.0, 5.0, 1.0, 2.0, 6.0, 1.0, 6.0, 6.0, 1.0, 1.0, 8.0, 1.0, 7.0, 8.0, 1.0, 3.0, 9.0, 1.0, 5.0, 9.0, 1.0, 2.0, 13.0, 1.0, 5.0, 13.0, 1.0]
    pose2_time1 = [4.0, 10.0, 1.0, 2.0, 11.0, 1.0, 6.0, 11.0, 1.0, 1.0, 13.0, 1.0, 7.0, 13.0, 1.0, 3.0, 14.0, 1.0, 5.0, 14.0, 1.0, 2.0, 18.0, 1.0, 5.0, 18.0, 1.0]

    pose1_time2 = [5.0, 4.0, 1.0, 3.0, 5.0, 1.0, 7.0, 5.0, 1.0, 2.0, 7.0, 1.0, 8.0, 7.0, 1.0, 4.0, 8.0, 1.0, 6.0, 8.0, 1.0, 3.0, 12.0, 1.0, 6.0, 12.0, 1.0]

    expected_bigraph = [(0, 2, 0.6153), (1, 2, 0.1666)]

    instances = [Instance(0, pose1_time1), Instance(1, pose2_time1)]
    new_poses = [pose1_time2]

    bigraph, _ = tracker._Internal__compute_similarity(instances, new_poses, distance.skeleton_iou, 0.5)

    check_bigraph(list(bigraph.edges.data('weight')), expected_bigraph)

    pose1_time1 = [4.0, 5.0, 1.0, 2.0, 6.0, 1.0, 6.0, 6.0, 1.0, 1.0, 8.0, 1.0, 7.0, 8.0, 1.0, 3.0, 9.0, 1.0, 5.0, 9.0, 1.0, 2.0, 13.0, 1.0, 5.0, 13.0, 1.0]

    pose1_time2 = [5.0, 4.0, 1.0, 3.0, 5.0, 1.0, 7.0, 5.0, 1.0, 2.0, 7.0, 1.0, 8.0, 7.0, 1.0, 4.0, 8.0, 1.0, 6.0, 8.0, 1.0, 3.0, 12.0, 1.0, 6.0, 12.0, 1.0]
    pose2_time2 = [5.0, 11.0, 1.0, 3.0, 12.0, 1.0, 7.0, 12.0, 1.0, 2.0, 14.0, 1.0, 8.0, 14.0, 1.0, 4.0, 15.0, 1.0, 6.0, 15.0, 1.0, 3.0, 19.0, 1.0, 6.0, 19.0, 1.0]

    expected_bigraph = [(0, 1, 0.6153), (0, 2, 0.1666)]

    instances = [Instance(0, pose1_time1)]
    new_poses = [pose1_time2, pose2_time2]

    bigraph, _ = tracker._Internal__compute_similarity(instances, new_poses, distance.skeleton_iou, 0.5)

    check_bigraph(list(bigraph.edges.data('weight')), expected_bigraph)

    # add test to check none bb

def test_matching(tracker):
    pose1_time1 = [4.0, 5.0, 1.0, 2.0, 6.0, 1.0, 6.0, 6.0, 1.0, 1.0, 8.0, 1.0, 7.0, 8.0, 1.0, 3.0, 9.0, 1.0, 5.0, 9.0, 1.0, 2.0, 13.0, 1.0, 5.0, 13.0, 1.0]
    pose2_time1 = [4.0, 15.0, 1.0, 2.0, 16.0, 1.0, 6.0, 16.0, 1.0, 1.0, 18.0, 1.0, 7.0, 18.0, 1.0, 3.0, 19.0, 1.0, 5.0, 19.0, 1.0, 2.0, 23.0, 1.0, 5.0, 23.0, 1.0]

    pose1_time2 = [5.0, 4.0, 1.0, 3.0, 5.0, 1.0, 7.0, 5.0, 1.0, 2.0, 7.0, 1.0, 8.0, 7.0, 1.0, 4.0, 8.0, 1.0, 6.0, 8.0, 1.0, 3.0, 12.0, 1.0, 6.0, 12.0, 1.0]
    pose2_time2 = [5.0, 16.0, 1.0, 3.0, 17.0, 1.0, 7.0, 17.0, 1.0, 2.0, 19.0, 1.0, 8.0, 19.0, 1.0, 4.0, 20.0, 1.0, 6.0, 20.0, 1.0, 3.0, 24.0, 1.0, 6.0, 24.0, 1.0]

    instances = [Instance(0, pose1_time1), Instance(1, pose2_time1)]
    new_poses = [pose1_time2, pose2_time2]

    expected_instances = [Instance(0, pose1_time2), Instance(1, pose2_time2)]

    bigraph, new_poses = tracker._Internal__compute_similarity(instances, new_poses, distance.skeleton_iou, 0.5)

    new_instances = tracker._Internal__matching(bigraph, instances, new_poses)

    check_matching(new_instances, expected_instances)

    pose1_time1 = [4.0, 5.0, 1.0, 2.0, 6.0, 1.0, 6.0, 6.0, 1.0, 1.0, 8.0, 1.0, 7.0, 8.0, 1.0, 3.0, 9.0, 1.0, 5.0, 9.0, 1.0, 2.0, 13.0, 1.0, 5.0, 13.0, 1.0]
    pose2_time1 = [4.0, 10.0, 1.0, 2.0, 11.0, 1.0, 6.0, 11.0, 1.0, 1.0, 13.0, 1.0, 7.0, 13.0, 1.0, 3.0, 14.0, 1.0, 5.0, 14.0, 1.0, 2.0, 18.0, 1.0, 5.0, 18.0, 1.0]

    pose1_time2 = [5.0, 4.0, 1.0, 3.0, 5.0, 1.0, 7.0, 5.0, 1.0, 2.0, 7.0, 1.0, 8.0, 7.0, 1.0, 4.0, 8.0, 1.0, 6.0, 8.0, 1.0, 3.0, 12.0, 1.0, 6.0, 12.0, 1.0]

    instances = [Instance(0, pose1_time1), Instance(1, pose2_time1)]
    new_poses = [pose1_time2]

    expected_instances = [Instance(0, pose1_time2)]

    bigraph, new_poses = tracker._Internal__compute_similarity(instances, new_poses, distance.skeleton_iou, 0.5)

    new_instances = tracker._Internal__matching(bigraph, instances, new_poses)

    check_matching(new_instances, expected_instances)

    pose1_time1 = [4.0, 5.0, 1.0, 2.0, 6.0, 1.0, 6.0, 6.0, 1.0, 1.0, 8.0, 1.0, 7.0, 8.0, 1.0, 3.0, 9.0, 1.0, 5.0, 9.0, 1.0, 2.0, 13.0, 1.0, 5.0, 13.0, 1.0]

    pose1_time2 = [5.0, 4.0, 1.0, 3.0, 5.0, 1.0, 7.0, 5.0, 1.0, 2.0, 7.0, 1.0, 8.0, 7.0, 1.0, 4.0, 8.0, 1.0, 6.0, 8.0, 1.0, 3.0, 12.0, 1.0, 6.0, 12.0, 1.0]
    pose2_time2 = [5.0, 11.0, 1.0, 3.0, 12.0, 1.0, 7.0, 12.0, 1.0, 2.0, 14.0, 1.0, 8.0, 14.0, 1.0, 4.0, 15.0, 1.0, 6.0, 15.0, 1.0, 3.0, 19.0, 1.0, 6.0, 19.0, 1.0]

    instances = [Instance(0, pose1_time1)]
    new_poses = [pose1_time2, pose2_time2]

    tracker.trackID = 1

    bigraph, new_poses = tracker._Internal__compute_similarity(instances, new_poses, distance.skeleton_iou, 0.5)

    expected_instances = [Instance(0, pose1_time2), Instance(1, pose2_time2)]

    new_instances = tracker._Internal__matching(bigraph, instances, new_poses)

    assert tracker.trackID == 2

    check_matching(new_instances, expected_instances)