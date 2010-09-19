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
# $id application/model/base/UserProfileBase.py created on 2010-07-18 15:21:02.501715 by Goliat $
'''
Created on 2010-07-18 15:21:02.501715

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

#from goliat.database.store import Store
from goliat.database.reference import Reference, ReferenceSet
from goliat.database import Database
from goliat.database.model import Model
from goliat.session.user import User

class UserProfileBase(Storm):
    __storm_table__="user_profile"

    id=Int(primary=True, value=Undef, allow_none=False)
    user_id=Int(primary=False, value=Undef, allow_none=False)
    nia=Int(primary=False, value=Undef, allow_none=False)
    comite=Bool(primary=False, value=False)
    title=Unicode(primary=False, value="Militante")
    validation_key=Unicode(primary=False, value=Undef, allow_none=True)
    validated=Bool(primary=False, value=False, allow_none=True)
    user=Reference(user_id, "User.id")

    #store=Store(Database().get_database())

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
    def view(controller):
        """Returns a list of every row at model."""
        return Model().view(UserProfileBase, controller)

    @staticmethod
    def create(controller):
        """Create a new UserProfileBase object and returns it."""
        data=controller._request.args.get('data')
        if data==None:
            controller._sendback({'success' : False, 'error' : 'No data received from UI.'})
        else:
            object=json.loads(data[0])
            result, msg=Model().isValidObject(object, UserProfileBase)
            if not result:
                controller._sendback({'success' : False, 'error' : msg})
                return

            obj=UserProfileBase()
            return Model().create(Model().generate_object(obj, object), UserProfileBase, controller)

    @staticmethod
    def update(controller):
        """Update an object."""
        data=controller._request.args.get('data')
        if data==None:
            controller._sendback({'success' : False, 'error' : 'No data received from UI.'})
        else:
            object=json.loads(data[0])
            result, msg=Model().is_valid_object(object, UserProfileBase)
            if not result:
                controller._sendback({'success' : False, 'error' : msg})
                return

            return Model().update(object, UserProfileBase, controller)

    @staticmethod
    def destroy(controller):
        """Destroy an object."""
        id=controller._request.args.get('id')
        if id==None:
            controller._sendback({'success' : False, 'error' : 'No data received from UI.'})
        else:
            return Model().destroy(int(id[0]), UserProfileBase, controller)

    @staticmethod
    def get(controller):
        """Get a row."""
        id=controller._request.args.get('id')
        if id==None:
            controller._sendback({'success' : False, 'error' : 'No data received from UI.'})
        else:
            if controller._request.args.get('ref')!=None:
                model='{0}Base'.format(controller._request.args.get('ref')[0].capitalize())
                model=eval(model)
                return Model().get(int(id[0]), model, controller)
            else:
                return Model().get(int(id[0]), UserProfileBase, controller)

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
