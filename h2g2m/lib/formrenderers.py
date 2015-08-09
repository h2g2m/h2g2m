# -*- coding: utf-8 -*-
from pyramid_simpleform.renderers import FormRenderer as OldFormRenderer
from webhelpers.html import tags

class FormRenderer(OldFormRenderer):
    def checkbox(self, name, value="1", checked=False, label=None, id=None, 
                 **attrs):
        """
        Outputs checkbox input.
        """
        id = id or name
        return tags.checkbox(name, value, checked, label, id, **attrs)
        return tags.checkbox(name, value, self.value(name), label, id, **attrs) # original line
