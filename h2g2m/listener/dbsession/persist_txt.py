from h2g2m.lib.bus.listener_base import Listener


class PersistTxtListener(Listener):
    def __call__(self, event):
        ':type event: TxtCreatedEvent|TxtEditedEvent'
        event.DBSession.add(event.txt)
        event.DBSession.flush()
