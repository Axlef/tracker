import argparse
import os, glob
import json
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import skimage.io as io
import numpy as np
import time

from tracker.tracker import PoseTracker
from visualization.visualize_matplotlib import show_annotation_frame

edges = [(0,1), (1,2), (2,8), (3,9), (3,4), (4,5), (6,7), (7,8), (9,10), (10,11), (8,12), (9,12), (12,13), (13,14)]

def parse_args():

    parser = argparse.ArgumentParser(description="Visualization of PoseTrack annotations")
    parser.add_argument("--dataset", required=True, type=str, help="Directory of the PoseTrack dataset")
    parser.add_argument("--annotations", required=True, type=str, help="Directory of the annotations to visualize")
    parser.add_argument("--save", required=False, type=str, default=None, help="Directory where to save the resulted images")
    return parser.parse_args()

def total_persons_count(annolist):
    person_count = -1
    for frame in annolist:
        if frame['is_labeled'] == [0]:
            continue
        track_id = [annorect['track_id'][0] for annorect in frame['annorect']]
        person_count = max(person_count, max(track_id))
    person_count += 1
    return person_count

def main():

    args = parse_args()
    (dataset_dir, annotations_dir, save_dir) = (args.dataset, args.annotations, args.save)

    if not os.path.exists(dataset_dir):
        raise IOError('Dataset dir {} does not exist'.format(dataset_dir))
    if not os.path.exists(annotations_dir):
        raise IOError('Annotations dir {} does not exist'.format(annotations_dir))
    if save_dir is not None and not os.path.exists(save_dir):
        raise IOError('Saving dir {} does not exist'.format(save_dir))

    for num_annotation, annotation_path in enumerate(sorted(glob.glob(annotations_dir + "/*.json"))):
        with open(annotation_path, 'r') as raw_annotation:
            annotation = json.load(raw_annotation)
        annolist = annotation['annolist']

        total_person = total_persons_count(annolist)
        colors = plt.cm.get_cmap('hsv', total_person)

        for image in annolist:
            if image['is_labeled'] == [1]:
                image_path = image['image'][0]['name']
                try:
                    I = io.imread(dataset_dir + image_path)
                except:
                    print('Error loading image {}, passing'.format(dataset_dir + image_path))
                    continue
                
                image_name = os.path.basename(image_path)
                (height, width, _) = I.shape

                fig = plt.figure(frameon=False)
                # fig.set_size_inches(width//96, height//96)
                ax = plt.Axes(fig, [0., 0., 1., 1.])
                ax.set_axis_off()
                fig.add_axes(ax)
                ax.imshow(I)

                # gather annotation data for this image
                persons = image['annorect']
                poses = {}
                for person in persons:
                    if len(person['annopoints']) == 0:
                        continue
                    track_id = person['track_id'][0]
                    points = person['annopoints'][0]['point']
                    pose = {}
                    for point in points:
                        if 'score' in point:
                            score = point['score'][0]
                        else:
                            score = 1.0
                        pose[point['id'][0]] = (point['x'][0], point['y'][0], score)
                    poses[track_id] = pose

                show_annotation_frame(poses, colors, edges, ax)

                if save_dir is None:
                    plt.show(block = True)
                else:
                    if not os.path.exists(save_dir + str(num_annotation)):
                        os.makedirs(save_dir + str(num_annotation))

                    plt.savefig(save_dir + str(num_annotation) + '/' + image_name)
                    plt.close(fig)

if __name__ == "__main__":
   main()