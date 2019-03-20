import appdaemon.plugins.hass.hassapi as hass
import datetime
from dateutil.relativedelta import relativedelta

INPUT_DATETIME_START_DATETIME = 'input_datetime.start_datetime'
INPUT_DATETIME_STOP_DATETIME = 'input_datetime.stop_datetime'
INPUT_NUMBER_LIVE_TIMER_DURATION_YEARS = 'input_number.on_duration_years_live'
INPUT_NUMBER_LIVE_TIMER_DURATION_MONTHS = 'input_number.on_duration_months_live'
INPUT_NUMBER_LIVE_TIMER_DURATION_DAYS = 'input_number.on_duration_days_live'
INPUT_NUMBER_LIVE_TIMER_DURATION_DAYS_TOTAL = 'input_number.on_duration_days_live_total'
INPUT_NUMBER_LIVE_TIMER_DURATION_WEEKS_TOTAL = 'input_number.on_duration_weeks_live_total'
INPUT_NUMBER_LIVE_TIMER_DURATION_HOURS = 'input_number.on_duration_hours_live'
INPUT_NUMBER_LIVE_TIMER_DURATION_MINUTES = 'input_number.on_duration_minutes_live'
INPUT_SELECT_TIMER_DURATION_PRESELECT_LIVE = 'input_select.timer_duration_preselect_live'

INPUT_BOOLEAN_PRESET_LIVE_DURATION_TIMER_SYNC = 'input_boolean.preset_live_duration_timer_sync'

INPUT_NUMBER_LIVE_TIMER_DURATION_YEARS_START = 'input_number.on_duration_years_live_start'
INPUT_NUMBER_LIVE_TIMER_DURATION_MONTHS_START = 'input_number.on_duration_months_live_start'
INPUT_NUMBER_LIVE_TIMER_DURATION_DAYS_START = 'input_number.on_duration_days_live_start'
INPUT_NUMBER_LIVE_TIMER_DURATION_DAYS_TOTAL_START = 'input_number.on_duration_days_live_total_start'
INPUT_NUMBER_LIVE_TIMER_DURATION_WEEKS_TOTAL_START = 'input_number.on_duration_weeks_live_total_start'
INPUT_NUMBER_LIVE_TIMER_DURATION_HOURS_START = 'input_number.on_duration_hours_live_start'
INPUT_NUMBER_LIVE_TIMER_DURATION_MINUTES_START = 'input_number.on_duration_minutes_live_start'
INPUT_SELECT_TIMER_DURATION_PRESELECT_LIVE_START = 'input_select.timer_duration_preselect_live_start'

INPUT_NUMBER_LIVE_TIMER_DURATION_YEARS_STOP = 'input_number.on_duration_years_live_stop'
INPUT_NUMBER_LIVE_TIMER_DURATION_MONTHS_STOP = 'input_number.on_duration_months_live_stop'
INPUT_NUMBER_LIVE_TIMER_DURATION_DAYS_STOP = 'input_number.on_duration_days_live_stop'
INPUT_NUMBER_LIVE_TIMER_DURATION_DAYS_TOTAL_STOP = 'input_number.on_duration_days_live_total_stop'
INPUT_NUMBER_LIVE_TIMER_DURATION_WEEKS_TOTAL_STOP = 'input_number.on_duration_weeks_live_total_stop'
INPUT_NUMBER_LIVE_TIMER_DURATION_HOURS_STOP = 'input_number.on_duration_hours_live_stop'
INPUT_NUMBER_LIVE_TIMER_DURATION_MINUTES_STOP = 'input_number.on_duration_minutes_live_stop'
INPUT_SELECT_TIMER_DURATION_PRESELECT_LIVE_STOP = 'input_select.timer_duration_preselect_live_stop'


class LiveDurationSliders(hass.Hass):

  def initialize(self): 
    self.listen_state(self.live_duration_time_slider_updated, INPUT_NUMBER_LIVE_TIMER_DURATION_YEARS)
    self.listen_state(self.live_duration_time_slider_updated, INPUT_NUMBER_LIVE_TIMER_DURATION_MONTHS)
    self.listen_state(self.live_duration_time_slider_updated, INPUT_NUMBER_LIVE_TIMER_DURATION_DAYS)
    self.listen_state(self.live_duration_time_slider_updated_td_days_total, INPUT_NUMBER_LIVE_TIMER_DURATION_DAYS_TOTAL)
    self.listen_state(self.live_duration_time_slider_updated_td_weeks_total, INPUT_NUMBER_LIVE_TIMER_DURATION_WEEKS_TOTAL)
    self.listen_state(self.live_duration_time_slider_updated, INPUT_NUMBER_LIVE_TIMER_DURATION_HOURS)
    self.listen_state(self.live_duration_time_slider_updated, INPUT_NUMBER_LIVE_TIMER_DURATION_MINUTES)
    self.listen_state(self.duration_preselect_live_updated, INPUT_SELECT_TIMER_DURATION_PRESELECT_LIVE)

    self.listen_state(self.live_duration_time_slider_updated_start, INPUT_NUMBER_LIVE_TIMER_DURATION_YEARS_START)
    self.listen_state(self.live_duration_time_slider_updated_start, INPUT_NUMBER_LIVE_TIMER_DURATION_MONTHS_START)
    self.listen_state(self.live_duration_time_slider_updated_start, INPUT_NUMBER_LIVE_TIMER_DURATION_DAYS_START)
    self.listen_state(self.live_duration_time_slider_updated_td_days_total_start, INPUT_NUMBER_LIVE_TIMER_DURATION_DAYS_TOTAL_START)
    self.listen_state(self.live_duration_time_slider_updated_td_weeks_total_start, INPUT_NUMBER_LIVE_TIMER_DURATION_WEEKS_TOTAL_START)
    self.listen_state(self.live_duration_time_slider_updated_start, INPUT_NUMBER_LIVE_TIMER_DURATION_HOURS_START)
    self.listen_state(self.live_duration_time_slider_updated_start, INPUT_NUMBER_LIVE_TIMER_DURATION_MINUTES_START)
    self.listen_state(self.duration_preselect_live_updated_start, INPUT_SELECT_TIMER_DURATION_PRESELECT_LIVE_START)

    self.listen_state(self.live_duration_time_slider_updated_stop, INPUT_NUMBER_LIVE_TIMER_DURATION_YEARS_STOP)
    self.listen_state(self.live_duration_time_slider_updated_stop, INPUT_NUMBER_LIVE_TIMER_DURATION_MONTHS_STOP)
    self.listen_state(self.live_duration_time_slider_updated_stop, INPUT_NUMBER_LIVE_TIMER_DURATION_DAYS_STOP)
    self.listen_state(self.live_duration_time_slider_updated_td_days_total_stop, INPUT_NUMBER_LIVE_TIMER_DURATION_DAYS_TOTAL_STOP)
    self.listen_state(self.live_duration_time_slider_updated_td_weeks_total_stop, INPUT_NUMBER_LIVE_TIMER_DURATION_WEEKS_TOTAL_STOP)
    self.listen_state(self.live_duration_time_slider_updated_stop, INPUT_NUMBER_LIVE_TIMER_DURATION_HOURS_STOP)
    self.listen_state(self.live_duration_time_slider_updated_stop, INPUT_NUMBER_LIVE_TIMER_DURATION_MINUTES_STOP)
    self.listen_state(self.duration_preselect_live_updated_stop, INPUT_SELECT_TIMER_DURATION_PRESELECT_LIVE_STOP)


  def live_duration_time_slider_updated (self, entity, attribute, old, new, kwargs):
    print ("*live_duration_time_slider_updated*")
    # self.select_option(INPUT_SELECT_TIMER_DURATION_PRESELECT_LIVE, INPUT_SELECT_TIMER_DURATION_PRESELECT_LIVE_DEFAULT_VALUE)
    current_datetime = datetime.datetime.now()
    timer_live_duration_slider_years = self.get_state(INPUT_NUMBER_LIVE_TIMER_DURATION_YEARS)
    timer_live_duration_slider_months = self.get_state(INPUT_NUMBER_LIVE_TIMER_DURATION_MONTHS)
    timer_live_duration_slider_days = self.get_state(INPUT_NUMBER_LIVE_TIMER_DURATION_DAYS)
    timer_live_duration_slider_hours = self.get_state(INPUT_NUMBER_LIVE_TIMER_DURATION_HOURS)
    timer_live_duration_slider_minutes = self.get_state(INPUT_NUMBER_LIVE_TIMER_DURATION_MINUTES)
    # timer_start_datetime = datetime.datetime.strptime(timer_start_datetime, "%Y-%m-%d %H:%M:%S")
    timer_start_time = self.get_state(INPUT_DATETIME_START_DATETIME)
    timer_start_time = datetime.datetime.strptime(timer_start_time, "%Y-%m-%d %H:%M:%S")
    timer_stop_time = self.get_state(INPUT_DATETIME_STOP_DATETIME)
    timer_stop_time = datetime.datetime.strptime(timer_stop_time, "%Y-%m-%d %H:%M:%S")
    # calc if start or stop is next timer ahead of current time to determine which is to be adusted
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

    if timer_duration_live_infocus != 'start' :
      timer_stop_datetime =  current_datetime + relativedelta(years=+int(float(timer_live_duration_slider_years)) , months=+int(float(timer_live_duration_slider_months)), days=+int(float(timer_live_duration_slider_days)), hours=+int(float(timer_live_duration_slider_hours)), minutes=+int(float(timer_live_duration_slider_minutes)))
      timer_stop_time =  timer_stop_datetime.strftime('%H:%M')
      timer_stop_date =  timer_stop_datetime.strftime('%Y-%m-%d')
      self.call_service("input_datetime/set_datetime", entity_id = INPUT_DATETIME_STOP_DATETIME, date=timer_stop_date , time=timer_stop_time)
    else :
      timer_start_datetime =  current_datetime + relativedelta(years=+int(float(timer_live_duration_slider_years)) , months=+int(float(timer_live_duration_slider_months)), days=+int(float(timer_live_duration_slider_days)), hours=+int(float(timer_live_duration_slider_hours)), minutes=+int(float(timer_live_duration_slider_minutes)))
      timer_start_time =  timer_start_datetime.strftime('%H:%M')
      timer_start_date =  timer_start_datetime.strftime('%Y-%m-%d')
      self.call_service("input_datetime/set_datetime", entity_id = INPUT_DATETIME_START_DATETIME, date=timer_start_date , time=timer_start_time)


  def live_duration_time_slider_updated_td_days_total (self, entity, attribute, old, new, kwargs):
    print ("*live_duration_time_slider_updated_td_days_total*")
    # self.select_option(INPUT_SELECT_TIMER_DURATION_PRESELECT_LIVE, INPUT_SELECT_TIMER_DURATION_PRESELECT_LIVE_DEFAULT_VALUE)
    current_datetime = datetime.datetime.now()
    timer_live_duration_slider_days_total = self.get_state(INPUT_NUMBER_LIVE_TIMER_DURATION_DAYS_TOTAL)
    timer_start_time = self.get_state(INPUT_DATETIME_START_DATETIME)
    timer_start_time = datetime.datetime.strptime(timer_start_time, "%Y-%m-%d %H:%M:%S")
    timer_stop_time = self.get_state(INPUT_DATETIME_STOP_DATETIME)
    timer_stop_time = datetime.datetime.strptime(timer_stop_time, "%Y-%m-%d %H:%M:%S")
    # calc if start or stop is next timer ahead of current time to determine which is to be adusted
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

    if timer_duration_live_infocus != 'start' :
      timer_stop_datetime =  current_datetime + relativedelta(days=+int(float(timer_live_duration_slider_days_total)))
      # print (current_datetime)
      # print (timer_stop_datetime)
      timer_stop_time =  timer_stop_datetime.strftime('%H:%M')
      timer_stop_date =  timer_stop_datetime.strftime('%Y-%m-%d')
      self.call_service("input_datetime/set_datetime", entity_id = INPUT_DATETIME_STOP_DATETIME, date=timer_stop_date , time=timer_stop_time)
    else :
      timer_start_datetime =  current_datetime + relativedelta(days=+int(float(timer_live_duration_slider_days_total)))
      # print (current_datetime)
      # print (timer_stop_datetime)
      timer_start_time =  timer_start_datetime.strftime('%H:%M')
      timer_start_date =  timer_start_datetime.strftime('%Y-%m-%d')
      self.call_service("input_datetime/set_datetime", entity_id = INPUT_DATETIME_START_DATETIME, date=timer_start_date , time=timer_start_time)


  def live_duration_time_slider_updated_td_weeks_total (self, entity, attribute, old, new, kwargs):
    print ("*live_duration_time_slider_updated_td_weeks_total*")
    # self.select_option(INPUT_SELECT_TIMER_DURATION_PRESELECT_LIVE, INPUT_SELECT_TIMER_DURATION_PRESELECT_LIVE_DEFAULT_VALUE)
    current_datetime = datetime.datetime.now()
    timer_live_duration_slider_weeks_total = self.get_state(INPUT_NUMBER_LIVE_TIMER_DURATION_WEEKS_TOTAL)
    timer_start_time = self.get_state(INPUT_DATETIME_START_DATETIME)
    timer_start_time = datetime.datetime.strptime(timer_start_time, "%Y-%m-%d %H:%M:%S")
    timer_stop_time = self.get_state(INPUT_DATETIME_STOP_DATETIME)
    timer_stop_time = datetime.datetime.strptime(timer_stop_time, "%Y-%m-%d %H:%M:%S")
    # calc if start or stop is next timer ahead of current time to determine which is to be adusted
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

    if timer_duration_live_infocus != 'start' :
      timer_stop_datetime =  current_datetime + relativedelta(weeks=+int(float(timer_live_duration_slider_weeks_total)))
      # print (current_datetime)
      # print (timer_stop_datetime)
      timer_stop_time =  timer_stop_datetime.strftime('%H:%M')
      timer_stop_date =  timer_stop_datetime.strftime('%Y-%m-%d')
      self.call_service("input_datetime/set_datetime", entity_id = INPUT_DATETIME_STOP_DATETIME, date=timer_stop_date , time=timer_stop_time)
    else :
      timer_start_datetime =  current_datetime + relativedelta(weeks=+int(float(timer_live_duration_slider_weeks_total)))
      # print (current_datetime)
      # print (timer_stop_datetime)
      timer_start_time =  timer_start_datetime.strftime('%H:%M')
      timer_start_date =  timer_start_datetime.strftime('%Y-%m-%d')
      self.call_service("input_datetime/set_datetime", entity_id = INPUT_DATETIME_START_DATETIME, date=timer_start_date , time=timer_start_time)


  def duration_preselect_live_updated (self, entity, attribute, old, new, kwargs):
    print ('*live_duration_preselect_updated*')
    current_datetime = datetime.datetime.now()
    # current_datetime = current_datetime.replace(second=0, microsecond=0)
    timer_start_datetime = current_datetime
    timer_duration_preset_live = self.get_state(INPUT_SELECT_TIMER_DURATION_PRESELECT_LIVE)
    timer_start_time = self.get_state(INPUT_DATETIME_START_DATETIME)
    timer_start_time = datetime.datetime.strptime(timer_start_time, "%Y-%m-%d %H:%M:%S")
    timer_stop_time = self.get_state(INPUT_DATETIME_STOP_DATETIME)
    timer_stop_time = datetime.datetime.strptime(timer_stop_time, "%Y-%m-%d %H:%M:%S")
    # calc if start or stop is next timer ahead of current time to determine which is to be adusted
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

    if timer_duration_live_infocus != 'start' :
      if timer_duration_preset_live == "Manual":
        return
      elif timer_duration_preset_live == "15 min":
        timer_stop_datetime = current_datetime + relativedelta(minutes=+15)
        self.select_option(INPUT_SELECT_TIMER_DURATION_PRESELECT_LIVE_STOP, "15 min")
      elif timer_duration_preset_live == "30 min":
        timer_stop_datetime = current_datetime + relativedelta(minutes=+30)
        self.select_option(INPUT_SELECT_TIMER_DURATION_PRESELECT_LIVE_STOP, "30 min")
      elif timer_duration_preset_live == "45 min":
        timer_stop_datetime = current_datetime + relativedelta(minutes=+45)
        self.select_option(INPUT_SELECT_TIMER_DURATION_PRESELECT_LIVE_STOP, "45 min")
      elif timer_duration_preset_live == "1 hour":
        timer_stop_datetime = current_datetime + relativedelta(hours=+1)
        self.select_option(INPUT_SELECT_TIMER_DURATION_PRESELECT_LIVE_STOP, "1 hour")
      elif timer_duration_preset_live == "2 hours":
        timer_stop_datetime = current_datetime + relativedelta(hours=+2)
        self.select_option(INPUT_SELECT_TIMER_DURATION_PRESELECT_LIVE_STOP, "2 hours")
      elif timer_duration_preset_live == "1 day":
        timer_stop_datetime = current_datetime + relativedelta(days=+1)
        self.select_option(INPUT_SELECT_TIMER_DURATION_PRESELECT_LIVE_STOP, "1 day")
      elif timer_duration_preset_live == "1 week":
        timer_stop_datetime = current_datetime + relativedelta(weeks=+1)
        self.select_option(INPUT_SELECT_TIMER_DURATION_PRESELECT_LIVE_STOP, "1 week")
      self.set_state(INPUT_BOOLEAN_PRESET_LIVE_DURATION_TIMER_SYNC, state='on')
      print ('*live duration sync turned ON*')
      timer_stop_time =  timer_stop_datetime.strftime('%H:%M')
      timer_stop_date =  timer_stop_datetime.strftime('%Y-%m-%d')
      self.call_service("input_datetime/set_datetime", entity_id = INPUT_DATETIME_STOP_DATETIME, date=timer_stop_date , time=timer_stop_time)
    else :
      if timer_duration_preset_live == "Manual":
        return
      elif timer_duration_preset_live == "15 min":
        timer_start_datetime = timer_start_datetime + relativedelta(minutes=+15)
        self.select_option(INPUT_SELECT_TIMER_DURATION_PRESELECT_LIVE_START, "15 min")
      elif timer_duration_preset_live == "30 min":
        timer_start_datetime = timer_start_datetime + relativedelta(minutes=+30)
        self.select_option(INPUT_SELECT_TIMER_DURATION_PRESELECT_LIVE_START, "30 min")
      elif timer_duration_preset_live == "45 min":
        timer_start_datetime = timer_start_datetime + relativedelta(minutes=+45)
        self.select_option(INPUT_SELECT_TIMER_DURATION_PRESELECT_LIVE_START, "45 min")
      elif timer_duration_preset_live == "1 hour":
        timer_start_datetime = timer_start_datetime + relativedelta(hours=+1)
        self.select_option(INPUT_SELECT_TIMER_DURATION_PRESELECT_LIVE_START, "1 hour")
      elif timer_duration_preset_live == "2 hours":
        timer_start_datetime = timer_start_datetime + relativedelta(hours=+2)
        self.select_option(INPUT_SELECT_TIMER_DURATION_PRESELECT_LIVE_START, "2 hours")
      elif timer_duration_preset_live == "1 day":
        timer_start_datetime = timer_start_datetime + relativedelta(days=+1)
        self.select_option(INPUT_SELECT_TIMER_DURATION_PRESELECT_LIVE_START, "1 day")
      elif timer_duration_preset_live == "1 week":
        timer_start_datetime = timer_start_datetime + relativedelta(weeks=+1)
        self.select_option(INPUT_SELECT_TIMER_DURATION_PRESELECT_LIVE_START, "1 week")
      self.set_state(INPUT_BOOLEAN_PRESET_LIVE_DURATION_TIMER_SYNC, state='on')
      print ('*live duration sync turned ON*')
      timer_start_time =  timer_start_datetime.strftime('%H:%M')
      timer_start_date =  timer_start_datetime.strftime('%Y-%m-%d')
      self.call_service("input_datetime/set_datetime", entity_id = INPUT_DATETIME_START_DATETIME, date=timer_start_date , time=timer_start_time)



# Live Duration Slider Start
  def live_duration_time_slider_updated_start (self, entity, attribute, old, new, kwargs):
    print ("*live_duration_time_slider_updated_start*")
    # self.select_option(INPUT_SELECT_TIMER_DURATION_PRESELECT_LIVE, INPUT_SELECT_TIMER_DURATION_PRESELECT_LIVE_DEFAULT_VALUE)
    current_datetime = datetime.datetime.now()
    timer_live_duration_slider_years_start = self.get_state(INPUT_NUMBER_LIVE_TIMER_DURATION_YEARS_START)
    timer_live_duration_slider_months_start = self.get_state(INPUT_NUMBER_LIVE_TIMER_DURATION_MONTHS_START)
    timer_live_duration_slider_days_start = self.get_state(INPUT_NUMBER_LIVE_TIMER_DURATION_DAYS_START)
    timer_live_duration_slider_hours_start = self.get_state(INPUT_NUMBER_LIVE_TIMER_DURATION_HOURS_START)
    timer_live_duration_slider_minutes_start = self.get_state(INPUT_NUMBER_LIVE_TIMER_DURATION_MINUTES_START)
    timer_start_datetime =  current_datetime + relativedelta(years=+int(float(timer_live_duration_slider_years_start)) , months=+int(float(timer_live_duration_slider_months_start)), days=+int(float(timer_live_duration_slider_days_start)), hours=+int(float(timer_live_duration_slider_hours_start)), minutes=+int(float(timer_live_duration_slider_minutes_start)))
    timer_start_time =  timer_start_datetime.strftime('%H:%M')
    timer_start_date =  timer_start_datetime.strftime('%Y-%m-%d')
    self.call_service("input_datetime/set_datetime", entity_id = INPUT_DATETIME_START_DATETIME, date=timer_start_date , time=timer_start_time)

# Live Duration Slider Stop
  def live_duration_time_slider_updated_stop (self, entity, attribute, old, new, kwargs):
    print ("*live_duration_time_slider_updated_stop*")
    # self.select_option(INPUT_SELECT_TIMER_DURATION_PRESELECT_LIVE, INPUT_SELECT_TIMER_DURATION_PRESELECT_LIVE_DEFAULT_VALUE)
    current_datetime = datetime.datetime.now()
    timer_live_duration_slider_years_stop = self.get_state(INPUT_NUMBER_LIVE_TIMER_DURATION_YEARS_STOP)
    timer_live_duration_slider_months_stop = self.get_state(INPUT_NUMBER_LIVE_TIMER_DURATION_MONTHS_STOP)
    timer_live_duration_slider_days_stop = self.get_state(INPUT_NUMBER_LIVE_TIMER_DURATION_DAYS_STOP)
    timer_live_duration_slider_hours_stop = self.get_state(INPUT_NUMBER_LIVE_TIMER_DURATION_HOURS_STOP)
    timer_live_duration_slider_minutes_stop = self.get_state(INPUT_NUMBER_LIVE_TIMER_DURATION_MINUTES_STOP)
    timer_stop_datetime =  current_datetime + relativedelta(years=+int(float(timer_live_duration_slider_years_stop)) , months=+int(float(timer_live_duration_slider_months_stop)), days=+int(float(timer_live_duration_slider_days_stop)), hours=+int(float(timer_live_duration_slider_hours_stop)), minutes=+int(float(timer_live_duration_slider_minutes_stop)))
    timer_stop_time =  timer_stop_datetime.strftime('%H:%M')
    timer_stop_date =  timer_stop_datetime.strftime('%Y-%m-%d')
    self.call_service("input_datetime/set_datetime", entity_id = INPUT_DATETIME_STOP_DATETIME, date=timer_stop_date , time=timer_stop_time)


  def live_duration_time_slider_updated_td_days_total_start (self, entity, attribute, old, new, kwargs):
    print ("*live_duration_time_slider_updated_td_days_total_start*")
    # self.select_option(INPUT_SELECT_TIMER_DURATION_PRESELECT_LIVE, INPUT_SELECT_TIMER_DURATION_PRESELECT_LIVE_DEFAULT_VALUE)
    current_datetime = datetime.datetime.now()
    timer_live_duration_slider_days_total_start = self.get_state(INPUT_NUMBER_LIVE_TIMER_DURATION_DAYS_TOTAL_START)
    timer_start_datetime =  current_datetime + relativedelta(days=+int(float(timer_live_duration_slider_days_total_start)))
    # print (current_datetime)
    # print (timer_stop_datetime)
    timer_start_time =  timer_start_datetime.strftime('%H:%M')
    timer_start_date =  timer_start_datetime.strftime('%Y-%m-%d')
    self.call_service("input_datetime/set_datetime", entity_id = INPUT_DATETIME_START_DATETIME, date=timer_start_date , time=timer_start_time)

  def live_duration_time_slider_updated_td_days_total_stop (self, entity, attribute, old, new, kwargs):
    print ("*live_duration_time_slider_updated_td_days_total_stop*")
    current_datetime = datetime.datetime.now()
    timer_live_duration_slider_days_total_stop = self.get_state(INPUT_NUMBER_LIVE_TIMER_DURATION_DAYS_TOTAL_STOP)
    timer_stop_datetime =  current_datetime + relativedelta(days=+int(float(timer_live_duration_slider_days_total_stop)))
    timer_stop_time =  timer_stop_datetime.strftime('%H:%M')
    timer_stop_date =  timer_stop_datetime.strftime('%Y-%m-%d')
    self.call_service("input_datetime/set_datetime", entity_id = INPUT_DATETIME_STOP_DATETIME, date=timer_stop_date , time=timer_stop_time)

  def live_duration_time_slider_updated_td_weeks_total_start (self, entity, attribute, old, new, kwargs):
    print ("*live_duration_time_slider_updated_td_weeks_total_start*")
    # self.select_option(INPUT_SELECT_TIMER_DURATION_PRESELECT_LIVE, INPUT_SELECT_TIMER_DURATION_PRESELECT_LIVE_DEFAULT_VALUE)
    current_datetime = datetime.datetime.now()
    timer_live_duration_slider_weeks_total_start = self.get_state(INPUT_NUMBER_LIVE_TIMER_DURATION_WEEKS_TOTAL_START)
    timer_start_datetime =  current_datetime + relativedelta(weeks=+int(float(timer_live_duration_slider_weeks_total_start)))
    # print (current_datetime)
    # print (timer_stop_datetime)
    timer_start_time =  timer_start_datetime.strftime('%H:%M')
    timer_start_date =  timer_start_datetime.strftime('%Y-%m-%d')
    self.call_service("input_datetime/set_datetime", entity_id = INPUT_DATETIME_START_DATETIME, date=timer_start_date , time=timer_start_time)

  def live_duration_time_slider_updated_td_weeks_total_stop (self, entity, attribute, old, new, kwargs):
    print ("*live_duration_time_slider_updated_td_weeks_total_stop*")
    current_datetime = datetime.datetime.now()
    timer_live_duration_slider_weeks_total_stop = self.get_state(INPUT_NUMBER_LIVE_TIMER_DURATION_WEEKS_TOTAL_STOP)
    timer_stop_datetime =  current_datetime + relativedelta(weeks=+int(float(timer_live_duration_slider_weeks_total_stop)))
    timer_stop_time =  timer_stop_datetime.strftime('%H:%M')
    timer_stop_date =  timer_stop_datetime.strftime('%Y-%m-%d')
    self.call_service("input_datetime/set_datetime", entity_id = INPUT_DATETIME_STOP_DATETIME, date=timer_stop_date , time=timer_stop_time)

  def duration_preselect_live_updated_start (self, entity, attribute, old, new, kwargs):
    print ('*live_duration_preselect_updated_start*')
    current_datetime = datetime.datetime.now()
    timer_duration_preset_live_start = self.get_state(INPUT_SELECT_TIMER_DURATION_PRESELECT_LIVE_START)
    if timer_duration_preset_live_start == "Manual":
      return
    elif timer_duration_preset_live_start == "15 min":
      timer_start_datetime = current_datetime + relativedelta(minutes=+15)
    elif timer_duration_preset_live_start == "30 min":
      timer_start_datetime = current_datetime + relativedelta(minutes=+30)
    elif timer_duration_preset_live_start == "45 min":
      timer_start_datetime = current_datetime + relativedelta(minutes=+45)
    elif timer_duration_preset_live_start == "1 hour":
      timer_start_datetime = current_datetime + relativedelta(hours=+1)
    elif timer_duration_preset_live_start == "2 hours":
      timer_start_datetime = current_datetime + relativedelta(hours=+2)
    elif timer_duration_preset_live_start == "1 day":
      timer_start_datetime = current_datetime + relativedelta(days=+1)
    elif timer_duration_preset_live_start == "1 week":
      timer_start_datetime = current_datetime + relativedelta(weeks=+1)
    
    self.set_state(INPUT_BOOLEAN_PRESET_LIVE_DURATION_TIMER_SYNC, state='on')
    self.global_vars['live_duration_preset_start'] = 'on'
    print ('*live duration sync turned ON*')

    timer_start_time =  timer_start_datetime.strftime('%H:%M')
    timer_start_date =  timer_start_datetime.strftime('%Y-%m-%d')
    self.call_service("input_datetime/set_datetime", entity_id = INPUT_DATETIME_START_DATETIME, date=timer_start_date , time=timer_start_time)

  def duration_preselect_live_updated_stop (self, entity, attribute, old, new, kwargs):
    print ('*live_duration_preselect_updated_stop*')
    current_datetime = datetime.datetime.now()
    timer_duration_preset_live_stop = self.get_state(INPUT_SELECT_TIMER_DURATION_PRESELECT_LIVE_STOP)
    if timer_duration_preset_live_stop == "Manual":
      return
    elif timer_duration_preset_live_stop == "15 min":
      timer_stop_datetime = current_datetime + relativedelta(minutes=+15)
    elif timer_duration_preset_live_stop == "30 min":
      timer_stop_datetime = current_datetime + relativedelta(minutes=+30)
    elif timer_duration_preset_live_stop == "45 min":
      timer_stop_datetime = current_datetime + relativedelta(minutes=+45)
    elif timer_duration_preset_live_stop == "1 hour":
      timer_stop_datetime = current_datetime + relativedelta(hours=+1)
    elif timer_duration_preset_live_stop == "2 hours":
      timer_stop_datetime = current_datetime + relativedelta(hours=+2)
    elif timer_duration_preset_live_stop == "1 day":
      timer_stop_datetime = current_datetime + relativedelta(days=+1)
    elif timer_duration_preset_live_stop == "1 week":
      timer_stop_datetime = current_datetime + relativedelta(weeks=+1)

    self.set_state(INPUT_BOOLEAN_PRESET_LIVE_DURATION_TIMER_SYNC, state='on')
    self.global_vars['live_duration_preset_stop'] = 'on'

    print ('*live duration sync turned ON*')
    timer_stop_time =  timer_stop_datetime.strftime('%H:%M')
    timer_stop_date =  timer_stop_datetime.strftime('%Y-%m-%d')
    self.call_service("input_datetime/set_datetime", entity_id = INPUT_DATETIME_STOP_DATETIME, date=timer_stop_date , time=timer_stop_time)
