from h2g2m.lib.bus.listener_base import Listener


class DeleteTxtListener(Listener):
    def __call__(self, event):
        ':type event: TxtDeletedEvent'
        event.DBSession.delete(event.txt)


