import appdaemon.plugins.hass.hassapi as hass
import datetime

# GLOBAL FOR EACH APP? / APP JUST FOR GLOBALS?
INPUT_DATETIME_START_TIME = 'input_datetime.start_datetime'
INPUT_DATETIME_STOP_TIME = 'input_datetime.stop_datetime'
INPUT_NUMBER_TIMER_START_HOUR = 'input_number.on_hour'
INPUT_NUMBER_TIMER_START_MINUTE = 'input_number.on_minute'
INPUT_NUMBER_TIMER_STOP_HOUR = 'input_number.off_hour'
INPUT_NUMBER_TIMER_STOP_MINUTE = 'input_number.off_minute'

class TimerSliders(hass.Hass):
 
  def initialize(self): 
    self.listen_state(self.start_time_slider_updated, INPUT_NUMBER_TIMER_START_HOUR)
    self.listen_state(self.start_time_slider_updated, INPUT_NUMBER_TIMER_START_MINUTE)
    self.listen_state(self.stop_time_slider_updated, INPUT_NUMBER_TIMER_STOP_HOUR)
    self.listen_state(self.stop_time_slider_updated, INPUT_NUMBER_TIMER_STOP_MINUTE)

  def start_time_slider_updated (self, entity, attribute, old, new, kwargs):
    timer_start_datetime = self.get_state(INPUT_DATETIME_START_TIME)
    timer_slider_start_hour = self.get_state(INPUT_NUMBER_TIMER_START_HOUR)
    timer_slider_start_minute = self.get_state(INPUT_NUMBER_TIMER_START_MINUTE)
    timer_start_datetime = datetime.datetime.strptime(timer_start_datetime, "%Y-%m-%d %H:%M:%S")
    timer_start_datetime = timer_start_datetime.replace(hour=int(float(timer_slider_start_hour)))
    timer_start_datetime = timer_start_datetime.replace(minute=int(float(timer_slider_start_minute)))
    timer_start_time =  timer_start_datetime.strftime('%H:%M')
    timer_start_date =  timer_start_datetime.strftime('%Y-%m-%d')
    # how to only update date or time and not both each time?
    self.call_service("input_datetime/set_datetime", entity_id = INPUT_DATETIME_START_TIME, date=timer_start_date , time=timer_start_time)

  def stop_time_slider_updated (self, entity, attribute, old, new, kwargs):
    timer_stop_datetime = self.get_state(INPUT_DATETIME_STOP_TIME)
    timer_slider_stop_hour = self.get_state(INPUT_NUMBER_TIMER_STOP_HOUR)
    timer_slider_stop_minute = self.get_state(INPUT_NUMBER_TIMER_STOP_MINUTE)
    timer_stop_datetime = datetime.datetime.strptime(timer_stop_datetime, "%Y-%m-%d %H:%M:%S")
    timer_stop_datetime = timer_stop_datetime.replace(hour=(int(float(timer_slider_stop_hour))))
    timer_stop_datetime = timer_stop_datetime.replace(minute=(int(float(timer_slider_stop_minute))))
    timer_stop_time =  timer_stop_datetime.strftime('%H:%M')
    timer_stop_date =  timer_stop_datetime.strftime('%Y-%m-%d')
    # how to only update date or time and not both each time?
    self.call_service("input_datetime/set_datetime", entity_id = INPUT_DATETIME_STOP_TIME, date=timer_stop_date , time=timer_stop_time)
