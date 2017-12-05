from prometheus_client import Gauge
import homematicip


def init(c = []):
    global config
    global metrics
    global h

    config = c

    homematicip.init(config["accesspointid"])
    homematicip.set_auth_token(config["authtoken"])

    h = homematicip.Home()

    metrics = {}
    metrics['heating'] = {}
    metrics['heating']['setPointTemperature'] = Gauge('homematicip_heating_setpointtemperature_celsius', 'Homematic IP setpoint temperature of a room', ['id', 'room'])
    metrics['heating']['actualTemperature'] = Gauge('homematicip_heating_actualtemperature_celsius', 'Homematic IP actual temperature of a room', ['id', 'room'])


def getdata():
    global config
    global metrics
    global h

    if not h.get_current_state():
        if not h.get_current_state():
            if not h.get_current_state():
                return

    heating = metrics['heating']

    for group in h.groups:
        if group.groupType == 'META':
            for g in group.groups:
                if g.groupType == 'HEATING':
                    heating['setPointTemperature'].labels(id=g.id, room=g.label).set(g.setPointTemperature)
                    heating['actualTemperature'].labels(id=g.id, room=g.label).set(g.actualTemperature)