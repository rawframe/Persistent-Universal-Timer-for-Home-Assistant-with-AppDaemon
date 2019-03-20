import appdaemon.plugins.hass.hassapi as hass
import datetime
from dateutil.rrule import *
# sudo apt-get install python3-dateutil (if pip install python-dateutil didn't work)
# http://jakubroztocil.github.io/rrule/

INPUT_SELECT_TIMER = 'input_select.timer_select'
SUN = 'sun.sun'

class Timer_Scheduler(hass.Hass):

  def initialize(self): 
    # run every minute on the minute - change second if other loads on cpu slowing
    time_check_interval = datetime.time(0, 0, 0)
    self.run_minutely(self.timer_scheduler, time_check_interval)
    self.listen_event(self.timer_scheduler, "MANAGE_TIMERS" , mode="run_scheduler" )

  def timer_scheduler (self, entity, *new, **kwargs):

    try:
      newly_saved_timer = self.global_vars['newly_saved_timer']
    except:
      newly_saved_timer = ""
    current_datetime_full = self.datetime()
    current_datetime = current_datetime_full.replace(second=0, microsecond=0)
    current_date = self.date()
    print ("[.. Timer Scheduler Scanning @", current_datetime, "]")

    dawn = self.get_state(SUN, attribute="next_dawn")
    sunrise = self.get_state(SUN, attribute="next_rising")
    sunset = self.get_state(SUN, attribute="next_setting")
    dusk = self.get_state(SUN, attribute="next_dusk")

    timers = self.global_vars['timers']
    for timer in timers :
      # runs only a freshly saved/updated timer through scheduler
      if newly_saved_timer != '' :
        if newly_saved_timer != timer :
          continue
        print (" ..... scheduler is processing newly saved timer : ", newly_saved_timer)

      print ("[... Scheduler is scanning saved timer : ", timer)
      timer_status = timers[timer]['State']
      timer_type = timers[timer]['Type']
      timer_start_datetime = timers[timer]['Start Time']
      timer_stop_datetime = timers[timer]['Stop Time']
      timer_start_sun_action = timers[timer]['Start Sun']
      timer_stop_sun_action = timers[timer]['Stop Sun']
      # move sun offsets to be read only if set ... ie in sun start and sun stop sections below
      timer_start_sun_offset = timers[timer]['Start Sun Offset']
      timer_stop_sun_offset = timers[timer]['Stop Sun Offset']
      # move rrule to rrules section ... ie only read when needed. also remove uneeded after testing
      timer_datetime_rule_preset = timers[timer]['Rule Preset']
      timer_datetime_rule_count = timers[timer]['Rule Count']
      timer_datetime_rule_txt = timers[timer]['Rule']

# if sun times set, update datetimes to match (reduce with for (start, stop) loop later)
      timer_start_date = datetime.datetime.date(timer_start_datetime)
      timer_stop_date = datetime.datetime.date(timer_stop_datetime)

      if timer_status == 'on' and (timer_start_sun_action != 'Off') :
        if timer_start_date == current_date :
          if timer_start_sun_action == 'Sunrise' :
            sun_start_datetime = sunrise
          elif timer_start_sun_action == 'Dusk' :
            sun_start_datetime = dusk
          elif timer_start_sun_action == 'Sunset' :
            sun_start_datetime = sunset
          elif timer_start_sun_action == 'Dawn' :
            sun_start_datetime = dawn
          # stripped timezone and seconds ... messy .. change !! allow seconds for later 
          sun_start_datetime = sun_start_datetime [:16]
          sun_start_datetime =  datetime.datetime.strptime(sun_start_datetime, "%Y-%m-%dT%H:%M")
          timer_start_datetime = sun_start_datetime + timer_start_sun_offset
        print ("[....  Start (Sun adjusted) ", timer_start_datetime)

      if timer_status == 'on' and (timer_stop_sun_action != 'Off') :
        if timer_stop_date == current_date :
          if timer_stop_sun_action == 'Sunrise' :
            sun_stop_datetime = sunrise
          elif timer_stop_sun_action == 'Dusk' :
            sun_stop_datetime = dusk
          elif timer_stop_sun_action == 'Sunset' :
            sun_stop_datetime = sunset
          elif timer_stop_sun_action == 'Dawn' :
            sun_stop_datetime = dawn
          # stripped timezone ... messy .. change !!
          sun_stop_datetime = sun_stop_datetime [:19]
          sun_stop_datetime =  datetime.datetime.strptime(sun_stop_datetime, "%Y-%m-%dT%H:%M:%S")
          timer_stop_datetime = sun_stop_datetime + timer_stop_sun_offset
        print ("[....  Stop (Sun adjusted) ", timer_stop_datetime)

      # turn off freshly saved timer if active
      if timer == newly_saved_timer :
        self.global_vars['newly_saved_timer'] = ''
        print ("..... newly saved timer run")

#  compare datetimes to current before proceeding with actions
      if (timer_start_datetime == current_datetime or timer_stop_datetime == current_datetime) and timer_status == 'on' :
        if timer_start_datetime == current_datetime :
          action = 'Start action'
        elif timer_stop_datetime == current_datetime :
          action = 'Stop action'
        scheduler_msg = "Scheduled timer: '" + timer + "' - '" + action + "', activated on " + str(current_datetime)
        self.call_service("persistent_notification/create", message = scheduler_msg, title = "TIMER Notification:", notification_id = "timer_name")
        print ("Scheduled timer: '", timer, "' - '", action, "', activated on", current_datetime)

        for entity in timers[timer]['Entities'] :
          entity_action = timers[timer]['Entities'][entity][action]
          #  do timer action
          if entity_action == 'Turn On' :
            self.turn_on(entity)
          elif entity_action == 'Turn Off' :
            self.turn_off(entity)
          elif entity_action == 'Toggle' :
          # do not calculate toggle from start action as can be already set with explicit on and off. use custom code option for more attributes
            self.toggle(entity)
          elif entity_action == 'Custom code' :
            print ('Custom start code for' , entity )

          print (" - Entity: '" , entity ,"' from timer '", timer, "' set to '", entity_action, "'")          

#      turn off countdown timer when finished
        if (timer_type == 'on') and (action == 'Stop action') :
          print ('Countdown timer completed :', timer)
          timers[timer]['State'] = 'off'
          scheduler_msg = "Countdown timer: '" + timer + "' completed"
          self.call_service("persistent_notification/create", message = scheduler_msg, title = "TIMER Notification:", notification_id = "timer_name")
          self.call_service('input_select/set_options', entity_id=INPUT_SELECT_TIMER, options=["Rebuilding list"] )

#      update next start or stop time if timer has a rrule set (excluding countdown timer)
        if (timer_status == 'on') and (timer_type != 'on') and (timer_datetime_rule_preset != 'Off') :
          # Rrule example 'RRULE:FREQ=MINUTELY;INTERVAL=2;COUNT=5' - see rrule docs about count and until combined usage) 
          timer_datetime_rule = rrulestr(timer_datetime_rule_txt)
          timer_datetime_rule = rrule.replace(timer_datetime_rule, dtstart=current_datetime)
          next_datetime_rule_occurance = timer_datetime_rule.after(current_datetime)
          print ('Timer rule run for :' , timer)
          print ('Next rule occurance :' , next_datetime_rule_occurance)
          # update start time of rrule timer to last run time or completed. this reduces rrule generation overhead instead of running every time the scheduler runs. count , interval, frequency etc will be overwritten on on save

          if action == 'Start action' :
            if next_datetime_rule_occurance != None :
              timers[timer]['Start Time'] = next_datetime_rule_occurance
              print ('New Start Time (rule) :', next_datetime_rule_occurance)
            else :
              print ('Start Timer Completed (rule) :', timer)

          elif action == 'Stop action' :
            if next_datetime_rule_occurance != None :
              timers[timer]['Stop Time'] = next_datetime_rule_occurance
              # stop datetime will also trigger rule updates that apply to start and stop dts
              # calc new rule count
              if timer_datetime_rule_count == 0 :
                print ('Rule has No Count set')
              else :
                new_count = timer_datetime_rule_count - 1
                new_count_r = new_count
                if new_count < 1 :
                  new_count = 0
                  new_count_r = None
                timer_datetime_rule = rrule.replace(timer_datetime_rule, count=new_count_r)
                timers[timer]['Rule Count'] = new_count
                print ('Rule Count New : ', new_count , new_count_r)

              print ('New Stop Time (rule) :', next_datetime_rule_occurance)
              timers[timer]['Rule'] = str(timer_datetime_rule)
              self.call_service('input_select/set_options', entity_id=INPUT_SELECT_TIMER, options=["Rebuilding list"] )
            else :
              timers[timer]['State'] = "off"
              timers[timer]['Rule Count'] = 0
              timer_datetime_rule = rrule.replace(timer_datetime_rule, count=None)
              timers[timer]['Rule'] = str(timer_datetime_rule)
              # turn off scheduled timer if rule finished
              scheduler_msg = "Scheduled timer with rule: '" + timer + "' completed"
              self.call_service("persistent_notification/create", message = scheduler_msg, title = "TIMER Notification:", notification_id = "timer_name")
              print ('Scheduled timer completed (Stop with rule) :', timer)
              self.call_service('input_select/set_options', entity_id=INPUT_SELECT_TIMER, options=["Rebuilding list"] )

#      turn off scheduled timer when finished
        if (timer_status == 'on') and (timer_type != 'on') and (action == 'Stop action') and (timer_datetime_rule_preset == 'Off') : # dont need first condition
          print ('Scheduled timer completed (Stop with no rule):', timer)
          timers[timer]['State'] = 'off'
          scheduler_msg = "Scheduled timer: '" + timer + "' completed"
          self.call_service("persistent_notification/create", message = scheduler_msg, title = "TIMER Notification:", notification_id = "timer_name")
          self.call_service('input_select/set_options', entity_id=INPUT_SELECT_TIMER, options=["Rebuilding list"] )

#  to save overhead, rrule list not created or saved to search through for scheduled occurances. so if hass is off then count will not register those missed occurances but continue the count (down) from last activation. This can be altered but saving the list and even trunkacting it by start date may run into problems with smaller regular intevals like minutely over longer unactive periods. Generating the list each time may make efficiency worse still. Maybe change in future if it is more important to retain expected counts from first save irrepective of whether the system is down inbetween occurances.
