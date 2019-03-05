import glib, os, glob, shutil, time, subprocess

from pyudev import Context, Monitor
from pyudev.glib import MonitorObserver

file_formats = ('.jpg', '.jpeg', '.png', '.gif', '.tiff', '.bmp')
base_folder = '/home/craig/Desktop/'
image_folder = base_folder + 'Images/'
usb_folder = '/media/craig/'
if os.path.exists(image_folder):
    process = subprocess.Popen('feh -Y -x -q -D 5 -B black -F -Z -z -r ' + image_folder, shell=True)
else:
    print 'Creating Images folder at' + image_folder
    os.makedirs(image_folder)

def device_event(observer, device):
    global process
    if device.action == 'add':
        print 'event {0} on device {1}'.format(device.action, device)
        time.sleep(5)
        drive_list = os.listdir(usb_folder)
	print(len(drive_list))
        if len(drive_list) > 0:
	    if process.poll() == None:
            	os.system('pkill -9 feh')
            pi_list = os.listdir(image_folder)
	    print(pi_list)
            for i, slide_image in enumerate( pi_list ):
                if slide_image.endswith(file_formats):
                    print('Removing '+slide_image)
                    os.remove(image_folder + slide_image)
            for i, drive_name in enumerate( drive_list ):
                s = usb_folder + drive_name + '/'
                slen = len(s)
		for formats in file_formats:
	                for j, image_path_name in enumerate( glob.glob( usb_folder + drive_name + '/*' + formats ) ):
	                    file_name = image_path_name[slen:]
	                    if image_path_name.endswith(formats):
	                        print('Copying ' + file_name + ' from USB key to' + image_folder)
	                        shutil.copyfile(image_path_name, image_folder + file_name)
	    print 'Starting feh'
            process = subprocess.Popen('feh -Y -x -q -D 5 -B black -F -Z -z -r ' + image_folder, shell=True)
            os.system('umount ' + usb_folder + drive_name)
	    print usb_folder + drive_name

context = Context()
monitor = Monitor.from_netlink(context)

monitor.filter_by(subsystem='usb')
observer = MonitorObserver(monitor)

observer.connect('device-event', device_event)
monitor.start()

glib.MainLoop().run()
print 'Ready for USB device'
