import cv2
import json
import argparse
import logging
import os
from tqdm import tqdm

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_bbox(coords):
    """
    Converts bounding box coordinates to the format required by OpenCV.
    Args:
        coords (list): List of coordinates [x, y, w, h].
    Returns:
        tuple: Tuple of coordinates (x, y, w, h).
    """
    x, y, w, h = coords
    return x, y, w, h

def track_objects(video_path, json_path, output_path):
    """
    Performs object tracking on a video using initial bounding boxes
    defined in a JSON file.
    Args:
        video_path (str): Path to the input video file.
        json_path (str): Path to the JSON file containing initial bounding boxes.
        output_path (str): Path to the output video file.
    """
    # Load initial conditions from JSON file
    with open(json_path, 'r') as file:
        initial_conditions = json.load(file)

    # Initialize object tracker
    trackers = cv2.legacy.MultiTracker_create()

    # Read input video
    cap = cv2.VideoCapture(video_path)

    # Variables for output video
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    # Initialize object tracking on the first frame
    ret, frame = cap.read()
    for obj in initial_conditions:
        bbox = get_bbox(obj['coordinates'])
        trackers.add(cv2.legacy.TrackerCSRT_create(), frame, tuple(bbox))

    # Process frames and update object tracking
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    with tqdm(total=frame_count) as pbar:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            success, boxes = trackers.update(frame)

            # Draw bounding boxes on each frame
            for box in boxes:
                x, y, w, h = [int(v) for v in box]
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Write frame to output video
            out.write(frame)
            pbar.update(1)

    # Release resources
    cap.release()
    out.release()
    cv2.destroyAllWindows()

def main():
    """
    Main function of the program.
    """
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Object tracking in a video.')
    parser.add_argument('--video', type=str, required=True, help='Path to the input video file.')
    parser.add_argument('--json', type=str, required=True, help='Path to the JSON file with initial bounding boxes.')
    parser.add_argument('--output', type=str, required=True, help='Path to the output video file.')
    args = parser.parse_args()

    # Check if input files exist
    if not os.path.isfile(args.video):
        logging.error(f"The video file '{args.video}' does not exist.")
        return
    if not os.path.isfile(args.json):
        logging.error(f"The JSON file '{args.json}' does not exist.")
        return

    # Perform object tracking
    logging.info("Starting object tracking...")
    track_objects(args.video, args.json, args.output)
    logging.info("Object tracking completed.")

if __name__ == '__main__':
    main()
