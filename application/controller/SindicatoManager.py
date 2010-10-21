# -*- coding: utf-8 -*-
##
# Goliat: The Twisted and ExtJS Web Framework
# Copyright (C) 2010 Open Phoenix IT
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA
##
# $id application/controller/SindicatoManager.py created on 2010-07-18 17:25:19.672724 by Goliat $
'''
Created on 2010-07-18 17:25:19.672724

@license: GPLv2
@copyright: © 2010 Open Phoenix IT SCA
@organization: Open Phoenix IT S.Coop.And
@author: Goliat
@contact: goliat@open-phoenix.com
@summary: SindicatoManager Module
@version: 0.1
'''
from twisted.web import server
import json

from goliat.webserver import gresource
from goliat.session.user import IUser, UserData
from goliat import http
from application.model.Sindicato import Sindicato

class SindicatoManager(gresource.GResource):
    """SindicatoManager class:"""


    def __init__(self):
        """Constructor:
        
        ADD YOUR INITIALIZATION CODE HERE
        """
        gresource.GResource.__init__(self)

    def render_GET(self, request):
        """Process GET Request."""

        return json.dumps({'success' : False, 'error' : 'Not implemented yet.'})

    def render_POST(self, request):
        """Process POST Request."""

        return json.dumps({'success' : False, 'error' : 'Not implemented yet.'})

    def save(self, request, **kwargs):
        """Save sindicato data."""

        data={
            'name' : unicode(kwargs.get('name')[0].decode('utf8')),
            'description' : unicode(kwargs.get('description')[0].decode('utf8'))
        }
        if kwargs.get('comite_id')[0]!='':
            data['comite_id']=int(kwargs.get('comite_id'))
        if kwargs.get('id')[0]!='':
            data['id']=int(kwargs.get('id')[0])

        if not kwargs.get('id', None) or kwargs.get('id')[0]=='':
            Sindicato.create(data).addCallback(self._save, request)
        else:
            Sindicato.update(data).addCallback(self._save, request)

        return server.NOT_DONE_YET

    def _save(self, result, request):
        self.sendback(request, {'success' : True})

    def get_register_path(self):
        """Returns the module resource registration path."""
        return "sindicatomanager"

    def get_schema_model(self, request, **kwargs):
        """Return the schema model Sindicato architecture."""
        model_schema, model_view=Sindicato.get_model_info()
        if model_schema==None:
            return json.dumps({
                "success" : False,
                "error" : "Unable to fetch a schema for model sindicato"
            })

        return json.dumps({
            "success" : True,
            "model" : model_schema,
            "view" : model_view
        })
