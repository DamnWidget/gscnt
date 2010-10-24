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
# $id application/model/UserProfile.py created on 2010-10-17 23:13:40.502370 by Goliat $
'''
Created on 2010-10-17 23:13:40.502370

@license: GPLv2
@copyright: © 2010 Open Phoenix IT SCA
@organization: Open Phoenix IT S.Coop.And
@author: Goliat
@contact: goliat@open-phoenix.com
@summary: UserProfile Model
@version: 0.1
'''
from zope.interface import implements
from storm.variables import *
from goliat.session.user import IUserProfile
from goliat.database.reference import ReferenceSet
from application.model.base.UserProfileBase import UserProfileBase
from application.model.Sindicato import Sindicato

class UserProfile(UserProfileBase):
    """This class inherits from UserProfileBase class"""

    sindicato=ReferenceSet("UserProfile.user_id", "SindicatoGoliatUser.goliat_user_id", "SindicatoGoliatUser.sindicato_id", "Sindicato.id")
    implements(IUserProfile)
    def __init__(self):
        """Consructor:
        
        ADD HERE YOUR INITIALIZATION CODE
        """
        UserProfileBase.__init__(self)

    @staticmethod
    def get_list():
        """Return a list of profile + user data."""

        def cb_find(result):
            return result.all().addCallback(cb_all)

        def cb_all(results):
            users=list()
            for res in results:
                users.append(res.user.addCallback(cb_prepare, res))

            return users

        def cb_prepare(user, profile):
            puser={'id' : profile.id, 'user_id' : user.id, 'name' : user.username, 'nia' : profile.nia}

            return puser

        return UserProfile.store.find(UserProfile, UserProfile.comite==False).addCallback(cb_find)
