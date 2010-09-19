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

        def cb_sendback(ign):
            return {'success' : True}

        def cb_create_federacion(ign, ugroup):
            federacion=Federacion()
            federacion.name=unicode(data.get('name')[0].decode('utf8'))
            federacion.comite_id=ugroup.id

            d=federacion.store.add(federacion)
            d.addCallback(lambda ign: federacion.store.commit()).addCallback(cb_sendback)

        ugroup=UsersGroup()
        ugroup.name=unicode(data.get('group_name')[0].decode('utf8'))
        ugroup.description=unicode(data.get('group_desc')[0].decode('utf8'))
        ugroup.active=True

        d=Federacion.store.add(ugroup)
        d.addCallback(lambda ign: Federacion.store.commit()).addCallback(cb_create_federacion, ugroup)

        return d

    @staticmethod
    def update(data):
        """Updates a Federacion object and the Users Group of its comite"""

        from application.model.UsersGroup import UsersGroup

        def cb_update(result):
            return Model().update(Federacion, {
                'id' : result[0]['id'],
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
    def get_comite(id):
        fl=Federacion.store.get(id)
        return fl.comite

    @staticmethod
    def check_group(group, id):
        """Checks if the given group id is equal to the configured comite_id"""

        if group[0]['comite_id']==id:
            return defer.succeed(True)

        return defer.succeed(False)
