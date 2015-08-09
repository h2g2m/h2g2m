from h2g2m.lib.bus.listener_base import Listener


class FlashTxtEditedListener(Listener):
    def __call__(self, event):
        ':type event: TxtEditedEvent'
        event.request.session.flash(('success', u'Text successfully edited.'))
