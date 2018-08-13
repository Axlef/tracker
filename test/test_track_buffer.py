import pytest
from tracker.track_buffer import TrackBuffer

@pytest.fixture
def track_buffer():
    return TrackBuffer(3)

def checker(track_buffer, 
            expected_cur_valid, 
            expected_counter_none, 
            expected_untracked):
    
    assert track_buffer.cur_valid == expected_cur_valid
    assert track_buffer.counter_none == expected_counter_none
    assert track_buffer.untracked == expected_untracked 

def test_append_simple(track_buffer):
    track_buffer.append(10)
    checker(track_buffer, 0, 0, False)
    assert track_buffer.get_last_valid_pose() == 10

    track_buffer.append(5)
    checker(track_buffer, 1, 0, False)
    assert track_buffer.get_last_valid_pose() == 5

    track_buffer.append(15)
    checker(track_buffer, 2, 0, False)
    assert track_buffer.get_last_valid_pose() == 15

def test_append_none(track_buffer):
    track_buffer.append(None)
    checker(track_buffer, -1, 1, False)
    assert track_buffer.get_last_pose() is None

    track_buffer.append(None)
    checker(track_buffer, -1, 2, False)
    assert track_buffer.get_last_pose() is None

def test_append_simple_none(track_buffer):
    track_buffer.append(10)
    track_buffer.append(None)

    checker(track_buffer, 0, 1, False)
    assert track_buffer.get_last_pose() is None
    assert track_buffer.get_last_valid_pose() == 10

def test_append_none_simple(track_buffer):
    track_buffer.append(None)
    checker(track_buffer, -1, 1, False)

    track_buffer.append(None)
    checker(track_buffer, -1, 2, False)

    track_buffer.append(10)

    checker(track_buffer, 2, 0, False)
    assert track_buffer.get_last_pose() == 10
    assert track_buffer.get_last_valid_pose() == 10

def test_append_full(track_buffer):
    track_buffer.append(10)
    track_buffer.append(None)
    track_buffer.append(12)

    checker(track_buffer, 2, 0, False)

    track_buffer.append(5)
    checker(track_buffer, 0, 0, False)
    assert track_buffer.get_last_pose() == 5
    assert track_buffer.get_last_valid_pose() == 5

    track_buffer.append(15)
    checker(track_buffer, 1, 0, False)
    assert track_buffer.get_last_pose() == 15
    assert track_buffer.get_last_valid_pose() == 15

def test_append_full_none(track_buffer):
    track_buffer.append(None)
    track_buffer.append(None)
    track_buffer.append(None)

    checker(track_buffer, -1, 3, True)
    assert track_buffer.is_untracked() == True
