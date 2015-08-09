class Bus(dict):

    def subscribe(self, event_class, listener):
        if event_class not in self:
            self[event_class] = []
        self[event_class].append(listener)

    def fire(self, event):
        for listener in self[event.__class__]:
            listener(event)
