#!/usr/bin/env python
#-----------------------------------------------------------------------------
# ex6_FIFO_Readings.py
#
# Simple example for the qwiic MAX3010x device
# Outputs all Red/IR/Green values at  about 5Hz by polling the FIFO
# Note, the Hz is slowed down by printing to the python terminal,
# It can be drmatically speed up if printing is omitted or intermittent
#
#------------------------------------------------------------------------
#
# Written by Pete Lewis
# SparkFun Electronics, May 2020
#
# Based on code from the SparkFun MAX3010x Sensor Arduino Library
# https://github.com/sparkfun/SparkFun_MAX3010x_Sensor_Library
# By: Nathan Seidle @ SparkFun Electronics, October 2nd, 2016
# 
# This python library supports the SparkFun Electroncis qwiic 
# qwiic sensor/board ecosystem on a Raspberry Pi (and compatable) single
# board computers. 
#
# More information on qwiic is at https://www.sparkfun.com/qwiic
#
# Do you like this library? Help support SparkFun. Buy a board!
#
#==================================================================================
# Copyright (c) 2019 SparkFun Electronics
#
# Permission is hereby granted, free of charge, to any person obtaining a copy 
# of this software and associated documentation files (the "Software"), to deal 
# in the Software without restriction, including without limitation the rights 
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell 
# copies of the Software, and to permit persons to whom the Software is 
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all 
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, 
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE 
# SOFTWARE.
#==================================================================================
# Example 6
#

from __future__ import print_function
import qwiic_max3010x
import time
import sys

def millis():
	return int(round(time.time() * 1000))

def runExample():

	print("\nSparkFun MAX3010x Photodetector - Example 6\n")
	sensor = qwiic_max3010x.QwiicMax3010x()

	if sensor.begin() == False:
		print("The Qwiic MAX3010x device isn't connected to the system. Please check your connection", \
			file=sys.stderr)
		return
	else:
		print("The Qwiic MAX3010x is connected.")

  	# Setup to sense up to 18 inches, max LED brightness
	ledBrightness = 0xFF # Options: 0=Off to 255=50mA
	sampleAverage = 4 # Options: 1, 2, 4, 8, 16, 32
	ledMode = 2 # Options: 1 = Red only, 2 = Red + IR, 3 = Red + IR + Green
	sampleRate = 400 # Options: 50, 100, 200, 400, 800, 1000, 1600, 3200
	pulseWidth = 411 # Options: 69, 118, 215, 411
	adcRange = 2048 # Options: 2048, 4096, 8192, 16384

	if sensor.setup(ledBrightness, sampleAverage, ledMode, sampleRate, pulseWidth, adcRange) == False:
		print("Device setup failure. Please check your connection", \
			file=sys.stderr)
		return
	else:
		print("Setup complete.")       
  
	startTime = millis() # Used to calculate measurement rate
	samplesTaken = 0 # Counter for calculating the Hz or read rate

	while True:

		sensor.check() # Check the sensor, read up to 3 samples

		while (sensor.available() > 0): # do we have new data?

			samplesTaken += 1

			hertz = samplesTaken / ((millis() - startTime) / 1000)
			hertz = round(hertz, 2)

			print(\
			'R[', sensor.getFIFORed() , '] \t'\
			'IR[', sensor.getFIFOIR() , '] \t'\
			'G[', sensor.getFIFOGreen() , '] \t'\
			'Hz[', hertz , ']'\
			)
			
			sensor.nextSample() # We're finished with this sample so move to next sample

if __name__ == '__main__':
	try:
		runExample()
	except (KeyboardInterrupt, SystemExit) as exErr:
		print("\nEnding Example 6")
		sys.exit(0)


