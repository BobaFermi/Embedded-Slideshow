# Embedded-Slideshow
A Python 2.7 script written to run on a Raspberry Pi Zero connected to a departmental LCD screen. The idea is that the script runs on startup using cron, copies image files from connected USB drives and runs a slide show of those images using feh. If the image folder already contains images, they are erased first, the idea being that if any of the images used are out-of-date (maybe a messageboard or schedule for the week), nobody needs to connect a keyboard or mouse to fidget with the files. 
