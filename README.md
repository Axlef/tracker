# Tracking human by skeletons

Tracker by skeletons for monitoring people in a frame

## Requirements

* Python 3.4 or superior

## Installation

The python dependencies can easily be installed with pip:

```bash
pip3 install -r requirements.txt
```

## Quick start

The tracker is easy to use with the `PoseTracker` object.

```python
import numpy as np
from tracker.tracker import PoseTracker

tracker = PoseTracker()

skeletons = np.array([[0.0, 0.0, 1.0, 1.5], [2.0, 4.0, 3.0, 5.0]]) # define two skeletons with only two keypoints
tracker.update(skeletons)
instances = tracker.get_current_poses()
for id, pose in instances.items():
    # check id and pose e.g.
    # 0 --> [0.0, 0.0, 1.0, 1.5]
    # 1 --> [2.0, 4.0, 3.0, 5.0]
```

Additional scripts are provided for visualisation and evaluation purposes. The visualisation scripts (i.e. `visualize_posetrack` and `visualize_posetrack_matplotlib.py`) allow to visualise tracking on images with skeletons groundtruth in the [PoseTrack](https://posetrack.net/) dataset format. Usage example:

```bash
python3 visualize_posetrack --dataset=posetrack-images/ --annotations=posetrack-gt/
```

The evaluation scripts (i.e. `eval_openpose.py` and `eval_posetrack.py`) measure the performance of the tracker on the PoseTrack dataset with groundtruth skeletons annotations from openpose (`eval_openpose.py`) and groundtruth skeletons annotations from PoseTrack (`eval_posetrack.py`). The two scripts outputs a .json file per sequence that may be upload on the PoseTrack server or checked locally with the PoseTrack evaluation API.