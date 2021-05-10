# HA-FanSpeedControl

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)
[![Donate](https://img.shields.io/badge/donate-Coffee-yellow.svg)](https://www.buymeacoffee.com/dodoro)

A python script for Home Assistant that control fan speed with [Fan Template](https://www.home-assistant.io/integrations/fan.template/) and [Broadlink](https://www.home-assistant.io/integrations/broadlink/).


# Document
- [Chinese Document](https://github.com/iml885203/HA-FanSpeedControl/blob/master/README_TW.md)
- [English Document](https://github.com/iml885203/HA-FanSpeedControl/blob/master/README.md)

# How it work
The script automatically call broadlink service when you set fan speed.

## Example
if your fan speed range is 1~12.

example1: call `increase` fan 4 times when you set fan speed from 1 to 5.

example2: call `decrease` fan 3 times when you set fan speed from 5 to 2.

example3: call `decrease` fan 2 times when you set fan speed from 2 to 12.



# Installation
Copy the Python script in to your `/config/python_scripts` directory or install via HACS.

# Script arguments
|key|required|type|description|
|-|-|-|-|
|fan_speed|true|string|speed from fan template|
|fan_speed_entity_id|true|string||
|fan_entity_id|true|string||
|fan_speed_count|true|integer||
|service_domain|true|string||
|service|true|string||
|service_data_increase|true|object||
|service_data_decrease|true|object||

# Config Example
`set_percentage` on template fan

```yaml
set_percentage:
  - service: python_script.fan_speed_control
    data_template:
      fan_speed: "{{ percentage }}"
      fan_speed_entity_id: 'input_text.status_fan_speed'
      fan_entity_id: 'fan.bedroom_fan'
      fan_speed_count: 12
      service_domain: 'remote'
      service: 'send_command'
      service_data_increase:
        entity_id: remote.broadlink
        device: fan
        command: increase
      service_data_decrease:
        entity_id: remote.broadlink
        device: fan
        command: decrease
```

## Template Fan config
```yaml
input_boolean:
  status_fan_power:
    name: 'Fan Power'

input_text:
  status_fan_speed:
    name: 'Fan Speed'

input_select:
  fan_osc:
    name: 'Fan osc'
    options:
      - 'True'
      - 'False'
fan:
  - platform: template
    fans:
      bedroom_fan:
        friendly_name: "myFan"
        speed_count: 12
        value_template: "{{ states('input_boolean.status_fan_power') }}"
        percentage_template: "{{ states('input_text.status_fan_speed') | int }}"
        oscillating_template: "{{ states('input_select.fan_osc') }}"
        turn_on:
          - condition: state
            entity_id: input_boolean.status_fan_power
            state: 'off'
          - service: remote.send_command
            data:
              entity_id: remote.broadlink
              device: fan
              command: toggle
          - service: input_boolean.turn_on
            entity_id: input_boolean.status_fan_power
        turn_off:
          - condition: state
            entity_id: input_boolean.status_fan_power
            state: 'on'
          - service: remote.send_command
            data:
              entity_id: remote.broadlink
              device: fan
              command: toggle
          - service: input_boolean.turn_off
            entity_id: input_boolean.status_fan_power
        set_percentage:
          - service: python_script.fan_speed_control
            data_template:
              fan_speed: "{{ percentage }}"
              fan_speed_entity_id: 'input_text.status_fan_speed'
              fan_entity_id: 'fan.bedroom_fan'
              fan_speed_count: 12
              service_domain: 'remote'
              service: 'send_command'
              service_data_increase:
                entity_id: remote.broadlink
                device: fan
                command: increase
              service_data_decrease:
                entity_id: remote.broadlink
                device: fan
                command: decrease
        set_oscillating:
          - condition: state
            entity_id: input_boolean.status_fan_power
            state: 'on'
          - service: remote.send_command
            data:
              entity_id: remote.broadlink
              device: fan
              command: oscillate
          - service: input_select.select_next
            entity_id: input_select.fan_osc
```

# Debug
add logger to your `configuration.yaml`
```yaml
logger:
  default: warn
  logs:
    homeassistant.components.python_script.fan_speed_control.py: debug
```

# Screenshot
![image](https://github.com/iml885203/HA-FanSpeedControl/blob/master/Screenshot/fan.png?raw=true)

## custom ui
![image](https://github.com/iml885203/HA-FanSpeedControl/blob/master/Screenshot/fanui.png?raw=true)



<br><br>
<p align="center">
<br>
<a href="https://www.buymeacoffee.com/dodoro" target="_blank">
  <img src="https://github.com/appcraftstudio/buymeacoffee/raw/master/Images/snapshot-bmc-button.png" width="300">
</a>
</p>
