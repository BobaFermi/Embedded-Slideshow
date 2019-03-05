import glib, os, glob, shutil, time, subprocess

from pyudev import Context, Monitor
from pyudev.glib import MonitorObserver

def device_event(observer, device):
    global process #make the process global so we can poll whether it's running or not
    if device.action == 'add': #if a USB device is connected
        print 'event {0} on device {1}'.format(device.action, device) #print that a device has been added, for debug
        time.sleep(5) #give the computer time to register the new USB device (takes time on Raspberry Pi Zero)
        drive_list = os.listdir(usb_folder) #create list of USB drives
	print(len(drive_list)) #print for debug
        if len(drive_list) > 0: #if there's at least one USB drive mounted here
            os.system('pkill -9 feh') #kill the feh process (this command still runs even if no feh process is running)
            pi_list = os.listdir(image_folder) #create list of files inside image folder
	    print(pi_list) #print for debug
            for i, slide_image in enumerate( pi_list ): #for all files in image folder
                if slide_image.endswith(file_formats): #delete the files that have the accepted image extensions
                    print('Removing '+slide_image)
                    os.remove(image_folder + slide_image)
            for i, drive_name in enumerate( drive_list ): #for each drive in the mounted drive folder
                drive_dir = usb_folder + drive_name + '/' #find full directory of each drive
                drive_dir_length = len(drive_dir) #get length of full directory
		for format in file_formats: #for each accepted file format, find the files with that extension on the drive
	            for j, image_path_name in enumerate( glob.glob( usb_folder + drive_name + '/*' + format ) ):
	                file_name = image_path_name[drive_dir_length:] #cut full file address down to file name
	                if image_path_name.endswith(format): #double check to see if filename still ends in accepted extension
	                    print('Copying ' + file_name + ' from USB key to' + image_folder) #print for debug
	                    shutil.copyfile(image_path_name, image_folder + file_name) #cope file from USB drive to image folder
		    os.system('umount ' + usb_folder + drive_name) #unmount the drive
	    
	    print 'Starting feh'
            process = subprocess.Popen('feh -Y -x -q -D 5 -B black -F -Z -z -r ' + image_folder, shell=True) #start feh slideshow from new images
            
file_formats = ('.jpg', '.jpeg', '.png', '.gif', '.tiff', '.bmp') #Most of the file formats accepted by feh
base_folder = '/home/craig/Desktop/' #folder where the images folder will be stored
image_folder = base_folder + 'Images/' #folder that all the images will be copied to, feh will look in here
usb_folder = '/media/craig/' #the folder where usb storage is mounted by default

if os.path.exists(image_folder): #if images folder already exists, we can run feh slideshow for any images that are inside
    process = subprocess.Popen('feh -Y -x -q -D 5 -B black -F -Z -z -r ' + image_folder, shell=True)
else: #if images folder doesn't exist, create it
    print 'Creating Images folder at' + image_folder #tell the user what's going on
    os.makedirs(image_folder)

context = Context()
monitor = Monitor.from_netlink(context)

monitor.filter_by(subsystem='usb')
observer = MonitorObserver(monitor)

observer.connect('device-event', device_event)
monitor.start()

print 'Ready for USB device'
glib.MainLoop().run()
