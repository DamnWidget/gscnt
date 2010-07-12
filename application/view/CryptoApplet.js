/*
        
    GsCNT : Gestion de Sindicatos de la CNT. 
    Copyright (C) 2010 Open Phoenix IT S.Coop.And. 
    Copyright (C) 2010 Confederación Nacional del Trabajo.    
          
    This program is free software; you can redistribute it and/or
    modify it under the terms of the GNU General Public License
    as published by the Free Software Foundation; either version 2
    of the License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program; if not, write to the Free Software
    Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA
          
*/

Ext.ns('GsCNT.view');

GsCNT.view.CryptoApplet = Ext.extend(Ext.Panel, {
    initComponent : function() {
        if(!Ext.isIE) {
            this.bodyCfg = {
                tag: 'applet',
                archive: 'uji-ui-applet-2.1.0-signed.jar,\n' +
                    '  uji-config-2.1.0-signed.jar,\n' +
                    '  uji-utils-2.1.0-signed.jar,\n' +
                    '  uji-crypto-core-2.1.0-signed.jar,\n' +
                    '  uji-keystore-2.1.0-signed.jar,\n' +
                    '  lib/jakarta-log4j-1.2.6.jar,\n' +
                    '  uji-crypto-cms-2.1.0-signed.jar,\n' +
                    '  lib/bcmail-jdk15-143.jar,\n' +
                    '  lib/bcprov-jdk15-143.jar',
                code: 'es.uji.security.ui.applet.SignatureApplet',
                codebase: 'app/',
                id: 'CryptoApplet',
                name: 'CryptoApplet'
            }
        } else {
            this.bodyCfg = {
                tag: 'applet',
                archive: 'uji-ui-applet-2.1.0-signed.jar,\n' +
                    '  uji-config-2.1.0-signed.jar,\n' +
                    '  uji-utils-2.1.0-signed.jar,\n' +
                    '  uji-crypto-core-2.1.0-signed.jar,\n' +
                    '  uji-keystore-2.1.0-signed.jar,\n' +
                    '  lib/jakarta-log4j-1.2.6.jar,\n' +
                    '  uji-crypto-cms-2.1.0-signed.jar,\n' +                        
                    '  uji-crypto-jxades-2.1.0-signed.jar,\n' +
                    '  uji-format-facturae-2.1.0-signed.jar,\n' +
                    '  uji-format-pdf-2.1.0-signed.jar,\n' +
                    '  uji-crypto-xmldsign-2.1.0-signed.jar,\n' +
                    '  uji-crypto-openxades-2.1.0-signed.jar,\n' +
                    '  uji-crypto-raw-2.1.0-signed.jar,\n' +                               
                    '  lib/xmlsec.jar,\n' +
                    '  lib/myxmlsec.jar,\n' +
                    '  lib/commons-logging.jar,\n' +
                    '  lib/jakarta-log4j-1.2.6.jar,\n' +
                    '  lib/bcprov-jdk15-143.jar\n' +
                    '  lib/bcmail-jdk15-143.jar\n' + 
                    '  lib/bctsp-jdk15-143.jar\n' +
                    '  lib/itext-1.4.8.jar\n' +
                    '  lib/xalan-2.7.0.jar\n' +
                    '  lib/jxades-1.0-signed.jar',                         
                code: 'es.uji.security.ui.applet.SignatureApplet',
                codebase: 'app/',
                id: 'CryptoApplet',
                name: 'CryptoApplet'
            }
        }
        
        GsCNT.view.CryptoApplet.superclass.initComponent.call(this);
    }
});

Ext.reg('cryptoapplet', GsCNT.view.CryptoApplet);

