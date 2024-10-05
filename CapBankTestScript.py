########################################################
#CapBankTestScript.py
#Created on: Jan 30, 2023
#Author: Swantika Dhundia
########################################################

import pyvisa
import time
import csv
from datetime import datetime
import msvcrt
import sys

#query HV PSU voltage and current measurement and log to csv
def HV_datalog(logFile,time_on_off):

	for i in range(int(time_on_off)):

		try:
			volt = float(hvPSU.query('MEAS:VOLT?', delay = 0.1)) #0.1s delay between query write and read
		except Exception as e:
			print(e)
			print(datetime.now(),'Resend Vout query...')
			try:
				volt = float(hvPSU.query('MEAS?', delay = 0.1)) #0.1s delay between query write and read
			except Exception as e:
				print(e)
				print(datetime.now(),'Still no response from PSU...')
				volt = -1.0

		time.sleep(0.05)

		try:
			curr = float(hvPSU.query('MEAS:CURR?', delay = 0.1)) #0.1s delay between query write and read
		except Exception as e:
			print(e)
			print(datetime.now(),'Resend Iout query...')
			try:
				curr = float(hvPSU.query('MEAS:CURR?', delay = 0.1)) #0.1s delay between query write and read
			except Exception as e:
				print(e)
				print(datetime.now(),'Still no response from PSU...')
				curr = -1.0

		time.sleep(0.05)

		ts = datetime.now()
		ts_trunc = ts.replace(microsecond=0)
		#sno = i+1

		#Print to console
		#print(ts_trunc, volt, curr)

		#write to csv file
		info = {'Timestamp': ts_trunc , 'Voltage': volt, 'Current': curr}
		with open('C:\\Data\\'+logFile, 'a', newline='') as csv_file:
			csv_writer = csv.DictWriter(csv_file, fieldnames1)
			csv_writer.writerow(info)

		#wait 0.7 sec
		time.sleep(0.7)

#query DMM voltage and capacitance measurement and log to csv
def CAP_datalog(logFile):

    try:
        volt = float(dmm.query('MEAS:VOLT?', delay = 0.5)) #0.5s delay between query write and read
    except Exception as e:
        print(e)
        print(datetime.now(),'Resend voltage query...')
        try:
            volt = float(dmm.query('MEAS:VOLT?', delay = 0.5)) #0.5s delay between query write and read
        except Exception as e:
            print(e)
            print(datetime.now(),'Still no response...')
            volt = -1.0

    time.sleep(0.1)

    try:
        cap = float(dmm.query(':MEASure:SCALar:CAPacitance? %s,%s' % ('MAXimum', 'DEFault'), delay = 0.5)) #0.5s delay between query write and read
    except Exception as e:
        print(e)
        print(datetime.now(),'Resend capacitance query...')
        try:
            cap = float(dmm.query(':MEASure:SCALar:CAPacitance? %s,%s' % ('MAXimum', 'DEFault'), delay = 0.5)) #0.5s delay between query write and read
        except Exception as e:
            print(e)
            print(datetime.now(),'Still no response...')
            cap = -1.0

    time.sleep(0.1)

    ts = datetime.now()
    ts_trunc = ts.replace(microsecond=0)
    #sno = i+1

    #Print to console
    #print(ts_trunc, volt, curr)

    #write to csv file
    info = {'Timestamp': ts_trunc , 'Voltage (V)': volt, 'Capacitance (uF)': cap*1000000}
    # print(info)
    with open('C:\\Data\\'+logFile, 'a', newline='') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames2)
        csv_writer.writerow(info)

#check if HV PSU is on or off
def query_HV_PSU():

    try:
        reply = int(hvPSU.query('OUTP?'))
    except Exception as e:
        print(e)
        print(datetime.now(), 'Resend query to HV PSU...')
        try:
            reply = int(hvPSU.query('OUTP?'))
        except Exception as e:
            print(e)
            print(datetime.now(), 'Still no response from HV PSU...')
            reply = -1
    finally:
        if reply == 1:
            print('HV is on...')
        elif reply == 0:
            print('HV is off...')
        else:
            print('HV PSU reply to query is: ' + str(reply))
        
    return reply 

#configure LV PSU two output channels to drive the power routing IGBT switches
def configure_E3646A(switch):

    if switch == '1':
        swControl.write(':INST:SELect OUT1')
        swControl.write(':APPLy 3.3,0.05')
        print('CH1 settings readback: ' + swControl.query(':APPLy?'))
        time.sleep(0.1)

        swControl.write(':INST:SELect OUT2')
        swControl.write(':APPLy 0,0')
        print('CH2 settings readback: ' + swControl.query(':APPLy?'))
        time.sleep(0.1)

        print ('E3646A is configured. Enable output to turn on SW1....\n')

    elif switch == '3':
        swControl.write(':INST:SELect OUT1')
        swControl.write(':APPLy 0,0')
        print('CH1 settings readback: ' + swControl.query(':APPLy?'))
        time.sleep(0.1)

        swControl.write(':INST:SELect OUT2')
        swControl.write(':APPLy 3.3,0.05')
        print('CH2 settings readback: ' + swControl.query(':APPLy?'))
        time.sleep(0.1)

        print ('E3646A is configured. Enable output to turn on SW3....\n')
    
#check if LV PSU is on or off                 
def query_E3646A():

    try:
        reply = int(swControl.query('OUTP?'))
    except Exception as e:
        print(e)
        print(datetime.now(), 'Resend query to 3.3V PSU...')
        try:
            reply = int(swControl.query('OUTP?'))
        except Exception as e:
            print(e)
            print(datetime.now(), 'Still no response from 3.3V PSU...')
            reply = -1
    finally:
        if reply == 1:
            print('3.3V is on...')
        elif reply == 0:
            print('3.3V is off...')
        else:
            print('3.3V PSU reply to query is: ' + str(reply))
        
    return reply           

#check if PWM generator is on or off
def query_33220A():

    try:
        reply = int(loadPWM.query('OUTP?'))
    except Exception as e:
        print(e)
        print(datetime.now(), 'Resend query to 33220A func generator...')
        try:
            reply = int(loadPWM.query('OUTP?'))
        except Exception as e:
            print(e)
            print(datetime.now(), 'Still no response from 33220A...')
            reply = -1
    finally:
        if reply == 1:
            print('SW2 PWM is on...')
        elif reply == 0:
            print('SW2 PWM is off...')
        else:
            print('Func. Gen. reply to query is: ' + str(reply))
        
    return reply 



#Generate csv filename
now = datetime.now()
now_str = now.strftime('%Y-%m-%d_%H-%M-%S')
csv_filename1 = 'SorensonPSU-{}.csv'.format(now_str)
print(csv_filename1)

#Create data log file with headers
fieldnames1 = ['Timestamp','Voltage','Current']
with open('C:\\Data\\' + csv_filename1, 'w', newline='') as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames1)
    csv_writer.writeheader()

print('HV PSU data log file created....\n')

#Generate csv filename
now = datetime.now()
now_str = now.strftime('%Y-%m-%d_%H-%M-%S')
csv_filename2 = 'DMMCapacitance-{}.csv'.format(now_str)
print(csv_filename2)

#Create data log file with headers
fieldnames2 = ['Timestamp','Voltage (V)', 'Capacitance (uF)']
with open('C:\\Data\\' + csv_filename2, 'w', newline='') as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames2)
    csv_writer.writeheader()

print('DMM Capacitance data log file created....\n')

#Get user inputs: V_set, I_set, t_on, t_off
v_set = input('Enter voltage setting in volts: ')
i_set = input('Enter current setting in amps: ')
t_on = input('Enter HV on time in sec: ')
t_off = input('Enter HV off time in sec: ')

#List visa resources
print('\nConnecting to instrument....')
rm = pyvisa.ResourceManager()
print('List of visa resources')
print(rm.list_resources())
hvPSU = rm.open_resource('ASRL4::INSTR') 
swControl = rm.open_resource('GPIB0::9::INSTR')
dmm = rm.open_resource('GPIB0::4::INSTR')
loadPWM = rm.open_resource('GPIB0::10::INSTR')

#configure measurement instrument
#HV PSU
hvPSU.read_termination = '\r'
hvPSU.write_termination = '\r'
hvPSU.timeout = 5000

#3.3V for switches
swControl.read_termination = '\n'
swControl.write_termination = '\n'
swControl.timeout = 5000 

#DMM (for capacitance measurement)
dmm.read_termination = '\n'
dmm.write_termination = '\n'
dmm.timeout = 5000 

#Load switch PWM (for capacitance measurement)
loadPWM.read_termination = '\n'
loadPWM.write_termination = '\n'
loadPWM.timeout = 5000


#check communication with all instruments        
try:
    string = hvPSU.query('*IDN?')
    print(string)
except Exception as e:
    print(e)
    print("Couldn't connect to instrument. Run program again...")
    #exit program
    sys.exit(1)
else:
    print ('HV PSU connection successful....\n')

    #Turn off power supply at start
    hvPSU_status = query_HV_PSU()
    if hvPSU_status == '1':
        hvPSU.write('OUTP OFF')
        time.sleep(0.05)
        print('Instrument output was on. Now turned: ' + query_HV_PSU())
    elif hvPSU_status == '0':
        print('HV PSU is off.')

    #Write settings input by user
    print('Writing voltage and current settings to the instrument...')
    hvPSU.write('VSET ' + v_set)
    hvPSU.write('ISET ' + i_set)
    time.sleep(0.1)
    print('Voltage setting readback: ' + hvPSU.query('VSET?'))
    print('Current setting readback: ' + hvPSU.query('ISET?'))
    print('HV PSU is ready...\n')

#3.3V check IDN and set voltage and current limit                   
try:
    string = swControl.query('*IDN?')
    print(string)
except Exception as e:
    print(e)
    print("Couldn't connect to instrument. Run program again...")
    sys.exit(1)
else:
    print ('E3646A connection successful....\n')

    #Turn off 3.3V to SW1 and SW3 at start
    swControlPSU_status = query_E3646A()
    if swControlPSU_status == '1':
        swControl.write('OUTP OFF')
        time.sleep(0.05)
        print('Instrument output was on. Now turned: ' + query_E3646A())
    elif swControlPSU_status == '0':
        print('3.3V PSU is off.')
    

try:
    string = dmm.query('*IDN?')
    print(string)
except Exception as e:
    print(e)
    print("Couldn't connect to instrument. Run program again...")
    sys.exit(1)
else:
    print ('34410A DMM connection successful....\n')


try:
    string = loadPWM.query('*IDN?')
    print(string)
except Exception as e:
    print(e)
    print("Couldn't connect to instrument. Run program again...")
    sys.exit(1)
else:
    print ('33220A PWM connection successful....\n')

    #Turn off SW2 PWM at start
    loadPWM_status = query_33220A()
    if loadPWM_status == '1':
        loadPWM.write('OUTP OFF')
        time.sleep(0.05)
        print('Instrument output was on. Now turned: ' + query_33220A())
    elif loadPWM_status == '0':
        print('SW2 PWM is off.')

print('\nInstrument checks and setup complete.') 
print('\nTest sequence started. Press ctrl+C to stop....')

try:

    while True:

        #Configure 3.3V PSU to turn on SW1
        configure_E3646A('1')

        time.sleep(1)

        #Turn on SW1
        swControl.write('OUTP ON')
        time.sleep(0.1)
        sw1Status = query_E3646A()
        if sw1Status != 1:
            raise Exception('SW1 did not turn on')

        time.sleep(1)

        #Turn on HV
        hvPSU.write('OUTP ON')
        time.sleep(0.1)
        hvStatus = query_HV_PSU()
        if hvStatus != 1:
            raise Exception('HV did not turn on')

        time.sleep(5)

        #Turn on SW2
        loadPWM.write('OUTP ON')
        time.sleep(0.1)
        sw2Status = query_33220A()
        if sw2Status != 1:
            raise Exception('SW2 (dynamic load) did not turn on')

        print('Cap board powered on with dynamic loading...\n')

        #log data
        HV_datalog(csv_filename1, t_on)

        #Turn off HV
        hvPSU.write('OUTP OFF')
        time.sleep(0.1)
        hvStatus = query_HV_PSU()
        if hvStatus != 0:
            raise Exception('HV did not turn off')

        time.sleep(5)

        #Turn off SW2
        loadPWM.write('OUTP OFF')
        time.sleep(0.1)
        sw2Status = query_33220A()
        if sw2Status != 0:
            raise Exception('SW2 (dynamic load) did not turn off')

        #log data
        HV_datalog(csv_filename1, t_off)

        #Turn off SW1
        swControl.write('OUTP OFF')
        time.sleep(0.1)
        sw1Status = query_E3646A()
        if sw1Status != 0:
            raise Exception('SW1 did not turn off')

        print('Cap board powered off and disconnected from HV as well as dynamic load...\n')

        #Configure 3.3V PSU to turn on SW1
        configure_E3646A('3')

        time.sleep(1)

        #Turn on SW3 
        swControl.write('OUTP ON')
        time.sleep(0.1)
        sw3Status = query_E3646A()
        if sw3Status != 1:
            raise Exception('SW3 did not turn on')

        print('Connected DMM for capacitance measurement..\n')

        time.sleep(5)

        #Capacitance measurement and datalog
        CAP_datalog(csv_filename2)

        time.sleep(1)

        print('Capacitance measurement done\n')

        #Turn off SW3 
        swControl.write('OUTP OFF')
        time.sleep(0.1)
        sw3Status = query_E3646A()
        if sw3Status != 0:
            raise Exception('SW3 did not turn off')

        print('Disconnected DMM\n')

        time.sleep(1)

except (KeyboardInterrupt, Exception) as e:
    print(e)
    loadPWM.write('OUTP OFF')
    hvPSU.write('OUTP OFF')
    swControl.write('OUTP OFF')
    loadPWM.close()
    hvPSU.close()
    swControl.close()
    dmm.close()
    rm.close()
    print('Program complete....')
    k = input('Press any key to close the console window...')