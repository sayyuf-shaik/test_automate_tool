# Device Driver Testing Tool
## Getting Started
These instructions will help you to install all the necessary software packages
 and configure project on your local machine for development and testing purposes.

### Prerequisites
##### 1.Hardware and OS requirements
    1.Ubuntu
    2.4 GB Ram or higher
##### 2.Software
    1. Python 3.5 or higher ver must be installed
### Installations
    Installing dependencies packages for Device Driver Testing Tool
    $ cd Device_Driver_Testing_Tool
    $ ./Installer.sh
### Configuring SSH
    update the variables in config.yaml
    $ cd resources/config.yaml
    
    SSH_IP      : "Update RPI3 IP here"
    SSH_UNAME   : "Update RPI3 UserName here"
    SSH_PASSWD  : "Update RPI3 Password here"
 
### Launching GUI
    $ cd gui/
    $ ./ltp_test_automation_gui.py 
    The App will be Launched
### Framework Logs
    Framework Logs will be stored in
    $ cd framework_logs
### LTP Test Logs
    LTP test logs will be stored in 
    $ cd results
