from beautifulhue.api import Bridge

class LightGateway:
    def __init__(self):
        self.bridge = Bridge(device={'ip':'192.168.1.17'}, user={'name':'kasra-hue-music-user'})

    def on(self, light_ids):
        for light_id in light_ids:
            resource = {'which': light_id, 'data': {'state': {'on': True, 'transitiontime': 0}}}
            self.bridge.light.update(resource)

    def brightness(self, light_ids, brightness):
        for light_id in light_ids:
            resource = {'which': light_id, 'data': {'state': {'bri': brightness, 'transitiontime': 0}}}
            self.bridge.light.update(resource)

    def update_one(self, light_id, hue):
        resource = {
            'which': light_id,
            'data': {'state': {'hue': hue, 'transitiontime': 0}}
        }
        self.bridge.light.update(resource)

    def update(self, light_ids, hue):
        for light_id in light_ids:
            self.update_one(light_id, hue)
