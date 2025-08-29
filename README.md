# IoT Threat Intelligence System
## A threat intelligence system for monitoring and detecting cybersecurity threats in IoT

## Introduction
This project is about building a system that monitors IoT devices for cybersecurity threats. 
It collects data, analyzes it using machine learning, and then detects attacks like Unauthorized Access, DoS, and DDoS. The results are displayed on a real-time dashboard.

## Features
- Data Collection – IoT data is collected through MQTT.

- Data Processing – Data is preprocessed and passed through a trained machine learning model.

- Database & Pipeline – Results are stored in SQLite and also sent through WebSockets in real time.

- Dashboard – A React frontend shows logs, devices, and analytics.


## Technologies Used
- Programming Languages: Python
- Machine Learning Frameworks: Scikit-learn
- Data Analysis: Pandas, NumPy
- Visualization: React
- Networking: MQTT
- Database: SQLite

## Installation
To install and run the project, follow this steps:

1. Clone the repository:
   ```
   git clone https://github.com/footst3p/iot-threat-intelligence-system.git
   cd iot-threat-intelligence-system
   ```

2. Run the project backend:
   ```
   python3 app.py
   ```

3. Run the project frontend
   ```
   cd iot-threat-intelligence-system/frontend
   npm start
   ```

## Usage

  1. Data Collection:

      - Predetermined and Trained Datasets.
      - Tested and trained on 4-8 Lakhs of possibilites/datasets.
      - The application will analyze the data and predict the attack possibilites.

  2. Homepage:
     Access at LocalHost to predict threat detection and attack status.

## Results
- Accuracy: 95.3%
- Precision: 93.2%
- Recall: 96.7%
- F1-score: 94.9

## Project Screenshots

![Login page](/images/login_page.png)<br>

![Overview](/images/Overview.png)<br>

![Logs](/images/Logs.png)


## Credits:

**Huge thanks to [ns7523](https://github.com/ns7523) 🙌 His repo saved me when I was stuck!**
