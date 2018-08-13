def extract_bounding_box(pose, threshold):
    # Discard pose with less than two keypoints (only one keypoint...)
    if len(pose) < 3*2:
        return None
    
    x_min = float('inf')
    x_max = 0.0
    y_min = x_min
    y_max = x_max

    for part in range(len(pose)//3):
        score = pose[3*part+2]

        if score > threshold:
            x = pose[3*part]
            y = pose[3*part+1]

            # set X
            if x_max < x:
                x_max = x
            if x_min > x:
                x_min = x

            # set Y
            if y_max < y:
                y_max = y
            if y_min > y:
                y_min = y
    
    if x_max >= x_min and y_max >= y_min:
        return [x_min, y_min, x_max, y_max]
    else:
        return None