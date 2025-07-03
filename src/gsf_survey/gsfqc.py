import os
import sys
from pathlib import Path
from datetime import datetime
import time
from argparse import ArgumentParser
import pandas as pd

# when developing locally use this...
sys.path.append(str(Path(__file__).parent.parent / "src/gsf_survey"))
import gsf
import fileutils

###############################################################################
def main():

    parser = ArgumentParser(description='\n * Process an GSF file or folder of GSF files and maske QC plots.')
    parser.add_argument('-i',         dest='inputfolder',     action='store',         default='.',    help='the root folder to find one more more group folders. Pease refer to procedure for the group folder layout - e.g. c:/mysurveyarea')
    
    args = parser.parse_args()

    if args.inputfolder == '.':
        args.inputfolder = os.getcwd()

    if os.path.isdir(args.inputfolder):
        files = fileutils.findFiles2(True, args.inputfolder, "*.gsf")
    else:
        files = [args.inputfolder]
        args.inputfolder = os.path.dirname(args.inputfolder)

    if len(files) == 0:
        return
    
    ##########################
    #now process the files....
    ##########################

    start_time = time.time() # time  the process
    tasks = []
    print ("Processing %d files in %s" % (len(files), args.inputfolder))
    update_progress("GSF QC", (0))
    for idx, filename in enumerate(files):
        tasks.append([args, filename])

    results = []
    previoustimestamp = 0
    for idx, task in enumerate(tasks):
        results.append(gsfqc(task[0], task[1]))
        update_progress("GSF QC...", (idx/len(files)))
    update_progress("GSF QC complete", (1))

    print ("Duration %.3fs" % (time.time() - start_time)) # print the processing time.

    # load the results into a pandas dataframe, make sure we get 1 row per file
    df = pd.DataFrame(results)

    # convert the start time to a timestamp using the from_timestamp function
    df['starttime'] = df['starttime'].apply(from_timestamp)
    # convert the end time to a timestamp using the from_timestamp function 
    df['endtime'] = df['endtime'].apply(from_timestamp)

    # print the dataframe
    print (df)
    # save the dataframe to a csv file
    csv_file = os.path.join(args.inputfolder, "gsfqc_results.csv")
    df.to_csv(csv_file, index=False)
    print ("Results saved to %s" % csv_file)

###############################################################################
def gsfqc(args, filename):
    '''here is a test script to demonstrate the use of gsf'''
    print (filename)
    # create a GSFREADER class and pass the filename
    r = gsf.GSFREADER(filename)

    result = {}
        # Process the file completely before returning
    # Initialize missing fields with default values to ensure consistent DataFrame structure
    result['filename'] = filename
    result['gsfversion'] = 'Unknown'
    result['starttime'] = 0
    result['endtime'] = 0
    result['minlatitude'] = 0.0
    result['maxlatitude'] = 0.0
    result['minlongitude'] = 0.0
    result['maxlongitude'] = 0.0
    result['mindepth'] = 0.0
    result['maxdepth'] = 0.0
    result['beamcount'] = 0
    result['soundvelocityrecordcount'] = 0
    result['hasbackscatter'] = False

    while r.moreData():
        # read a datagram.  If we support it, return the datagram type and aclass for that datagram
        # The user then needs to call the read() method for the class to undertake a fileread and binary decode.  This keeps the read super quick.
        numberofbytes, recordidentifier, datagram = r.readdatagram()
        # print(recordidentifier)

        if recordidentifier == gsf.HEADER:
            datagram.read()
            result['gsfversion'] = datagram.version
            # print(datagram)
        
        if recordidentifier == gsf.SWATH_BATHY_SUMMARY:
            datagram.read()
            result['starttime'] = datagram.BEGIN_TIME
            result['endtime'] = datagram.END_TIME
            result['minlatitude'] = datagram.MIN_LATITUDE
            result['maxlatitude'] = datagram.MAX_LATITUDE
            result['minlongitude'] = datagram.MIN_LONGITUDE
            result['maxlongitude'] = datagram.MAX_LONGITUDE
            result['mindepth'] = datagram.MIN_DEPTH
            result['maxdepth'] = datagram.MAX_DEPTH

        if recordidentifier ==     gsf.COMMENT:
            datagram.read()
            # print(datagram)

        if recordidentifier ==     gsf.PROCESSING_PARAMETERS:
            datagram.read()
            # print(datagram)

        if recordidentifier ==     gsf.SOUND_VELOCITY_PROFILE:
            datagram.read()
            result['soundvelocityrecordcount'] = datagram.numpoints
            # print(datagram)

        if recordidentifier ==     gsf.ATTITUDE:
            datagram.read()
            # r.attitudedata = np.append(r.attitudedata, datagram.attitudearray, axis=0)
            # print(datagram)

        if recordidentifier == gsf.SWATH_BATHYMETRY:
            r.scalefactorsd =  datagram.read(r.scalefactorsd, False)
            result['hasbackscatter'] = datagram.MEAN_CAL_AMPLITUDE_ARRAY is not None
            result['hasperbeambackscatter'] = datagram.perbeam
            result['beamcount'] = len(datagram.TRAVEL_TIME_ARRAY)
            result['hasheave'] = datagram.heave != 0.00
            result['hasdraft'] = datagram.depthcorrector != 0.00
            result['hastide'] = datagram.tidecorrector != 0.00
            # result['haspitch'] = datagram.pitch != 0.00
            # result['hasroll'] = datagram.roll != 0.00
            # result['hasheading'] = datagram.heading != 0.00
            return result

        
    return result

###############################################################################
# TIME HELPER FUNCTIONS
###############################################################################
def to_timestamp(dateObject):
    return (dateObject - datetime(1970, 1, 1)).total_seconds()

def from_timestamp(unixtime):
    return datetime.utcfromtimestamp(unixtime)

###############################################################################
def update_progress(job_title, progress):
    '''progress value should be a value between 0 and 1'''
    length = 20 # modify this to change the length
    block = int(round(length*progress))
    msg = "\r{0}: [{1}] {2}%".format(job_title, "#"*block + "-"*(length-block), round(progress*100, 2))
    if progress >= 1: msg += " DONE\r\n"
    sys.stdout.write(msg)
    sys.stdout.flush()


#########################################################################################
#########################################################################################
if __name__ == "__main__":
    main()
