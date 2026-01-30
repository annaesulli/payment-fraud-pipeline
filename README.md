# Payment Fraud Data Pipeline
Class project that utilizes Docker, Zookeeper, and Kafka to simulate a payment data stream. Sample payment data is used to train a model using the sklean library, which then interprets the "fraud score" of a payment. Data is collected in a .csv file for further training and analysis.

# Output

<img width="800" height="420" alt="A data stream in PowerShell running split-screen, showing payments being sent from producer to consumer." src="https://github.com/user-attachments/assets/3dc94d1d-d4b5-4836-b0fd-e5c21bab6bc7" />

<img width="800" height="300" alt="csv output of project." src="https://github.com/user-attachments/assets/517ee9c3-985c-47d3-9195-8eaf40bc7e2a" />


A data stream runs split screen in PowerShell, with Kafka sending and receiving payments. Payments received are given a fraud score. This is stored in the csv output. 

# How to Set Up 
  1. Ensure Docker Desktop is installed.
  2. Install the Kafka Python client using pip install kafka-python
  3. Create a folder in the C: drive titled "kafka-docker", with a subfolder titled "solutions". Place files from this repo in respective folders.
  4. Open the "solutions" folder in a code editor and run the "train_fraud_model.py" file to create a "fraud_model.pkl" file. This will be used to evaluate fraud scores.

# How to Run
  Create a desktop shortcut targeting "launch_project1.ps1". Or, simply right-click in the folder and run with PowerShell.
  On the initial run, Kafka must create containers, which may take a while.


