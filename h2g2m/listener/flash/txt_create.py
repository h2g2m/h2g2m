from h2g2m.lib.bus.listener_base import Listener


class FlashTxtCreatedListener(Listener):
    def __call__(self, event):
        ':type event: TxtCreatedEvent'
        event.request.session.flash(('success', u'Text successfully created.'))

