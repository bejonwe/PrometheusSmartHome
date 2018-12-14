from prometheus_client import Gauge
from homematicip.home import Home


def init(c = []):
    global config
    global metrics
    global h

    config = c

    h = Home()
    h.set_auth_token(config["authtoken"])
    h.init(config["accesspointid"])

    metrics = {}
    metrics['heating'] = {}
    metrics['heating']['setPointTemperature'] = Gauge('homematicip_heating_setpointtemperature_celsius', 'Homematic IP setpoint temperature of a room', ['id', 'room'])
    metrics['heating']['actualTemperature'] = Gauge('homematicip_heating_actualtemperature_celsius', 'Homematic IP actual temperature of a room', ['id', 'room'])
    metrics['heating']['boostmode'] = Gauge('homematicip_heating_boostmode', 'Homematic IP wether boost mode is on or off', ['id', 'room'])
    metrics['heating']['ecomode'] = Gauge('homematicip_heating_ecomode', 'Homematic IP wether eco mode is on or off', ['id', 'room'])
    metrics['heating']['partymode'] = Gauge('homematicip_heating_partymode', 'Homematic IP wether party mode is on or off', ['id', 'room'])
    metrics['heating']['humidity'] = Gauge('homematicip_heating_humidity_percent', 'Homematic IP current relative humidity in percent', ['id', 'room'])

    metrics['heating']['lowbattery'] = Gauge('homematicip_heating_lowbattery', 'Homematic IP wether the battery is low or not', ['id', 'name', 'room', 'devicetype', 'modeltype'])
    metrics['heating']['reachable'] = Gauge('homematicip_heating_reachable', 'Homematic IP wether the device is reachable or not', ['id', 'name', 'room', 'devicetype', 'modeltype'])

    metrics['heating']['valveposition'] = Gauge('homematicip_heating_valveposition', 'Homematic IP position of the valve', ['id', 'name', 'room', 'modeltype'])
    metrics['heating']['windowState'] = Gauge('homematicip_heating_windowstate', 'Homematic IP wether the window is open or closed', ['id', 'name', 'room', 'modeltype'])

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
                    if g.actualTemperature is not None:
                        heating['actualTemperature'].labels(id=g.id, room=g.label).set(g.actualTemperature)
                    if g.humidity is not None:
                        heating['humidity'].labels(id=g.id, room=g.label).set(g.humidity)

                    if g.windowState is not None:
                        if g.windowState == 'CLOSED':
                            heating['windowState'].labels(id=g.id, room=g.label, name=g.label, modeltype='ROOM').set(0)
                        else:
                            heating['windowState'].labels(id=g.id, room=g.label, name=g.label, modeltype='ROOM').set(1)

                    if g.boostMode:
                        heating['boostmode'].labels(id=g.id, room=g.label).set(1)
                    else:
                        heating['boostmode'].labels(id=g.id, room=g.label).set(0)

                    if g.controlMode == 'ECO':
                        heating['ecomode'].labels(id=g.id, room=g.label).set(1)
                    else:
                        heating['ecomode'].labels(id=g.id, room=g.label).set(0)

                    if g.partyMode:
                        heating['partymode'].labels(id=g.id, room=g.label).set(1)
                    else:
                        heating['partymode'].labels(id=g.id, room=g.label).set(0)

                    for d in g.devices:
                        if d.lowBat:
                            heating['lowbattery'].labels(id=g.id, name=d.label, room=g.label, devicetype=d.deviceType, modeltype=d.modelType).set(1)
                        else:
                            heating['lowbattery'].labels(id=g.id, name=d.label, room=g.label, devicetype=d.deviceType, modeltype=d.modelType).set(0)

                        if d.unreach:
                            heating['reachable'].labels(id=g.id, name=d.label, room=g.label, devicetype=d.deviceType,
                                                         modeltype=d.modelType).set(0)
                        else:
                            heating['reachable'].labels(id=g.id, name=d.label, room=g.label, devicetype=d.deviceType,
                                                         modeltype=d.modelType).set(1)

                        if d.deviceType == 'HEATING_THERMOSTAT':
                            heating['valveposition'].labels(id=g.id, name=d.label, room=g.label, modeltype=d.modelType).set(d.valvePosition)
                        elif d.deviceType == 'SHUTTER_CONTACT':
                            if d.windowState == 'CLOSED':
                                heating['windowState'].labels(id=g.id, room=g.label, name=d.label, modeltype=d.modelType).set(0)
                            else:
                                heating['windowState'].labels(id=g.id, room=g.label, name=d.label, modeltype=d.modelType).set(1)
