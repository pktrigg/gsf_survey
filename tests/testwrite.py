import os
import sys
import time
from pathlib import Path
from datetime import datetime
from argparse import ArgumentParser

# when developing locally use this...
sys.path.append(str(Path(__file__).parent.parent / "src/gsf_survey"))
import gsf

# # when installed use this...
# from gsf_survey import gsf

###############################################################################
def main():
	'''demonstrate how to write a gsf file'''
	filename = r"C:\sampledata\gsf\testwrite.gsf"
	w = gsf.GSFWRITER(filename)
	#create a datagram of the header
	dg = gsf.CHEADER()
	dg.write("GSF-v03.09")
	w.writeDatagram(dg)

	# create an attitude datagram
	dg = gsf.CATTITUDE()
	timestamp = to_timestamp(datetime.now())
	nanoseconds = 1000
	nummeasurements = 1
	dg.write(timestamp, nanoseconds, nummeasurements)

	# create an SVP datagram


	w.writeDatagram(dg)
	w.close()

	
###############################################################################
def to_timestamp(self, recordDate):
	return (recordDate - datetime(1970, 1, 1)).total_seconds()

#########################################################################################
#########################################################################################
if __name__ == "__main__":
	main()
