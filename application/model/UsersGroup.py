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
# $id application/model/UsersGroup.py created on 2010-07-18 17:25:42.723711 by Goliat $
'''
Created on 2010-07-18 17:25:42.723711

@license: GPLv2
@copyright: © 2010 Open Phoenix IT SCA
@organization: Open Phoenix IT S.Coop.And
@author: Goliat
@contact: goliat@open-phoenix.com
@summary: UsersGroup Model
@version: 0.1
'''
from storm.variables import *
from twisted.internet import defer
from goliat.database.model import Model
import json
from application.model.base.UsersGroupBase import UsersGroupBase

class UsersGroup(UsersGroupBase):
    """This class inherits from UsersGroupBase class"""

    def __init__(self):
        """Consructor:
        
        ADD HERE YOUR INITIALIZATION CODE
        """
        UsersGroupBase.__init__(self)

    @staticmethod
    def create(data):
        """Creates a new UsersGroup object."""

        if not data:
            return  defer.succeed({'success' : False, 'error' : 'No data received by frontend.'})

        object=data
        result, msg=Model().is_valid_object(object, UsersGroupBase)
        if not result:
            return defer.succeed({'success' : False, 'error' : msg})
        obj=UsersGroupBase()
        return Model().create(Model().generate_object(obj, object), UsersGroupBase)
