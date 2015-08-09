# -*- coding: utf-8 -*-
from pyramid.path import AssetResolver
from pyramid.response import Response
from pyramid.view import view_config
import json
from ..lib.repositories import LanguageRepository


@view_config(
    route_name='language.json',
)
def view(request):
    return Response(json.dumps(request.container['language_repository'].find_all()))
