# Series-Cap-Bank-Test-Script

## Overview
This Python script fully automates the endurance testing of a DC link capacitor bank PCB, designed for energy storage and voltage stabilization. It controls multiple instruments: the Sorenson XG600-1.4 to power the PCB, the Keysight 33220A Function Generator to generate IGBT gating signal and manage cap bank dynamic loading, the Keysight 34410A DMM to periodically measure capacitance on the DC link bus, and the E3646A power supply to control two additional switches for power routing. The script automates power cycling, dynamic load control, and periodic capacitance measurement, ensuring efficient and repeatable long-term testing. Diagnostics are logged for continuous monitoring and troubleshooting.

The repository includes the Python script for customization, along with an executable (.exe) available in the "Releases" section for direct use without setup.


## Features
- **Instrument communication check:** Automatically verifies connectivity with all instruments at the start of each test.
- **User-configurable HV PSU settings:** Allows control of input voltage, current, and power cycle timing.
- **Automated capacitance measurement:** Automatically configures the setup by disconnecting power and load, then connecting the DMM to measure capacitance when the PCB is powered off.
- **Data logging:** Logs Sorenson (HV) power supply voltage and current every second during operation. Also, captures PCB capacitance and voltage during power-off to ensure the capacitor bank is fully discharged before measurement. 
- **Retry mechanism:** Retries communication with instruments up to 2 times before aborting the test.
- **Safe shutdown:** Easily stop the test and power off all instruments with CTRL+C.


## Prerequisites 

- ***For running/customizing the Python script (CapBankTestScript.py):***

    - Python 3.10 (or higher)
    - PyVISA (`pip install pyvisa==1.13.0` or `pip install -r requirements.txt`)
    - National Instruments VISA (or another VISA backend)
      You can download the NI-VISA drivers from the [NI website](https://www.ni.com/en-us/support/downloads/drivers/download.ni-visa.html).

- ***For running the Executable (CapBankTestScript.exe):***

    - National Instruments VISA (or another VISA backend)
      You can download the NI-VISA drivers from the [NI website](https://www.ni.com/en-us/support/downloads/drivers/download.ni-visa.html).


## Usage
1. Download and extract `Cap-Bank-Tester-v1.0.0.zip` from the Releases section of this [repository](https://github.com/SwantikaD/Series-Cap-Bank-Test-Script). The extracted folder will contain the executable. 

2. Create `Data` folder in C drive to store the test data logs. 

3. Open command prompt, navigate to the folder containing the executable and run it:
    - cd <path/to/executable>
    - CapBankTestScript.exe

4. Enter the settings for input HV Power Supply when prompted. See example below:
    - Enter voltage setting in volts: 400
    - Enter current setting in amps: 0.8
    - Enter HV on time in sec: 900
    - Enter HV off time in sec: 900

5. The test starts automatically after configuration.

6. Press Ctrl+C to stop the test at any time. 


## Logging
- Sorenson power supply voltage and current are logged every second with timestamps and saved as `SorensonPSU-{}.csv` in the C:/Data folder. The log includes:
    - HV Voltage (HV_V)
    - HV Current (HV_I)

- During the user-configurable PCB power-off period, the capacitor bank voltage and capacitance are logged with timestamps and saved as `DMMCapacitance-{}.csv` in the C:/Data folder. The log includes:
    - Capacitor Bank Off Voltage (UUT_OFF_V)
    - Capacitor Bank Capacitance (UUT_OFF_CAP)

## Troubleshooting
1. Connection Issues
    - Ensure all hardware connections are correct and secure.
    - Verify that the instruments are using the correct serial port and GPIB addresses:
        - HV PSU: ASRL4::INSTR
        - Function Generator: GPIB0::10::INSTR
        - DMM: GPIB0::4::INSTR
        - LV PSU: GPIB0::9::INSTR


2. Communication Errors
    If the instrument connects but fails to communicate (i.e., 2 retry attempts fail):
    - Power cycle the instrument and rerun the script.
    - If the issue persists, use Keysight Command Expert(CE) to reset the instrument:
        - Install Keysight Command Expert.
        - Connect to the instrument and send a reset SCPI command.
        - Watch this [tutorial](https://www.youtube.com/watch?v=nHSU6RjHCqE) to set up an instrument and send SCPI commands in CE.  