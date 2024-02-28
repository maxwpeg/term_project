class Entity(object):
    def __init__(self, name, mission):
        self._name = name
        self._mission = mission

    @property
    def name(self):
        return self._name

    @property
    def mission(self):
        return self._mission