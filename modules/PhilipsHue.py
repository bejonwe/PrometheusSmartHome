from prometheus_client import Gauge
from phue import Bridge

def init(c = []):
    global config
    global metrics
    global b

    config = c

    b = Bridge(config['bridgeip'], config['username'])
    b.connect()
    #lights = b.get_light_objects('id')

    metrics = {}
    metrics['lights'] = {}
    metrics['lights']['on'] = Gauge('philipshue_light_on', 'Philips Hue light on/off state', ['id','name'])


def getdata():
    global config
    global metrics
    global b

    lights = b.get_light_objects('id')



    for light in lights:
        l = lights[light]
        metrics['lights']['on'].labels(id=l.light_id, name=l.name).set(l.on)