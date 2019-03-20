import appdaemon.plugins.hass.hassapi as hass

INPUT_SELECT = 'input_select.timer_select'
INPUT_TEXT = 'input_text.entity_timer_name'
DEFAULT_NAME = "Enter new timer name"
INPUT_SELECT_REFRESH_OPTION = 'Rebuilding list'
MENU_NEW_COUNTDOWN = '* NEW - Countdown Timer'
MENU_NEW_SCHEDULED = '* NEW - Scheduled Timer'
MENU_COUNTDOWN_ACTIVE = '* COUNTDOWN Timers ACTIVE   :-'
MENU_COUNTDOWN_INACTIVE = '* COUNTDOWN Timers INACTIVE :-'
MENU_SCHEDULED_ACTIVE = '* SCHEDULED Timers ACTIVE   :-'
MENU_SCHEDULED_INACTIVE = '* SCHEDULED Timers INACTIVE :-'
TIMER_PRESET_LIST = [ MENU_NEW_COUNTDOWN, MENU_NEW_SCHEDULED, MENU_COUNTDOWN_ACTIVE, MENU_COUNTDOWN_INACTIVE, MENU_SCHEDULED_ACTIVE, MENU_SCHEDULED_INACTIVE, INPUT_SELECT_REFRESH_OPTION ]

class EntityTimerName(hass.Hass):
 
  def initialize(self): 
    self.listen_state(self.edit_timer_name, INPUT_SELECT)

  def edit_timer_name (self, entity, attribute, old, new, kwargs):
    current_timer = self.get_state(INPUT_SELECT)
    print ('T1')
    if current_timer in TIMER_PRESET_LIST:
      self.call_service('input_text/set_value', entity_id=INPUT_TEXT, value=DEFAULT_NAME)
      print ('T2')
    else:
      self.call_service('input_text/set_value', entity_id=INPUT_TEXT, value=current_timer)
      print ('T3')
