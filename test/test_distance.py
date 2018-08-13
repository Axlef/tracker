import pytest
import tracker.distance as distance

def test_bb_iou():
    bb1 = [39, 63, 203, 112]
    bb2 = [54, 66, 198, 114]
    expected_iou = 0.7980

    assert distance.bb_iou(bb1, bb2) == pytest.approx(expected_iou, 0.001)

    bb1 = [49, 75, 203, 125]
    bb2 = [42, 78, 186, 126]
    expected_iou = 0.7899

    assert distance.bb_iou(bb1, bb2) == pytest.approx(expected_iou, 0.001)

    bb1 = [31, 69, 201, 125]
    bb2 = [18, 63, 235, 135]
    expected_iou = 0.6125

    assert distance.bb_iou(bb1, bb2) == pytest.approx(expected_iou, 0.001)

    bb1 = [50, 72, 197, 121]
    bb2 = [54, 72, 198, 120]
    expected_iou = 0.9472

    assert distance.bb_iou(bb1, bb2) == pytest.approx(expected_iou, 0.001)

    bb1 = [35, 51, 196, 110]
    bb2 = [36, 60, 180, 108]
    expected_iou = 0.7310

    assert distance.bb_iou(bb1, bb2) == pytest.approx(expected_iou, 0.001)

    bb1 = [142, 208, 158, 346]
    bb2 = [243, 203, 348, 279]
    expected_iou = 0.0

    assert distance.bb_iou(bb1, bb2) == pytest.approx(expected_iou, 0.001)

def test_skeleton_iou():
    pose1 = [4.0, 5.0, 1.0, 2.0, 6.0, 1.0, 6.0, 6.0, 1.0, 1.0, 8.0, 1.0, 7.0, 8.0, 1.0, 3.0, 9.0, 1.0, 5.0, 9.0, 1.0, 2.0, 13.0, 1.0, 5.0, 13.0, 1.0]
    pose2 = [8.0, 1.0, 1.0, 6.0, 3.0, 1.0, 10.0, 3.0, 1.0, 5.0, 5.0, 1.0, 7.0, 5.0, 1.0, 9.0, 5.0, 1.0, 11.0, 5.0, 1.0, 6.0, 9.0, 1.0, 10.0, 9.0, 1.0]
    expected_iou = 0.1351

    assert distance.skeleton_iou(pose1, pose2, 0.5) == pytest.approx(expected_iou, 0.001)

    pose1 = [4.0, 5.0, 1.0, 2.0, 6.0, 1.0, 6.0, 6.0, 1.0, 1.0, 8.0, 1.0, 7.0, 8.0, 1.0, 3.0, 9.0, 1.0, 5.0, 9.0, 1.0, 2.0, 13.0, 1.0, 5.0, 13.0, 1.0]
    pose2 = [5.0, 4.0, 1.0, 3.0, 6.0, 1.0, 7.0, 6.0, 1.0, 2.0, 8.0, 1.0, 4.0, 8.0, 1.0, 6.0, 8.0, 1.0, 8.0, 8.0, 1.0, 3.0, 12.0, 1.0, 7.0, 12.0, 1.0]
    expected_iou = 0.6153

    assert distance.skeleton_iou(pose1, pose2, 0.5) == pytest.approx(expected_iou, 0.001)
    
    pose1 = [4.0, 5.0, 1.0, 2.0, 6.0, 1.0, 6.0, 6.0, 1.0, 1.0, 8.0, 1.0, 7.0, 8.0, 1.0, 3.0, 9.0, 1.0, 5.0, 9.0, 1.0, 2.0, 13.0, 1.0, 5.0, 13.0, 1.0]
    pose2 = [11.0, 1.0, 1.0, 9.0, 3.0, 1.0, 13.0, 3.0, 1.0, 8.0, 5.0, 1.0, 10.0, 5.0, 1.0, 12.0, 5.0, 1.0, 14.0, 5.0, 1.0, 9.0, 9.0, 1.0, 13.0, 9.0, 1.0]
    expected_iou = 0.0

    assert distance.skeleton_iou(pose1, pose2, 0.5) == pytest.approx(expected_iou, 0.001)

    pose1 = [4.0, 5.0, 1.0, 2.0, 6.0, 1.0, 6.0, 6.0, 1.0, 1.0, 8.0, 0.4, 7.0, 8.0, 1.0, 3.0, 9.0, 1.0, 5.0, 9.0, 1.0, 2.0, 13.0, 0.4, 5.0, 13.0, 0.4]
    pose2 = [5.0, 4.0, 1.0, 3.0, 6.0, 1.0, 7.0, 6.0, 1.0, 2.0, 8.0, 1.0, 4.0, 8.0, 1.0, 6.0, 8.0, 1.0, 8.0, 8.0, 1.0, 3.0, 12.0, 1.0, 7.0, 12.0, 1.0]
    expected_iou = 0.4761

    assert distance.skeleton_iou(pose1, pose2, 0.5) == pytest.approx(expected_iou, 0.001)

#TODO test euclidean_distance