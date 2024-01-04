import os
import sys
from pathlib import Path
from datetime import datetime
import time


# when developing locally use this...
sys.path.append(str(Path(__file__).parent.parent / "src/gsf_survey"))
import gsf

# when installed use this...
# from gsf_survey import gsf

###############################################################################
def main():
	'''here is a test script to demonstrate the use of gsf'''
	filename = r"C:\sampledata\gsf\J313N000.gsf"
	print (filename)
	# create a GSFREADER class and pass the filename
	r = gsf.GSFREADER(filename)

	while r.moreData():
		# read a datagram.  If we support it, return the datagram type and aclass for that datagram
		# The user then needs to call the read() method for the class to undertake a fileread and binary decode.  This keeps the read super quick.

		numberofbytes, recordidentifier, datagram = r.readdatagram()
		# print(recordidentifier)

		if recordidentifier == gsf.HEADER:
			datagram.read()
			# print(datagram)
		
		if recordidentifier == gsf.SWATH_BATHY_SUMMARY:
			datagram.read()
			print(datagram)

		if recordidentifier == 	gsf.COMMENT:
			datagram.read()
			# print(datagram)

		if recordidentifier == 	gsf.PROCESSING_PARAMETERS:
			datagram.read()
			# print(datagram)

		if recordidentifier == 	gsf.SOUND_VELOCITY_PROFILE:
			datagram.read()
			# print(datagram)

		# if recordidentifier == 	gsf.ATTITUDE:
			datagram.read()
			# r.attitudedata = np.append(r.attitudedata, datagram.attitudearray, axis=0)
			# print(datagram)

		if recordidentifier == gsf.SWATH_BATHYMETRY:
			r.scalefactorsd =  datagram.read(r.scalefactorsd, False)
			print ( datagram.from_timestamp(datagram.timestamp), datagram.timestamp, datagram.longitude, datagram.latitude, datagram.heading, datagram.DEPTH_ARRAY[0])

	return

###############################################################################
# TIME HELPER FUNCTIONS
###############################################################################
def to_timestamp(dateObject):
	return (dateObject - datetime(1970, 1, 1)).total_seconds()

def from_timestamp(unixtime):
	return datetime.utcfromtimestamp(unixtime)

#########################################################################################
#########################################################################################
if __name__ == "__main__":
	main()
