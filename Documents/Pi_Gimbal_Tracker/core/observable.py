class Observable:
    def __init__(self, value=None):
        self._value = value
        self._observers = []

    def subscribe(self, observer):
        self._observers.append(observer)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        if self._value != new_value:
            self._value = new_value
            for observer in self._observers:
                observer(self._value)