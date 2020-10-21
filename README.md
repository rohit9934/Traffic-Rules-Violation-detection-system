### Disclaimer:
This project was created by [Rohit Sharma](https://github.com/rohit9934/) as the final year project for bachelors course. I thouroughly enjoyed working on these projects and training the dataset for helmet detection.

# Traffic Rules Violation Detection System
The number of vehicles has increased drastically in the last few decades making it difficult to monitor each and every vehicle for traffic management and law enforcement purposes. We proposed a computer vision-based solution using deep learning that automatically detects traffic violators.
The main objective is to detect vehicles that do not follow the rules of traffic, such as overspeeding, overloading, not wearing a helmet and running on the wrong side of the road. We use Yolov3 for object detection and DeepSort for tracking the vehicles and pedestrians. The system detects the type of violation along with the vehicle information, maintains a log of violations, provides a detailed dashboard and provides alerts to the traffic police personnel. The logs can also be used for forensic purposes.

# Datasets and Models
I have used dataset available in internet for helmet images and trained the model, the [Model](https://drive.google.com/file/d/1_xBdP1GRK4i7yzJP8_a5GWaejZZKjdyI/view) is required to run the project. Kindly download it.

# Working
I have done detection of traffic violations in real time using our owned trained haar cascades for vehicle and pedestrians detection, our own trained helmet detection model written in **YOLO v3** and got satisfactory results.

# Get Started
* Clone the Repository
* Download the model and copy it into the same directory
* Make sure all files are in same directory.
* Go to line 16 of all_vehicles.py and rename the video.
* Run all_vehicles.py

# Our Results
 To see, the results. open **video.mp4**
