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
# $id application/controller/SeccionManager.py created on 2010-10-24 23:01:03.354172 by Goliat $
'''
Created on 2010-10-24 23:01:03.354172

@license: GPLv2
@copyright: © 2010 Open Phoenix IT SCA
@organization: Open Phoenix IT S.Coop.And
@author: Goliat
@contact: goliat@open-phoenix.com
@summary: SeccionManager Module
@version: 0.1
'''
from twisted.web import server
import json

from goliat.webserver import gresource
from goliat.session.user import IUser, UserData
from goliat import http
from application.model.Seccion import Seccion

class SeccionManager(gresource.GResource):
    """SeccionManager class:"""


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

        def cb_sendback(result):
            self.sendback(request, result)

        Seccion.view().addCallback(cb_sendback)

        return server.NOT_DONE_YET

    def create(self, request, **kwargs):
        """Performs create CRUD action."""

        def cb_sendback(result):
            self.sendback(request, result)

        Seccion.create(eval(kwargs.get('data')[0])).addCallback(cb_sendback)

        return server.NOT_DONE_YET

    def update(self, request, **kwargs):
        """Performs update CRUD action."""

        def cb_sendback(result):
            self.sendback(request, result)

        Seccion.update(eval(kwargs.get('data')[0])).addCallback(cb_sendback)

        return server.NOT_DONE_YET

    def destroy(self, request, **kwargs):
        """Performs destroy CRUD action."""

        def cb_sendback(result):
            self.sendback(request, result)

        Seccion.destroy(kwargs.get('data')).addCallback(cb_sendback)

        return server.NOT_DONE_YET

    def get(self, request, **kwargs):
        """Performs an extra read CRUD action."""

        def cb_sendback(result):
            self.sendback(request, result)

        Seccion.get(int(kwargs.get('id')[0]), kwargs.get('ref', None)).addCallback(cb_sendback)

        return server.NOT_DONE_YET

    def search(self, request, **kwargs):
        """Performs a search."""

        def cb_sendback(result):
            self.sendback(request, result)

        Seccion.search(kwargs.get('object')[0], kwargs.get('condition')[0]).addCallback(cb_sendback)

        return server.NOT_DONE_YET

    def get_register_path(self):
        """Returns the module resource registration path."""
        return "seccionmanager"

    def get_schema_model(self, request, **kwargs):
        """Return the schema model Seccion architecture."""
        model_schema, model_view=Seccion.get_model_info()
        if model_schema==None:
            return json.dumps({
                "success" : False,
                "error" : "Unable to fetch a schema for model seccion"
            })

        return json.dumps({
            "success" : True,
            "model" : model_schema,
            "view" : model_view
        })
