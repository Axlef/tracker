import argparse
import os, glob
import json
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import skimage.io as io
import numpy as np
import time
import cv2
import colorsys

from tracker.tracker import PoseTracker
from visualization.visualize_cv import show_annotation_frame

edges = [(0,1), (1,2), (2,8), (3,9), (3,4), (4,5), (6,7), (7,8), (9,10), (10,11), (8,12), (9,12), (12,13), (13,14)]

def parse_args():

    parser = argparse.ArgumentParser(description="Visualization of PoseTrack annotations")
    parser.add_argument("--dataset", required=True, type=str, help="Directory of the PoseTrack dataset")
    parser.add_argument("--annotations", required=True, type=str, help="Directory of the annotations to visualize")
    parser.add_argument("--save", required=False, type=str, help="Directory where to save the resulted images")
    return parser.parse_args()

def total_persons_count(annolist):
    person_count = -1
    for frame in annolist:
        if frame['is_labeled'] == [0]:
            continue
        track_id = [annorect['track_id'][0] for annorect in frame['annorect']]
        if track_id:
            person_count = max(person_count, max(track_id))
    person_count += 1
    return person_count

def get_N_HexCol(N):

    HSV_tuples = [(x*1.0/N, 0.5, 0.5) for x in range(N)]
    RGB_tuples = list(map(lambda x: colorsys.hsv_to_rgb(*x), HSV_tuples))
    RGB_tuples = [tuple(map(lambda x: int(255 * x), color)) for color in RGB_tuples]
    return RGB_tuples

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
        print('Processing annotation {}...'.format(annotation_path))
        
        with open(annotation_path, 'r') as raw_annotation:
            annotation = json.load(raw_annotation)
        annolist = annotation['annolist']

        total_person = total_persons_count(annolist)
        colors = get_N_HexCol(total_person)

        for image in annolist:
            if image['is_labeled'] == [1]:
                image_path = image['image'][0]['name']
                I = cv2.imread(dataset_dir + image_path)
                if I is None:
                    print('Error loading image {}, passing'.format(dataset_dir + image_path))
                    continue
                
                image_name = os.path.basename(image_path)

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

                show_annotation_frame(poses, colors, edges, I)

                if save_dir is None:
                    cv2.imshow('Image', I)
                    cv2.waitKey(300)
                    #cv2.destroyAllWindows()
                else:
                    if not os.path.exists(save_dir + str(num_annotation)):
                        os.makedirs(save_dir + str(num_annotation))
                    cv2.imwrite(save_dir + str(num_annotation) + '/' + image_name, I)
    
if __name__ == "__main__":
   main()