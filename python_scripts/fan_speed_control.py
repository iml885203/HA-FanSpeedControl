#### Init
service_domain = data.get('service_domain')
service = data.get('service')
service_data_increase = data.get('service_data_increase')
service_data_decrease = data.get('service_data_decrease')
# fan speed data
speed = data.get('fan_speed')
status_speed = hass.states.get(data.get('fan_speed_entity_id'))
fan = hass.states.get(data.get('fan_entity_id'))
speed_list = fan.attributes.get('speed_list')

logger.debug('<fan_speed_control> fan state ({})'.format(fan.state))
logger.debug('<fan_speed_control> Received fan speed from ({}) to ({})'.format(status_speed.state, speed))

### def
def check_speed(logger, speed, speed_list):
  if speed is None:
    logger.warning('<fan_speed_control> Received fan speed is invalid (None)')
    return False

  if speed not in speed_list:
    logger.warning('<fan_speed_control> Received fan speed is invalid ({})'.format(speed))
    return False

  if not isinstance(speed, str):
    logger.warning('<fan_speed_control> speed variable is not string')
    return False

  if not speed.isnumeric():
    logger.warning('<fan_speed_control> speed variable is not numeric: ({})'.format(speed))
    return False

  if fan.state is 'off':
    logger.warning('<fan_speed_control> can not change speed when fan is off')
    return False

  return True


### Run
if check_speed(logger, speed, speed_list):
  speed = int(speed)
  last_speed = int(status_speed.state) if status_speed.state else 1
  speed_max = int(speed_list[-1])

  if speed > last_speed:
    increase_loop = speed - last_speed
    decrease_loop = last_speed + speed_max - speed
  else:
    increase_loop = speed + speed_max - last_speed
    decrease_loop = last_speed - speed

  # check use increase or decrease
  if decrease_loop < increase_loop:
    loop = decrease_loop
    service_data = service_data_decrease
  else:
    loop = increase_loop
    service_data = service_data_increase

  # update speed state
  hass.states.set(data.get('fan_speed_entity_id'), speed)

  # Call service
  if data.get('support_num_repeats', False):
    service_data['num_repeats'] = loop
    logger.debug('<fan_speed_control> call service ({}.{}) {}'.format(service_domain, service, service_data))
    hass.services.call(service_domain, service, service_data)
  else:
    for i in range(loop):
      logger.debug('<fan_speed_control> call service ({}.{}) {}'.format(service_domain, service, service_data))
      result = hass.services.call(service_domain, service, service_data)
      time.sleep(0.75)


elif fan.state is not 'off' and speed == 'off':
  logger.debug('<fan_speed_control> call fan off')
  hass.services.call('fan', 'turn_off', {
    'entity_id': data.get('fan_entity_id')
  })
