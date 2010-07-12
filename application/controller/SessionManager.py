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
# $id application/controller/SessionManager.py created on 2010-07-04 23:19:14.492402 by Goliat $
'''
Created on 2010-07-04 23:19:14.492402

@license: GPLv2
@copyright: © 2010 Open Phoenix IT SCA
@organization: Open Phoenix IT S.Coop.And
@author: Goliat
@contact: goliat@open-phoenix.com
@summary: SessionManager Module
@version: 0.1
'''
from OpenSSL import SSL
from twisted.web import server
from twisted.internet import defer
from twisted.internet import utils
from storm.store import Store
import json
import os

from goliat.webserver import gresource
from goliat.session.user import IUser, UserData
from goliat.database import Database
from goliat import http

from application.model.UserProfile import UserProfile

class SessionManager(gresource.GResource):
    """SessionManager class:"""


    def __init__(self):
        """Constructor:
        
        ADD YOUR INITIALIZATION CODE HERE
        """
        gresource.GResource.__init__(self)

    def render_GET(self, request):
        """
        render_GET Method
        """
        self.senderrback(request, {'message' : 'No implementado.', 'number' : 100 })
        return server.NOT_DONE_YET

    def render_POST(self, request):
        self.senderrback(request, {'message' : 'No implementado.', 'number' : 100 })
        return server.NOT_DONE_YET

    def get_register_path(self):
        """Returns the module resource registration path."""
        return "sessionmanager"

    def fill_session(self, request):
        """
        Fills session data.
        """
        session=request.getSession()
        user=IUser(session)
        profile=user.get_profile()
        if not profile.validated:
            self.senderrback(
                request,
                {'message' : 'Lo sentimos pero parece ser que su usuario aún no ha sido validado.<br />'+\
                'Revise la dirección de correo que facilitó cuando se registró en la aplicación.<br />'+\
                'Si no puedes solucionar el problema por tus propios medios ponte en contacto con'+\
                ' la secretaría de Organización de tu sindicato.', 'number' : http.SESSION_NOT_VALID })
            session.expire()
            return
        if not user.is_active():
            self.senderrback(
                request,
                {'message' : 'Lo sentimos pero parece ser que su usuario aún no ha sido activado.<br />'+\
                'Revise la dirección de correo que facilitó cuando se registró en la aplicación.<br />'+\
                'Si no puedes solucionar el problema por tus propios medios ponte en contacto con'+\
                ' la secretaría de Organización de tu sindicato.', 'number' : http.SESSION_NOT_ACTIVE })
            session.expire()
            return
        sess_data=user.__rpr__()
        sess_data['userProfile']={ 'nia' : profile.nia }

        return sess_data

    def sign(self, request, **kwargs):
        """
        Signs with User's Digital Certificates.
        """
        sign=kwargs.get('sign', None)
        if not sign:
            return json.dumps({ 'success' : False, 'error' : 'Su navegador no ha enviado ninguna cadena de firma. Revise su soporte Java'})
        os.chdir('signVerify')
        fd=file('./tmp/pkcs7.pem', 'wb')
        fd.write(sign[0])
        fd.close()
        output=utils.getProcessOutput('/usr/bin/java', ['-jar', './dist/signVerify.jar', '-f', './tmp/pkcs7.pem'])
        output.addCallback(self._signVerify, request).addErrback(self._signFail, request)
        os.chdir('../')
        return server.NOT_DONE_YET

    def check_session(self, request, **kwargs):
        """
        Checks the User's Session.
        """
        session=request.getSession()
        if session.is_authed():
            sess_data=self.fill_session(request)
            self.sendback(request, {'success' : True, 'session' : sess_data })
        else:
            self.senderrback(request, {'message' : 'La sesión no está autenticada.', 'number' : http.SESSION_NOT_AUTHED })

        return server.NOT_DONE_YET

    def logout(self, request, **kwargs):
        """
        Do logout
        """
        request.getSession().expire()
        return json.dumps({'success' : True, 'msg' : 'Done.'})

    def _signFail(self, error, request):
        print error
        request.write(json.dumps({'success' : False, 'error' : 'La firma no es válida.'}))
        request.finish()


    def _signVerify(self, result, request):
        succ, data, ign=result.split('\n')
        if succ=='true':
            name=data.split('=')[1].split('-')[0].rstrip()
            nia=int(data.split('NIA')[1].lstrip())
            store=Store(Database().get_database())
            result=store.find(UserProfile, UserProfile.nia==nia).one()
            if not result:
                request.write(json.dumps({'success' : False, 'error' : 'Este certificado digital no tiene un usuario asociado.'}))
                request.finish()
                return
            user=store.find(UserData, UserData.id==result.user_id).one()
            if not user:
                request.write(json.dumps({'success' : False, 'error' : 'Este certificado digital no tiene un usuario asociado.'}))
                request.finish()
                return
            request.write(json.dumps({'success' : True, 'data' : {'username' : user.username, 'password' : user.password }}))
            request.finish()
            return
        else:
            request.write(json.dumps({'success' : False, 'error' : 'La firma no es válida.'}))
            request.finish()
            return
