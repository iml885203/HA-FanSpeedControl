# HA-FanSpeedControl
用於Home Assistant的Python腳本，使用[Fan Template](https://www.home-assistant.io/integrations/fan.template/)和[Broadlink](https://www.home-assistant.io/integrations/broadlink/)控制風扇速度。

- [中文說明](https://github.com/iml885203/HA-FanSpeedControl/blob/master/README_TW.md)
- [英文說明](https://github.com/iml885203/HA-FanSpeedControl/blob/master/README.md)

# 如何運作
當你設定風速時，腳本會自動呼叫多次broadlink service

## 範例
如果你的風速範圍為1~12

範例1: 當你設定風速從1到5時，會呼叫 `增加` 風速4次

範例2: 當你設定風速從5到2時，會呼叫 `減少` 風速3次

範例3: 當你設定風速從2到12時，會呼叫 `減少` 風速2次


# 安裝
複製Python腳本到你的`/config/python_scripts`資料夾裡面，或者透過HACS安裝

# 參數
|key|required|type|description|
|-|-|-|-|
|fan_speed|true|string|speed from fan template|
|fan_speed_entity_id|true|string||
|fan_entity_id|true|string||
|service_domain|true|string||
|service|true|string||
|service_data_increase|true|object||
|service_data_decrease|true|object||

# 設定範例
設定在[Fan template](https://www.home-assistant.io/integrations/fan.template/)的 `set_percentage` 上

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

## 完整範例
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

# 除錯
增加logger到 `configuration.yaml`
```yaml
logger:
  default: warn
  logs:
    homeassistant.components.python_script.fan_speed_control.py: debug
```

# 截圖
![image](https://github.com/iml885203/HA-FanSpeedControl/blob/master/Screenshot/fan.png?raw=true)

## 客製化UI
![image](https://github.com/iml885203/HA-FanSpeedControl/blob/master/Screenshot/fanui.png?raw=true)



<br><br>
<p align="center">
<br>
<a href="https://www.buymeacoffee.com/dodoro" target="_blank">
  <img src="https://github.com/appcraftstudio/buymeacoffee/raw/master/Images/snapshot-bmc-button.png" width="300">
</a>
</p>
