# homeassistant
General Purpose Timer
Author : rawframe

Hello,
Im not a programmer or like but threw this together and thought this may be of use.
Started it in standard yaml but some limitations pushed me towards Appdaemon.

Requirements:
. Home Assistant
. Appdaemon
. sudo apt-get install python3-dateutil (if pip install python-dateutil didn't work)

Usage:
. Just play with it. Made it fairly open in function so it should be able to do most things.
. The timers will persist even after restart.
. http://jakubroztocil.github.io/rrule/ will help you generate complex rrules like every 4th months on a Saturday etc..

Future:
. Finish the 'custom code' action by adding a txt box and dict entry similar to rrule. Not so motivated to do so because not sure its of great benefit ... could just run a scene or script or automation ... etc to achieve same.
. Can change to work secondly without too much effort but think it will be too much overhead for most setups.

Bugs:
. A New timer currently forces the minutley scheduler to run again, so any active timers scheduled to run at that same minute will go again. May add a flag to solve or just write code to pass only that timer through the scheduler/copy.
. Countdown timer sometimes doesnt set corresponding times corretly when selected. Loop issue. Just select another timer and then reselect usually solves.

