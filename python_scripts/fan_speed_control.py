#### Init
service_domain = data.get('service_domain')
service = data.get('service')
service_data_increase = data.get('service_data_increase')
service_data_decrease = data.get('service_data_decrease')
# fan speed data
speed = data.get('fan_speed')
speed_count = data.get('fan_speed_count')
fan_speed_entity = hass.states.get(data.get('fan_speed_entity_id'))
fan_entity = hass.states.get(data.get('fan_entity_id'))

logger.debug('<fan_speed_control> fan state ({})'.format(fan_entity.state))
logger.debug('<fan_speed_control> Received fan speed from ({}) to ({})'.format(fan_speed_entity.state, speed))

### def
def check_speed(logger, speed):
  if speed is None:
    logger.warning('<fan_speed_control> Received fan speed is invalid (None)')
    return False

  if fan_entity.state is 'off':
    logger.warning('<fan_speed_control> can not change speed when fan is off')
    return False

  return True


### Run
if check_speed(logger, speed):
  speed_step = 100 // speed_count
  target_speed = int(speed) // speed_step
  last_speed = int(float(fan_speed_entity.state)) // speed_step if fan_speed_entity.state else 1
  speed_max = speed_count

  if target_speed > last_speed:
    increase_loop = target_speed - last_speed
    decrease_loop = last_speed + speed_max - target_speed
  else:
    increase_loop = target_speed + speed_max - last_speed
    decrease_loop = last_speed - target_speed

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


elif fan_entity.state is not 'off' and speed == 'off':
  logger.debug('<fan_speed_control> call fan off')
  hass.services.call('fan', 'turn_off', {
    'entity_id': data.get('fan_entity_id')
  })
