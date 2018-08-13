import tracker.skeleton_utils as utils
import math

def euclidean_similarity(pose1, pose2, threshold):
    return -1/(1+euclidean_distance(pose1, pose2, threshold))

def euclidean_distance(pose1, pose2, threshold):
    num_joints = len(pose1)//3
    distance = 0.0
    for joint_idx in range(num_joints):
        if max(pose1(3*joint_idx+2), pose2(3*joint_idx+2)) > threshold:
            distance += (pose1[3*joint_idx]-pose2[3*joint_idx])**2 + (pose1[3*joint_idx+1]-pose2[3*joint_idx+1])**2
    
    return math.sqrt(distance)

def check_skeleton_bb(pose, threshold):
    return utils.extract_bounding_box(pose, threshold)

def skeleton_iou(pose1, pose2, threshold):
    '''
    *--x--*
    |x   x|
    |     |
    x     x
    | x x |
    |     |
    |x   x|
    |     |
    *x---x*
    '''

    bb1 = utils.extract_bounding_box(pose1, threshold)
    bb2 = utils.extract_bounding_box(pose2, threshold)

    if bb1 is None or bb2 is None:
        return 0.0
    else:
        return bb_iou(bb1, bb2)

def bb_iou(bb1, bb2):
    '''
    Calculates the Intersection over Union (IoU) of two bounding boxes.
    see <https://stackoverflow.com/questions/25349178/calculating-percentage-of-bounding-box-overlap-for-image-detector-evaluation>

    Parameters
    ----------
    bb1 : list ['x1', 'y1', 'x2', 'y2']
        The (x1, y1) position is at the top left corner,
        the (x2, y2) position is at the bottom right corner
    bb2 : list ['x1', 'y1', 'x2', 'y2']
        The (x1, y2) position is at the top left corner,
        the (x2, y2) position is at the bottom right corner

        p1 *-----
           |     |
           |_____* p2

    Returns
    -------
    float
        in [0, 1]
    '''

    # determine the (x, y)-coordinates of the intersection rectangle
    x_left = max(bb1[0], bb2[0])
    y_top = max(bb1[1], bb2[1])
    x_right = min(bb1[2], bb2[2])
    y_bottom = min(bb1[3], bb2[3])

    if x_right < x_left or y_bottom < y_top:
        return 0.0

    # compute the area of intersection rectangle
    # handles both corner cases of non overlapping boxes
    intersection_area = max(0, x_right - x_left + 1) * max(0, y_bottom - y_top + 1)

    # compute the area of both AABBs
    bb1_area = (bb1[2] - bb1[0] + 1) * (bb1[3] - bb1[1] + 1)
    bb2_area = (bb2[2] - bb2[0] + 1) * (bb2[3] - bb2[1] + 1)

    # compute the intersection over union by taking the intersection
    # area and dividing it by the sum of prediction + ground-truth
    # areas - the interesection area
    iou = intersection_area / float(bb1_area + bb2_area - intersection_area)

    # if no intersection, return 0.0 instead of a negative IoU
    if iou < 0.0:
        return 0.0
    else:
        return iou