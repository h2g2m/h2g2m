# -*- coding: utf-8 -*-
import formencode 
from ..models import DBSession
from sqlalchemy.orm.exc import NoResultFound

class FormSchema(formencode.Schema):
    filter_extra_fields = True
    allow_extra_fields = True

class IdExists(formencode.validators.FancyValidator):
    Table = None
    __unpackargs__ = ('*', 'Table')
    messages = {
        'id_does_not_exist'  : 'The id %(id)s does not exist. ',
        'id_does_not_belong' : 'The id %(id)s does not belong to you.'
    }
    def __init__(self, *args, **kw):
        super(formencode.validators.FancyValidator, self).__init__(*args, **kw)
        if len(self.Table) != 1: 
            raise TypeError('IdExists() should be called with a database class')
        self.Table = self.Table[0]

    def validate_python(self, id, state):
        try: 
            obj = DBSession.query(self.Table).filter_by(id=id).one()
            if hasattr(self,'usr') and hasattr(obj,'creator_id') and obj.creator_id != self.usr.id:
                raise formencode.Invalid(
                    self.message('id_does_not_belong', state, id=id), id, state
                )
        except NoResultFound: 
            raise formencode.Invalid(
                self.message('id_does_not_exist', state, id=id), id, state
            ) # TODO hier irgendwie herausfinden, auf welchem Feld dieser Validator aufgerufen wurde und nicht den fixen Feldnamen usr_id verwenden (bisher wird dieser Validator für die eMail-Verifizierung verwendet)
    
    def to_python(self, id, state):
        return int(id)

class Isbn(formencode.validators.String):
    pass # TODO: ISBN Validator schreiben
