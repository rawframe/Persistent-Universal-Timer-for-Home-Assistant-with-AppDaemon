# Author : RAWFRAME

import appdaemon.plugins.hass.hassapi as hass
import datetime
from dateutil.rrule import *
import pickle

INPUT_BOOLEAN_TIMERS = "input_boolean.timers"
INPUT_DATETIME_START_DATETIME = 'input_datetime.start_datetime'
INPUT_DATETIME_STOP_DATETIME = 'input_datetime.stop_datetime'
INPUT_SELECT_TIMER = 'input_select.timer_select'
INPUT_SELECT_TIMER_ENTITY_HIDDEN = 'input_select.timer_entity_select_hidden'
INPUT_SELECT_TIMER_ENTITY_FRIENDLY = 'input_select.timer_entity_select_friendly'
TIMER_SCHEDULER_SCRIPT = 'script.scheduler'
PRESET_SAVED_ENTITIES = "* SAVED ENTITIES :-"
PRESET_AVAILABLE_ENTITIES = "* AVAILABLE ENTITIES :-"
PRESET_LIST = [PRESET_SAVED_ENTITIES] + [PRESET_AVAILABLE_ENTITIES]
# NEW_TIMER_SCHEDULER_CALL_BOOLEAN = '

class Timer_Management(hass.Hass):

  def initialize(self):
    self.listen_event(self.save_timer, "MANAGE_TIMERS" , mode="save_timer" )
    self.listen_event(self.delete_timer, "MANAGE_TIMERS" , mode="delete_timer" )
    self.listen_event(self.delete_timer_entity, "MANAGE_TIMERS" , mode="delete_timer_entity" )
    self.listen_event(self.backup_timers, "MANAGE_TIMERS" , mode="backup_timers" )
    self.listen_event(self.restore_timers, "MANAGE_TIMERS" , mode="restore_timers" )
    self.listen_event(self.restore_timers,"plugin_started") # autostart
    self.listen_event(self.reset_timers, "MANAGE_TIMERS" , mode="reset_timers" )
    self.listen_event(self.reset_datetimes, "MANAGE_TIMERS" , mode="reset_datetimes" )
    self.listen_event(self.synchronise_timers, "MANAGE_TIMERS" , mode="synchronise_timers" ) # after timer restore
    self.listen_state(self.synchronise_timers, INPUT_BOOLEAN_TIMERS, new = "on")

#  SAVE SELECTED TIMER AND ENITIY
  def save_timer (self, entity, new, kwargs):
    timers = self.global_vars['timers']
    timer_name = self.get_state('input_text.entity_timer_name')
    timer_name_default = "Enter new timer name"
    timer_state = self.get_state('input_boolean.timer_status')
    timer_type = self.get_state('input_boolean.timer_type')
    timer_start_time = self.get_state('input_datetime.start_datetime')
    timer_start_time = datetime.datetime.strptime(timer_start_time, "%Y-%m-%d %H:%M:%S")
    timer_stop_time = self.get_state('input_datetime.stop_datetime')
    timer_stop_time = datetime.datetime.strptime(timer_stop_time, "%Y-%m-%d %H:%M:%S")
    timer_sun_start_action = self.get_state('input_select.timer_start_sun_select')
    timer_sun_start_offset_hour = self.get_state('input_number.on_hour_sun')
    timer_sun_start_offset_hour = int(float(timer_sun_start_offset_hour))
    timer_sun_start_offset_minute = self.get_state('input_number.on_minute_sun')
    timer_sun_start_offset_minute = int(float(timer_sun_start_offset_minute))
    timer_sun_stop_action = self.get_state('input_select.timer_stop_sun_select')
    timer_sun_stop_offset_hour = self.get_state('input_number.off_hour_sun')
    timer_sun_stop_offset_hour = int(float(timer_sun_stop_offset_hour))
    timer_sun_stop_offset_minute = self.get_state('input_number.off_minute_sun')
    timer_sun_stop_offset_minute = int(float(timer_sun_stop_offset_minute))
    # print (timer_sun_start_offset_hour , timer_sun_start_offset_minute)
    timer_sun_start_offset = datetime.timedelta(hours=timer_sun_start_offset_hour, minutes=timer_sun_start_offset_minute)
    timer_sun_stop_offset = datetime.timedelta(hours=timer_sun_stop_offset_hour, minutes=timer_sun_stop_offset_minute)

    timer_rule = self.get_state('input_text.timer_rule')
    timer_rule_preset = self.get_state('input_select.timer_rule_select')
    timer_rule_interval = int(float(self.get_state('input_number.rule_interval')))
    timer_rule_byweekday = self.get_state('input_select.timer_rule_select_by_weekday')
    timer_rule_count = int(float(self.get_state('input_number.rule_count')))
    timer_rule_until = self.get_state('input_datetime.rule_until')
    timer_rule_until = datetime.datetime.strptime(timer_rule_until, "%Y-%m-%d %H:%M:%S")

    timer_entity_id = self.get_state(INPUT_SELECT_TIMER_ENTITY_HIDDEN)
    timer_entity_friendly = self.get_state(INPUT_SELECT_TIMER_ENTITY_FRIENDLY)
    timer_entity_start_action = self.get_state('input_select.entity_start_action_select')
    timer_entity_stop_action = self.get_state('input_select.entity_stop_action_select')
    current_datetime = self.datetime()

    # create/update timer rrule
    timer_rule_default = 'RRULE:FREQ=DAILY'
    if timer_rule == "" :
      timer_rule = rrulestr(timer_rule_default)
    else :
      timer_rule = rrulestr(timer_rule)
    
    if timer_rule_preset != 'Off' :
      timer_rule = rrule.replace(timer_rule, freq=eval(timer_rule_preset))
      
    timer_rule = rrule.replace(timer_rule, interval=timer_rule_interval)

    if timer_rule_byweekday != 'Custom' :
      if timer_rule_byweekday == 'None' :
        timer_rrule_byweekday = None
      elif timer_rule_byweekday == 'MONDAYS' :
        timer_rrule_byweekday = MO
      elif timer_rule_byweekday == 'TUEDAYS' :
        timer_rrule_byweekday = TU
      elif timer_rule_byweekday == 'WEDNESDAYS' :
        timer_rrule_byweekday = WE
      elif timer_rule_byweekday == 'THURSDAYS' :
        timer_rrule_byweekday = TH
      elif timer_rule_byweekday == 'FRIDAYS' :
        timer_rrule_byweekday = FR
      elif timer_rule_byweekday == 'SATURDAYS' :
        timer_rrule_byweekday = SA
      elif timer_rule_byweekday == 'SUNDAYS' :
        timer_rrule_byweekday = SU
      elif timer_rule_byweekday == 'WEEKDAYS' :
        timer_rrule_byweekday = (MO,TU,WE,TH,FR)
      elif timer_rule_byweekday == 'WEEKENDS' :
        timer_rrule_byweekday = (SA,SU)
      timer_rule = rrule.replace(timer_rule, byweekday=timer_rrule_byweekday)

    if timer_rule_count == 0 : # 0 signifies turn off count (=none)
      timer_rule = rrule.replace(timer_rule, count=None)
    else :
      timer_rule = rrule.replace(timer_rule, count=timer_rule_count)

    if timer_rule_until < current_datetime :
      timer_rule = rrule.replace(timer_rule, until=None)
    else :
      timer_rule = rrule.replace(timer_rule, until=timer_rule_until)

    timer_rule = rrule.replace(timer_rule, dtstart=timer_start_time)

    timer_rule = str(timer_rule)
    print ('Rrule for timer:', timer_rule)
    # turn of rule if timer is a countdown
    if timer_type == 'on' :
      timer_rule_preset = "Off"
    # check a timer name has been entered before proceeding and notify
    if timer_name == timer_name_default:
      timer_save_datetime = current_datetime.replace(microsecond=0)
      timer_name = timer_entity_friendly + ' [' + str(timer_save_datetime) + ']'
      self.call_service("persistent_notification/create", message = "Timer name not entered. Timer name set to default entity and creation time. You can change it at anytime.", title = "TIMER Notification:", notification_id = "timer_name")
    # then add new timer to timers if unique
    if timer_name not in timers:
      timers.update(
      {timer_name : 
        {"State" : timer_state,
        "Type" : timer_type,
        "Start Time" : timer_start_time,
        "Stop Time" : timer_stop_time,
        "Start Sun" : timer_sun_start_action,
        "Start Sun Offset" : timer_sun_start_offset,
        "Stop Sun" : timer_sun_stop_action,
        "Stop Sun Offset" : timer_sun_stop_offset,
        "Rule" : timer_rule,
        "Rule Preset" : timer_rule_preset,
        "Rule Interval" : timer_rule_interval,
        "Rule Weekday" : timer_rule_byweekday,
        "Rule Count" : timer_rule_count,
        "Rule Until" : timer_rule_until,
        "Entities" : {}}})
    else:
    # or update timer state and times 
      timers[timer_name].update( 
        {"State" : timer_state,
        "Type" : timer_type,
        "Start Time" : timer_start_time,
        "Stop Time" : timer_stop_time,
        "Start Sun" : timer_sun_start_action,
        "Start Sun Offset" : timer_sun_start_offset,
        "Stop Sun" : timer_sun_stop_action,
        "Stop Sun Offset" : timer_sun_stop_offset,
        "Rule" : timer_rule,
        "Rule Preset" : timer_rule_preset,
        "Rule Interval" : timer_rule_interval,
        "Rule Weekday" : timer_rule_byweekday,
        "Rule Count" : timer_rule_count,
        "Rule Until" : timer_rule_until,})

    # check entity selected and not preset option
    if timer_entity_id not in PRESET_LIST :
      # add new entity to timer if unique
      if timer_entity_id not in timers[timer_name]['Entities']:
        timers[timer_name]['Entities'].update({timer_entity_id:{}})
      # update timer entity actions 
      timers[timer_name]['Entities'][timer_entity_id].update( 
        {"Start action" : timer_entity_start_action,
        "Stop action" : timer_entity_stop_action,})

    self.global_vars['timers'] = timers

    # pass new timer through synchroniser for past dated or reactivated timers with rules etc
    self.global_vars['newly_saved_timer'] = timer_name
    self.synchronise_timers (entity, new, kwargs)
    # pass new timer through scheduler to catch instant start or stop
    self.turn_on(TIMER_SCHEDULER_SCRIPT)

    # refresh timer selection list and set value to current
    self.call_service('input_select/set_options', entity_id=INPUT_SELECT_TIMER, options=["Rebuilding list"] )
    try:
      self.select_option(INPUT_SELECT_TIMER, timer_name)
    except Exception:
      print ("Timer select name not found in timer list")


#  DELETE SELECTED TIMER
  def delete_timer (self, entity, new, kwargs):
    print ("DELETE SELECTED TIMER")
    timers = self.global_vars['timers']
    timer_selected = self.get_state(INPUT_SELECT_TIMER)
    try:
      del timers[timer_selected]
    except Exception:
      self.call_service("persistent_notification/create", message = "Current selection cannot be deleted", title = "TIMER Notification:", notification_id = "timer_name")
    self.global_vars['timers'] = timers
    self.call_service('input_select/set_options', entity_id=INPUT_SELECT_TIMER, options=["Rebuilding list"] )


#  DELETE SELECTED TIMER ENTITY
  def delete_timer_entity (self, entity, new, kwargs):
    print ("DELETE SELECTED TIMER ENTITY")
    timers = self.global_vars['timers']
    timer_selected = self.get_state(INPUT_SELECT_TIMER)
    timer_entity_selected = self.get_state(INPUT_SELECT_TIMER_ENTITY_HIDDEN)
    try:
      del timers[timer_selected]['Entities'][timer_entity_selected]
    except Exception:
      self.call_service("persistent_notification/create", message = "Current selection cannot be deleted", title = "TIMER Notification:", notification_id = "timer_name")
    self.global_vars['timers'] = timers
    self.call_service('input_select/set_options', entity_id=INPUT_SELECT_TIMER_ENTITY_FRIENDLY, options=["Rebuilding list"] )


#  BACKUP TIMERS
  def backup_timers (self, entity, new, kwargs):
    print ("BACKUP TIMERS")
    timers = self.global_vars['timers']
    pickle.dump( timers, open( "timer_backup.p", "wb" ) )
    self.call_service("persistent_notification/create", message = "Timers backup successful (timer_backup.p)", title = "TIMER Notification:", notification_id = "timer_name")
    print (timers)


#  RESTORE TIMERS
  def restore_timers (self, entity, new, kwargs):
    print ("RESTORE TIMERS")
#  to do : call timerreset function if there is no dict yet
    timers = pickle.load( open( "timer_backup.p", "rb" ) )
    self.global_vars['timers'] = timers
    self.call_service("persistent_notification/create", message = "Timers restoration successful (timer_backup.p)", title = "TIMER Notification:", notification_id = "timer_name")
    self.call_service('input_select/set_options', entity_id=INPUT_SELECT_TIMER, options=["Rebuilding list"] )
    try:
      self.select_option(INPUT_SELECT_TIMER, timer_name)
    except Exception:
      print ("Timer select name not found in timer list")
    print ('TIMERS RESTORE DICT', timers)

    self.global_vars['newly_saved_timer'] = ''
    self.global_vars['live_duration_preset_start'] = ''
    self.global_vars['live_duration_preset_stop'] = ''
    self.synchronise_timers (entity, new, kwargs)


#  RESET TIMERS
  def reset_timers (self, entity, new, kwargs):
    print ("RESET TIMERS")
    # to add for when dict is new and empty
    timers = {}
    self.global_vars['timers'] = timers
    # self.global_vars['timers'] = pickle.load( open( "timer_backup.p", "rb" ) )
    self.global_vars['newly_saved_timer'] = ''

    self.call_service("persistent_notification/create", message = "Timers Reset successful (timer_backup.p)", title = "TIMER Notification:", notification_id = "timer_name")
    self.call_service('input_select/set_options', entity_id=INPUT_SELECT_TIMER, options=["Rebuilding list"] )

    print ('TIMERS RESET DICT', timers)
    # try:
    #   self.select_option(INPUT_SELECT_TIMER, timer_name)
    # except Exception:
    #   print ("Timer select name not found in timer list")

#  RESET DATETIMES
  def reset_datetimes (self, entity, new, kwargs):
    # current_datetime = datetime.datetime.now()
    print ("DATETIMES RESET")
    current_datetime = self.datetime()
    current_stop_date =  current_datetime.strftime('%Y-%m-%d')
    current_stop_time =  current_datetime.strftime('%H:%M')
    self.call_service("input_datetime/set_datetime", entity_id = INPUT_DATETIME_START_DATETIME, date=current_stop_date , time=current_stop_time)
    self.call_service("input_datetime/set_datetime", entity_id = INPUT_DATETIME_STOP_DATETIME, date=current_stop_date , time=current_stop_time)
    self.call_service("persistent_notification/create", message = "Datetimes Reset to current values", title = "TIMER Notification:", notification_id = "timer_name")


#  TIMER RE-SYNC
  def synchronise_timers (self, entity, new, *kwargs):
    print ("SYNCHRONISING TIMERS")
    try:
      newly_saved_timer = self.global_vars['newly_saved_timer']
    except:
      newly_saved_timer = ""
    current_datetime_full = self.datetime()
    current_datetime = current_datetime_full.replace(second=0, microsecond=0)
    if newly_saved_timer != "" :
      current_datetime = current_datetime - datetime.timedelta(milliseconds=1) #to enable catching of newly saved timers set for this moment. we do not want all timers processed like this to avoid timer activation repition if scheduler called more than once in the minute. maybe in the future flag ammended timers only to run through the scheduler.

    timers = self.global_vars['timers']
    for timer in timers :
      # runs only a freshly saved/updated timer through scheduler
      if newly_saved_timer != '' :
        if newly_saved_timer != timer :
          continue
        print ("..Synchroniser is processing Newly saved timer : ", newly_saved_timer)

      # print ('timer', timer)
      timer_status = timers[timer]['State']
      timer_type = timers[timer]['Type']
      timer_start_datetime = timers[timer]['Start Time']
      timer_stop_datetime = timers[timer]['Stop Time']
      timer_datetime_rule_preset = timers[timer]['Rule Preset']
      # timer_datetime_rule_until = timers[timer]['Rule Until']
      timer_datetime_rule_count = timers[timer]['Rule Count']
      timer_datetime_rule_interval = timers[timer]['Rule Interval']
      timer_datetime_rule_txt = timers[timer]['Rule']
      timer_datetime_rule = rrulestr(timer_datetime_rule_txt)

      if timer_status == 'on' :
      # timer is on
        print('Timer is On')

        if timer_datetime_rule_preset == "Off" :
        # rule is off
          print('Rule is Off')
          if timer_stop_datetime < current_datetime :
          # timer has expired
            print('Timer Expired')
            timers[timer]['State'] = "off"

        else :
        # rule is on
          print('Rule is On')
          timer_datetime_rule_until_r = timer_datetime_rule._until # until value must be read from rule

          if (timer_datetime_rule_until_r != None) and (timer_datetime_rule_until_r < current_datetime) :
          # until has expired
            print('Until Expired')
            timers[timer]['State'] = "off"
          else :
          # until is unexpired
            print('Until Unexpired')
            timer_datetimes_types = ["start_datetime_loop", "stop_datetime_loop"]
          
            for timer_datetime_type in timer_datetimes_types :

              if timer_datetime_type == "start_datetime_loop" :
                timer_datetime = timer_start_datetime
                print('Start Timer')
              else :
                timer_datetime = timer_stop_datetime
                print('Stop Timer')

              if timer_datetime == current_datetime : # no need to process rule here. pass to scheduler to run
                continue

              # list iterations between then and now time to calculate count and next occurance
              timer_datetime_rule_tmp = rrule.replace(timer_datetime_rule, dtstart=timer_datetime, until=current_datetime)
              occurances_missed_list = list(timer_datetime_rule_tmp)
              occurances_missed_count = len(occurances_missed_list)
              if occurances_missed_count < 1 :
                occurance_missed_last = timer_datetime # none missed so old time remains valid
              else :
                occurance_missed_last = occurances_missed_list[-1]
              print ('Missed count : ', occurances_missed_count)
              # print ('Last expected occurance before now : ', occurance_missed_last)

              # calc new rule count
              if timer_datetime_rule_count == 0 :
                print ('Rule has No Count set')
                new_count = 0
                new_count_r = None
                timer_datetime_rule_tmp = rrule.replace(timer_datetime_rule, dtstart=occurance_missed_last, count=new_count_r)
              else :
                new_count = timer_datetime_rule_count - occurances_missed_count
                new_count_r = new_count
                if new_count < 1 :
                  new_count = 0
                  new_count_r = None
                timer_datetime_rule_tmp = rrule.replace(timer_datetime_rule, dtstart=occurance_missed_last, count=new_count)
                print ('Rule New Count : ', new_count , new_count_r)

              # set last iteration as new dtstart to find next occurance  
              next_datetime_rule_occurance = timer_datetime_rule_tmp.after(current_datetime)

              # start datetime update
              if timer_datetime_type == "start_datetime_loop" :
                if next_datetime_rule_occurance == None :
                  timers[timer]['Start Time'] = occurance_missed_last
                else :
                  timers[timer]['Start Time'] = next_datetime_rule_occurance
                print ('START UPDATED - [Timer Name: ', timer, ' Last missed: ', timer_datetime, ' Last due: ', occurance_missed_last, ' Next due: ', next_datetime_rule_occurance, ']')

              # stop datetime update
              else :
                if next_datetime_rule_occurance == None :
                  timers[timer]['Stop Time'] = occurance_missed_last
                  timers[timer]['State'] = 'off'
                  dtstart_new = occurance_missed_last
                else :
                  timers[timer]['Stop Time'] = next_datetime_rule_occurance
                  dtstart_new = next_datetime_rule_occurance
                print ('STOP UPDATED - [Timer Name: ', timer, ' Last missed: ', timer_datetime, ' Last due: ', occurance_missed_last, ' Next due: ', next_datetime_rule_occurance, ']')

                # rule and count update
                timer_datetime_rule_new = rrule.replace(timer_datetime_rule, dtstart=dtstart_new, count=new_count_r)
                timers[timer]['Rule'] = str(timer_datetime_rule_new)
                timers[timer]['Rule Count'] = new_count
                print ('Rule updated : ', str(timer_datetime_rule_new))

    print ('SYNCHRONISING COMPLETE')
    self.call_service("persistent_notification/create", message = "Timer Synchronisation complete", title = "TIMER Notification:", notification_id = "timer_name")

