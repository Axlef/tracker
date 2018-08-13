import pytest
from tracker.graph_tracks import GraphTracks, Instance

@pytest.fixture
def tracks():
    return GraphTracks(3)

def instances_lists_checker(instances1, instances2):
    assert len(instances1) == len(instances2)

    for instance1 in instances1:
        (id1, pose1) = (instance1.id, instance1.pose)
        instance_found = False
        for instance2 in instances2:
            (id2, pose2) = (instance2.id, instance2.pose)
            if id1 == id2:
                assert pose1 == pose2
                instance_found = True
                break
        assert instance_found

def instances_dicts_checker(instances1, instances2):
    assert len(instances1) == len(instances2)

    for id, pose in instances1.items():
        assert id in instances2
        assert pose == instances2[id]


def test_add_simple(tracks):
    instances = [Instance(0, 10), Instance(1, 5)]
    instances_dict = {0:10, 1:5}

    tracks.add_instances(instances)

    res_instances_valid = tracks.get_last_valid_poses()
    instances_lists_checker(res_instances_valid, instances)

    res_instances = tracks.get_last_poses()
    instances_dicts_checker(res_instances, instances_dict)

    instances = [Instance(0,15), Instance(1,20)]
    instances_dict = {0:15, 1:20}

    tracks.add_instances(instances)

    res_instances_valid = tracks.get_last_valid_poses()
    instances_lists_checker(res_instances_valid, instances)

    res_instances = tracks.get_last_poses()
    instances_dicts_checker(res_instances, instances_dict)

def test_add_new_id(tracks):
    instances = [Instance(0, 10), Instance(1, 5)]
    instances_dict = {0:10, 1:5}

    tracks.add_instances(instances)

    res_instances_valid = tracks.get_last_valid_poses()
    instances_lists_checker(res_instances_valid, instances)

    res_instances = tracks.get_last_poses()
    instances_dicts_checker(res_instances, instances_dict)

    instances = [Instance(0, 15), Instance(2, 20)]
    tracks.add_instances(instances)

    res_instances_valid = tracks.get_last_valid_poses()
    res_instances_valid_expected = [Instance(0, 15), Instance(1,5), Instance(2,20)]
    instances_lists_checker(res_instances_valid, res_instances_valid_expected)

    res_instances = tracks.get_last_poses()
    res_instances_expected = {0:15,2:20}
    instances_dicts_checker(res_instances, res_instances_expected)

def test_track_extinction(tracks):
    instances =  [Instance(0,1)]
    tracks.add_instances(instances)

    assert len(tracks.graph) == 1

    instances = [Instance(1,2)]
    tracks.add_instances(instances)

    assert len(tracks.graph) == 2

    tracks.add_instances(instances)

    assert len(tracks.graph) == 2

    tracks.add_instances(instances)

    assert len(tracks.graph) == 1


