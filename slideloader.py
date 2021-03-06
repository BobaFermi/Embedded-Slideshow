#!/usr/bin/python

import glib, os, glob, shutil, time, subprocess, psutil

from pyudev import Context, Monitor
from pyudev.glib import MonitorObserver

def device_event(observer, device):
    global process, finishedtime #make the process global so we can poll whether it's running or not
    if device.action == 'add' and time.time() > finishedtime + 30: #if a USB device is connected
        print 'event {0} on device {1}'.format(device.action, device) #print that a device has been added, for debug
	fehstatus = False	#Use this flag to tell whether an instance of feh is already running, to prevent more than one instance
        time.sleep(5) #give the computer time to register the new USB device (takes time on Raspberry Pi Zero)
        drive_list = os.listdir(usb_folder) #create list of USB drives
	print(len(drive_list)) #print for debug
        if len(drive_list) > 0: #if there's at least one USB drive mounted here
#            os.system('pkill -9 feh') #kill the feh process (this command still runs even if no feh process is running)
            pi_list = os.listdir(image_folder) #create list of files inside image folder
	    print(pi_list) #print for debug
#            for i, slide_image in enumerate( pi_list ): #for all files in image folder
#                if slide_image.endswith(file_formats): #delete the files that have the accepted image extensions
#                    print('Removing '+slide_image)
#                    os.remove(image_folder + slide_image)
            for i, drive_name in enumerate( drive_list ): #for each drive in the mounted drive folder
                drive_dir = usb_folder + drive_name + '/' #find full directory of each drive
                drive_dir_length = len(drive_dir) #get length of full directory
		for format in file_formats: #for each accepted file format, find the files with that extension on the drive
	            for j, image_path_name in enumerate( glob.glob( usb_folder + drive_name + '/*' + format ) ):
	                file_name = image_path_name[drive_dir_length:] #cut full file address down to file name
	                if file_name.endswith(format): #double check to see if filename still ends in accepted extension
			    if file_name in pi_list:		#*SO* much faster than copying everything across every time
				print('The file ' + file_name + ' already exists in the images folder. Skipping.')
			    else:
		                print('Copying ' + file_name + ' from USB key to ' + image_folder) #print for debug
		                shutil.copyfile(image_path_name, image_folder + file_name) #copy file from USB drive to image folder
	    for process in psutil.process_iter():
		if "feh".lower() in process.name().lower():
		    fehstatus = True
	    if fehstatus == False:
		#we open feh using its full path because cron runs in a different environment so is unlikely to know what just 'feh' means
		#changed to lxsessions autostart file, but kept the full path because why not?
		process = subprocess.Popen('/usr/bin/feh -Y -x -q -D 5 -B black -F -Z -r -R 600 ' + image_folder, shell=True)
	    time.sleep(5)
	    os.system('umount ' + usb_folder + drive_name) #unmount the drive
	    finishedtime = time.time()
	    	    
#	    print 'Starting feh'
	    #feh arguments: -Y, hide cursor; -x, borderless window; -q, quiet mode (don't report errors); 
			   #-D, duration in seconds to display each image; -B background colour; -F fullscreen;
			   #-Z, zoom pictures to fill a dimension of the screen; -z, randomise image order; 
			   #-r, recursive (look in the entire directory tree beyond the selected folder)
			   #-R (int), reload with an interval in seconds, for how often feh should check the folder
#		process = subprocess.Popen('/usr/bin/feh -Y -x -q -D 5 -B black -F -Z -r -R 600 ' + image_folder, shell=True)
           
finishedtime = 0 #For some reason, USB devices trigger twice. I've introduced a timeout so we don't perform the same file operations twice.
file_formats = ('.jpg', '.jpeg', '.png', '.gif', '.tiff', '.bmp') #Most of the file formats accepted by feh
base_folder = '/home/pi/Desktop/' #folder where the images folder will be stored
image_folder = base_folder + 'Images/' #folder that all the images will be copied to, feh will look in here
usb_folder = '/media/pi/' #the folder where usb storage is mounted by default

if os.path.exists(image_folder): #if images folder already exists, we can run feh slideshow for any images that are inside
    process = subprocess.Popen('/usr/bin/feh -Y -x -q -D 5 -B black -F -Z -r -R 600 ' + image_folder, shell=True)
else: #if images folder doesn't exist, create it
    print 'Creating Images folder at ' + image_folder #tell the user what's going on
    os.makedirs(image_folder)

context = Context()
monitor = Monitor.from_netlink(context)

monitor.filter_by(subsystem='usb')
observer = MonitorObserver(monitor)

observer.connect('device-event', device_event)
monitor.start()

print 'Ready for USB device'
glib.MainLoop().run()
