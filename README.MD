gsf_survey
=====
* created:       December 2023
* by:            paul.kennedy@guardiangeomatics.com
* description:   python module to read an SDB file
* developed for Python version 3++
* based on GSF V3.09

Notes
====
The Generic Sensor Format (GSF) which is used to store multibeam sonar data

GSF is designed to efficiently store and exchange information produced by geophysical measurement systems before it has been processed into either vector or raster form. 
A sensor data set contains all the information needed to compute the depth or other values at a specific geographic position, but that calculation has not yet been made. 
This structure is particularly useful for data sets created by systems such as multibeam echosounders that collect a large quantity of data from a single location and initially express geographic positions in relative terms. 
GSF not only saves storage space and reduces data transfer volumes, it also provides the receiver with critical information that may be lost when processing the oversampled data to either raster or vector form.

GSF is Portable, Extensible, Efficient, consistent and has gained much acceptance.

Motivation
===
GSF has become a common intercahnce standard.  while the default implementaiton is in native c language and is extremely fast at readong, the language is a barrier for modern cloud based computing frameworks.  Python is a lot slower but is more flexible and provides easy access to GSF data, thereby promoting the use of GSF.  With Python it is easy to take advantage of multi-core CPU's and cloud infrastructure.Therefore we have made a pure python decode for the gsf file format.  The belief is that GSF combined with python can be used to create an opensource processing engine for multibeam bathymetry and backscatter which can be run on the cloud to provide an open and transparent means for MBES processing.

The file format comprises the following sections:

File Header
====
A header of the first timestamp
A slot for the WGS84 specification.  the samples tested are all wmpty, so no WKT / EPSG available
A slot for the UTM specification.  the samples tested are all wmpty, so no WKT / EPSG available
A table of sensors with name, interfacing details and installation offsets and disabled/enabled status

Datagrams
====
A series of datagrams each comprising a header, followed by data

File Footer
====
there us no file footer

Done
====
* Initial implementation was in 2017/2018
* since that time we have used the package internally, so many bug fixes are in place already
* make gsf_survey a pip installable package

2Do
===

Example to load navigation
```
	'''demonstrate how to load navigation'''
	filename = r"C:\sampledata\gsf\J313N000.gsf"
	r = gsf.GSFREADER(filename)
	navigation = r.loadnavigation()
	r.close()
	print (navigation)
```
Example to load attitude records into time series numpy arrays
```
	'''demonstrate how to load attitude'''
	filename = r"C:\sampledata\gsf\J313N000.gsf"
	r = gsf.GSFREADER(filename)
	ts, roll, pitch, heave, heading = r.loadattitude()
	r.close()
	for idx in range(len(ts)):
		print (ts[idx], pitch[idx], roll[idx], heading[idx], heave[idx])
```

Example to iterate through all records
```
	import gsf

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
```

Package Creation Notes
===

* we use twine to create and upload...
```
pip install twine
``````

* to create package...
```
python -m build
``````

* to upload package...
```
python -m twine upload --repository testpypi dist/* --verbose
``````

* to install the package
```
pip install -i https://test.pypi.org/simple/ gsf-survey
``````

* to uninstall the package
```
pip uninstall -y gsf-survey
``````