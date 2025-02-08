# ----------------------------------------------------------------------------------------------------------------------------------
# -- tkinter
from tkinter import *
# -- PIL 
from PIL import ImageTk, Image
# -- Serial
import serial
# -- To Detect Availabe ComPort
import serial.tools.list_ports
# -- Time
import time
# -- Continuous Thread
import continuous_threading
import csv
import os
# ----------------------------------------------------------------------------------------------------------------------------------
#                                                  Main Window
# ----------------------------------------------------------------------------------------------------------------------------------

# -- Creating main window widget
mainWindow = Tk()
# -- Configuring window
mainWindow.title("IITK RaSET TELEMETRY GUI")
# -- Main Window Dimensions
mainWindow.geometry("1155x555") 
# -- main Window Icon

# ----------------------------------------------------------------------------------------------------------------------------------
#                                       Serial Communication Initialization
# ----------------------------------------------------------------------------------------------------------------------------------

# -- [Step 1] -> Detect availabe ComPort and Initialize Serial Communication
ports = serial.tools.list_ports.comports()
for port, desc, hwid in sorted(ports):
        ComPortAvailable = port
#       print for debugging        
        #print(ComPortAvailable)

# -- [Step 2] -> Initialize Serial Communication
dataFromSerial = serial.Serial(ComPortAvailable,9600, timeout = 1)

# To hold raw telemetry data [directly from serial]
global rawData

# Define CSV file name
csv_filename = "telemetry_data.csv"

# Define header for CSV file
csv_header = [
    "Team ID","Time Stamp (s)","Packet Count","Altitude (m)","Pressure (Pa)",
    "Temperature (°C)","Voltage (V)","GNSS Time (s)","GNSS Latitude (°)","GNSS Longitude (°)","GNSS Altitude (m)","GNSS Satellite"
    ,"Acceleration X (m/s2)","Acceleration Y (m/s2)","Acceleration Z (m/s2)","Roll (°)","Pitch (°)","Yaw (°)","Gyro Spin Rate","Flight Software State"
    ]

if not os.path.exists(csv_filename):
    with open(csv_filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(csv_header)

# Function to append telemetry data to CSV
def save_to_csv(data):
    """ Append telemetry data to CSV file. """
    if len(data) > 1 and data[0] == "<" and data[-1] == ">":
        with open(csv_filename, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(data[1:-1])  # Remove "<" and ">" from data

# Check if the file exists, if not, create it with headers
if not os.path.exists(csv_filename):
    with open(csv_filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(csv_header)

# Function to append telemetry data to CSV
def save_to_csv(data):
    """ Append telemetry data to CSV file. """
    if len(data) > 1 and data[0] == "<" and data[-1] == ">":
        with open(csv_filename, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(data[1:-1])  # Remove "<" and ">" from data

# ----------------------------------------------------------------------------------------------------------------------------------
#                                               Frame and Labels
# ----------------------------------------------------------------------------------------------------------------------------------

# -- First layer of main Window [Label Frames: Controls, Logo, Exit]
frame_First_Layer = Frame(mainWindow, width = 1400, height = 350, relief = "raised")
frame_First_Layer.grid(row = 0, column = 0, columnspan=3)
# -- [Label Frame: Controls]
frame_Controls = LabelFrame(frame_First_Layer, text = "Controls",borderwidth = 2,relief = "raised",padx = 5,pady = 5)
frame_Controls.grid(row = 0, column = 0, padx = 25, pady = 25)
# -- [Label Frame: Logo]
# -- Image
imgLogo = ImageTk.PhotoImage(Image.open("Rass.png"))
labelLogoImg = Label(image = imgLogo)
# -- Frame
LebelLogo = Label(frame_First_Layer, text = "l",borderwidth = 2,relief = "flat", height = 130, width = 850,image = imgLogo)
LebelLogo.grid(row = 0, column = 1, padx = 1, pady = 40) 
# -- [Label Frame: Exit]
frameExit = LabelFrame(frame_First_Layer, text = "Exit",borderwidth = 2,relief = "raised",padx = 5,pady = 5)
frameExit.grid(row = 0, column = 2, padx = 25, pady = 25) 

# -- [Label: Port Availabe Display]
label_port = Label(frame_Controls, text = "Port :", width = 4, height = 1)
label_port.grid(row = 1, column = 0)
# -- Display Connected ComPort
label_port = Label(frame_Controls, text = ComPortAvailable, width = 6, height = 1)
label_port.grid(row = 1, column = 1)

# -- Second layer of main Window [Label Frames: Telemetry Data]
frame_Second_Layer = Frame(mainWindow, width = 1150, height = 250)
frame_Second_Layer.grid(row = 1, column = 0, columnspan=3)
# -- Telemetry Data Name Fields
# -- TEAM ID
labelName_TeamID = Label(frame_Second_Layer, text = "Team ID :", width = 14, height = 1, anchor="w")
labelName_TeamID.grid(row = 0, column = 0)
# -- Time Stamping
labelName_Stamp = Label(frame_Second_Layer, text = "Time stamp (s) :", width = 14, height = 1, anchor="w")
labelName_Stamp.grid(row = 0, column = 2)
# -- Packet Count
labelName_Packet = Label(frame_Second_Layer, text = "Packet Count:", width = 14, height = 1, anchor="w")
labelName_Packet.grid(row = 1, column = 0)
# -- GNSS ALTITUDE
labelName_Altitude = Label(frame_Second_Layer, text = "Altitude (m) :", width = 14, height = 1, anchor="w")
labelName_Altitude.grid(row = 2, column = 0)
# -- PRESSURE
labelName_Pressure = Label(frame_Second_Layer, text = "Pressure (Pa) :", width = 14, height = 1, anchor="w")
labelName_Pressure.grid(row = 3, column = 0)
# -- TEMPERATURE
labelName_Temperature = Label(frame_Second_Layer, text = "Temperature (°C) :", width = 14, height = 1, anchor="w")
labelName_Temperature.grid(row = 4, column = 0)
# -- VOLTAGE
labelName_Volt = Label(frame_Second_Layer, text = "Voltage (V) :", width = 14, height = 1, anchor="w")
labelName_Volt.grid(row = 1, column = 2, padx = 8)
# -- GNSS TIME
labelName_GNSStime = Label(frame_Second_Layer, text = "GNSS Time (s) :", width = 14, height = 1, anchor="w")
labelName_GNSStime.grid(row = 2, column = 2, padx=8)
# -- GNSS LATITUDE
labelName_GNSSLatitude = Label(frame_Second_Layer, text = "GNSS Latitude (°) :", width = 14, height = 1, anchor="w")
labelName_GNSSLatitude.grid(row = 3, column = 2,padx=8)
# -- GNSS LONGITUDE
labelName_GNSSLongitude = Label(frame_Second_Layer, text = "GNSS Longitude (°) :", width = 14, height = 1, anchor="w")
labelName_GNSSLongitude.grid(row = 4, column = 2,padx=8)
# -- GPS ALTITUDE
labelName_GNSSAltitude = Label(frame_Second_Layer, text = "GNSS Altitude (m) :", width = 14, height = 1, anchor="w")
labelName_GNSSAltitude.grid(row = 0, column = 4 , padx=8)
# -- GNSS SATELLITE
labelName_GNSSSats = Label(frame_Second_Layer, text = "GNSS Satellite :", width = 14, height = 1, anchor="w")
labelName_GNSSSats.grid(row = 1, column = 4, padx = 8)
# ACCELEROMETER DATA
   # -- Acceleration X
labelName_AcceX = Label(frame_Second_Layer, text = "Acceleration X (m/s2) :", width = 14, height = 1, anchor="w")
labelName_AcceX.grid(row = 2, column = 4, padx = 8)
   # -- Acceleration Y
labelName_AcceY = Label(frame_Second_Layer, text = "Acceleration Y (m/s2) :", width = 14, height = 1, anchor="w")
labelName_AcceY.grid(row = 3, column = 4, padx = 8)
   # -- Acceleration Z
labelName_AcceZ = Label(frame_Second_Layer, text = "Acceleration Z (m/s2) :", width = 14, height = 1, anchor="w")
labelName_AcceZ.grid(row = 4, column = 4, padx = 8)
   # -- ROLL
labelName_Roll = Label(frame_Second_Layer, text = "Roll (°) :", width = 8, height = 1, anchor="w")
labelName_Roll.grid(row = 1, column = 6, padx = 8)
   # -- PITCH
labelName_Pitch = Label(frame_Second_Layer, text = "Pitch (°) :", width = 8, height = 1, anchor="w")
labelName_Pitch.grid(row = 2, column = 6, padx = 8)
   # -- YAW
labelName_Yaw = Label(frame_Second_Layer, text = "Yaw (°) :", width = 8, height = 1, anchor="w")
labelName_Yaw.grid(row = 3, column = 6, padx = 8)
# -- GYRO SPIN RATE
labelName_GyroSpin = Label(frame_Second_Layer, text = "Gyro Spin Rate (°/s) :", width = 15, height = 1, anchor="w")
labelName_GyroSpin.grid(row = 1, column = 8, padx = 8)
# -- FLIGHT SOFTWARE STATE
labelName_SoftState = Label(frame_Second_Layer, text = "Flight Software State :", width = 18, height = 1, anchor="w")
labelName_SoftState.grid(row = 2, column = 8, padx = 8)

# -- Third layer of main Window [Frame: Indicators, Raw Data, others ]
frame_Third_Layer = Frame(mainWindow, width = 1150, height = 250)
frame_Third_Layer.grid(row = 2, column = 0, columnspan=3)

# -- [Label Frame: Raw Telemetry Data]
Labelframe_RawData = LabelFrame(frame_Third_Layer, text = "Raw Telemetry Data", width = 250, height = 5)
Labelframe_RawData.grid(row = 0, column = 0, padx = 25, pady = 20)

# -- Raw Data
labelName_RawData = Label(Labelframe_RawData, text = "<,data,>", width = 80, height = 2, anchor="center")
labelName_RawData.grid(row = 0, column = 0)   

# ----------------------------------------------------------------------------------------------------------------------------------
#                                                       Functions
# ----------------------------------------------------------------------------------------------------------------------------------

# Start reading and displaying Telemetry Data
def startTelemetry():    
#   Update Start/Stop indicator Color [START = GREEN lightish Shade #00E600]
    button_StartStopIndicator = Button(frame_Controls, width = 2, height = 1, bg = "#00E600")
    button_StartStopIndicator.grid(row = 0, column = 2)
#   Telemetry variables           
    global receivedTelemetry
    receivedTelemetry = dataFromSerial.readline().decode('windows-1252')
#   Removing \r\n from the end of the received data     
    receivedTelemetry = receivedTelemetry.rstrip("\r\n")
    global rawData
    rawData = receivedTelemetry
#   Print Raw Telemetry for debugging    
    #print(receivedTelemetry)
    global splitData
    splitData = receivedTelemetry.split(",")
    print(len(splitData))
#   Print Split data for debugging
   #print(splitData)
    if (len(splitData) > 1):
        if (splitData[0] == "<") and (splitData[21] == ">"):
#       Displaying Received Data 
            # -- Team ID
            labelVal_TeamID = Label(frame_Second_Layer, text = splitData[1], width = 14, height = 1, anchor="w", relief = "sunken")
            labelVal_TeamID.grid(row = 0, column = 1)    
            # -- Time Stamping
            labelVal_Stamp = Label(frame_Second_Layer, text = splitData[2], width = 14, height = 1, anchor="w" ,relief = "sunken")
            labelVal_Stamp.grid(row = 0, column = 3)
            # -- Packet Count
            labelVal_Packet = Label(frame_Second_Layer, text = splitData[3], width = 14, height = 1, anchor="w", relief = "sunken")
            labelVal_Packet.grid(row = 1, column = 1)
            # -- ALTITUDE
            labelVal_Altitude = Label(frame_Second_Layer, text = splitData[4], width = 14, height = 1, anchor="w", relief = "sunken")
            labelVal_Altitude.grid(row = 2, column = 1)
            # -- PRESSURE
            labelVal_Pressure = Label(frame_Second_Layer, text = splitData[5], width = 14, height = 1, anchor="w", relief = "sunken")
            labelVal_Pressure.grid(row = 3, column = 1)
            # -- TEMPERATURE
            labelVal_Temperature = Label(frame_Second_Layer, text = splitData[6], width = 14, height = 1, anchor="w" , relief = "sunken")
            labelVal_Temperature.grid(row = 4, column = 1)
            # -- VOLTAGE
            labelVal_Volt = Label(frame_Second_Layer, text = splitData[7], width = 14, height = 1, anchor="w", relief = "sunken")
            labelVal_Volt.grid(row = 1, column = 3)
            # -- GNSS TIME
            labelVal_GNSStime = Label(frame_Second_Layer, text = splitData[8],  width = 14, height = 1, anchor="w",relief = "sunken")
            labelVal_GNSStime.grid(row = 2, column = 3)
            # -- GNSS LATITUDE
            labelVal_GNSSLatitude = Label(frame_Second_Layer, text = splitData[9], width = 14, height = 1, anchor="w",relief = "sunken")
            labelVal_GNSSLatitude.grid(row = 3, column = 3)
            # -- GNSS LONGITUDE
            labelVal_GNSSLongitude = Label(frame_Second_Layer, text = splitData[10], width = 14, height = 1, anchor="w",relief = "sunken")
            labelVal_GNSSLongitude.grid(row = 4, column = 3)
            # -- GPS ALTITUDE
            labelVal_GNSSAltitude = Label(frame_Second_Layer, text = splitData[11], width = 14, height = 1, anchor="w",relief = "sunken")
            labelVal_GNSSAltitude.grid(row = 0, column = 5)
            # -- GNSS SATELLITE
            labelVal_GNSSSats = Label(frame_Second_Layer, text = splitData[12], width = 14, height = 1, anchor="w",relief = "sunken")
            labelVal_GNSSSats.grid(row = 1, column = 5)
            # ACCELEROMETER DATA
            # -- Acceleration X
            labelVal_AcceX = Label(frame_Second_Layer, text = splitData[13], width = 14, height = 1, anchor="w",relief = "sunken")
            labelVal_AcceX.grid(row = 2, column = 5)
            # -- Acceleration Y
            labelVal_AcceY = Label(frame_Second_Layer, text = splitData[14], width = 14, height = 1, anchor="w",relief = "sunken")
            labelVal_AcceY.grid(row = 3, column = 5)
            # -- Acceleration Z
            labelVal_AcceZ = Label(frame_Second_Layer, text = splitData[15], width = 14, height = 1, anchor="w",relief = "sunken")
            labelVal_AcceZ.grid(row = 4, column =5)
            # -- ROLL
            labelVal_Roll = Label(frame_Second_Layer, text = splitData[16], width = 8, height = 1, anchor="w",relief = "sunken")
            labelVal_Roll.grid(row = 1, column = 7)
            # -- PITCH
            labelVal_Pitch = Label(frame_Second_Layer, text = splitData[17], width = 8, height = 1, anchor="w",relief = "sunken")
            labelVal_Pitch.grid(row = 2, column = 7)
            # -- YAW
            labelVal_Yaw = Label(frame_Second_Layer, text = splitData[18], width = 8, height = 1, anchor="w",relief = "sunken")
            labelVal_Yaw.grid(row = 3, column = 7)
            # -- GYRO SPIN RATE
            labelVal_GyroSpin = Label(frame_Second_Layer, text = splitData[19], width = 8, height = 1, anchor="w",relief = "sunken")
            labelVal_GyroSpin.grid(row = 1, column = 9)
            # -- FLIGHT SOFTWARE STATE
            labelVal_SoftState = Label(frame_Second_Layer, text = splitData[20], width = 14, height = 1, anchor="w",relief = "sunken")
            labelVal_SoftState.grid(row = 2, column = 9)

            #Raw Data
            labelName_RawData = Label(Labelframe_RawData, text = rawData, width = 110, height = 2, anchor="center")
            labelName_RawData.grid(row = 0, column = 0)
            save_to_csv(splitData)
            #Update Readings Every 1 seconds    
            time.sleep(1)                         

    else:
        #print("Data Error")
    #   Raw Data [Error Message]
        labelName_RawData = Label(Labelframe_RawData, text = "Telemetry Error", width = 80, height = 2, anchor="center")
        labelName_RawData.grid(row = 0, column = 0)         

# To pause the continuous thread [thread_ShowData]
def stopTelemetry():
#   pause the Continuous Thread (startTelemetry())    
    thread_ShowData.stop()
#   Update Start/Stop indicator Color [STOP = RED]
    button_StartStopIndicator = Button(frame_Controls, width = 2, height = 1, bg = "red")
    button_StartStopIndicator.grid(row = 0, column = 2)
#   Enable Exit Button
    button_Exit = Button(frameExit, text = "Exit", width = 4, height = 1, command = mainWindow.quit, state = "active")
    button_Exit.grid(row = 0, column = 0)           

# Continuous thread to keep reading and displaying the serial data
thread_ShowData = continuous_threading.PausableThread(startTelemetry)

# To disable the Exit Button when the Start button is pressed
def disableExitButton():
    #   Disable Exit Button (Done when Start button is clicked)    
        button_Exit = Button(frameExit, text = "Exit", width = 4, height = 1, command = mainWindow.quit, state = "disabled")
        button_Exit.grid(row = 0, column = 0)

# To initialize the data fields on the startup
def initTelemetryDisplay():
            # -- Team ID
            labelVal_TeamID = Label(frame_Second_Layer, text = "--", width = 14, height = 1, anchor="w", relief = "sunken")
            labelVal_TeamID.grid(row = 0, column = 1)    
            # -- Time Stamping
            labelVal_Stamp = Label(frame_Second_Layer, text = "--", width = 14, height = 1, anchor="w" ,relief = "sunken")
            labelVal_Stamp.grid(row = 0, column = 3)
            # -- Packet Count
            labelVal_Packet = Label(frame_Second_Layer, text = "--", width = 14, height = 1, anchor="w", relief = "sunken")
            labelVal_Packet.grid(row = 1, column = 1)
            # -- ALTITUDE
            labelVal_Altitude = Label(frame_Second_Layer, text = "--", width = 14, height = 1, anchor="w", relief = "sunken")
            labelVal_Altitude.grid(row = 2, column = 1)
            # -- PRESSURE
            labelVal_Pressure = Label(frame_Second_Layer, text = "--", width = 14, height = 1, anchor="w", relief = "sunken")
            labelVal_Pressure.grid(row = 3, column = 1)
            # -- TEMPERATURE
            labelVal_Temperature = Label(frame_Second_Layer, text ="--", width = 14, height = 1, anchor="w" , relief = "sunken")
            labelVal_Temperature.grid(row = 4, column = 1)
            # -- VOLTAGE
            labelVal_Volt = Label(frame_Second_Layer, text = "--", width = 14, height = 1, anchor="w", relief = "sunken")
            labelVal_Volt.grid(row = 1, column = 3)
            # -- GNSS TIME
            labelVal_GNSStime = Label(frame_Second_Layer, text = "--",  width = 14, height = 1, anchor="w",relief = "sunken")
            labelVal_GNSStime.grid(row = 2, column = 3)
            # -- GNSS LATITUDE
            labelVal_GNSSLatitude = Label(frame_Second_Layer, text = "--", width = 14, height = 1, anchor="w",relief = "sunken")
            labelVal_GNSSLatitude.grid(row = 3, column = 3)
            # -- GNSS LONGITUDE
            labelVal_GNSSLongitude = Label(frame_Second_Layer, text = "--", width = 14, height = 1, anchor="w",relief = "sunken")
            labelVal_GNSSLongitude.grid(row = 4, column = 3)
            # -- GPS ALTITUDE
            labelVal_GNSSAltitude = Label(frame_Second_Layer, text = "--", width = 14, height = 1, anchor="w",relief = "sunken")
            labelVal_GNSSAltitude.grid(row = 0, column = 5)
            # -- GNSS SATELLITE
            labelVal_GNSSSats = Label(frame_Second_Layer, text = "--", width = 14, height = 1, anchor="w",relief = "sunken")
            labelVal_GNSSSats.grid(row = 1, column = 5)
            # ACCELEROMETER DATA
            # -- Acceleration X
            labelVal_AcceX = Label(frame_Second_Layer, text = "--", width = 14, height = 1, anchor="w",relief = "sunken")
            labelVal_AcceX.grid(row = 2, column = 5)
            # -- Acceleration Y
            labelVal_AcceY = Label(frame_Second_Layer, text = "--", width = 14, height = 1, anchor="w",relief = "sunken")
            labelVal_AcceY.grid(row = 3, column = 5)
            # -- Acceleration Z
            labelVal_AcceZ = Label(frame_Second_Layer, text = "--", width = 14, height = 1, anchor="w",relief = "sunken")
            labelVal_AcceZ.grid(row = 4, column = 5)
            # -- ROLL
            labelVal_Roll = Label(frame_Second_Layer, text = "--", width = 8, height = 1, anchor="w",relief = "sunken")
            labelVal_Roll.grid(row = 1, column = 7)
            # -- PITCH
            labelVal_Pitch = Label(frame_Second_Layer, text = "--", width = 8, height = 1, anchor="w",relief = "sunken")
            labelVal_Pitch.grid(row = 2, column = 7)
            # -- YAW
            labelVal_Yaw = Label(frame_Second_Layer, text = "--", width = 8, height = 1, anchor="w",relief = "sunken")
            labelVal_Yaw.grid(row = 3, column = 7)
            # -- GYRO SPIN RATE
            labelVal_GyroSpin = Label(frame_Second_Layer, text = "--", width = 8, height = 1, anchor="w",relief = "sunken")
            labelVal_GyroSpin.grid(row = 1, column = 9)
            # -- FLIGHT SOFTWARE STATE
            labelVal_SoftState = Label(frame_Second_Layer, text = "--", width = 8, height = 1, anchor="w",relief = "sunken")
            labelVal_SoftState.grid(row = 2, column = 9)
# ----------------------------------------------------------------------------------------------------------------------------------
#                                                       Buttons
# ----------------------------------------------------------------------------------------------------------------------------------

# -- Start Button
button_Start = Button(frame_Controls, text = "Start", width = 4, height = 1, command = lambda: [thread_ShowData.start(), disableExitButton()])
button_Start.grid(row = 0, column = 0)
# -- Stop Button
button_Stop = Button(frame_Controls, text = "Stop", width = 4, height = 1, command = stopTelemetry)
button_Stop.grid(row = 0, column = 1, padx = 5, pady = 5)
# -- Start/Stop Indicator
button_StartStopIndicator = Button(frame_Controls, text = "", width = 2, height = 1)
button_StartStopIndicator.grid(row = 0, column = 2)
# -- Exit Button
button_Exit = Button(frameExit, text = "Exit", width = 4, height = 1, command = mainWindow.quit)
button_Exit.grid(row = 0, column = 0)

# ----------------------------------------------------------------------------------------------------------------------------------
#                                           Initializing Telemetry Data Fields
# ----------------------------------------------------------------------------------------------------------------------------------

initTelemetryDisplay()

# ----------------------------------------------------------------------------------------------------------------------------------
# -- Event Looping
mainWindow.mainloop() 
# ----------------------------------------------------------------------------------------------------------------------------------