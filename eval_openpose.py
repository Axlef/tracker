import argparse
import os, glob
import json
import time

from tracker.tracker import PoseTracker

def parse_args():

    parser = argparse.ArgumentParser(description="Evaluation of tracker against Openpose generated keypoint annotation on PoseTrack dataset")
    parser.add_argument("--annotations", required=True, type=str, help="Directory containing ground truth annotatations per sequence in json format")
    parser.add_argument("--predictions", required=True, type=str, help="Directory to output the json tracking result")
    return parser.parse_args()

def openpose_to_posetrack(pose_openpose):
    openpose_to_posetrack_list = [10, 9, 8, 11, 12, 13, 4, 3, 2, 5, 6, 7, 15, 0, 15]
    return [tuple(pose_openpose[3*kp:3*kp+3]) for kp in openpose_to_posetrack_list]

def main():

    args = parse_args()
    (annotations_dir, predictions_dir) = (args.annotations, args.predictions)

    if not os.path.exists(annotations_dir):
        raise IOError('Annotations dir {} does not exist'.format(annotations_dir))
    if not os.path.exists(predictions_dir):
        raise IOError('Predictions dir {} does not exist'.format(predictions_dir))

    tracker = PoseTracker()
    annolists = []

    for root, dirs, files in os.walk(annotations_dir):
        print('Traversing {}'.format(root))
        annotations = [file for file in files if '.json' in file]
        for annotation_file in sorted(annotations):
            with open(os.path.join(root, annotation_file), 'r') as raw_annotation:
                annotation = json.load(raw_annotation)
            
            image_name = os.path.join(root, annotation_file.split('_')[0] + '.jpg')
            annolist = \
            {
                'is_labeled': [1],
                'image': [{'name': image_name}]
            }

            poses = []
            for people in annotation['people']:
                pose = people['pose_keypoints_2d']
                if pose:
                    poses.append(pose)

            tracker.update(poses)
            instances = tracker.get_current_poses()

            annorects = []
            for id, pose in instances.items():
                annorect = \
                {
                    'score': [1.0],
                    'track_id': [id]
                }
                pose = openpose_to_posetrack(pose)
                point = []
                for id_kp, kp in enumerate(pose):
                    if kp[0] == 0.0 and kp[1] == 0.0:
                        continue
                    keypoint = \
                    {
                        'id': [id_kp],
                        'x': [kp[0]],
                        'y': [kp[1]],
                        'score': [kp[2]],
                        'is_visible': [1]
                    }
                    point.append(keypoint)

                annorect['annopoints'] = [{'point': point}]
                annorects.append(annorect)
            
            annolist['annorect'] = annorects
            annolists.append(annolist)
    
        raw_prediction_data = {'annolist': annolists}
        prediction_path = predictions_dir + root.split('/')[-1] + '_relpath_5sec_testsub.json'
        with open(prediction_path, 'w') as prediction_file:
            json.dump(raw_prediction_data, prediction_file)
    
if __name__ == "__main__":
   main()