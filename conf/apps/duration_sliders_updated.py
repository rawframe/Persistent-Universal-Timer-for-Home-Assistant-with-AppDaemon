import appdaemon.plugins.hass.hassapi as hass
import datetime
from dateutil.relativedelta import relativedelta

INPUT_DATETIME_START_DATETIME = 'input_datetime.start_datetime'
INPUT_DATETIME_STOP_DATETIME = 'input_datetime.stop_datetime'
INPUT_NUMBER_TIMER_DURATION_YEARS = 'input_number.on_duration_years'
INPUT_NUMBER_TIMER_DURATION_MONTHS = 'input_number.on_duration_months'
INPUT_NUMBER_TIMER_DURATION_DAYS = 'input_number.on_duration_days'
INPUT_NUMBER_TIMER_DURATION_DAYS_TOTAL = 'input_number.on_duration_days_total'
INPUT_NUMBER_TIMER_DURATION_WEEKS_TOTAL = 'input_number.on_duration_weeks_total'
INPUT_NUMBER_TIMER_DURATION_HOURS = 'input_number.on_duration_hours'
INPUT_NUMBER_TIMER_DURATION_MINUTES = 'input_number.on_duration_minutes'
INPUT_BOOLEAN_PRESET_DURATION_TIMER_SYNC = 'input_boolean.preset_duration_timer_sync'
INPUT_SELECT_TIMER_DURATION_PRESELECT = 'input_select.timer_duration_preselect'
# INPUT_SELECT_TIMER_DURATION_PRESELECT_DEFAULT_VALUE = 'None'

class DurationSliders(hass.Hass):

  def initialize(self): 
    self.listen_state(self.duration_time_slider_updated, INPUT_NUMBER_TIMER_DURATION_YEARS)
    self.listen_state(self.duration_time_slider_updated, INPUT_NUMBER_TIMER_DURATION_MONTHS)
    self.listen_state(self.duration_time_slider_updated, INPUT_NUMBER_TIMER_DURATION_DAYS)
    self.listen_state(self.duration_time_slider_updated_td_days_total, INPUT_NUMBER_TIMER_DURATION_DAYS_TOTAL)
    self.listen_state(self.duration_time_slider_updated_td_weeks_total, INPUT_NUMBER_TIMER_DURATION_WEEKS_TOTAL)
    self.listen_state(self.duration_time_slider_updated, INPUT_NUMBER_TIMER_DURATION_HOURS)
    self.listen_state(self.duration_time_slider_updated, INPUT_NUMBER_TIMER_DURATION_MINUTES)
    self.listen_state(self.duration_preselect_updated, INPUT_SELECT_TIMER_DURATION_PRESELECT)


  def duration_time_slider_updated (self, entity, attribute, old, new, kwargs):
    print ('*duration_time_slider_updated*')
    # self.select_option(INPUT_SELECT_TIMER_DURATION_PRESELECT, INPUT_SELECT_TIMER_DURATION_PRESELECT_DEFAULT_VALUE)
    timer_start_datetime = self.get_state(INPUT_DATETIME_START_DATETIME)
    timer_start_datetime = datetime.datetime.strptime(timer_start_datetime, "%Y-%m-%d %H:%M:%S")
    timer_stop_datetime = self.get_state(INPUT_DATETIME_STOP_DATETIME)
    timer_stop_datetime = datetime.datetime.strptime(timer_stop_datetime, "%Y-%m-%d %H:%M:%S")
    timer_duration_slider_years = self.get_state(INPUT_NUMBER_TIMER_DURATION_YEARS)
    timer_duration_slider_months = self.get_state(INPUT_NUMBER_TIMER_DURATION_MONTHS)
    timer_duration_slider_days = self.get_state(INPUT_NUMBER_TIMER_DURATION_DAYS)
    timer_duration_slider_hours = self.get_state(INPUT_NUMBER_TIMER_DURATION_HOURS)
    timer_duration_slider_minutes = self.get_state(INPUT_NUMBER_TIMER_DURATION_MINUTES)

    if timer_start_datetime > timer_stop_datetime :
      timer_start_datetime =  timer_stop_datetime + relativedelta(years=+int(float(timer_duration_slider_years)) , months=+int(float(timer_duration_slider_months)), days=+int(float(timer_duration_slider_days)), hours=+int(float(timer_duration_slider_hours)), minutes=+int(float(timer_duration_slider_minutes)))
      timer_start_time =  timer_start_datetime.strftime('%H:%M')
      timer_start_date =  timer_start_datetime.strftime('%Y-%m-%d')
      self.call_service("input_datetime/set_datetime", entity_id = INPUT_DATETIME_START_DATETIME, date=timer_start_date , time=timer_start_time)
    else :
      timer_stop_datetime =  timer_start_datetime + relativedelta(years=+int(float(timer_duration_slider_years)) , months=+int(float(timer_duration_slider_months)), days=+int(float(timer_duration_slider_days)), hours=+int(float(timer_duration_slider_hours)), minutes=+int(float(timer_duration_slider_minutes)))
      timer_stop_time =  timer_stop_datetime.strftime('%H:%M')
      timer_stop_date =  timer_stop_datetime.strftime('%Y-%m-%d')
      self.call_service("input_datetime/set_datetime", entity_id = INPUT_DATETIME_STOP_DATETIME, date=timer_stop_date , time=timer_stop_time)


  def duration_time_slider_updated_td_days_total (self, entity, attribute, old, new, kwargs):
    print ('*duration_time_slider_updated_td_days_total*')
    # self.select_option(INPUT_SELECT_TIMER_DURATION_PRESELECT, INPUT_SELECT_TIMER_DURATION_PRESELECT_DEFAULT_VALUE)
    timer_start_datetime = self.get_state(INPUT_DATETIME_START_DATETIME)
    timer_start_datetime = datetime.datetime.strptime(timer_start_datetime, "%Y-%m-%d %H:%M:%S")
    timer_stop_datetime = self.get_state(INPUT_DATETIME_STOP_DATETIME)
    timer_stop_datetime = datetime.datetime.strptime(timer_stop_datetime, "%Y-%m-%d %H:%M:%S")
    timer_duration_slider_days_total = self.get_state(INPUT_NUMBER_TIMER_DURATION_DAYS_TOTAL)

    if timer_start_datetime > timer_stop_datetime :
      timer_start_datetime =  timer_stop_datetime + relativedelta(days=+int(float(timer_duration_slider_days_total)))
      timer_start_time =  timer_start_datetime.strftime('%H:%M')
      timer_start_date =  timer_start_datetime.strftime('%Y-%m-%d')
      self.call_service("input_datetime/set_datetime", entity_id = INPUT_DATETIME_START_DATETIME, date=timer_start_date , time=timer_start_time)
    else :
      timer_stop_datetime =  timer_start_datetime + relativedelta(days=+int(float(timer_duration_slider_days_total)))
      timer_stop_time =  timer_stop_datetime.strftime('%H:%M')
      timer_stop_date =  timer_stop_datetime.strftime('%Y-%m-%d')
      self.call_service("input_datetime/set_datetime", entity_id = INPUT_DATETIME_STOP_DATETIME, date=timer_stop_date , time=timer_stop_time)

  def duration_time_slider_updated_td_weeks_total (self, entity, attribute, old, new, kwargs):
    print ('*duration_time_slider_updated_td_weeks_total*')
    # self.select_option(INPUT_SELECT_TIMER_DURATION_PRESELECT, INPUT_SELECT_TIMER_DURATION_PRESELECT_DEFAULT_VALUE)
    timer_start_datetime = self.get_state(INPUT_DATETIME_START_DATETIME)
    timer_start_datetime = datetime.datetime.strptime(timer_start_datetime, "%Y-%m-%d %H:%M:%S")
    timer_stop_datetime = self.get_state(INPUT_DATETIME_STOP_DATETIME)
    timer_stop_datetime = datetime.datetime.strptime(timer_stop_datetime, "%Y-%m-%d %H:%M:%S")
    timer_duration_slider_weeks_total = self.get_state(INPUT_NUMBER_TIMER_DURATION_WEEKS_TOTAL)

    if timer_start_datetime > timer_stop_datetime :
      timer_start_datetime =  timer_stop_datetime + relativedelta(weeks=+int(float(timer_duration_slider_weeks_total)))
      timer_start_time =  timer_start_datetime.strftime('%H:%M')
      timer_start_date =  timer_start_datetime.strftime('%Y-%m-%d')
      self.call_service("input_datetime/set_datetime", entity_id = INPUT_DATETIME_START_DATETIME, date=timer_start_date , time=timer_start_time)
    else :
      timer_stop_datetime =  timer_start_datetime + relativedelta(weeks=+int(float(timer_duration_slider_weeks_total)))
      timer_stop_time =  timer_stop_datetime.strftime('%H:%M')
      timer_stop_date =  timer_stop_datetime.strftime('%Y-%m-%d')
      self.call_service("input_datetime/set_datetime", entity_id = INPUT_DATETIME_STOP_DATETIME, date=timer_stop_date , time=timer_stop_time)

  def duration_preselect_updated (self, entity, attribute, old, new, kwargs):
    print ('*duration_preselect_updated*')
    timer_start_datetime = self.get_state(INPUT_DATETIME_START_DATETIME)
    timer_start_datetime = datetime.datetime.strptime(timer_start_datetime, "%Y-%m-%d %H:%M:%S")
    timer_stop_datetime = self.get_state(INPUT_DATETIME_STOP_DATETIME)
    timer_stop_datetime = datetime.datetime.strptime(timer_stop_datetime, "%Y-%m-%d %H:%M:%S")
    timer_duration_preset = self.get_state(INPUT_SELECT_TIMER_DURATION_PRESELECT)

    if timer_start_datetime > timer_stop_datetime :
      if timer_duration_preset == "Manual":
        return
      elif timer_duration_preset == "15 min":
        timer_start_datetime = timer_stop_datetime + relativedelta(minutes=+15)
      elif timer_duration_preset == "30 min":
        timer_start_datetime = timer_stop_datetime + relativedelta(minutes=+30)
      elif timer_duration_preset == "45 min":
        timer_start_datetime = timer_stop_datetime + relativedelta(minutes=+45)
      elif timer_duration_preset == "1 hour":
        timer_start_datetime = timer_stop_datetime + relativedelta(hours=+1)
      elif timer_duration_preset == "2 hours":
        timer_start_datetime = timer_stop_datetime + relativedelta(hours=+2)
      elif timer_duration_preset == "1 day":
        timer_start_datetime = timer_stop_datetime + relativedelta(days=+1)
      elif timer_duration_preset == "1 week": 
        timer_start_datetime = timer_stop_datetime + relativedelta(weeks=+1)
      self.set_state(INPUT_BOOLEAN_PRESET_DURATION_TIMER_SYNC, state='on')
      print ('*duration sync turned ON*')
      timer_start_time =  timer_start_datetime.strftime('%H:%M')
      timer_start_date =  timer_start_datetime.strftime('%Y-%m-%d')
      self.call_service("input_datetime/set_datetime", entity_id = INPUT_DATETIME_START_DATETIME, date=timer_start_date , time=timer_start_time)
    else :  # lazy coding ... change later 
      if timer_duration_preset == "Manual":
        return
      elif timer_duration_preset == "15 min":
        timer_stop_datetime = timer_start_datetime + relativedelta(minutes=+15)
      elif timer_duration_preset == "30 min":
        timer_stop_datetime = timer_start_datetime + relativedelta(minutes=+30)
      elif timer_duration_preset == "45 min":
        timer_stop_datetime = timer_start_datetime + relativedelta(minutes=+45)
      elif timer_duration_preset == "1 hour":
        timer_stop_datetime = timer_start_datetime + relativedelta(hours=+1)
      elif timer_duration_preset == "2 hours":
        timer_stop_datetime = timer_start_datetime + relativedelta(hours=+2)
      elif timer_duration_preset == "1 day":
        timer_stop_datetime = timer_start_datetime + relativedelta(days=+1)
      elif timer_duration_preset == "1 week": 
        timer_stop_datetime = timer_start_datetime + relativedelta(weeks=+1)
      self.set_state(INPUT_BOOLEAN_PRESET_DURATION_TIMER_SYNC, state='on')
      print ('*duration sync turned ON*')
      timer_stop_time =  timer_stop_datetime.strftime('%H:%M')
      timer_stop_date =  timer_stop_datetime.strftime('%Y-%m-%d')
      self.call_service("input_datetime/set_datetime", entity_id = INPUT_DATETIME_STOP_DATETIME, date=timer_stop_date , time=timer_stop_time)
