#This script takes a list of CTIO images, fixes their headers, uploads them to nova.astrometry.net, and gets the WCS-coordinate attached FITS file back
#You need to be connected to the internet to use this script since it makes use of the nova.astrometry.net API
#Script & CTIO FITS file bug patch by Rohan Naidu (rohan.naidu@u.yale-nus.edu.sg), 15th March 2017

from astropy.io import fits
import glob, os, subprocess

#Specify the paths of your unprocessed CTIO images here. 
#This is currently set up to take in all the files from a particular folder as input.
#can be easily modfied by changing "ctio_raw_images":
ctio_raw_images = glob.glob("../../../Dropbox/LCRO_Images_Sem2_2016-17/Mar_14_SN_NGC5643_CTIO/rccd*.fits")[-1::]
print ctio_raw_images

output_folder = "./trial_run/"  

failed_images = []

for input_file in ctio_raw_images:
	try:
		data, header = fits.getdata(input_file, header=True)
		del header['PIXOFFST']
		del header['PIXXMIT']
	except (KeyboardInterrupt, SystemExit):
		raise
	except:
		print "Failed to delete FITS file header PIXOFFST, PIXXMIT"
		failed_images.append(input_file)

	try:
		fits.writeto('temp_file.fits', data, header, clobber=True)
		subprocess.check_call("python client.py --private --apikey YOURAPIKEY --upload temp_file.fits --newfits %s"%(output_folder + os.path.basename(input_file).replace(".fits",".astrometry.fits"))   )
		#The above command calls the api.
		#Register on the website and go here to generate a key: http://nova.astrometry.net/api_help.
	except (KeyboardInterrupt, SystemExit):
		raise
	except:
		print "Writing temp fits file, or API call failed."
		failed_images.append(input_file)

print "Exiting gracefully."
if len(failed_images)>0:
	print "Failed images:"
	print failed_images