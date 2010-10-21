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
# $id application/model/base/CargoBase.py created on 2010-10-20 00:03:43.131970 by Goliat $
'''
Created on 2010-10-20 00:03:43.131970

@license: GPLv2
@copyright: © 2010 Open Phoenix IT SCA
@organization: Open Phoenix IT S.Coop.And
@author: Goliat
@contact: goliat@open-phoenix.com
@summary: CargoBase Model Base Class
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

class CargoBase(Storm):
    __storm_table__ = "cargo"
    
    id = Int(primary=True, value=Undef, allow_none=False)
    name = Unicode(primary=False, value=Undef, allow_none=False)
    
    store = Store(Database().get_database())
    
    def __init__(self):
        """Storm object representation of SQL table cargo
        
        This method will be overriden by Cargo class
        """
        pass         

    @staticmethod
    def get_model_info():
        """Returns a dict containing the model scheme information."""
        return Model().get_model_info(CargoBase)

    @staticmethod
    def view():
        """Returns a list of every row at model."""
        return Model().view(CargoBase)     
    
    @staticmethod
    def create(data):
        """Create a new CargoBase object and returns it."""
        
        if not data:
            return defer.succeed({'success' : False, 'message' : 'No data received from UI.'})            
                    
        object = data
        result, msg = Model().is_valid_object(object, CargoBase)
        if not result:            
            return defer.succeed({'success' : False, 'message' : msg})            
        obj = CargoBase()            
        return Model().create(Model().generate_object(obj, object), CargoBase, data)
    
    @staticmethod
    def update(data):
        """Update an object."""
                
        if not data:
            return defer.succeed({'success' : False, 'message' : 'No data received from UI.'})            
        
        return Model().update(CargoBase, data)
    
    @staticmethod
    def destroy(id):
        """Destroy an object."""
        
        if not id:
            return defer.succeed({'success' : False, 'message' : 'No data received from UI.'})            
        else:            
            return Model().destroy(int(id[0]), CargoBase)

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
                return Model().get(int(id), CargoBase)

    @staticmethod
    def search(data):
        """Perform a very basic search."""
        
        objects = tuple([eval(p) for p in eval(data['objects'])])
        where = eval(data['conditions'])
        
        return Model().search(objects, where)
    