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
	'''demonstrate how to load attitude'''
	filename = r"C:\sampledata\gsf\J313N000.gsf"
	r = gsf.GSFREADER(filename)
	ts, roll, pitch, heave, heading = r.loadattitude()
	r.close()

	for idx in range(len(ts)):
		print (ts[idx], pitch[idx], roll[idx], heading[idx], heave[idx])
	
#########################################################################################
#########################################################################################
if __name__ == "__main__":
	main()
