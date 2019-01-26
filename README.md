# homeassistant
General Purpose Timer
Author : rawframe

Hello,
Im not a programmer as but threw this together and thought this may be of use.
Started it in standard yaml but some limitations pushed me towards Appdaemon.

Requirements:
. Home Assistant
. Appdaemon
. sudo apt-get install python3-dateutil (if pip install python-dateutil didn't work)

Usage:
. Just play with it. Made it fairly open in function so it should be able to do most things.
. The timers will persist even after restart.
. http://jakubroztocil.github.io/rrule/ will help you generate complex rrules like every 4th month on the last Saturday etc..

Future:
. Finish the 'custom code' action by adding a txt box and dict entry similar to rrule. (Not so motivated to do so because not sure its of great benefit ... could just run a scene or script or automation ... etc to achieve same).
. Can change to work secondly without too much effort but think it could be too much overhead for most setups.
. Make a quick start, per second accurate, countdown timer option.
. Change code to work better with zone information.

Bugs:
. A New timer currently forces the scheduler (minutely) to run again, so any active timers scheduled to run at that minute will also run again. May add a flag to solve or just write code to pass only that timer through the scheduler/copy.
. Countdown timer sometimes doesnt set corresponding times corretly when selected. Loop issue. Just select another timer and then reselect usually solves.

