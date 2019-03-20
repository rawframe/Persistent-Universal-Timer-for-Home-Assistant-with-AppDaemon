import appdaemon.plugins.hass.hassapi as hass

INPUT_SELECT_ENTITY_FILTER = 'input_select.entity_filter_select'
INPUT_SELECT_ENTITY_FRIENDLY = 'input_select.timer_entity_select_friendly'
INPUT_SELECT_ENTITY_HIDDEN = 'input_select.timer_entity_select_hidden'
INPUT_SELECT_TIMER = 'input_select.timer_select'
INPUT_SELECT_START_ACTION = 'input_select.entity_start_action_select'
INPUT_SELECT_STOP_ACTION = 'input_select.entity_stop_action_select'
saved_entity_title = "* SAVED ENTITIES :-"
available_entity_title = "* AVAILABLE ENTITIES :-"
entity_title_list = [ saved_entity_title , available_entity_title ]

class DynamicEntityInputSelect(hass.Hass):

  def initialize(self): 
    self.listen_state(self.create_friendly_entity_list, INPUT_SELECT_ENTITY_FRIENDLY)
    self.listen_state(self.create_friendly_entity_list, INPUT_SELECT_TIMER)
    self.listen_state(self.create_friendly_entity_list, INPUT_SELECT_ENTITY_FILTER)

  def create_friendly_entity_list (self, entity, attribute, old, new, kwargs):
    print ('Creating Entity Lists')
    current_selection = self.get_state(INPUT_SELECT_ENTITY_FRIENDLY)
    timer_selection = self.get_state(INPUT_SELECT_TIMER)
    entity_filter_selection = self.get_state(INPUT_SELECT_ENTITY_FILTER)
    if entity_filter_selection == 'Lights':
      entity_filter = 'light'
    elif entity_filter_selection == 'Switches':
      entity_filter = 'switch'
    elif entity_filter_selection == 'Scripts':
      entity_filter = 'script'
    elif entity_filter_selection == 'Automations':
      entity_filter = 'automation'
    elif entity_filter_selection == 'Groups':
      entity_filter = 'group'
    elif entity_filter_selection == 'Sensors':
      entity_filter = 'sensor'
    elif entity_filter_selection == 'Scenes':
      entity_filter = 'scene'
    else:
      entity_filter = '.'
    states = self.get_state()
    timers = self.global_vars['timers']
#  GET ENTITIES FROM HOME ASSISTANT INTO LIST
    ha_entity_list = []  
    for entity in states:
      if entity_filter in entity:
        try:
          ha_entity_list.append(states[entity]['entity_id'])
        except Exception:
          print ("No Home Assistant entity found :", entity)
#  GET ENTITIES FROM TIMER INTO LIST (too messy + add quick timer option detect)  
    timer_entity_list = []
    try:
      for entity in timers[timer_selection]["Entities"]:
        try:
          timer_entity_list.append(entity)
        except Exception:
          print ("No timer entity found")
    except Exception:
      print ("No timer entity found")
#  CREATE ALL ENTITIES LIST LESS TIMER ENTITIES LIST
    available_entity_list = []
    available_entity_list = ha_entity_list
    for entity in timer_entity_list :
      try:
        available_entity_list.remove(entity)
      except Exception:
        error_msg = "Saved timer entity, " + entity + ", is not currently present in Home Assistant"
        self.call_service("persistent_notification/create", message = error_msg, title = "TIMER Notification:", notification_id = "timer_name")
#  CREATE SORTED FRIENDLY TIMER ENTITY LIST
    timer_entity_list_friendly = []
    for entity in timer_entity_list:
      try:
        timer_entity_list_friendly.append('{} -  ({})'.format(states[entity]['attributes']['friendly_name'], states[entity]['entity_id']))
      except Exception:
        not_present_entity = '! ' + entity + ' ! NOT present ' + ' - ''(' + entity + ')'
        timer_entity_list_friendly.append(not_present_entity)
    timer_entity_list_friendly.sort()
#  CREATE SORTED FRIENDLY AVAILABLE ENTITY LIST
    available_entity_list_friendly = []
    for entity in available_entity_list:
      try:
        available_entity_list_friendly.append('{} -  ({})'.format(states[entity]['attributes']['friendly_name'], states[entity]['entity_id']))
      except Exception:
        available_entity_list_friendly.append(entity)
    available_entity_list_friendly.sort()
#  CREATE FRIENDLY INPUT SELECT ENTITY LIST
    entity_list_friendly = [saved_entity_title] + timer_entity_list_friendly + [available_entity_title] + available_entity_list_friendly
  #  if this list differs from the current input select list :
#     current_list = self.get_state(INPUT_SELECT_ENTITY_FRIENDLY, attribute="options")
    current_list = self.get_state(INPUT_SELECT_ENTITY_FRIENDLY, attribute="options")

    if current_list != entity_list_friendly :
      self.call_service( 'input_select/set_options', entity_id=INPUT_SELECT_ENTITY_FRIENDLY, options= entity_list_friendly )
      self.select_option(INPUT_SELECT_ENTITY_FRIENDLY, current_selection)

#  CREATE UNSORTED HIDDEN INPUT SELECT ENTITY LIST (MAINTAINING FRIENDLY INDEX MIRROR)
    entity_list = []
    for entity in entity_list_friendly:
      try:
        if entity in entity_title_list :
          entity_list.append(entity)
        else:
          entity_list.append(entity[entity.find("(")+1:entity.find(")")])
      except Exception:
        print ('exception:', entity)
        entity_list.append(entity)
    self.call_service( 'input_select/set_options', entity_id=INPUT_SELECT_ENTITY_HIDDEN, options=entity_list )
#  UPDATE HIDDEN INPUT SELECT TO MATCH FRIENDLY
    try:
      entity_match_index = entity_list_friendly.index(current_selection)
      timer_entity = entity_list[entity_match_index]
      self.select_option(INPUT_SELECT_ENTITY_HIDDEN, timer_entity)
    except Exception:
      self.call_service("persistent_notification/create", message = "Friendly name entity mismatch. Please select another entity to reload list.", title = "TIMER Notification:", notification_id = "timer_name")

#  UPDATE START AND STOP ACTIONS TO MATCH HIDDEN INPUT SELECT
  # could use if INPUT_SELECT_TIMER != DEFAULT TIMER OPTION ... quicker than below maybe 
    MISSING_TIMER_DEFAULT_ACTION = "Do Nothing"
    try:
      entity_start_action = timers[timer_selection]['Entities'][timer_entity]['Start action']
      entity_stop_action = timers[timer_selection]['Entities'][timer_entity]['Stop action']
    except:
      print ('No start or stop actions assciated with selection :', timer_selection, ',', timer_entity)
      return

    start_action_list = self.get_state(INPUT_SELECT_START_ACTION, attribute="options")
    stop_action_list = self.get_state(INPUT_SELECT_STOP_ACTION, attribute="options")

    if entity_start_action in start_action_list:
      self.select_option(INPUT_SELECT_START_ACTION, entity_start_action)
    else:
      self.select_option(INPUT_SELECT_START_ACTION, MISSING_TIMER_DEFAULT_ACTION)
      start_error_msg = 'Start Action for saved timer Entity (' + timer_entity + ') is no longer available. Default action (' + MISSING_TIMER_DEFAULT_ACTION + ') selected but not saved.'
      self.call_service("persistent_notification/create", message = start_error_msg, title = "TIMER Notification:", notification_id = "timer_name")
    if entity_stop_action in stop_action_list:
      self.select_option(INPUT_SELECT_STOP_ACTION, entity_stop_action)
    else:
      self.select_option(INPUT_SELECT_STOP_ACTION, MISSING_TIMER_DEFAULT_ACTION)
      stop_error_msg = 'Stop Action for saved timer Entity (' + timer_entity + ') is no longer available. Default action (' + MISSING_TIMER_DEFAULT_ACTION + ') selected but not saved.'
      self.call_service("persistent_notification/create", message = start_error_msg, title = "TIMER Notification:", notification_id = "timer_name")

