/*
        
    Goliat : The Twisted and ExtJS Web Application Framwork. 
    Copyright (C) 2010 Open Phoenix IT S.Coop.And.
    Visit us at: http://www.open-phoenix.com
          
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
Ext.ns("GsCNT");
 
var _version = "0.1b";
        
/**
 * @class GsCNT.workspace
 * This is the main application class
 * <br />
 * @constructor
 * @singleton
 */
GsCNT.workspace = function() {
    var viewport, mainPanel, loginWindow, centerPanel, session;
     
    return {
        window: null,
        
        init: function() {            
            this.checkSession();
        },        
                 
        buildViewPort: function() {                              
            // Viewport         
            mainPanel = new Ext.Panel({
                itemId      : 'mainPanel',
                layout      : 'border',
                border      : false,
                items       : this.buildLayout()
            });          
            
            this.window = mainPanel;
            this.configurePanels();            
            
            viewport = new Ext.Viewport({
                layout      : 'fit',
                items       : mainPanel
            });
            Ext.QuickTips.init();
        },
        
        configurePanels: function() {            
            this.buildHeader();
        },
        
        buildLayout : function() {             
            centerPanel = new Ext.Panel({
                layout          : 'card',
                activeItem      : 0,
                border          : false,
                defaults        :  { workspace : this },
                itemId          : 'centerPanel',
                region          : 'center',                
                items           : [
                    { 
                        xtype       : 'escritorio',
                        pLayout     : {                            
                            columns     : [
                                {
                                    columnWidth : .30,
                                    items       : [
                                        { title: 'Another Panel 1', tools: GsCNT.view.Portlet.Tools, html: 'Perico palotes' }
                                    ]
                                },
                                {
                                    columnWidth : .70,
                                    items       : [
                                        { title: 'Panel 2', tools: GsCNT.view.Portlet.Tools, html: 'Perico palotes' },
                                        { title: 'Another Panel 2', tools: GsCNT.view.Portlet.Tools, html: 'Perico palotes' }   
                                    ]
                                }
                            ]                                                    
                        }                        
                    },
                    { xtype : 'panel' },
                    { xtype : 'panel' },
                    { xtype : 'panel' },
                    { xtype : 'panel' },
                    { xtype : 'panel' },
                    { xtype : 'panel' },
                    { xtype : 'panel' }
                ],
                tbar            : [
                    { text: 'Escritorio', iconCls: 'icon_desktop', toggleGroup: 'navGrp', itemType: 'dashboard', enableToggle: true, pressed: true, scope: this, handler: this.onSwitchPanel },
                    '-',
                    { text: 'Federación Local', iconCls: 'icon_federacion', itemType: 'federacionmanager', toggleGroup: 'navGrp', enableToggle: true, scope: this, handler: this.onSwitchPanel },
                    '-',
                    { text: 'Calendario', iconCls      : 'icon_calendar', itemType: 'calendarmanager', toggleGroup: 'navGrp', enableToggle: true, scope: this, handler: this.onSwitchPanel },
                    '-',
                    { text: 'Documentos', iconCls: 'icon_documents', itemType: 'documentsmanager', toggleGroup: 'navGrp', enableToggle: true, scope: this, handler: this.onSwitchPanel },
                    '-',
                    { text: 'Almacen', iconCls: 'icon_store', itemType: 'storemanager', toggleGroup: 'navGrp', enableToggle: true, scope: this, handler: this.onSwitchPanel },
                    '-',
                    { text: 'Conflictos', iconCls: 'icon_conflictos', itemType: 'conflictosmanager', toggleGroup: 'navGrp', enableToggle: true, scope: this, handler: this.onSwitchPanel },
                    '-',
                    { text: 'Actividades', iconCls: 'icon_actividades', itemType: 'actividadesmanager', toggleGroup: 'navGrp', enableToggle: true, scope: this, handler: this.onSwitchPanel },
                    '-',
                    { text: 'Tesorería', iconCls: 'icon_tesoreria', itemType: 'tesoreriamanager', toggleGroup: 'navGrp', enableToggle: true, scope: this, handler: this.onSwitchPanel },
                    '->',
                    { text: 'Salir', iconCls: 'icon_logout', scope: this, handler: this.onLogout }
                ],
                bbar        : [
                    {
                        xtype   : 'tbtext',
                        itemId  : 'userText',
                        text    : 'Usuario Conectado : <b>'+Ext.util.Format.capitalize(session.name)+'</b>'
                    },
                    '->',
                    {
                        xtype       : 'button',
                        text        : 'Opciones de Usuario',        
                        iconCls     : 'icon_user',                        
                        listeners   : {
                            scope       : this,
                            click       : this.userButton_onClick
                        }
                    }
                ]
            });
            
            centerPanel.getComponent('escritorioPanel').addPortlet(1, {title: 'Another Panel 2 on 2', tools: GsCNT.view.Portlet.Tools, html: 'Perico palotes'});
            
            topPanel = new Ext.Panel({            
                itemId          : 'topPanel',
                region          : 'north',            
                height          : 60,
                minSize         : 60                                                    
            });
            
            return [ centerPanel, topPanel ];
        },
        
        buildHeader: function() {
            topPanel = this.window.getComponent('topPanel');
            topPanel.height = 100;
            header = { xtype : 'gscnt_header_panel' };
            topPanel.add(header);
            topPanel.doLayout();
        },
        
        checkSession : function() {  
            if(!session) {
                lw = new Goliat.UserLoginWindow({
                    title       : 'GsCNT: Autenticación',
                    scope       : this,
                    handler     : this.onLogin,
                    url         : '/sessionmanager/check_session',
                    bodyStyle   : "background: url(/media/login.png) no-repeat; padding: 260px 0 0 174px;"                      
                });   
                
                lw.items.items[0].add({
                    xtype   : 'button',
                    itemId  : 'certBtn',
                    disabled: true,
                    style   : 'margin: 16px 0 0 8px;',
                    iconCls : 'icon_cert',
                    width   : 70,                    
                    text    : 'Acceder con Certificado Digital',
                    handler : this.Sign,
                    scope   : this.scope || this
                });
                
                lw.add({
                    xtype   : 'cryptoapplet'
                });  
                
                loginWindow = lw;         
                         
                session = new Goliat.session.Session({
                    loginWindow         : lw,
                    logout              : '/sessionmanager/logout',                    
                    listeners           : {
                        scope       : this,
                        logout      : this.destroy,
                        login       : this.buildInterface,
                        checked     : this.buildInterface
                    }
                });
            }     
                  
            session.check();
        },
        
        switchToCard : function(newCardIndex) {
            var layout         = centerPanel.getLayout(),
                activePanel    = layout.activeItem,
                activePanelIdx = centerPanel.items.indexOf(activePanel);

            if (activePanelIdx !== newCardIndex) {
                var  newPanel = centerPanel.items.itemAt(newCardIndex);

                layout.setActiveItem(newCardIndex);

                if (newPanel.cleanSlate) {
                    newPanel.cleanSlate();
                }
            }
        },
        
        onSwitchPanel : function(btn) {
            var xtype    = btn.itemType,
                panels   = centerPanel.findByType(xtype),
                newPanel = panels[0];

            var newCardIndex = centerPanel.items.indexOf(newPanel);
            this.switchToCard(newCardIndex);
        },
        
        onLogin : function() {
            session.onLogin();
        },
        
        onLogout : function() {
            session.onLogout();
        },
        
        userButton_onClick : function() {
        
        },
        
        buildInterface : function() {            
            this.buildViewPort();            
        },

        destroy: function() {
            viewport.destroy();
            session = null;
            viewport = null;
            mainPanel = null;
            this.init();
        },
        
        getSession : function() {
            return session;
        },
        
        Sign : function() {
            var texto = "Q2FkZW5hIGRlIHZlcmlmaWNhY2lvbgo=";            
            var cp= document.getElementById("CryptoApplet");            
            cp.setSignatureOutputFormat("CMS");
            cp.setInputDataEncoding("BASE64");
            cp.setOutputDataEncoding("BASE64");
            cp.setLanguage("ES_es");
            cp.signDataParamToFunc(texto,"onSignOk");
        },

        onInitOk : function() {
            certBtn = loginWindow.items.items[0].items.items[3];
            certBtn.enable();
        },
        
        onSignOk : function(res) {
            Goliat.data.JsonRequest({
                method  : 'GET',
                url     : '/sessionmanager/sign',
                data    : { sign : res },
                scope   : this
            }, this.onSignVerified);
        },
        
        onSignVerified: function(data) {
            if (!data.success) {
                Goliat.Msg.error(data.error, this);
            }
            else {
                var form = loginWindow.get(0);
                form.getForm().setValues({
                    username: data.data.username,
                    password: data.data.password,
                });
                this.onLogin();
            }
        }
    }
}();

// Main application entry point
Ext.onReady(GsCNT.workspace.init, GsCNT.workspace)

function onInitOk() {
    GsCNT.workspace.onInitOk();
}

function onSignOk(res) {
    GsCNT.workspace.onSignOk(res);
}
