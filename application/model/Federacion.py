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
# $id application/model/Federacion.py created on 2010-07-18 16:50:30.027144 by Goliat $
'''
Created on 2010-07-18 16:50:30.027144

@license: GPLv2
@copyright: © 2010 Open Phoenix IT SCA
@organization: Open Phoenix IT S.Coop.And
@author: Goliat
@contact: goliat@open-phoenix.com
@summary: Federacion Model
@version: 0.1
'''
from storm.variables import *
from twisted.internet import defer
from goliat.database.model import Model
from application.model.base.FederacionBase import FederacionBase

class Federacion(FederacionBase):
    """This class inherits from FederacionBase class"""

    def __init__(self):
        """Consructor:
        
        ADD HERE YOUR INITIALIZATION CODE
        """
        FederacionBase.__init__(self)

    @staticmethod
    def create(data):
        """Creates a new Federacion object and a Users Group for its comite"""

        from application.model.UsersGroup import UsersGroup

        ugroup=UsersGroup()
        ugroup.name=unicode(data.get('group_name')[0].decode('utf8'))
        ugroup.description=unicode(data.get('group_desc')[0].decode('utf8'))
        ugroup.active=True

        Federacion.store.add(ugroup)
        Federacion.store.commit()

        federacion=Federacion()
        federacion.name=unicode(data.get('name')[0].decode('utf8'))
        federacion.comite_id=ugroup.id
        federacion.store.add(federacion)
        federacion.store.commit()
        return defer.succeed({'success' : True})

    @staticmethod
    def update(data):
        """Updates a Federacion object and the Users Group of its comite"""

        from application.model.UsersGroup import UsersGroup

        def cb_update(result):
            return Model().update(Federacion, {
                'id' : result['data'][0]['id'],
                'name' : unicode(data.get('name')[0].decode('utf8'))
            })

        def cb_read(ign):
            return Federacion.view().addCallback(cb_update)

        params={
            'id' : int(data.get('group_id')[0]),
            'name' : unicode(data.get('group_name')[0].decode('utf8')),
            'description' : unicode(data.get('group_desc')[0].decode('utf8'))
        }

        return Model().update(UsersGroup, params).addCallback(cb_read)

    @staticmethod
    def get_comite():
        def retrieve_comite(fl):
            if type(fl) is dict:
                return fl
            return defer.succeed(fl.comite).addCallback(cb_get_comite)

        def cb_get_comite(comite):
            if not comite:
                return {'success' : False, 'message' : 'No existen datos del Comité de la Federación Local'}
            return comite

        return Federacion.get_fl().addCallback(retrieve_comite)

    @staticmethod
    def get_fl():
        def cb_get(results):
            if len(results) is 0:
                return {'success' : False, 'message' : 'No existen datos de la Federación Local'}
            return Federacion.store.get(Federacion, results['data'][0]['id'])

        return Federacion.view().addCallback(cb_get)

    @staticmethod
    def check_group(group, id):
        """Checks if the given group id is equal to the configured comite_id"""

        if group['data'][0]['comite_id']==id:
            return defer.succeed(True)

        return defer.succeed(False)

    @staticmethod
    def save_secretario(kwargs):
        """Save a secretario."""

        from application.model.UserProfile import UserProfile
        from goliat.session.user import UserData

        user_id=int(kwargs.get('afiliado_id')[0])
        cargo_id=int(kwargs.get('cargo_id')[0])

        def cb_get_user(comite):
            if type(comite) is dict:
                return comite

            user=Federacion.store.get(UserData, user_id)
            comite.user_ids.add(user)
            print dir(user)
            profile=Federacion.store.get(UserProfile, user.id)
            profile.title=unicode(kwargs.get('cargo_name')[0].decode('utf8'))
            Federacion.store.commit()

            return {'success' : True}

        return Federacion.get_comite().addCallback(cb_get_user)

    @staticmethod
    def remove_secretario(ids):
        """Remove secretarios."""

        from application.model.UserProfile import UserProfile
        from goliat.session.user import UserData

        def cb_get_user(comite, user_id):
            if type(comite) is dict:
                return comite
            return Federacion.store.get(UserData, user_id).addCallback(cb_remove, comite)

        def cb_remove(user, comite):
            return comite.user_ids.remove(user).addCallback(cb_get_profile, user)

        def cb_get_profile(ign, user):
            return Federacion.store.get(UserProfile, user.id).addCallback(cb_unset_title)

        def cb_unset_title(user_profile):
            user_profile.title=unicode('')

            return True

        def cb_return_data(ign):
            Federacion.store.commit()
            return {'success' : True}

        dl=list()
        for user_id in ids:
            dl.append(Federacion.get_comite().addCallback(cb_get_user, user_id))

        return defer.DeferredList(dl).addCallback(cb_return_data)

    @staticmethod
    def get_comite_members():
        """Get comite members."""

        from application.model.UserProfile import UserProfile

        def cb_get_members(comite):
            if type(comite) is dict:
                return comite

            return cb_parse(comite.user_ids)

        def cb_parse(users):
            if users.count() is 0:
                return {'success' : True, 'people' : [] }
            rusers=list()
            for user in users:
                profile=Federacion.store.get(UserProfile, user.id)
                sindicato_name=''
                for sindicato in profile.sindicato:
                    sindicato_name=sindicato.name

                rusers.append({
                    'id' : user.id,
                    'profile_id' : profile.id,
                    'name' : user.username,
                    'nia' : profile.nia,
                    'title' : profile.title,
                    'sindicato_name' : sindicato_name
                })

            return rusers

        return Federacion.get_comite().addCallback(cb_get_members)
