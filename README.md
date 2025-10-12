# IoT Threat Intelligence System
## A threat intelligence system for monitoring and detecting cybersecurity threats in IoT

## Introduction
The IoT Threat Intelligence System is a real-time cybersecurity platform designed to monitor, detect, and classify cyber threats targeting Internet of Things (IoT) environments. The system leverages machine learning and lightweight communication protocols to provide accurate, efficient, and scalable protection for resource-constrained IoT devices.

## Features
- Data Collection – IoT data is collected through MQTT.

- Data Processing – Data is preprocessed and passed through a trained machine learning model.

- Database & Pipeline – Results are stored in SQLite and also sent through WebSockets in real time.

- Dashboard – A React frontend shows logs, devices, and analytics.


## Technologies Used
- Programming Languages: Python
- Machine Learning Frameworks: Scikit-learn
- Data Analysis: Pandas, NumPy
- Visualisation: React
- Networking: MQTT
- Database: SQLite

## System Implementation

  1. Data Collection:
      - Predetermined and Trained Datasets.
  2. Data Preprocessing
     - Refined data to ensure effective ML algorithm usage
  3. Feature Selection
     - Selected needed features from the data
  4. Train Model
     - Trained model using Random Forest 

## Installation and Usage
To install and run the project, follow these steps:

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

4. run data ingestor
   ```
   python3 mqtt_ingestor.py

   ```
5. Homepage:
     Access to LocalHost to predict threat detection and attack status.

## Project Screenshots
![Programs launch](/images/programmes_launch.png)<br>

![Login page](/images/login_page.png)<br>

![Overview](/images/Overview.png)<br>

![Logs](/images/Logs.png)


## Credits:

**Many thanks to ns7523 🙌! His repo saved me when I got stuck.**
