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
# $id application/model/relation/UsersGroupGoliatUser.py created on 2010-07-18 16:37:53.726449 by Goliat $
'''
Created on 2010-07-18 16:37:53.726449

@license: GPLv2
@copyright: © 2010 Open Phoenix IT SCA
@organization: Open Phoenix IT S.Coop.And
@author: Goliat
@contact: goliat@open-phoenix.com
@summary: UsersGroupGoliatUser Model Base Class
@version: 0.1
'''
from storm.base import Storm
from storm.locals import *
from storm import Undef

class UsersGroupGoliatUser(Storm):
    """Relational many2many object"""
    __storm_table__ = "users_group_goliat_user"
    __storm_primary__ = "users_group_id","goliat_user_id"
    users_group_id = Int()
    goliat_user_id = Int()
