import appdaemon.plugins.hass.hassapi as hass
import datetime
from dateutil import relativedelta

INPUT_DATETIME_START_DATETIME = 'input_datetime.start_datetime'
INPUT_DATETIME_STOP_DATETIME = 'input_datetime.stop_datetime'
INPUT_NUMBER_TIMER_DURATION_YEARS_LIVE = 'input_number.on_duration_years_live'
INPUT_NUMBER_TIMER_DURATION_MONTHS_LIVE = 'input_number.on_duration_months_live'
INPUT_NUMBER_TIMER_DURATION_DAYS_LIVE = 'input_number.on_duration_days_live'
INPUT_NUMBER_TIMER_DURATION_DAYS_LIVE_TOTAL = 'input_number.on_duration_days_live_total'
INPUT_NUMBER_TIMER_DURATION_WEEKS_LIVE_TOTAL = 'input_number.on_duration_weeks_live_total'
INPUT_NUMBER_TIMER_DURATION_HOURS_LIVE = 'input_number.on_duration_hours_live'
INPUT_NUMBER_TIMER_DURATION_MINUTES_LIVE = 'input_number.on_duration_minutes_live'

INPUT_NUMBER_TIMER_DURATION_YEARS_LIVE_START = 'input_number.on_duration_years_live_start'
INPUT_NUMBER_TIMER_DURATION_MONTHS_LIVE_START = 'input_number.on_duration_months_live_start'
INPUT_NUMBER_TIMER_DURATION_DAYS_LIVE_START = 'input_number.on_duration_days_live_start'
INPUT_NUMBER_TIMER_DURATION_DAYS_LIVE_TOTAL_START = 'input_number.on_duration_days_live_total_start'
INPUT_NUMBER_TIMER_DURATION_WEEKS_LIVE_TOTAL_START = 'input_number.on_duration_weeks_live_total_start'
INPUT_NUMBER_TIMER_DURATION_HOURS_LIVE_START = 'input_number.on_duration_hours_live_start'
INPUT_NUMBER_TIMER_DURATION_MINUTES_LIVE_START = 'input_number.on_duration_minutes_live_start'

INPUT_NUMBER_TIMER_DURATION_YEARS_LIVE_STOP = 'input_number.on_duration_years_live_stop'
INPUT_NUMBER_TIMER_DURATION_MONTHS_LIVE_STOP = 'input_number.on_duration_months_live_stop'
INPUT_NUMBER_TIMER_DURATION_DAYS_LIVE_STOP = 'input_number.on_duration_days_live_stop'
INPUT_NUMBER_TIMER_DURATION_DAYS_LIVE_TOTAL_STOP = 'input_number.on_duration_days_live_total_stop'
INPUT_NUMBER_TIMER_DURATION_WEEKS_LIVE_TOTAL_STOP = 'input_number.on_duration_weeks_live_total_stop'
INPUT_NUMBER_TIMER_DURATION_HOURS_LIVE_STOP = 'input_number.on_duration_hours_live_stop'
INPUT_NUMBER_TIMER_DURATION_MINUTES_LIVE_STOP = 'input_number.on_duration_minutes_live_stop'

INPUT_BOOLEAN_LIVE_TIMER_SYNC = 'input_boolean.live_timer_sync'

class LiveDuration(hass.Hass):

  def initialize(self):
    time_check_interval = datetime.time(0, 0, 0)
    self.run_minutely(self.live_duration, time_check_interval)
    # self.listen_state(self.live_duration, INPUT_DATETIME_START_DATETIME)
    # self.listen_state(self.live_duration, INPUT_DATETIME_STOP_DATETIME)

  def live_duration (self, entity, *new, **kwargs):
    print ("Live duration update")
    self.set_state(INPUT_BOOLEAN_LIVE_TIMER_SYNC, state='off')
    timer_start_time = self.get_state(INPUT_DATETIME_START_DATETIME)
    timer_start_time = datetime.datetime.strptime(timer_start_time, "%Y-%m-%d %H:%M:%S")
    timer_stop_time = self.get_state(INPUT_DATETIME_STOP_DATETIME)
    timer_stop_time = datetime.datetime.strptime(timer_stop_time, "%Y-%m-%d %H:%M:%S")
    current_datetime = datetime.datetime.now()
    current_datetime = current_datetime.replace(second=0, microsecond=0)
    # calc if start or stop is next timer ahead of current time and adjust sliders
    timer_start_duration_live_rd = relativedelta.relativedelta(timer_start_time, current_datetime)
    timer_start_duration_live_td = timer_start_time - current_datetime
    timer_stop_duration_live_rd = relativedelta.relativedelta(timer_stop_time, current_datetime)
    timer_stop_duration_live_td = timer_stop_time - current_datetime

    if timer_start_duration_live_td > datetime.timedelta() :
      if timer_stop_duration_live_td >  datetime.timedelta() :
        if timer_start_duration_live_td < timer_stop_duration_live_td :
          timer_duration_live_rd = timer_start_duration_live_rd
          timer_duration_live_td = timer_start_duration_live_td
        else :
          timer_duration_live_rd = timer_stop_duration_live_rd
          timer_duration_live_td = timer_stop_duration_live_td
      else :
        timer_duration_live_rd = timer_start_duration_live_rd
        timer_duration_live_td = timer_start_duration_live_td
    else :
      if timer_stop_duration_live_td > datetime.timedelta() :
        timer_duration_live_rd = timer_stop_duration_live_rd
        timer_duration_live_td = timer_stop_duration_live_td
      else :
        timer_duration_live_rd = relativedelta.relativedelta()
        timer_duration_live_td = datetime.timedelta()
    # print (timer_duration_live_rd, timer_duration_live_td)

    timer_duration_live_td_days = int(timer_duration_live_td.days)
    if (timer_duration_live_td_days >= 91) or (timer_duration_live_td_days < 0):
      timer_duration_live_td_days = 0

    timer_duration_live_td_weeks = int((timer_duration_live_td.days)/7)
    if (timer_duration_live_td_weeks > 51) or (timer_duration_live_td_weeks < 0):
      timer_duration_live_td_weeks = 0

    self.call_service("input_number/set_value",entity_id=INPUT_NUMBER_TIMER_DURATION_YEARS_LIVE,value=(max(0, timer_duration_live_rd.years)))
    self.call_service("input_number/set_value",entity_id=INPUT_NUMBER_TIMER_DURATION_MONTHS_LIVE,value=(max(0, timer_duration_live_rd.months)))
    self.call_service("input_number/set_value",entity_id=INPUT_NUMBER_TIMER_DURATION_DAYS_LIVE,value=(max(0, timer_duration_live_rd.days)))
    self.call_service("input_number/set_value",entity_id=INPUT_NUMBER_TIMER_DURATION_DAYS_LIVE_TOTAL,value=(timer_duration_live_td_days))
    self.call_service("input_number/set_value",entity_id=INPUT_NUMBER_TIMER_DURATION_WEEKS_LIVE_TOTAL,value=(timer_duration_live_td_weeks))
    self.call_service("input_number/set_value",entity_id=INPUT_NUMBER_TIMER_DURATION_HOURS_LIVE,value=(max(0,timer_duration_live_rd.hours)))
    self.call_service("input_number/set_value",entity_id=INPUT_NUMBER_TIMER_DURATION_MINUTES_LIVE,value=(max(0, timer_duration_live_rd.minutes)))

    timer_duration_live_td_days_start = int(timer_start_duration_live_td.days)
    if (timer_duration_live_td_days_start >= 91) or (timer_duration_live_td_days_start < 0):
      timer_duration_live_td_days_start = 0

    timer_duration_live_td_weeks_start = int((timer_start_duration_live_td.days)/7)
    if (timer_duration_live_td_weeks_start > 51) or (timer_duration_live_td_weeks_start < 0):
      timer_duration_live_td_weeks_start = 0

    self.call_service("input_number/set_value",entity_id=INPUT_NUMBER_TIMER_DURATION_YEARS_LIVE_START,value=(max(0, timer_start_duration_live_rd.years)))
    self.call_service("input_number/set_value",entity_id=INPUT_NUMBER_TIMER_DURATION_MONTHS_LIVE_START,value=(max(0, timer_start_duration_live_rd.months)))
    self.call_service("input_number/set_value",entity_id=INPUT_NUMBER_TIMER_DURATION_DAYS_LIVE_START,value=(max(0, timer_start_duration_live_rd.days)))
    self.call_service("input_number/set_value",entity_id=INPUT_NUMBER_TIMER_DURATION_DAYS_LIVE_TOTAL_START,value=(timer_duration_live_td_days_start))
    self.call_service("input_number/set_value",entity_id=INPUT_NUMBER_TIMER_DURATION_WEEKS_LIVE_TOTAL_START,value=(timer_duration_live_td_weeks_start))
    self.call_service("input_number/set_value",entity_id=INPUT_NUMBER_TIMER_DURATION_HOURS_LIVE_START,value=(max(0,timer_start_duration_live_rd.hours)))
    self.call_service("input_number/set_value",entity_id=INPUT_NUMBER_TIMER_DURATION_MINUTES_LIVE_START,value=(max(0,timer_start_duration_live_rd.minutes)))

    timer_duration_live_td_days_stop = int(timer_stop_duration_live_td.days)
    if (timer_duration_live_td_days_stop >= 91) or (timer_duration_live_td_days_stop < 0):
      timer_duration_live_td_days_stop = 0

    timer_duration_live_td_weeks_stop = int((timer_stop_duration_live_td.days)/7)
    if (timer_duration_live_td_weeks_stop > 51) or (timer_duration_live_td_weeks_stop < 0):
      timer_duration_live_td_weeks_stop = 0

    self.call_service("input_number/set_value",entity_id=INPUT_NUMBER_TIMER_DURATION_YEARS_LIVE_STOP,value=(max(0, timer_stop_duration_live_rd.years)))
    self.call_service("input_number/set_value",entity_id=INPUT_NUMBER_TIMER_DURATION_MONTHS_LIVE_STOP,value=(max(0, timer_stop_duration_live_rd.months)))
    self.call_service("input_number/set_value",entity_id=INPUT_NUMBER_TIMER_DURATION_DAYS_LIVE_STOP,value=(max(0, timer_stop_duration_live_rd.days)))
    self.call_service("input_number/set_value",entity_id=INPUT_NUMBER_TIMER_DURATION_DAYS_LIVE_TOTAL_STOP,value=(timer_duration_live_td_days_stop))
    self.call_service("input_number/set_value",entity_id=INPUT_NUMBER_TIMER_DURATION_WEEKS_LIVE_TOTAL_STOP,value=(timer_duration_live_td_weeks_stop))
    self.call_service("input_number/set_value",entity_id=INPUT_NUMBER_TIMER_DURATION_HOURS_LIVE_STOP,value=(max(0, timer_stop_duration_live_rd.hours)))
    self.call_service("input_number/set_value",entity_id=INPUT_NUMBER_TIMER_DURATION_MINUTES_LIVE_STOP,value=(max(0, timer_stop_duration_live_rd.minutes)))

    print ("[ Live duration update @", current_datetime, "]")

    self.set_state(INPUT_BOOLEAN_LIVE_TIMER_SYNC, state='on')