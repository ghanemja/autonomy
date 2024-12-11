import cv2
import numpy as np

from pupil_apriltags import Detector

at_detector = Detector(
    families='tag36h11',
    nthreads=1,
    quad_decimate=1.0,
    quad_sigma=0.0,
    refine_edges=1,
    decode_sharpening=0.25,
    debug=0
)

def get_point_below_tag(T_camera_tag, meters_below, K):
    """
    given a 4x4 transform FROM the tag TO the camera,
    compute the 3D location of a point meters_below the tag
    and return the 2D location of that point in the image frame.

    returns (3d loc), (2d loc)
    """
    # get inverse transform
    T_tag_camera = np.linalg.inv(T_camera_tag)
    # find 3D location of point below the tag
    T_tag_camera[1,3] -= meters_below
    # convert back to being wrt the camera frame
    T_camera_tag = np.linalg.inv(T_tag_camera)
    
    x_cam = T_camera_tag[0:3, 3:]
    x_image = np.matmul(K, x_cam)

    return x_cam, [x_image[0] / x_image[2], x_image[1] / x_image[2]]

def detect_tags(img, target_point_dist=None, visualize=None):
    cx = img.shape[1] / 2.0
    cy = img.shape[0] / 2.0
    fx = 600
    fy = 600
    intrinsics = ([fx, fy, cx, cy])
    K = np.array([[fx, 0.0, cx],
                [0.0, fy, cy],
                [0.0, 0.0, 1.0]])
    tag_size = 0.165    # (meters)
    
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    tags = at_detector.detect(img_gray, estimate_tag_pose=True,
                              camera_params=intrinsics, tag_size=tag_size)
    out = {}

    # loop over the AprilTag detection results
    for tag in tags:
        out[tag.tag_id] = {
            "tag": tag,
        }
        
        if visualize:
            # extract the bounding box (x, y)-coordinates for the AprilTag
            # and convert each of the (x, y)-coordinate pairs to integers
            (ptA, ptB, ptC, ptD) = tag.corners
            ptB = (int(ptB[0]), int(ptB[1]))
            ptC = (int(ptC[0]), int(ptC[1]))
            ptD = (int(ptD[0]), int(ptD[1]))
            ptA = (int(ptA[0]), int(ptA[1]))
            # draw the bounding box of the AprilTag detection
            cv2.line(img, ptA, ptB, (0, 255, 0), 2)
            cv2.line(img, ptB, ptC, (0, 255, 0), 2)
            cv2.line(img, ptC, ptD, (0, 255, 0), 2)
            cv2.line(img, ptD, ptA, (0, 255, 0), 2)
            # draw the center (x, y)-coordinates of the AprilTag
            (cX, cY) = (int(tag.center[0]), int(tag.center[1]))
            cv2.circle(img, (cX, cY), 5, (0, 0, 255), -1)
            # draw the tag family on the image
            tagFamily = tag.tag_family.decode("utf-8")
            cv2.putText(img, tagFamily, (ptA[0], ptA[1] - 15),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        if target_point_dist is not None:
            ##### Detect point set distance below tag #####
            T_camera_tag = np.zeros((4,4))
            T_camera_tag[3,3] = 1.0
            T_camera_tag[0:3,3:] = tag.pose_t
            T_camera_tag[0:3,0:3] = tag.pose_R
            
            p, (px, py) = get_point_below_tag(T_camera_tag, meters_below=target_point_dist, K=K)
            
            out[tag.tag_id]["target"] = {
                "position": p,
                "pixel_coords": (px, py)
            }

            if visualize:
                # Draw line from tag center to (px,py) on img. Hint, use cv2.line
                cv2.line(img, (int(px), int(py)), (cX, cY), (0, 255, 0), 5)
    return out