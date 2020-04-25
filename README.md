# HA-FanSpeedControl
A python script for Home Assistant that control fan speed with [Fan Template](https://www.home-assistant.io/integrations/fan.template/) and [Broadlink](https://www.home-assistant.io/integrations/broadlink/).

# How it work
The script automatically call broadlink service when you set fan speed.

## Example
if your fan speed range is 1~12.

example1: call `increase` fan 4 times when you set fan speed from 1 to 5.

example2: call `decrease` fan 3 times when you set fan speed from 5 to 2.

example3: call `decrease` fan 2 times when you set fan speed from 2 to 12.



# Installation
Copy the Python script in to your /config/python_scripts directory.

# Script arguments
|key|required|type|description|
|-|-|-|-|
|fan_speed|true|string|speed from fan template|
|increase_code|true|string|increase fan seppd code|
|decrease_code|true|string|decrease fan seppd code|
|broadlink_host|true|string|broadlink ip address|
|fan_speed_entity_id|true|string||
|fan_entity_id|true|string||

# Config Example
```yaml
input_boolean:
  status_fan_power:
    name: 'Fan Power'

input_text:
  status_fan_speed:
    name: 'Fan Speed'
  home_notify_word:

input_select:
  fan_osc:
    name: 'Fan osc'
    options:
      - true
      - false
fan:
  - platform: template
    fans:
      bedroom_fan:
        friendly_name: "myFan"
        value_template: "{{ states('input_boolean.status_fan_power') }}"
        speed_template: "{{ states('input_text.status_fan_speed') }}"
        oscillating_template: "{{ states('input_select.fan_osc') }}"
        turn_on:
          - condition: state
            entity_id: input_boolean.status_fan_power
            state: 'off'
          - service: broadlink.send
            data:
                host: 192.168.0.0
                packet: your_
          - service: input_boolean.turn_on
            entity_id: input_boolean.status_fan_power
        turn_off:
          - condition: state
            entity_id: input_boolean.status_fan_power
            state: 'on'
          - service: broadlink.send
            data:
                host: 192.168.0.0
                packet: your_fan_power_toggle_code
          - service: input_boolean.turn_off
            entity_id: input_boolean.status_fan_power
        set_speed:
          - service: python_script.fan_speed_control
            data_template:
                fan_speed: "{{ speed }}"
                increase_code: your_fan_increase_speed_code
                decrease_code: your_fan_decrease_speed_code
                broadlink_host: 192.168.0.0
                fan_speed_entity_id: 'input_text.status_fan_speed'
                fan_entity_id: 'fan.bedroom_fan'
        set_oscillating:
          - condition: state
            entity_id: input_boolean.status_fan_power
            state: 'on'
          - service: broadlink.send
            data:
                host: 192.168.0.0
                packet: your_fan_osc_toggle_code
          - service: input_select.select_next
            entity_id: input_select.fan_osc
        speeds: ['off', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']
```

# Screenshot
![image](/Screenshot/fan.png)

## custom ui
![image](/Screenshot/fanui.png)
