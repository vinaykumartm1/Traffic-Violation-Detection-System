# Traffic Violation and Distracted Driving Detection

## Overview

This project focuses on detecting various traffic violations and distracted driving behaviors using deep learning models (YOLO v5 & v8) combined with OpenCV.

## Features

*   **Helmet Compliance Detection:** Identifies whether a motorcyclist is wearing a helmet.
*   **Triple Riding Detection:** Detects if more than two people are riding a motorcycle.
*   **Red-Light Violation Detection:** Flags vehicles that cross a red light.
*   **Distracted Driving Behavior Detection:** Recognizes activities like mobile phone usage and eating or drinking while driving.

## Technologies Used

*   **YOLO (v5, v8):** Object detection models for accurate and real-time violation detection.
*   **OpenCV:** Image and video processing for pre-processing and visualization.
*   **Python:** Core programming language for model implementation and processing.
*   **OCR technique:** To extract licence plate number

## How It Works

1.  **Video Processing:** The model processes video footage from traffic cameras or dashcams.
2.  **Object Detection:** YOLO detects vehicles, motorcyclists, and drivers.
3.  **Violation Classification:** The system analyzes detected objects to identify specific violations.


## Installation & Usage

### Prerequisites

*   Python 3.x
*   OpenCV
*   PyTorch
*   YOLOv5 or YOLOv8 repository

### Steps to Run

1.  **Clone the repository:**

    ```bash
    git clone [https://github.com/yathish08/yathish08-Intelligent-Traffic-Violation-Detection-System.git](https://github.com/yathish08/yathish08-Intelligent-Traffic-Violation-Detection-System.git)
    cd traffic_violation_detection
    ```

2.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the detection script:**

    ```bash
    python main.py --sample_test_cases/test.mp4 --model yolov8.pt
    ```

## Future Enhancements

*   Enhancing accuracy with improved dataset augmentation and fine-tuning.

## Contributing

Contributions are welcome! Feel free to fork the repository and submit pull requests.

## License

This project is open-source and available under the Apache Lisence.
