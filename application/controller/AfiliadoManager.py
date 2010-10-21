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
# $id application/controller/AfiliadoManager.py created on 2010-10-17 23:13:40.505052 by Goliat $
'''
Created on 2010-10-17 23:13:40.505052

@license: GPLv2
@copyright: © 2010 Open Phoenix IT SCA
@organization: Open Phoenix IT S.Coop.And
@author: Goliat
@contact: goliat@open-phoenix.com
@summary: AfiliadoManager Module
@version: 0.1
'''
from twisted.web import server
from twisted.internet import defer
import json

from goliat.webserver import gresource
from goliat.session.user import IUser, UserData
from goliat import http
from application.model.UserProfile import UserProfile

class AfiliadoManager(gresource.GResource):
    """AfiliadoManager class:"""


    def __init__(self):
        """Constructor:
        
        ADD YOUR INITIALIZATION CODE HERE
        """
        gresource.GResource.__init__(self)

    def render_GET(self, request):
        """Process GET Request."""

        return json.dumps({'success' : False, 'message' : 'Not implemented yet.'})

    def render_POST(self, request):
        """Process POST Request."""

        return json.dumps({'success' : False, 'message' : 'Not implemented yet.'})

    def view(self, request, **kwargs):
        """Performs read CRUD action."""

        def cb_sendback(results):
            users=[]
            for user in results:
                users.append(user[1])

            self.sendback(request, {'success' : True, 'data' : users})

        def cb_get_data(results):
            dl=defer.DeferredList(results).addCallback(cb_sendback)

        UserProfile.get_list().addCallback(cb_get_data)

        return server.NOT_DONE_YET

    def create(self, request, **kwargs):
        """Performs create CRUD action."""

        def cb_sendback(result):
            self.sendback(request, result)

        UserProfile.create(kwargs).addCallback(cb_sendback)

        return server.NOT_DONE_YET

    def update(self, request, **kwargs):
        """Performs update CRUD action."""

        def cb_sendback(result):
            self.sendback(request, result)

        UserProfile.update(kwargs).addCallback(cb_sendback)

        return server.NOT_DONE_YET

    def destroy(self, request, **kwargs):
        """Performs destroy CRUD action."""

        def cb_sendback(result):
            self.sendback(request, result)

        UserProfile.destroy(int(kwargs.get('id')[0])).addCallback(cb_sendback)

        return server.NOT_DONE_YET

    def get(self, request, **kwargs):
        """Performs an extra read CRUD action."""

        def cb_sendback(result):
            self.sendback(request, result)

        UserProfile.get(int(kwargs.get('id')[0]), kwargs.get('ref', None)).addCallback(cb_sendback)

        return server.NOT_DONE_YET

    def search(self, request, **kwargs):
        """Performs a search."""

        def cb_sendback(result):
            self.sendback(request, result)

        UserProfile.search(kwargs.get('object')[0], kwargs.get('condition')[0]).addCallback(cb_sendback)

        return server.NOT_DONE_YET

    def get_register_path(self):
        """Returns the module resource registration path."""
        return "afiliadomanager"

    def get_schema_model(self, request, **kwargs):
        """Return the schema model UserProfile architecture."""
        model_schema, model_view=UserProfile.get_model_info()
        if model_schema==None:
            return json.dumps({
                "success" : False,
                "error" : "Unable to fetch a schema for model user_profile"
            })

        return json.dumps({
            "success" : True,
            "model" : model_schema,
            "view" : model_view
        })
