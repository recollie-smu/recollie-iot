#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import serial
import csv
import os
import subprocess
import json
import re
import sys
import logging
import argparse
import getpass
import random
import urllib
import pprint
import sched
import time
import datetime
import threading
import dweepy
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("memorease-9a0bf-firebase-adminsdk-czypx-5d75f1b2e8.json")
firebase_admin.initialize_app(cred)
db = firestore.client()
# Configure logging
# logging.basicConfig(format=settings.LOGGING["format"], datefmt=settings.LOGGING["datefmt"], level=settings.LOGGING["level"])
logging.basicConfig(
    format = "%(asctime)s %(levelname)s %(filename)s:%(funcName)s():%(lineno)i: %(message)s",
    datefmt = "%Y-%m-%d %H:%M:%S",
    level = logging.DEBUG)

logger = logging.getLogger(__name__)


# Handles the case when the serial port can't be found
def handle_missing_serial_port() -> None:
    print("Couldn't connect to the micro:bit. Try these steps:")
    print("1. Unplug your micro:bit")
    print("2. Close Tera Term, PuTTY, and all other apps using the micro:bit")
    print("3. Close all MakeCode browser tabs using the micro:bit")
    print("4. Plug the micro:bit in")
    print("5. Run this app again")
    exit()


# Initializes the serial device. Tries to get the serial port that the micro:bit is connected to
def get_serial_dev_name() -> str:
    logger.info(f"sys.platform: {sys.platform}")
    logger.info(f"os.uname().release: {os.uname().release}")
    logger.info("")

    serial_dev_name = None
    if "microsoft" in os.uname().release.lower(): # Windows Subsystem for Linux

        # List the serial devices available
        try:
            stdout = subprocess.check_output("/mnt/c/Program Files/PowerShell/7/pwsh.exe -Command '[System.IO.Ports.SerialPort]::getportnames()'", shell = True).decode("utf-8").strip()
            if not stdout:
                handle_missing_serial_port()
        except subprocess.CalledProcessError:
            logger.error(f"Couldn't list serial ports: {e.output.decode('utf8').strip()}")
            handle_missing_serial_port()


        # Guess the serial device
        stdout = stdout.splitlines()[-1]
        serial_dev_name = re.search("COM([0-9]*)", stdout)
        if serial_dev_name:
            serial_dev_name = f"/dev/ttyS{serial_dev_name.group(1)}"

    elif "linux" in sys.platform.lower(): # Linux

        # List the serial devices available
        try:
            stdout = subprocess.check_output("ls /dev/ttyACM*", stderr=subprocess.STDOUT, shell = True).decode("utf-8").strip()
            if not stdout:
                handle_missing_serial_port()
        except subprocess.CalledProcessError as e:
            logger.error(f"Couldn't list serial ports: {e.output.decode('utf8').strip()}")
            handle_missing_serial_port()

        # Guess the serial device
        serial_dev_name = re.search("(/dev/ttyACM[0-9]*)", stdout)
        if serial_dev_name:
            serial_dev_name = serial_dev_name.group(1)

    elif sys.platform == "darwin": # macOS

        # List the serial devices available
        try:
            stdout = subprocess.check_output("ls /dev/cu.usbmodem*", stderr=subprocess.STDOUT, shell = True).decode("utf-8").strip()
            if not stdout:
                handle_missing_serial_port()
        except subprocess.CalledProcessError:
            logger.error(f"Error listing serial ports: {e.output.decode('utf8').strip()}")
            handle_missing_serial_port()

        # Guess the serial device
        serial_dev_name = re.search("(/dev/cu.usbmodem[0-9]*)", stdout)
        if serial_dev_name:
            serial_dev_name = serial_dev_name.group(1)

    else:
        logger.error(f"Unknown sys.platform: {sys.platform}")
        exit()

    logger.info(f"serial_dev_name: {serial_dev_name}")
    logger.info("Serial ports available:")
    logger.info("")
    logger.info(stdout)

    if not serial_dev_name:
        handle_missing_serial_port()

    return serial_dev_name


# Handles incoming serial data
def handle_serial_data(s: serial.Serial) -> None:
    print(f"{s.readline().decode('utf-8').strip()}")


def main(location) -> None:
    global mqttc

    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--device", type=str, help="serial device to use, e.g. /dev/ttyS1")

    args = parser.parse_args()
    args_device = args.device

    if args.device:
        serial_dev_name = args.device
    else:
       # Device was not specified as an argument, try to get the serial device name
        serial_dev_name = get_serial_dev_name()

    with serial.Serial(port=serial_dev_name, baudrate=115200, timeout=10) as s:
        # Sleep a while to make sure serial port is open before doing anything else
        time.sleep(1)

        # Reset the input and output buffers in case there is leftover data
        s.reset_input_buffer()
        s.reset_output_buffer()

        location_dict = { "Bathroom": bathroom, "Kitchen": kitchen, "Bedroom": bedroom, "Living Room": living_room }
        # Make the icon blink once a second for a few seconds
        #for i in range(0, 3):
        while(True):
          print("Reminder Location: " + location)
          location_dict[location](s)
          latest_dweet = dweepy.get_latest_dweet_for('memorease')[0]["content"]
          time.sleep(1.5)
          if 'stop' in latest_dweet or s.in_waiting > 0:
              print("Stopping reminder alarm...")
              data = {
                u'audioUrl': u'',
                u'body': u'',
                u'imageUrl': u'',
                u'location': u''
            }
              db.collection(u'message').document(u'displayed').set(data)
              break

        cycle_from_dweet()

        # Forever friends loopy loop
      #  while True:

            # Read from the serial port
           # if s.in_waiting > 0:
              #  handle_serial_data(s)

def bedroom(s):
    logger.info("Writing to serial port: i, 3")
    s.write(f"i,3\r".encode())

def living_room(s):
    logger.info("Writing to serial port: i, 2")
    s.write(f"i,2\r".encode())

def kitchen(s):
    logger.info("Writing to serial port: i, 1")
    s.write(f"i,1\r".encode())

def bathroom(s):
    logger.info("Writing to serial port: i, 0")
    s.write(f"i,0\r".encode())

def cycle_from_dweet():
    try:
        print("Listening to updates from dweet thing 'memorease'...")
        for dweet in dweepy.listen_for_dweets_from('memorease'):
            print(dweet)
            content = dweet['content']
            if "location" in content:
                location = dweet["content"]["location"]
                main(location)
    except requests.exceptions.ConnectionError as e:
        print(e.response)
        print("Connection closed by dweet, restarting now..")
        cycle_from_dweet()

if __name__ == "__main__":
    cycle_from_dweet()
    #main()