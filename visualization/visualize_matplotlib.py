import matplotlib.pyplot as plt
import matplotlib.patches as patches
import tracker.skeleton_utils as utils

marker_size = 8
line_width  = 3

def show_annotation_frame(annotation, colors, edges, ax):
    for id, pose in annotation.items():
        draw_sticks(pose, edges, colors(id), line_width, ax)
        draw_joints(pose, colors(id), marker_size, ax)

        flattened_pose = [value for _, keypoint in pose.items() for value in keypoint]
        bb = utils.extract_bounding_box(flattened_pose, 0.5)
        if bb is not None:
            text_location = (bb[0], bb[1] - 10)
            draw_bounding_box(bb, colors(id), ax)
            draw_id(id, text_location, ax)

def draw_sticks(joints, edges, person_color, line_width, ax):
    for edge in edges:
        if edge[0] in joints and edge[1] in joints:
            joint1 = joints[edge[0]]
            joint2 = joints[edge[1]]
            ax.plot([joint1[0], joint2[0]], [joint1[1], joint2[1]], linewidth = line_width, color = person_color)

def draw_joints(joints, person_color, marker_size, ax):
    for _, joint in joints.items():
        ax.plot(joint[0], joint[1],'o', markersize = marker_size, markerfacecolor = person_color, markeredgecolor = 'k', markeredgewidth = 2)

def draw_bounding_box(bb, person_color, ax):
    xy  = tuple(bb[0:2])
    width  = abs(bb[2] - bb[0])
    height = abs(bb[3] - bb[1])
    ax.add_patch \
    (
        patches.Rectangle \
        (
            xy,
            width,
            height,
            fill = False,
            edgecolor = person_color,
            linewidth = line_width
        )
    )

def draw_id(id, location, ax):
    (x,y) = location
    ax.text(x, y, 'id: {}'.format(id), fontsize=14)

