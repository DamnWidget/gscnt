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

    def check_certificate(self, request, **kwargs):
        """
        Checks a client certificate.
        """

        session=request.getSession()
        if session.is_authed():
            request.redirect('https://'+request.getRequestHostname()+':8080')

        cert=request.transport.getPeerCertificate()
        if not cert:
            request.write('<html lang="en" xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" class=" ext-strict">'+\
                          '<head>\n'+\
                          '    <meta content="text/html; charset=utf-8" http-equiv="Content-Type">\n'+\
                          '    <title>Error {0}</title>'.format(http.NO_CERT_REQUEST))
            request.write('</head>')
            request.write('<body>')
            request.write('    <h1>Error {0}</h1>'.format(http.NO_CERT_REQUEST))
            request.write('    <p>Su cliente web no ha emitido ningún certificado.</p>')
            request.write('    <a style="margin: 10px auto;" href="https://{0}:8080/">Volver</a>'.format(request.getRequestHostname()))
            request.write('</body>')
            request.write('</html>')
            request.finish()
        else:
            res=self._process_certificate(cert)
            if res['success']:
                if not session.is_authed():
                    session.authenticate()
                from goliat.session.usermanager import UserManager
                if not UserManager().exists(res['user'].id):
                    user=UserManager().get(res['user'].id, session)
                    user.set_last_login()
                    user.save()

                request.redirect('https://'+request.getRequestHostname()+':8080/')
                request.finish()
            else:
                request.write('<html lang="en" xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" class=" ext-strict">'+\
                          '<head>\n'+\
                          '    <meta content="text/html; charset=utf-8" http-equiv="Content-Type">\n'+\
                          '    <title>Error {0}</title>'.format(http.NO_CERT_REQUEST))
                request.write('</head>')
                request.write('<body>')
                request.write('    <h1>Error {0}</h1>'.format(http.NO_CERT_REQUEST))
                request.write('    <p>{0}.</p>'.format(res['message']))
                request.write('    <a style="margin: 10px auto;" href="https://{0}:8080/">Volver</a>'.format(request.getRequestHostname()))
                request.write('</body>')
                request.write('</html>')
                request.finish()


    def sign(self, request, **kwargs):
        """
        Signs with User's Digital Certificates.
        """

        session=request.getSession()
        if session.is_authed():
            return self.check_session(request)

        output=None
        cert=request.transport.getPeerCertificate()
        if not cert:
            output={ 'success' : False, 'message' : 'Su cliente web no ha emitido ningún certificado', 'number' : http.NO_CERT_REQUEST }
        else:
            output=self._process_certificate(cert)

        if kwargs.get('callback', None):
            cb=kwargs.get('callback')[0]
            request.setHeader('Content-Type', 'text/javascript')
            request.write(cb+'('+json.dumps(output)+');')
        else:
            request.setHeader('Content-Type', 'application/x-json')
            request.write(json.dumps(output))

        request.finish()

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

    def _process_certificate(self, cert):
        """
        Process an Client Certificate.
        """
        try:
            nia=cert.get_subject().get_components()[4][1].split('NIA')[1].lstrip()
        except:
            return {'success' : False, 'message' : 'El certificado no es válido.'}

        store=Store(Database().get_database())
        result=store.find(UserProfile, UserProfile.nia==int(nia)).one()
        if not result:
            return {'success' : False, 'message' : 'Este certificado digital no tiene un usuario asociado.'}
        user=store.find(UserData, UserData.id==result.user_id).one()
        if not user:
            return {'success' : False, 'message' : 'Este certificado digital no tiene un usuario asociado.'}

        return {'success' : True, 'user' : user }
