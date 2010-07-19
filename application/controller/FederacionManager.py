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
import json

from goliat.webserver import gresource
from goliat.session.user import IUser, UserData
from goliat import http
from application.model.Federacion import Federacion

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

    def read(self, request, **kwargs):
        """
        Returns a sindicatos list.
        """

        Federacion.view().addCallback(self._read, request)
        return server.NOT_DONE_YET

    def _read(self, result, request):
        if len(result) is 0:
            self.sendback(request, {'success' : False, 'message' : 'No hay datos de la Federación Local'})
        else:
            result[0]['success']=True
            self.sendback(request, result[0])

    def get_comite(self, request, **kwargs):
        """
        Returns the Comite Members.
        """

        def cb_comite_dump(results):
            self._get_all_comites(request, results)

        def cb_dump(results):
            if not results:
                self.sendback(request, {'success' : False, 'message' : 'No existen datos del Comité de la Federación Local'})
            else:
                results.comite.addCallback(cb_comite_dump)

        def cb_read(results):
            if len(results) is 0:
                self.sendback(request, {'success' : False, 'message' : 'No existen datos de la Federación Local'})
            else:
                Federacion.store.get(Federacion, results[0]['id']).addCallback(cb_dump)

        if not kwargs.get('id', None):
            Federacion.view().addCallback(cb_read)
        else:
            cb_read([int(kwargs['id'][0])])
        return server.NOT_DONE_YET

    def _get_all_comites(self, request, users_group):
        """Returns all comites from user group."""

        from application.model.UsersGroup import UsersGroup
        from goliat.session.user import UserProfileProxy

        def cb_order(users):
            rusers=[]
            for user in users:
                uprofile=UserProfileProxy()
                uprofile.load(user.id)
                rusers.append({
                    'id'       : user.id,
                    'name'     : user.username,
                    'nia'      : uprofile.nia,
                    'comite'   : uprofile.comite,
                    'title'    : uprofile.title
                })
            self.sendback(request, {'success' : True, 'people' :  rusers, 'group' :
                { 'name' : users_group.name, 'id' : users_group.id, 'desc' : users_group.description }})

        def cb_read(results):
            results.user_ids.all().addCallback(cb_order)

        ugroup=UsersGroup()
        ugroup.store.get(UsersGroup, users_group.id).addCallback(cb_read)

    def get_register_path(self):
        """Returns the module resource registration path."""
        return "federacionmanager"

    def get_schema_model(self):
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
