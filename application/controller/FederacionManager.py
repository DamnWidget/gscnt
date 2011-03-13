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
# $id application/controller/FederacionManager.py created on 2010-07-18 16:50:30.030695 by Goliat $
'''
Created on 2010-07-18 16:50:30.030695

@license: GPLv2
@copyright: © 2010 Open Phoenix IT SCA
@organization: Open Phoenix IT S.Coop.And
@author: Goliat
@contact: goliat@open-phoenix.com
@summary: FederacionManager Module
@version: 0.1
'''
from twisted.web import server
from twisted.internet import defer
import json

from goliat.webserver import gresource
from goliat.session.user import IUser, UserData
from goliat import http
from application.model.Federacion import Federacion
from application.model.UsersGroup import UsersGroup
from application.model.Sindicato import Sindicato

class FederacionManager(gresource.GResource):
    """FederacionManager class:"""


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

    def add_secretario(self, request, **kwargs):
        """Adds a new secretario to the federacion."""

        print kwargs

    def read(self, request, **kwargs):
        """
        Returns the Federación data.
        """

        Federacion.view().addCallback(self._read, request)
        return server.NOT_DONE_YET

    def _read(self, result, request):

        def cb_read_group(group, data):
            data['success']=True
            data['group']={ 'name' : group.name, 'id' : group.id, 'desc' : group.description, 'active' : group.active }
            self.sendback(request, data)

        if len(result['data']) is 0:
            self.sendback(request, {'success' : False, 'message' : 'No hay datos de la Federación Local'})
        else:
            defer.succeed(UsersGroup.store.get(UsersGroup, result['data'][0]['comite_id'])).addCallback(cb_read_group, result['data'][0])

    def save(self, request, **kwargs):
        """Save federacion data."""

        if not kwargs.get('group_id', None) or int(kwargs.get('group_id')[0])==0:
            Federacion.create(kwargs).addCallback(self._save, request)
        else:
            Federacion.update(kwargs).addCallback(self._save, request)

        return server.NOT_DONE_YET

    def _save(self, result, request):
        self.sendback(request, result)

    def save_secretario(self, request, **kwargs):
        """
        Save a Comité Member.
        """

        def cb_sendback(result):
            self.sendback(request, result)

        Federacion.save_secretario(kwargs).addCallback(cb_sendback)

        return server.NOT_DONE_YET

    def remove_secretario(self, request, **kwargs):
        """
        Remove Comité Members.
        """

        def cb_sendback(result):
            self.sendback(request, result)

        user_ids=[int(p) for p in kwargs.get('secretarios')]
        Federacion.remove_secretario(user_ids).addCallback(cb_sendback)

        return server.NOT_DONE_YET

    def get_comite(self, request, **kwargs):
        """
        Returns the Comite Members.
        """

        def cb_get_data(results):
            if type(results) is dict:
                self.sendback(request, results)
            else:
                people=list()
                for user in results:
                    people.append(user)

                self.sendback(request, {'success' : True, 'people' : people})

        Federacion.get_comite_members().addCallback(cb_get_data)

        return server.NOT_DONE_YET

    def check_sindicatos(self, request, **kwargs):
        """Check if this federacion has sindicatos"""

        def cb_read(sindicatos):
            if not len(sindicatos):
                self.sendback(request, {'success' : False, 'message' : 'No hay sindicatos federados a la Federación Local'})
            else:
                self.sendback(request, sindicatos)

        Sindicato.view().addCallback(cb_read)

        return server.NOT_DONE_YET

    def get_register_path(self):
        """Returns the module resource registration path."""
        return "federacionmanager"

    def get_schema_model(self, request, **kwargs):
        """Return the schema model Federacion architecture."""
        model_schema, model_view=Federacion.get_model_info()
        if model_schema==None:
            return json.dumps({
                "success" : False,
                "error" : "Unable to fetch a schema for model federacion"
            })

        return json.dumps({
            "success" : True,
            "model" : model_schema,
            "view" : model_view
        })
