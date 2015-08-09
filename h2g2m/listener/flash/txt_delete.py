from h2g2m.lib.bus.listener_base import Listener


class FlashTxtDeletedListener(Listener):
    def __call__(self, event):
        ':type event: TxtDeletedEvent'
        event.request.session.flash(('success', u'Text successfully deleted.'))
