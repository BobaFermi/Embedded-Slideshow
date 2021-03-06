# Embedded-Slideshow
A Python 2.7 script written to run on a Raspberry Pi Zero connected to a departmental LCD screen. The idea is that the script runs on startup using cron, copies image files from connected USB drives and runs a slide show of those images using feh. Currently, the file copier is in an 'additive' state, so that it continues to add unique images to the folder parsed by feh, but it is simple to adjust to remove all images each time new images are copied (useful in the case of message board images that will become out of date).

Maybe other people can try to get this working with crontab, but all my attempts ended with failure (cron only seems to run code in the background, so feh would not appear onscreen, although all the USB transfer stuff would still run). 

The steps I used to get this running automatically are as follows:

1. Copy slideloader.py to the desired folder. All of the folder references in the code are absolute, so it will currently save all the images in /home/pi/Desktop/Images

2. Make slideloader.py executable by running the command 'chmod +x /path/to/slideloader.py' (without quotes) in the terminal.

3. This step assumes the default build of raspbian with the default desktop manager. Add a line to the end of the file ~/.config/lxsession/LXDE-pi/autostart to execute slideloader. The line should read '@/path/to/slideloader.py' (without quotes).
