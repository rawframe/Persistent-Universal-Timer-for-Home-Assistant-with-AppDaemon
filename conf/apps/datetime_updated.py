import appdaemon.plugins.hass.hassapi as hass
import datetime
from dateutil import relativedelta

INPUT_SELECT_START_DATETIME = 'input_datetime.start_datetime'
INPUT_SELECT_STOP_DATETIME = 'input_datetime.stop_datetime'
INPUT_NUMBER_TIMER_START_HOUR = 'input_number.on_hour'
INPUT_NUMBER_TIMER_START_MINUTE = 'input_number.on_minute'
INPUT_NUMBER_TIMER_STOP_HOUR = 'input_number.off_hour'
INPUT_NUMBER_TIMER_STOP_MINUTE = 'input_number.off_minute'
INPUT_NUMBER_TIMER_DURATION_YEARS = 'input_number.on_duration_years'
INPUT_NUMBER_TIMER_DURATION_MONTHS = 'input_number.on_duration_months'
INPUT_NUMBER_TIMER_DURATION_DAYS = 'input_number.on_duration_days'
INPUT_NUMBER_TIMER_DURATION_DAYS_TOTAL = 'input_number.on_duration_days_total'
INPUT_NUMBER_TIMER_DURATION_WEEKS_TOTAL = 'input_number.on_duration_weeks_total'
INPUT_NUMBER_TIMER_DURATION_HOURS = 'input_number.on_duration_hours'
INPUT_NUMBER_TIMER_DURATION_MINUTES = 'input_number.on_duration_minutes'
INPUT_BOOLEAN_TIMER_SYNC = 'input_boolean.timer_sync'
INPUT_BOOLEAN_PRESET_DURATION_TIMER_SYNC = 'input_boolean.preset_duration_timer_sync'
INPUT_BOOLEAN_PRESET_LIVE_DURATION_TIMER_SYNC = 'input_boolean.preset_live_duration_timer_sync'
INPUT_SELECT_TIMER_DURATION_PRESELECT = 'input_select.timer_duration_preselect'
INPUT_SELECT_TIMER_DURATION_PRESELECT_DEFAULT_VALUE = 'Manual'
INPUT_SELECT_TIMER_DURATION_PRESELECT_LIVE = 'input_select.timer_duration_preselect_live'
INPUT_SELECT_TIMER_DURATION_PRESELECT_LIVE_DEFAULT_VALUE = 'Manual'
INPUT_SELECT_TIMER_DURATION_PRESELECT_LIVE_START = 'input_select.timer_duration_preselect_live_start'
INPUT_SELECT_TIMER_DURATION_PRESELECT_LIVE_STOP = 'input_select.timer_duration_preselect_live_stop'

class TimerDateTime(hass.Hass):
 
  def initialize(self): 
    self.listen_state(self.start_datetime_updated, INPUT_SELECT_START_DATETIME)
    self.listen_state(self.stop_datetime_updated, INPUT_SELECT_STOP_DATETIME)


  def start_datetime_updated (self, entity, attribute, old, new, kwargs):
    print ("*start_datetime_updated*")
    # timer_sync_state = self.get_state('input_boolean.timer_sync')
    self.set_state(INPUT_BOOLEAN_TIMER_SYNC, state='off')

    timer_start_datetime = self.get_state(INPUT_SELECT_START_DATETIME)
    timer_start_time = datetime.datetime.strptime(timer_start_datetime, "%Y-%m-%d %H:%M:%S")
    timer_start_hour = timer_start_time.hour
    timer_start_minute = timer_start_time.minute
    #! replace all when appd fixed # self.set_value(INPUT_NUMBER_TIMER_START_HOUR, timer_start_hour)
    self.call_service("input_number/set_value",entity_id=INPUT_NUMBER_TIMER_START_HOUR,value=(max(0, timer_start_hour)))
    self.call_service("input_number/set_value",entity_id=INPUT_NUMBER_TIMER_START_MINUTE,value=(max(0, timer_start_minute)))

    timer_stop_datetime = self.get_state(INPUT_SELECT_STOP_DATETIME)
    timer_stop_time = datetime.datetime.strptime(timer_stop_datetime, "%Y-%m-%d %H:%M:%S")

    if timer_stop_time > timer_start_time :
      timer_duration = relativedelta.relativedelta(timer_stop_time, timer_start_time)
      timer_duration_td = timer_stop_time - timer_start_time
      direction = "normal"
    else :
      timer_duration = relativedelta.relativedelta(timer_start_time, timer_stop_time)
      timer_duration_td = timer_start_time - timer_stop_time
      direction = "reverse"

    timer_duration_td_days = int(timer_duration_td.days)
    if (timer_duration_td_days >= 91) or (timer_duration_td_days < 0):
      timer_duration_td_days = 0
    timer_duration_td_weeks = int(timer_duration_td_days/7)
    if (timer_duration_td_weeks > 51) or (timer_duration_td_weeks < 0):
      timer_duration_td_weeks = 0

    self.call_service("input_number/set_value",entity_id=INPUT_NUMBER_TIMER_DURATION_YEARS,value=(timer_duration.years))
    self.call_service("input_number/set_value",entity_id=INPUT_NUMBER_TIMER_DURATION_MONTHS,value=(timer_duration.months))
    self.call_service("input_number/set_value",entity_id=INPUT_NUMBER_TIMER_DURATION_DAYS,value=(timer_duration.days))
    self.call_service("input_number/set_value",entity_id=INPUT_NUMBER_TIMER_DURATION_DAYS_TOTAL,value=(timer_duration_td_days))
    self.call_service("input_number/set_value",entity_id=INPUT_NUMBER_TIMER_DURATION_WEEKS_TOTAL,value=(timer_duration_td_weeks))
    self.call_service("input_number/set_value",entity_id=INPUT_NUMBER_TIMER_DURATION_HOURS,value=(timer_duration.hours))
    self.call_service("input_number/set_value",entity_id=INPUT_NUMBER_TIMER_DURATION_MINUTES,value=(timer_duration.minutes))
    # live_timer_duration = relativedelta.relativedelta(timer_stop_time, timer_start_time)

    preset_duration_timer_sync = self.get_state(INPUT_BOOLEAN_PRESET_DURATION_TIMER_SYNC)
    preset_live_duration_timer_sync = self.get_state(INPUT_BOOLEAN_PRESET_LIVE_DURATION_TIMER_SYNC)
    if ((preset_duration_timer_sync == "off") and (preset_live_duration_timer_sync == "off")) :
      print ("Either Sync ON : ")
      timer_duration_preselect = self.get_state(INPUT_SELECT_TIMER_DURATION_PRESELECT)
      timer_duration_preselect_live = self.get_state(INPUT_SELECT_TIMER_DURATION_PRESELECT_LIVE)
      timer_duration_preselect_live_start = self.get_state(INPUT_SELECT_TIMER_DURATION_PRESELECT_LIVE_START)
      if (timer_duration_preselect != INPUT_SELECT_TIMER_DURATION_PRESELECT_DEFAULT_VALUE) :
        self.select_option(INPUT_SELECT_TIMER_DURATION_PRESELECT, INPUT_SELECT_TIMER_DURATION_PRESELECT_DEFAULT_VALUE)
        print ("Either ON - D reset to 'Manual'")
      elif (timer_duration_preselect_live != INPUT_SELECT_TIMER_DURATION_PRESELECT_LIVE_DEFAULT_VALUE) or (timer_duration_preselect_live_start != INPUT_SELECT_TIMER_DURATION_PRESELECT_LIVE_DEFAULT_VALUE) :
        self.select_option(INPUT_SELECT_TIMER_DURATION_PRESELECT_LIVE, INPUT_SELECT_TIMER_DURATION_PRESELECT_LIVE_DEFAULT_VALUE)
        self.select_option(INPUT_SELECT_TIMER_DURATION_PRESELECT_LIVE_START, INPUT_SELECT_TIMER_DURATION_PRESELECT_LIVE_DEFAULT_VALUE)
        print ("Either ON - L reset  to 'Manual'")
    elif preset_duration_timer_sync == "on" : 
      print ("turn duration off")
      self.select_option(INPUT_SELECT_TIMER_DURATION_PRESELECT_LIVE, INPUT_SELECT_TIMER_DURATION_PRESELECT_LIVE_DEFAULT_VALUE)
      self.select_option(INPUT_SELECT_TIMER_DURATION_PRESELECT_LIVE_START, INPUT_SELECT_TIMER_DURATION_PRESELECT_LIVE_DEFAULT_VALUE)
      self.set_state(INPUT_BOOLEAN_PRESET_DURATION_TIMER_SYNC, state='off')
    elif preset_live_duration_timer_sync == "on" :
      print ("turn live off")
      self.select_option(INPUT_SELECT_TIMER_DURATION_PRESELECT, INPUT_SELECT_TIMER_DURATION_PRESELECT_DEFAULT_VALUE)

      timer_duration_preselect_live_start = self.get_state(INPUT_SELECT_TIMER_DURATION_PRESELECT_LIVE_START)
      current_datetime = datetime.datetime.now()
      timer_start_time = self.get_state(INPUT_SELECT_START_DATETIME)
      timer_start_time = datetime.datetime.strptime(timer_start_time, "%Y-%m-%d %H:%M:%S")
      timer_stop_time = self.get_state(INPUT_SELECT_STOP_DATETIME)
      timer_stop_time = datetime.datetime.strptime(timer_stop_time, "%Y-%m-%d %H:%M:%S")
      timer_start_duration_live_td = timer_start_time - current_datetime
      timer_stop_duration_live_td = timer_stop_time - current_datetime
      if timer_start_duration_live_td > datetime.timedelta() :
        if timer_stop_duration_live_td >  datetime.timedelta() :     
          if timer_start_duration_live_td < timer_stop_duration_live_td :
            timer_duration_live_infocus = 'start'
          else :
            timer_duration_live_infocus = 'stop'
        else :
          timer_duration_live_infocus = 'start'
      else :   
        if timer_stop_duration_live_td > datetime.timedelta() :
          timer_duration_live_infocus = 'stop'
        else :
          timer_duration_live_infocus = 'stop'

      live_duration_preset_stop = self.global_vars['live_duration_preset_stop']
      live_duration_preset_start = self.global_vars['live_duration_preset_start']
      if (live_duration_preset_stop == 'on') and (timer_duration_live_infocus == 'stop') :
        self.select_option(INPUT_SELECT_TIMER_DURATION_PRESELECT_LIVE, INPUT_SELECT_TIMER_DURATION_PRESELECT_LIVE_DEFAULT_VALUE)
        self.global_vars['live_duration_preset_stop'] = 'off'
      elif (live_duration_preset_start == 'on') and (timer_duration_live_infocus == 'start') :
        self.select_option(INPUT_SELECT_TIMER_DURATION_PRESELECT_LIVE, timer_duration_preselect_live_start)
        self.global_vars['live_duration_preset_start'] = 'off'

      self.set_state(INPUT_BOOLEAN_PRESET_LIVE_DURATION_TIMER_SYNC, state='off')

    self.set_state(INPUT_BOOLEAN_TIMER_SYNC, state='on')

    live_duration_app = self.get_app("live_duration")
    live_duration_app.live_duration(self, entity, *new, **kwargs)


  def stop_datetime_updated (self, entity, attribute, old, new, kwargs):
    print ("*stop_datetime_updated*")
    # timer_sync_state = self.get_state('input_boolean.timer_sync')
    self.set_state(INPUT_BOOLEAN_TIMER_SYNC, state='off')

    timer_stop_time = self.get_state(INPUT_SELECT_STOP_DATETIME)
    timer_stop_time = datetime.datetime.strptime(timer_stop_time, "%Y-%m-%d %H:%M:%S")
    timer_stop_hour = timer_stop_time.hour
    timer_stop_minute = timer_stop_time.minute
    #! replace all with self.set_value when fixed in appd ?
    self.call_service("input_number/set_value",entity_id=INPUT_NUMBER_TIMER_STOP_HOUR,value=(max(0, timer_stop_hour)))
    self.call_service("input_number/set_value",entity_id=INPUT_NUMBER_TIMER_STOP_MINUTE,value=(max(0, timer_stop_minute)))

    timer_start_datetime = self.get_state(INPUT_SELECT_START_DATETIME)
    timer_start_time = datetime.datetime.strptime(timer_start_datetime, "%Y-%m-%d %H:%M:%S")

    if timer_stop_time > timer_start_time :
      timer_duration = relativedelta.relativedelta(timer_stop_time, timer_start_time)
      timer_duration_td = timer_stop_time - timer_start_time
      direction = "normal"
    else :
      timer_duration = relativedelta.relativedelta(timer_start_time, timer_stop_time)
      timer_duration_td = timer_start_time - timer_stop_time
      direction = "reverse"

    timer_duration_td_days = int(timer_duration_td.days)
    if (timer_duration_td_days >= 91) or (timer_duration_td_days < 0):
      timer_duration_td_days = 0
    timer_duration_td_weeks = int((timer_duration_td.days)/7)
    if (timer_duration_td_weeks > 51) or (timer_duration_td_weeks < 0):
      timer_duration_td_weeks = 0

    self.call_service("input_number/set_value",entity_id=INPUT_NUMBER_TIMER_DURATION_YEARS,value=(timer_duration.years))
    self.call_service("input_number/set_value",entity_id=INPUT_NUMBER_TIMER_DURATION_MONTHS,value=(timer_duration.months))
    self.call_service("input_number/set_value",entity_id=INPUT_NUMBER_TIMER_DURATION_DAYS,value=(timer_duration.days))
    self.call_service("input_number/set_value",entity_id=INPUT_NUMBER_TIMER_DURATION_DAYS_TOTAL,value=(timer_duration_td_days))
    self.call_service("input_number/set_value",entity_id=INPUT_NUMBER_TIMER_DURATION_WEEKS_TOTAL,value=(timer_duration_td_weeks))
    self.call_service("input_number/set_value",entity_id=INPUT_NUMBER_TIMER_DURATION_HOURS,value=(timer_duration.hours))
    self.call_service("input_number/set_value",entity_id=INPUT_NUMBER_TIMER_DURATION_MINUTES,value=(timer_duration.minutes))

    preset_duration_timer_sync = self.get_state(INPUT_BOOLEAN_PRESET_DURATION_TIMER_SYNC)
    preset_live_duration_timer_sync = self.get_state(INPUT_BOOLEAN_PRESET_LIVE_DURATION_TIMER_SYNC)
    if ((preset_duration_timer_sync == "off") and (preset_live_duration_timer_sync == "off")) :
      # print ("Either Sync ON : ")
      timer_duration_preselect = self.get_state(INPUT_SELECT_TIMER_DURATION_PRESELECT)
      timer_duration_preselect_live = self.get_state(INPUT_SELECT_TIMER_DURATION_PRESELECT_LIVE)
      timer_duration_preselect_live_stop = self.get_state(INPUT_SELECT_TIMER_DURATION_PRESELECT_LIVE_STOP)
      if timer_duration_preselect != INPUT_SELECT_TIMER_DURATION_PRESELECT_DEFAULT_VALUE :
        self.select_option(INPUT_SELECT_TIMER_DURATION_PRESELECT, INPUT_SELECT_TIMER_DURATION_PRESELECT_DEFAULT_VALUE)
        # print ("Either ON - D reset to 'Manual'")
      elif timer_duration_preselect_live != INPUT_SELECT_TIMER_DURATION_PRESELECT_LIVE_DEFAULT_VALUE or (timer_duration_preselect_live_stop != INPUT_SELECT_TIMER_DURATION_PRESELECT_LIVE_DEFAULT_VALUE) :
        self.select_option(INPUT_SELECT_TIMER_DURATION_PRESELECT_LIVE, INPUT_SELECT_TIMER_DURATION_PRESELECT_LIVE_DEFAULT_VALUE)
        self.select_option(INPUT_SELECT_TIMER_DURATION_PRESELECT_LIVE_STOP, INPUT_SELECT_TIMER_DURATION_PRESELECT_LIVE_DEFAULT_VALUE)
        # print ("Either ON - L reset to 'Manual'")
    elif preset_duration_timer_sync == "on" :
      # print ("turn duration off")
      self.select_option(INPUT_SELECT_TIMER_DURATION_PRESELECT_LIVE, INPUT_SELECT_TIMER_DURATION_PRESELECT_LIVE_DEFAULT_VALUE)
      self.select_option(INPUT_SELECT_TIMER_DURATION_PRESELECT_LIVE_STOP, INPUT_SELECT_TIMER_DURATION_PRESELECT_LIVE_DEFAULT_VALUE)
      self.set_state(INPUT_BOOLEAN_PRESET_DURATION_TIMER_SYNC, state='off')
    elif preset_live_duration_timer_sync == "on" :
      # print ("turn live off")
      self.select_option(INPUT_SELECT_TIMER_DURATION_PRESELECT, INPUT_SELECT_TIMER_DURATION_PRESELECT_DEFAULT_VALUE)

      timer_duration_preselect_live_stop = self.get_state(INPUT_SELECT_TIMER_DURATION_PRESELECT_LIVE_STOP)
      current_datetime = datetime.datetime.now()
      timer_start_time = self.get_state(INPUT_SELECT_START_DATETIME)
      timer_start_time = datetime.datetime.strptime(timer_start_time, "%Y-%m-%d %H:%M:%S")
      timer_stop_time = self.get_state(INPUT_SELECT_STOP_DATETIME)
      timer_stop_time = datetime.datetime.strptime(timer_stop_time, "%Y-%m-%d %H:%M:%S")
      timer_start_duration_live_td = timer_start_time - current_datetime
      timer_stop_duration_live_td = timer_stop_time - current_datetime
      if timer_start_duration_live_td > datetime.timedelta() :
        if timer_stop_duration_live_td >  datetime.timedelta() :     
          if timer_start_duration_live_td < timer_stop_duration_live_td :
            timer_duration_live_infocus = 'start'
          else :
            timer_duration_live_infocus = 'stop'
        else :
          timer_duration_live_infocus = 'start'
      else :   
        if timer_stop_duration_live_td > datetime.timedelta() :
          timer_duration_live_infocus = 'stop'
        else :
          timer_duration_live_infocus = 'stop'

      live_duration_preset_stop = self.global_vars['live_duration_preset_stop']
      live_duration_preset_start = self.global_vars['live_duration_preset_start']
      if (live_duration_preset_stop == 'on') and (timer_duration_live_infocus == 'stop') :
        self.select_option(INPUT_SELECT_TIMER_DURATION_PRESELECT_LIVE, timer_duration_preselect_live_stop)
        self.global_vars['live_duration_preset_stop'] = 'off'
      elif (live_duration_preset_start == 'on') and (timer_duration_live_infocus == 'start') :
        self.select_option(INPUT_SELECT_TIMER_DURATION_PRESELECT_LIVE, INPUT_SELECT_TIMER_DURATION_PRESELECT_LIVE_DEFAULT_VALUE)
        self.global_vars['live_duration_preset_start'] = 'off'

      self.set_state(INPUT_BOOLEAN_PRESET_LIVE_DURATION_TIMER_SYNC, state='off')

    self.set_state(INPUT_BOOLEAN_TIMER_SYNC, state='on')

    live_duration_app = self.get_app("live_duration")
    live_duration_app.live_duration(self, entity, *new, **kwargs)
