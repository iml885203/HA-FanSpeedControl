# broadlink data
increase_code = data.get('increase_code')
decrease_code = data.get('decrease_code')
broadlink_host = data.get('broadlink_host')
# fan speed data
speed = data.get('fan_speed')
status_speed = hass.states.get(data.get('fan_speed_entity_id'))
fan = hass.states.get(data.get('fan_entity_id'))
speed_list = fan.attributes.get('speed_list')

# logger.warning('<fan_speed_control> fan state ({})'.format(fan.state))
# logger.warning('<fan_speed_control> Received fan speed from ({}) to ({})'.format(status_speed.state, speed))

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
    service_data = {'host': broadlink_host, 'packet': decrease_code}
  else:
    loop = increase_loop
    service_data = {'host': broadlink_host, 'packet': increase_code}

  # Set the IP address to match the one used by your Broadlink device
  for i in range(loop):
    hass.services.call('broadlink', 'send', service_data, False)
    # logger.warning('<fan_speed_control> call service_data')
    time.sleep(0.5)

  # update speed state
  hass.states.set(data.get('fan_speed_entity_id'), speed)
elif fan.state is not 'off' and speed == 'off':
  # logger.warning('<fan_speed_control> call fan off')
  hass.services.call('fan', 'turn_off', {
    'entity_id': data.get('fan_entity_id')
  })