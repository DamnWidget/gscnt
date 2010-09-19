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
# $id application/model/base/UsersGroupBase.py created on 2010-07-18 16:37:53.723173 by Goliat $
'''
Created on 2010-07-18 16:37:53.723173

@license: GPLv2
@copyright: © 2010 Open Phoenix IT SCA
@organization: Open Phoenix IT S.Coop.And
@author: Goliat
@contact: goliat@open-phoenix.com
@summary: UsersGroupBase Model Base Class
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
from goliat.session.user import UserData as GoliatUser
from application.model.relation.UsersGroupGoliatUser import UsersGroupGoliatUser

class UsersGroupBase(Storm):
    __storm_table__="users_group"

    id=Int(primary=True, value=Undef, allow_none=False)
    name=Unicode(primary=False, value=Undef, allow_none=False)
    description=Unicode(primary=False, value=Undef, allow_none=True)
    active=Bool(primary=False, value=True, allow_none=True)
    user_ids=ReferenceSet("UsersGroup.id", UsersGroupGoliatUser.users_group_id, UsersGroupGoliatUser.goliat_user_id, GoliatUser.id)

    store=Store(Database().get_database())

    def __init__(self):
        """Storm object representation of SQL table users_group
        
        This method will be overriden by UsersGroup class
        """
        pass

    @staticmethod
    def get_model_info():
        """Returns a dict containing the model scheme information."""
        return Model().get_model_info(UsersGroupBase)

    @staticmethod
    def view():
        """Returns a list of every row at model."""
        return Model().view(UsersGroupBase)

    @staticmethod
    def create(controller):
        """Create a new UsersGroupBase object and returns it."""
        data=controller._request.args.get('data')
        if data==None:
            controller._sendback({'success' : False, 'message' : 'No data received from UI.'})
        else:
            object=json.loads(data[0])
            result, msg=Model().isValidObject(object, UsersGroupBase)
            if not result:
                controller._sendback({'success' : False, 'message' : msg})
                return

            obj=UsersGroupBase()
            return Model().create(Model().generate_object(obj, object), UsersGroupBase, controller)

    @staticmethod
    def update(data):
        """Update an object."""
        return Model().update(UsersGroupBase, data)

    @staticmethod
    def destroy(id):
        """Destroy an object."""

        if not id:
            return {'success' : False, 'message' : 'No data received from UI.'}
        else:
            return Model().destroy(int(id[0]), UsersGroupBase)

    @staticmethod
    def get(id, ref=None):
        """Get a row."""
        if not id:
            return {'success' : False, 'message' : 'No data received from UI.'}
        else:
            if ref:
                model='{0}Base'.format(ref.capitalize())
                model=eval(model)
                return Model().get(int(id[0]), model)
            else:
                return Model().get(int(id[0]), UsersGroupBase)

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
            return Model().search(UsersGroupBase, controller, eval(c))
