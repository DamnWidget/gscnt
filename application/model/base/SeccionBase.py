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
# $id application/model/base/SeccionBase.py created on 2010-10-24 23:00:15.612262 by Goliat $
'''
Created on 2010-10-24 23:00:15.612262

@license: GPLv2
@copyright: © 2010 Open Phoenix IT SCA
@organization: Open Phoenix IT S.Coop.And
@author: Goliat
@contact: goliat@open-phoenix.com
@summary: SeccionBase Model Base Class
@version: 0.1
'''
import json
from storm.base import Storm
from storm.locals import *
from storm import Undef

from goliat.database.store import Store
from goliat.database.reference import Reference, ReferenceSet
from goliat.database import Database
from goliat.database.model import Model
from twisted.internet import defer
from goliat.session.user import UserData as GoliatUser
from application.model.base.UsersGroupBase import UsersGroupBase
from application.model.base.SindicatoBase import SindicatoBase
from application.model.base.AddressBase import AddressBase

class SeccionBase(Storm):
    __storm_table__ = "seccion"
    
    id = Int(primary=True, value=Undef, allow_none=False)
    name = Unicode(primary=False, value=Undef, allow_none=False)
    description = Unicode(primary=False, value=Undef, allow_none=True)
    active = Bool(primary=False, value=True, allow_none=True)
    sindicato_id = Int(primary=False, value=Undef, allow_none=True)
    comite_id = Int(primary=False, value=Undef, allow_none=True)
    user_ids = ReferenceSet("Seccion.id", "GoliatUser.id")
    comite = Reference(comite_id, "UsersGroup.id")
    sindicato = Reference(sindicato_id, "Sindicato.id")
    address = ReferenceSet("Seccion.id", "Address.id")
    
    store = Store(Database().get_database())
    
    def __init__(self):
        """Storm object representation of SQL table seccion
        
        This method will be overriden by Seccion class
        """
        pass         

    @staticmethod
    def get_model_info():
        """Returns a dict containing the model scheme information."""
        return Model().get_model_info(SeccionBase)

    @staticmethod
    def view():
        """Returns a list of every row at model."""
        return Model().view(SeccionBase)     
    
    @staticmethod
    def create(data):
        """Create a new SeccionBase object and returns it."""
        
        if not data:
            return defer.succeed({'success' : False, 'message' : 'No data received from UI.'})            
                    
        object = data
        result, msg = Model().is_valid_object(object, SeccionBase)
        if not result:            
            return defer.succeed({'success' : False, 'message' : msg})            
        obj = SeccionBase()            
        return Model().create(Model().generate_object(obj, object), SeccionBase, data)
    
    @staticmethod
    def update(data):
        """Update an object."""
                
        if not data:
            return defer.succeed({'success' : False, 'message' : 'No data received from UI.'})            
        
        return Model().update(SeccionBase, data)
    
    @staticmethod
    def destroy(id):
        """Destroy an object."""
        
        if not id:
            return defer.succeed({'success' : False, 'message' : 'No data received from UI.'})            
        else:            
            return Model().destroy(int(id[0]), SeccionBase)

    @staticmethod
    def get(id, ref=None):
        """Get a row."""
                
        if not id:
            return defer.succeed({'success' : False, 'message' : 'No data received from UI.'})
        else:
            if ref:
                model = '{0}Base'.format(ref.capitalize())
                model = eval(model)
                return Model().get(int(id), model)            
            else:            
                return Model().get(int(id), SeccionBase)

    @staticmethod
    def search(data):
        """Perform a very basic search."""
        
        objects = tuple([eval(p) for p in eval(data['objects'])])
        where = eval(data['conditions'])
        
        return Model().search(objects, where)
    