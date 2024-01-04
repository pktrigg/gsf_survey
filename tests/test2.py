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
	'''demonstrate how to load navigation'''
	filename = r"C:\sampledata\gsf\J313N000.gsf"
	r = gsf.GSFREADER(filename)
	navigation = r.loadnavigation()
	r.close()

	print (navigation)

#########################################################################################
#########################################################################################
if __name__ == "__main__":
	main()
