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
# $id application/model/base/FederacionBase.py created on 2010-07-18 17:14:40.190876 by Goliat $
'''
Created on 2010-07-18 17:14:40.190876

@license: GPLv2
@copyright: © 2010 Open Phoenix IT SCA
@organization: Open Phoenix IT S.Coop.And
@author: Goliat
@contact: goliat@open-phoenix.com
@summary: FederacionBase Model Base Class
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
from application.model.base.UsersGroupBase import UsersGroupBase
from application.model.base.AddressBase import AddressBase

class FederacionBase(Storm):
    __storm_table__="federacion"

    id=Int(primary=True, value=Undef, allow_none=False)
    name=Unicode(primary=False, value=Undef, allow_none=False)
    comite_id=Int(primary=False, value=Undef, allow_none=True)
    comite=Reference(comite_id, "UsersGroup.id")
    address=ReferenceSet("Federacion.id", "Address.id")

    store=Store(Database().get_database())

    def __init__(self):
        """Storm object representation of SQL table federacion
        
        This method will be overriden by Federacion class
        """
        pass

    @staticmethod
    def get_model_info():
        """Returns a dict containing the model scheme information."""
        return Model().get_model_info(FederacionBase)

    @staticmethod
    def view():
        """Returns a list of every row at model."""
        return Model().view(FederacionBase)

    @staticmethod
    def create(controller):
        """Create a new FederacionBase object and returns it."""
        data=controller._request.args.get('data')
        if data==None:
            controller._sendback({'success' : False, 'error' : 'No data received from UI.'})
        else:
            object=json.loads(data[0])
            result, msg=Model().isValidObject(object, FederacionBase)
            if not result:
                controller._sendback({'success' : False, 'error' : msg})
                return

            obj=FederacionBase()
            return Model().create(Model().generate_object(obj, object), FederacionBase, controller)

    @staticmethod
    def update(controller):
        """Update an object."""
        data=controller._request.args.get('data')
        if data==None:
            controller._sendback({'success' : False, 'error' : 'No data received from UI.'})
        else:
            object=json.loads(data[0])
            result, msg=Model().is_valid_object(object, FederacionBase)
            if not result:
                controller._sendback({'success' : False, 'error' : msg})
                return

            return Model().update(object, FederacionBase, controller)

    @staticmethod
    def destroy(controller):
        """Destroy an object."""
        id=controller._request.args.get('id')
        if id==None:
            controller._sendback({'success' : False, 'error' : 'No data received from UI.'})
        else:
            return Model().destroy(int(id[0]), FederacionBase, controller)

    @staticmethod
    def get(id=None, ref=None):
        """Get a row."""
        if not id:
            return {'success' : False, 'error' : 'No data received from UI.'}
        else:
            if ref:
                model='{0}Base'.format(ref.capitalize())
                model=eval(model)
                return Model().get(int(id), model)
            else:
                return Model().get(int(id), FederacionBase)

    @staticmethod
    def search(controller):
        """Perform a very basic search."""
        data=controller._request.args.get('data')
        if data==None:
            controller._sendback({'success' : False, 'error' : 'No data received from UI.'})
        else:
            args=json.loads(data[0])
            c=''
            for rec in args:
                for k, v in rec.iteritems():
                    c+='{0} == {1},'.format("EmployeeBase."+k, v)
            return Model().search(FederacionBase, controller, eval(c))
