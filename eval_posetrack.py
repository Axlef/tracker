import argparse
import os, glob
import json

from tracker.tracker import PoseTracker

def parse_args():

    parser = argparse.ArgumentParser(description="Evaluation of tracker against PoseTrack dataset")
    parser.add_argument("--annotations", required=True, type=str, help="Directory containing ground truth annotatations per sequence in json format")
    parser.add_argument("--predictions", required=True, type=str, help="Directory to output the json tracking result")
    return parser.parse_args()


def main():

    args = parse_args()
    (annotations_dir, predictions_dir) = (args.annotations, args.predictions)

    if not os.path.exists(annotations_dir):
        raise IOError('Annotations dir {} does not exist'.format(annotations_dir))
    if not os.path.exists(predictions_dir):
        raise IOError('Predictions dir {} does not exist'.format(predictions_dir))
    
    for annotation_path in sorted(glob.glob(annotations_dir + "/*.json")):

        tracker = PoseTracker()

        filename = os.path.basename(annotation_path)

        print('Processing file {}...'.format(filename))

        with open(annotation_path, 'r') as raw_annotation:
            annotation = json.load(raw_annotation)
        gt = annotation['annolist']
        annolists_out = []
        for image in gt:
            # copy immutable data
            annolist_out = \
            {
                'image': image['image'],
                'annorect': image['annorect'],
                'is_labeled': image['is_labeled']
            }
            if 'ignore_regions' in image:
                annolist_out['ignore_regions'] = image['ignore_regions']
            if image['is_labeled'] == [0]:
                annolists_out.append(annolist_out)
                continue
            
            persons = image['annorect']
            poses = []

            for person in persons:
                if len(person['annopoints']) == 0:
                    continue
                points = person['annopoints'][0]['point']
                pose = []
                for point in points:
                    pose.extend([point['x'][0], point['y'][0], 1.0])
                poses.append(pose)
            
            tracker.update(poses)
            instances = tracker.get_current_poses()

            annorects_out = []
            for id, pose in instances.items():
                # print('id: {}'.format(id))
                annorect = \
                {
                    'score': [1.0],
                    'track_id': [id]
                }
                point = []
                for idx in range(len(pose)//3):
                    keypoint = \
                    {
                        'id': [idx],
                        'x':  [pose[idx*3]],
                        'y':  [pose[idx*3+1]],
                        'score': [1.0],
                        'is_visible': [1]
                    }
                    point.append(keypoint)

                annorect['annopoints'] = [{'point': point}]
                annorects_out.append(annorect)
            
            annolist_out['annorect'] = annorects_out
            annolists_out.append(annolist_out)
        
        raw_prediction_data = {'annolist': annolists_out}
        prediction_path = predictions_dir + filename
        with open(prediction_path, 'w') as prediction_file:
            json.dump(raw_prediction_data, prediction_file)
        print('Data dumped to {}'.format(prediction_path))

if __name__ == "__main__":
   main()
        
        