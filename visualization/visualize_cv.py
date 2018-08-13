import tracker.skeleton_utils as utils
import cv2

marker_size = 8
line_width  = 3

def show_annotation_frame(annotation, colors, edges, img):
    for id, pose in annotation.items():
        color = colors[id]
        draw_sticks(pose, edges, color, line_width, img)
        draw_joints(pose, color, marker_size, img)

        flattened_pose = [value for _, keypoint in pose.items() for value in keypoint]
        bb = utils.extract_bounding_box(flattened_pose, 0.5)
        if bb is not None:
            text_location = (int(bb[0]), int(bb[1] - 10))
            draw_bounding_box(bb, color, img, line_width)
            draw_id(id, text_location, img)

def draw_sticks(joints, edges, person_color, line_width, img):
    for edge in edges:
        if edge[0] in joints and edge[1] in joints:
            joint1 = tuple(map(int, joints[edge[0]]))
            joint2 = tuple(map(int, joints[edge[1]]))
            cv2.line(img, joint1[0:2], joint2[0:2], person_color, line_width)

def draw_joints(joints, person_color, marker_size, img):
    for _, joint in joints.items():
        center = tuple(map(int,joint[0:2]))
        cv2.circle(img, center, marker_size, person_color, -1)

def draw_bounding_box(bb, person_color, img, line_width):
    xy_top_left = tuple(map(int, bb[0:2]))
    xy_bottom_right = tuple(map(int, bb[2:4]))
    cv2.rectangle(img, xy_top_left, xy_bottom_right, person_color, line_width)

def draw_id(id, location, img):
    cv2.putText(img, 'id {}'.format(id), location, cv2.FONT_HERSHEY_PLAIN, 2, (255,255,255), 2, cv2.LINE_AA)