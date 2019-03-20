import appdaemon.plugins.hass.hassapi as hass
import datetime

INPUT_SELECT_TIMER = 'input_select.timer_select'
INPUT_BOOLEAN_STATE = 'input_boolean.timer_status'
INPUT_TIMER_TYPE = 'input_boolean.timer_type'
INPUT_DATETIME_START_TIME = 'input_datetime.start_datetime'
INPUT_DATETIME_STOP_TIME = 'input_datetime.stop_datetime'
INPUT_SELECT_REFRESH_OPTION = 'Rebuilding list'
TIMER_TYPE_BOOLEAN_COUNTDOWN = "on"
TIMER_TYPE_BOOLEAN_SCHEDULE = "off"
MENU_NEW_COUNTDOWN = '* NEW - Countdown Timer'
MENU_NEW_SCHEDULED = '* NEW - Scheduled Timer'
MENU_COUNTDOWN_ACTIVE = '* COUNTDOWN Timers ACTIVE   :-'
MENU_COUNTDOWN_INACTIVE = '* COUNTDOWN Timers INACTIVE :-'
MENU_SCHEDULED_ACTIVE = '* SCHEDULED Timers ACTIVE   :-'
MENU_SCHEDULED_INACTIVE = '* SCHEDULED Timers INACTIVE :-'
TIMER_PRESET_LIST = [ MENU_NEW_COUNTDOWN, MENU_NEW_SCHEDULED, MENU_COUNTDOWN_ACTIVE, MENU_COUNTDOWN_INACTIVE, MENU_SCHEDULED_ACTIVE, MENU_SCHEDULED_INACTIVE, INPUT_SELECT_REFRESH_OPTION ]

INPUT_SELECT_SUN_ACTION_START = 'input_select.timer_start_sun_select'
INPUT_SELECT_SUN_ACTION_STOP = 'input_select.timer_stop_sun_select'
INPUT_NUMBER_SUN_START_OFFSET_HOUR = 'input_number.on_hour_sun'
INPUT_NUMBER_SUN_START_OFFSET_MINUTE = 'input_number.on_minute_sun'
INPUT_NUMBER_SUN_STOP_OFFSET_HOUR = 'input_number.off_hour_sun'
INPUT_NUMBER_SUN_STOP_OFFSET_MINUTE = 'input_number.off_minute_sun'

INPUT_SELECT_TIMER_RULE = 'input_select.timer_rule_select'
INPUT_TEXT_TIMER_RULE = 'input_text.timer_rule'
INPUT_NUMBER_TIMER_RULE_INTERVAL = 'input_number.rule_interval'
INPUT_SELECT_TIMER_BYWEEKDAY = 'input_select.timer_rule_select_by_weekday'
INPUT_NUMBER_TIMER_RULE_COUNT = 'input_number.rule_count'
INPUT_DATETIME_TIMER_RULE_UNTIL = 'input_datetime.rule_until'


class DynamicTimerInputSelect(hass.Hass):

  def initialize(self): 
    self.listen_state(self.timer_select_fn, INPUT_SELECT_TIMER)

  def timer_select_fn (self, entity, attribute, old, new, kwargs):
    timer_selection = self.get_state(INPUT_SELECT_TIMER)

#  CREATE TIMER LIST
    timers = self.global_vars['timers']
    timer_list = []
    timer_list_countdown_active = []
    timer_list_countdown_inactive = []
    timer_list_scheduled_active = []
    timer_list_scheduled_inactive = []

    for timer in timers :
      if timers[timer]['Type'] == TIMER_TYPE_BOOLEAN_COUNTDOWN :
        if timers[timer]['State'] == 'on' :
          timer_list_countdown_active.append(timer)
        else :
          timer_list_countdown_inactive.append(timer)
      else :
        if timers[timer]['State'] == 'on' :
          timer_list_scheduled_active.append(timer)
        else :
          timer_list_scheduled_inactive.append(timer)

    timer_list_countdown_active.sort()
    timer_list_countdown_inactive.sort()
    timer_list_scheduled_active.sort()
    timer_list_scheduled_active.sort()
    new_timer_list = [MENU_NEW_COUNTDOWN] + [MENU_NEW_SCHEDULED] + [MENU_COUNTDOWN_ACTIVE] + timer_list_countdown_active + [MENU_COUNTDOWN_INACTIVE] + timer_list_countdown_inactive + [MENU_SCHEDULED_ACTIVE] + timer_list_scheduled_active + [MENU_SCHEDULED_INACTIVE] + timer_list_scheduled_inactive
    current_list = (self.get_state(INPUT_SELECT_TIMER, attribute="options"))

  #  update timer list if changed
    if new_timer_list != current_list :
      self.call_service('input_select/set_options', entity_id=INPUT_SELECT_TIMER, options=new_timer_list)
      self.select_option(INPUT_SELECT_TIMER, timer_selection)

#  UPDATE TIMER ON/OFF STATUS
#     timer_selection = self.get_state(INPUT_SELECT_TIMER)
    if timer_selection == MENU_NEW_COUNTDOWN :
      self.set_state(INPUT_TIMER_TYPE, state=TIMER_TYPE_BOOLEAN_COUNTDOWN)
      # countdown timers have no rules so turn off rule 
      self.select_option(INPUT_SELECT_TIMER_RULE, "Off")
      print ("Countdown timer selected - Rule Preset set to Off")
    
    else :
      self.set_state(INPUT_TIMER_TYPE, state=TIMER_TYPE_BOOLEAN_SCHEDULE)

    if timer_selection not in TIMER_PRESET_LIST :
      timer_state = timers[timer_selection]['State']
      self.set_state(INPUT_BOOLEAN_STATE, state=timer_state) # ? change to service call to avoid appd break
      timer_type = timers[timer_selection]['Type']
      self.set_state(INPUT_TIMER_TYPE, state=timer_type) # ? change to service call ...
      timer_start_datetime = timers[timer_selection]['Start Time']
      timer_stop_datetime = timers[timer_selection]['Stop Time']

# INACTIVE COUNTDOWN ADJUSTED TO CURRENT TIME (OF SELECTION)
      #  countdown timer adjusted to current time while maintaining saved duration
      #  if countdown timer active do not reset times unless reset selected
      if (timer_type == TIMER_TYPE_BOOLEAN_COUNTDOWN) and (timer_state == 'off') :
        current_datetime = self.datetime()
        countdown_duration = timer_stop_datetime - timer_start_datetime
        timer_start_datetime = current_datetime
        timer_stop_datetime = timer_start_datetime + countdown_duration
        print ('Countdown Timer Start and Stop Dates adjusted', current_datetime, timer_stop_datetime)
      # countdown timer set to on for quick activation but not saved (as seen in list). 
        self.set_state(INPUT_BOOLEAN_STATE, state='on')

      timer_start_time =  timer_start_datetime.strftime('%H:%M')
      timer_start_date =  timer_start_datetime.strftime('%Y-%m-%d')  
      timer_stop_time =  timer_stop_datetime.strftime('%H:%M')
      timer_stop_date =  timer_stop_datetime.strftime('%Y-%m-%d')
      self.call_service("input_datetime/set_datetime", entity_id = INPUT_DATETIME_START_TIME, date=timer_start_date , time=timer_start_time)
      self.call_service("input_datetime/set_datetime", entity_id = INPUT_DATETIME_STOP_TIME, date=timer_stop_date , time=timer_stop_time)

# START SUN ACTIONS
      timer_sun_start_action = timers[timer_selection]['Start Sun']
      timer_sun_start_offset = timers[timer_selection]['Start Sun Offset']
      start_sun_offset_total_seconds = ((timer_sun_start_offset.days)*86400)+ timer_sun_start_offset.seconds 
      start_sun_offset_direction = '+'
      if start_sun_offset_total_seconds < 0 :
        start_sun_offset_direction = '-'
        start_sun_offset_total_seconds = abs(start_sun_offset_total_seconds)
      start_sun_offset_hour, start_sun_offset_minute = divmod(start_sun_offset_total_seconds, 3600)
      start_sun_offset_minute, start_seconds = divmod(start_sun_offset_minute, 60)
      if start_sun_offset_direction == '-' :
        start_sun_offset_hour = -(start_sun_offset_hour)
        start_sun_offset_minute = -(start_sun_offset_minute)
      #  start_seconds = -seconds
      self.select_option(INPUT_SELECT_SUN_ACTION_START, timer_sun_start_action)
      self.call_service("input_number/set_value",entity_id=INPUT_NUMBER_SUN_START_OFFSET_HOUR,value=(start_sun_offset_hour))
      # self.set_value(INPUT_NUMBER_SUN_START_OFFSET_HOUR, start_sun_offset_hour)
      self.call_service("input_number/set_value",entity_id=INPUT_NUMBER_SUN_START_OFFSET_MINUTE,value=(start_sun_offset_minute))
      # self.set_value(INPUT_NUMBER_SUN_START_OFFSET_MINUTE, start_sun_offset_minute)

# STOP SUN ACTIONS
      timer_sun_stop_action = timers[timer_selection]['Stop Sun']
      timer_sun_stop_offset = timers[timer_selection]['Stop Sun Offset']
      stop_sun_offset_total_seconds = ((timer_sun_stop_offset.days)*86400)+ timer_sun_stop_offset.seconds 
      stop_sun_offset_direction = '+'
      if stop_sun_offset_total_seconds < 0 :
        stop_sun_offset_direction = '-'
        stop_sun_offset_total_seconds = abs(stop_sun_offset_total_seconds)
      stop_sun_offset_hour, stop_sun_offset_minute = divmod(stop_sun_offset_total_seconds, 3600)
      stop_sun_offset_minute, stop_seconds = divmod(stop_sun_offset_minute, 60)
      if stop_sun_offset_direction == '-' :
        stop_sun_offset_hour = -(stop_sun_offset_hour)
        stop_sun_offset_minute = -(stop_sun_offset_minute)
      #  stop_seconds = -seconds
      self.select_option(INPUT_SELECT_SUN_ACTION_STOP, timer_sun_stop_action)
      self.call_service("input_number/set_value",entity_id=INPUT_NUMBER_SUN_STOP_OFFSET_HOUR,value=(stop_sun_offset_hour))
      # self.set_value(INPUT_NUMBER_SUN_STOP_OFFSET_HOUR, stop_sun_offset_hour)
      self.call_service("input_number/set_value",entity_id=INPUT_NUMBER_SUN_STOP_OFFSET_MINUTE,value=(stop_sun_offset_minute))
      # self.set_value(INPUT_NUMBER_SUN_STOP_OFFSET_MINUTE, stop_sun_offset_minute)

#  RRULES
      timer_rule_select = timers[timer_selection]['Rule Preset']
      timer_rule = timers[timer_selection]['Rule']
      timer_rule_interval = timers[timer_selection]['Rule Interval']
      timer_rule_byweekday = timers[timer_selection]['Rule Weekday']
      timer_rule_count = timers[timer_selection]['Rule Count']
      timer_rule_until = timers[timer_selection]['Rule Until']

      self.select_option(INPUT_SELECT_TIMER_RULE, timer_rule_select)
      self.call_service('input_text/set_value', entity_id=INPUT_TEXT_TIMER_RULE, value=timer_rule)
      self.call_service("input_number/set_value",entity_id=INPUT_NUMBER_TIMER_RULE_INTERVAL,value=(timer_rule_interval))
      # self.set_value(INPUT_NUMBER_TIMER_RULE_INTERVAL, timer_rule_interval)

      self.select_option(INPUT_SELECT_TIMER_BYWEEKDAY, timer_rule_byweekday)

      self.call_service("input_number/set_value",entity_id=INPUT_NUMBER_TIMER_RULE_COUNT,value=(timer_rule_count))
      # self.set_value(INPUT_NUMBER_TIMER_RULE_COUNT, timer_rule_count)

      timer_rule_until_time =  timer_rule_until.strftime('%H:%M')
      timer_rule_until_date =  timer_rule_until.strftime('%Y-%m-%d')  
      self.call_service("input_datetime/set_datetime", entity_id = INPUT_DATETIME_TIMER_RULE_UNTIL, date=timer_rule_until_date , time=timer_rule_until_time)
