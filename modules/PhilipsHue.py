from prometheus_client import Gauge
from phue import Bridge
import os

def init(c = []):
    global config
    global metrics
    global b

    config = c


    bridgeip = os.getenv('BRIDGEIP', '127.0.0.1')
    username = os.getenv('HUEUSERNAME', 'XXXXXX')
    b = Bridge(bridgeip, username)
    b.connect()
    #lights = b.get_light_objects('id')

    metrics = {}
    metrics['lights'] = {}
    metrics['lights']['on'] = Gauge('philipshue_light_on', 'Philips Hue light on/off state', ['id','name','type'])
    metrics['lights']['reachable'] = Gauge('philipshue_light_reachable', 'Philips Hue light wether it''s reachable or not', ['id','name','type'])
    metrics['lights']['brightness_8bit'] = Gauge('philipshue_light_brightness_8bit', 'Philips Hue light brightness in 8bit (1-254)', ['id','name','type'])
    metrics['lights']['brightness_percent'] = Gauge('philipshue_light_brightness_percent', 'Philips Hue light brightness in percent', ['id','name','type'])
    metrics['lights']['colortemp_mired'] = Gauge('philipshue_light_colortemp_mired', 'Philips Hue light mired colortemp', ['id','name','type'])
    metrics['lights']['colortemp_kelvin'] = Gauge('philipshue_light_colortemp_kelvin', 'Philips Hue light colortemp in kelvin', ['id','name','type'])

    metrics['sensors'] = {}
    metrics['sensors']['on'] = Gauge('philipshue_sensor_on', 'Philips Hue sensor on/off state', ['id','name','type'])
    metrics['sensors']['battery'] = Gauge('philipshue_sensor_battery_percent', 'Philips Hue sensor battery in percent', ['id','name','type'])
    metrics['sensors']['temperature'] = Gauge('philipshue_sensor_temperature', 'Philips Hue sensor temperature', ['id','name','type'])
    metrics['sensors']['lightlevel'] = Gauge('philipshue_sensor_lightlevel', 'Philips Hue sensor lightlevel', ['id','name','type'])
    metrics['sensors']['presence'] = Gauge('philipshue_sensor_presence', 'Philips Hue sensor presence', ['id','name','type'])
    metrics['sensors']['reachable'] = Gauge('philipshue_sensor_reachable', 'Philips Hue sensor wether it''s reachable or not', ['id','name','type'])

def getdata():
    global config
    global metrics
    global b

    lights = b.get_light_objects('id')
    sensors = b.get_sensor_objects()

    for s in sensors:
        if s.type in  ['ZLLSwitch','ZLLTemperature'] :
            metrics['sensors']['on'].labels(id=s.sensor_id, name=s.name, type=s.type).set(s.config['on'])
            if s.config['battery'] is not None:
                metrics['sensors']['battery'].labels(id=s.sensor_id, name=s.name, type=s.type).set(s.config['battery'])
            if s.config['reachable']:
                metrics['sensors']['reachable'].labels(id=s.sensor_id, name=s.name, type=s.type).set(1)
            else:
                metrics['sensors']['reachable'].labels(id=s.sensor_id, name=s.name, type=s.type).set(0)
            if s.type == 'ZLLTemperature':
                metrics['sensors']['temperature'].labels(id=s.sensor_id, name=s.name, type=s.type).set(s.state['temperature']/100)
        if s.type == 'ZLLLightLevel':
                metrics['sensors']['lightlevel'].labels(id=s.sensor_id, name=s.name, type=s.type).set(s.state['lightlevel'])
        if s.type == 'ZLLPresence':
                metrics['sensors']['presence'].labels(id=s.sensor_id, name=s.name, type=s.type).set(s.state['presence'])



    for light in lights:
        l = lights[light]
        metrics['lights']['on'].labels(id=l.light_id, name=l.name, type=l.type).set(l.on)
        metrics['lights']['brightness_8bit'].labels(id=l.light_id, name=l.name, type=l.type).set(l.brightness)
        metrics['lights']['brightness_percent'].labels(id=l.light_id, name=l.name, type=l.type).set(round((l.brightness-1)*0.395256917))

        if l.reachable:
            metrics['lights']['reachable'].labels(id=l.light_id, name=l.name, type=l.type).set(1)
        else:
            metrics['lights']['reachable'].labels(id=l.light_id, name=l.name, type=l.type).set(0)

        if l.type in ['Color temperature light','Extended color light']:
            metrics['lights']['colortemp_mired'].labels(id=l.light_id, name=l.name, type=l.type).set(l.colortemp)
            metrics['lights']['colortemp_kelvin'].labels(id=l.light_id, name=l.name, type=l.type).set(l.colortemp_k)
