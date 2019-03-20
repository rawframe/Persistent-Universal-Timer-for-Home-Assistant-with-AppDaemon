![](Timer.gif)

### home assistant
# General Purpose Timer for Home Assistant (devices, scripts, scenes, etc.)
### Author : rawframe

**Intro:**
- Hello, I'm not a programmer but put this together for my specific needs.
- It's a universal persistent timer (devices, scripts, scenes, etc.) which allows grouping and individual actions.
  - eg1. Every weekday an hour after sunrise, turn on radio, turn on light and turn off electric blanket- Then turn all off an hour later.
  - eg2. Turn off the TV in 2 hours from now.
  - eg3. Turn on a water sprinkler an hour after sunrise for an hour if the temperature is over 15deg (using script for now / custom code future feature).
- Started it in standard yaml but limitations pushed me towards App daemon (python integration)- (Old yaml code left in place in case HA one day supports the missing features needed).
- Overall it's not a very smart implementation in terms of fault tolerance or efficiency; as my primitive, learn as you need, improvised coding reveals. Also, it's usage has expanded alot and is now clunky and in need of complete re-working in recognition of this.
- Haven't tested it extensively either, so if it's critical I would try your timer first.

**Requirements:**
- Home Assistant
- App daemon
- sudo apt-get install python3-dateutil (if pip install python-dateutil didn't work)

**Usage:**
- Each timer has a start and stop date and time which can have sun time offsets and repeat rules. (If sun timers are on they override the time on the date and time set)
- Each timer can also have 1 or more entities (lights, scripts, automations, switches etc.) and each entity can have a start and stop action.
- The timers will persist even after restart, and can be backed up, restored, etc.
- A rule count or timer is only considered complete when the stop part of the timer is run. So if you only want a single time timer set the start action to 'do nothing'.
- On saving a timer with an until rule, if the until value is less than the current date and time, then it is considered as set to None/Off. (Best option for the limited interface without adding more menu clutter).
- A count value of 0 indicates that no count rule is to be set, with count rule set to None/Off. (Best option for the limited interface without adding more menu clutter).
- If entered, a manual rule is used as the base rule and then overwritten by menu selected values- http://jakubroztocil-github-io/rrule/ will help you generate complex rrules like every 4th month on the last Saturday, or only the day before Easter etc.
- Inactive Countdown timers will update to the current date and time while maintaining duration for ease of re-using.
- Timer durations do not fully account for sun related timings because forward data is not available in HA, and it would be confusing to use a dual system to account for same day for now.
- Timer duration changes are applied to the later occurrence of the start and stop date-times. This means it still works if the start date-time is actually after the stop date-time as may occur with rules based timers, and in this instance the start date-time is adjusted instead of the stop date-time. By default the stop date-times is after the start date-time.

**Future/Maybe:**
- Make a quick start, per second accurate, countdown timer option. Current implementation is extension of primary schedule timer functionality and is a clunky countdown implementation.
- Perhaps it now makes sense to run a sync before scheduler (but increases load) or just on timer selection.
- Once timer save and automatic reselect bug is solved, apply reselect to rule timers to keep them looking live in the HA interface also.
- Parse custom rrule on save using 'try:' to catch invalid entries.
- Display live sun timing via external source.
- Reduce scheduler timer scanning time by only reading in start and stop date-times either directly or via matching tuples.
- Highlight/remove timer entities that are no longer in the system.
- Finish the 'custom code' action by adding a text box and dict entry. (Not sure it's of great benefit ... could just run a scene, script, automation etc. to achieve same).
- Change code to work with zone information.
- Scheduler should update both start and stop times if either run to avoid having to re-sync - i.e. check them both at the same time though this will increase load unnecessarily for a larger system that doesn't restart off switch of timers often- better to leave this to the save sync for now.
- Sun timers with rules - match is on sun adjusted time and then the rule for next uses this last occurrence time. This is ok so long as the offset isn't so large it tips the timer to another day- the rule could be run only on the original start/stop times and then adjusted through the scheduler but i prefer it adjusting after itself closer to the real times so i can see roughly when they will be running.
- Run updated sync timers through scheduler to catch instant activations? (Not sure this is preferred as minutely should refer to the beginning of the minute). to fix and avoid already run timer repeats, maybe flag only changed timers for scheduler to identify as per newly saved timers.
- Skin the interface. (Having 0 or a past until date-time to signify none etc.is not perfectly clear but a current compromise over adding more menu clutter).
- The timer grew in functionality (as required) and as such its somewhat disjoined and unintuitive especially in code. Also it transitioned from standard yaml into app-daemon so techniques such as input boolean loop control remain when they could be replaced.
- Ideally I would like to add to or create a true calendar that can provide similar options. At the time I couldn't find enough flexibility in mainstream free calenders (i.e.- remotely updatable custom fields or offline use). Then add the calendar as a HA side tab which shows upcoming and past timers.

**Notes:**
- To have the persistent timer functionality, Timer Restore will only automatically activate if AppD is loaded before HA reloads. (i.e. its listening for a HA restart).
- RRule count does not decrease unless timer actually run, i.e. count will not decrease if the system is off or while the timer is off (i.e. the last scheduled occurrence was missed). The last run occurrence will hence be the last start and stop times saved before any re-syncing
- Rrule docs suggest not to use rule count and until in the same rule but works in simple tests for me.
- If sync has missed a lot of activations it may take some time to get all the iterations and receive the synchronised completion notification.
- Learnt and expanded features as I needed them, so maybe someone could optimise and clean up the code using global variables, modules and functions (now I think I know what they are) to avoid repetitive code and to correct logic.
- From 'SELECT YOUR DEVICE' you can choose to enable the input box showing the actual entity as exposed by HA - helpful for migration/maintenance/missing identification.
- Can change to work secondly without too much effort but think it could be too much overhead for most setups and unnecessary.

**Bugs known:**
- Countdown timer sometimes doesn't set corresponding times correctly when selected- Loop issue? Select another timer and then re-selecting usually solves.
- On timer save, sometimes the timer is not automatically reselected in the timer menu list. Loop selection issue?
- Restart Auto Timer Restore can be temperamental ... maybe appd hass load order issue. Manual restore works as usual.
- Next live occurrence compact views preselect doesn't distinguish between start or stop. (Can be changed but better to re-work whole system at once than put time into this).
- Live duration presets do not reflect in next live duration preset option and appear as manual when one start or stop timer in a set surpass eachother. Logic used was makeshift.
- Feedback loop occurs (datetimes updated, live timer, duration, and timer sync) which requires a manual restart on occasion! May be due to bad boolean app control and not using global var alternative. Better to solve on rebuild with modules, functions, and globals. ; especially if converted entirley to AppD.
