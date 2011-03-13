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
# $id application/model/base/UserProfileBase.py created on 2010-10-17 16:09:25.092322 by Goliat $
'''
Created on 2010-10-17 16:09:25.092322

@license: GPLv2
@copyright: © 2010 Open Phoenix IT SCA
@organization: Open Phoenix IT S.Coop.And
@author: Goliat
@contact: goliat@open-phoenix.com
@summary: UserProfileBase Model Base Class
@version: 0.1
'''
import json
from storm.base import Storm
from storm.locals import *
from storm import Undef
from storm.store import Store
from storm.references import Reference, ReferenceSet

from goliat.database import Database
from goliat.database.model import Model
from twisted.internet import defer
from goliat.session.user import UserData
from application.model.base.AddressBase import AddressBase

class UserProfileBase(Storm):
    __storm_table__="user_profile"

    id=Int(primary=True, value=Undef, allow_none=False)
    user_id=Int(primary=False, value=Undef, allow_none=False)
    nia=Int(primary=False, value=Undef, allow_none=False)
    comite=Bool(primary=False, value=False, allow_none=True)
    title=Unicode(primary=False, value='Militante', allow_none=True)
    validation_key=Unicode(primary=False, value=Undef, allow_none=True)
    validated=Bool(primary=False, value=False, allow_none=True)
    user=Reference(user_id, UserData.id)
    address=ReferenceSet("UserProfile.id", "Address.id")

    store=Store(Database().get_database())

    def __init__(self):
        """Storm object representation of SQL table user_profile
        
        This method will be overriden by UserProfile class
        """
        pass

    @staticmethod
    def get_model_info():
        """Returns a dict containing the model scheme information."""
        return Model().get_model_info(UserProfileBase)

    @staticmethod
    def view():
        """Returns a list of every row at model."""
        return Model().view(UserProfileBase)

    @staticmethod
    def create(data):
        """Create a new UserProfileBase object and returns it."""

        if not data:
            return defer.succeed({'success' : False, 'message' : 'No data received from UI.'})

        object=data
        result, msg=Model().is_valid_object(object, UserProfileBase)
        if not result:
            return defer.succeed({'success' : False, 'message' : msg})
        obj=UserProfileBase()
        return Model().create(Model().generate_object(obj, object), UserProfileBase)

    @staticmethod
    def update(data):
        """Update an object."""

        if not data:
            return defer.succeed({'success' : False, 'message' : 'No data received from UI.'})

        return Model().update(UserProfileBase, data)

    @staticmethod
    def destroy(id):
        """Destroy an object."""

        if not id:
            return defer.succeed({'success' : False, 'message' : 'No data received from UI.'})
        else:
            return Model().destroy(int(id[0]), UserProfileBase)

    @staticmethod
    def get(id, ref=None):
        """Get a row."""

        if not id:
            return defer.succeed({'success' : False, 'message' : 'No data received from UI.'})
        else:
            if ref:
                model='{0}Base'.format(ref.capitalize())
                model=eval(model)
                return Model().get(int(id), model)
            else:
                return Model().get(int(id), UserProfileBase)

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
            return Model().search(UserProfileBase, controller, eval(c))
