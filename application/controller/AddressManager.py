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
# $id application/controller/AddressManager.py created on 2010-07-18 17:25:31.066512 by Goliat $
'''
Created on 2010-07-18 17:25:31.066512

@license: GPLv2
@copyright: © 2010 Open Phoenix IT SCA
@organization: Open Phoenix IT S.Coop.And
@author: Goliat
@contact: goliat@open-phoenix.com
@summary: AddressManager Module
@version: 0.1
'''
from twisted.web import server
import json

from goliat.webserver import gresource
from goliat.session.user import IUser, UserData
from goliat import http
from application.model.Address import Address

class AddressManager(gresource.GResource):
    """AddressManager class:"""
    
    
    def __init__(self):
        """Constructor:
        
        ADD YOUR INITIALIZATION CODE HERE
        """
        gresource.GResource.__init__(self)
    
    def render_GET(self, request):
        """Process GET Request."""
        self._request = request
        _act = request.args.get('act')
        if _act != None and 'getSchemaModel' in _act:            
            return self.get_schema_model()
        elif _act != None and 'view' in _act:
            Address.view(self)
            return server.NOT_DONE_YET
        elif _act != None and 'get' in _act:
            Address.get(self)
            return server.NOT_DONE_YET
        else:
            return json.dumps(
                {'success' : False, 'error' : 'Not implemented yet.'})
                    
    
    def render_POST(self, request):
        """Process POST Request."""
        self._request = request
        _act = request.args.get('act')
        if _act != None and 'create' in _act:
            Address.create(self)
            return server.NOT_DONE_YET
        elif _act != None and 'update' in _act:
            Address.update(self)
            return server.NOT_DONE_YET
        elif _act != None and 'destroy' in _act:
            Address.destroy(self)
            return server.NOT_DONE_YET
        else:
            return json.dumps(
                {'success' : False, 'error' : 'Not implemented yet.'})
            
    
    def get_register_path(self):
        """Returns the module resource registration path."""
        return "addressmanager"
    
    def get_schema_model(self): 
        """Return the schema model Address architecture.""" 
        model_schema, model_view = Address.get_model_info() 
        if model_schema == None: 
            return json.dumps({
                "success" : False,
                "error" : "Unable to fetch a schema for model address"
            })        
                
        return json.dumps({
            "success" : True,
            "model" : model_schema,
            "view" : model_view
        })
        