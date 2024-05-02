# Object Tracking Project

This project performs object tracking on a video using initial bounding boxes defined in a JSON file. It utilizes OpenCV for computer vision tasks.

## Usage

### Prerequisites
- Python 3.8 or later
- Docker

### Installation

1. Clone the repository:

```
git clone https://github.com/federicoguilenea/object-tracking-project.git
cd object-tracking-project
```

2. Install dependencies:

```
pip install -r requirements.txt
```

### Usage

Run the object tracking script using the following command:

```
python src/main.py --video /path/to/input/video.mkv --json /path/to/initial_conditions.json --output /path/to/output/video.mp4
```

Replace `/path/to/input/video.mkv` with the path to your input video file, `/path/to/initial_conditions.json` with the path to your JSON file containing initial bounding boxes, and `/path/to/output/video.mp4` with the desired output path.

### Docker Usage

Alternatively, you can use Docker to run the project:

```
docker build -t object-tracking .
docker run --name object-tracking-container -v /path/to/assets:/app/assets -v /path/to/output:/app/output object-tracking --video /app/assets/input.mkv --json /app/assets/initial_conditions.json --output /app/output/output.mp4
```

## How It Works

The object tracking script utilizes the following steps:

1. **Initialization**: It loads the input video and the initial bounding boxes from the JSON file.

2. **Object Tracking**: Using the initial bounding boxes, it initializes object trackers for each object in the video. The CSRT (Discriminative Correlation Filter with Channel and Spatial Reliability) algorithm is used for object tracking by default.

3. **Frame Processing**: The script iterates through each frame of the video, updating the object trackers to track the objects.

4. **Output Generation**: Bounding boxes are drawn around the tracked objects in each frame, and the resulting frames are written to an output video file.

By following these steps, the script is able to perform object tracking on the input video with the provided initial conditions.

## Example

An example input video (`input.mkv`) with three football players is provided in the `assets` directory. After running the object tracking script, a video (`output.mp4`) demonstrating the tracking results will be generated in the `output` directory. You can use this example to test the functionality of the object tracking script and explore different tracking algorithms such as KCF (Kernelized Correlation Filters).


## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvement, feel free to open an issue or create a pull request.
