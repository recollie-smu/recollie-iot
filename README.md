# Setup for micro:bit
1. Need at least 2 micro:bit
    - One acting as the sender
    - One acting as receiver (any of the four location)
2. Flash sender.py code into the micro:bit that is the sender
3. Flash any of the receiver code (bathroom.py, bedroom.py, kitchen.py, livingroom.py)
   for the receiver micro:bit(s)

# Setup for Raspberry Pi
## Display/Website
1. Follow this [Github](https://github.com/recollie-smu/recollie) README.md and to build the frontend code
   which will be a dist folder
2. Transfer the dist folder into the Raspberry Pi
3. To run the website type ```serve -s dist``` into the terminal, one folder level before where the dist folder is located
## Backend
1. Transfer the code from this [repo](https://github.com/recollie-smu/recollie-backend) into the Raspberry Pi.
     - Follow the README.md to setup the backend
## IoT Side
1. Transfer basestn_app.py into the Raspberry Pi
2. Type and enter ```pip3 install python-socketio``` in the terminal to install this package
3. To run basestn_app.py type ```python3 basestn_app.py``` into the terminal 


