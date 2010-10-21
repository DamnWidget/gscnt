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

GsCNT.view.FederacionManager = Ext.extend(Ext.Panel, {   
    layout  : 'border',
    border  : false,
    initComponent : function() {
        this.checkFederacion();
        this.tbar = this.buildToolbar();
        this.items = [
            this.buildSindicatosList(),
            this.buildSindicatoPanel()
        ];        
        GsCNT.view.FederacionManager.superclass.initComponent.call(this);        
    },
    
    buildSindicatosList : function() {
        return {
            xtype       : 'sindicatoslist',
            itemId      : 'sindicatosList',
            title       : 'Lista de Sindicatos',
            flex        : 1,
            split       : true,
            resizable   : true,
            collapsible : true,            
            region      : 'west',
            width       : 200,
            maxWidth    : 300,
            minWidth    : 200,
            border      : false,
            bodyStyle   : "background: #fff url(media/gatonegro_mini.png) no-repeat bottom right;",
            listeners   : {
                scope       : this,
                click       : this.sindicatosList_onClick
            }            
        }
    },
    
    buildSindicatoPanel : function() {
        return {
            xtype       : 'panel',
            itemId      : 'sindicatosPanel',
            id          : 'sindicatospanel',
            region      : 'center',
            layout      : 'fit'                        
        };
    },
    
    buildToolbar : function() {
        federacionBtn = '';
        federacionComiteBtn = '';
        session = GsCNT.workspace.getSession();
        if(session.hasGroup('admin') || session.hasGroup('org')) {
            federacionBtn = {
                text    : 'Configuración de la Federación Local',
                iconCls : 'icon_config',
                scope   : this,
                handler : this.onModifyFederacion
            };            
            federacionComiteBtn = {
                text    : 'Comité de la Federación Local',
                iconCls : 'icon_utilities',
                scope   : this,
                handler : this.onModifyFederacionComite
            };
        }        
        
        return [
            '->',
            federacionBtn,
            federacionComiteBtn,
            {
                text    : 'Federar nuevo Sindicato',
                iconCls : 'icon_register',
                scope   : this,
                handler : this.onNewSindicato
            }
        ];
    },
    
    checkFederacion : function() {
        Goliat.data.JsonRequest({
            method      : 'GET',
            url         : '/federacionmanager/read',
            data        : {},
            scope       : this                        
        }, this.onCheckFederacion);
    },
    
    onCheckFederacion : function(jsonData, options) {        
        if (jsonData.success) {
            session = GsCNT.workspace.getSession();                        
            session.federacionData = jsonData;
            GsCNT.workspace.FbarUpdate('federacionText', 'Federación : <b>' + jsonData.name + '</b>');
        } else {            
            Goliat.Msg.error('<b><h3>No hay datos de la Federación Local.</h3></b><br />' + 
            '<img src="/media/Help1.png" border="0" /><br /><br />' +
            'Haz click en el menu de Federación Local y procede con su configuración.');
        }
    },
    
    sindicatosList_onClick : function() {
        
    },
    
    onNewSindicato : function() {
        if (!GsCNT.workspace.getSession().federacionData) {
            Goliat.Msg.alert('No existen datos de la Federación Local, primero debe configurarla.', this);
            return;
        }
        this.sw = new Ext.Window({
            layout      : 'fit',
            modal       : true,
            width       : 320,
            height      : 210,
            resizable   : false,
            draggable   : true,
            center      : true,
            closable    : false,
            title       : 'Federar nuevo Sindicato',
            iconCls     : 'icon_bandera',  
            cls         : 'GsCNT',          
            items       : [
                new GsCNT.view.SindicatoForm()
            ],
            buttons     : [            
                {
                    text    : 'Guardar',
                    iconCls : 'icon_accept',
                    scope   : this,
                    handler : this.sindicatoSaveButton_onClick
                },
                {
                    text    : 'Cerrar',
                    iconCls : 'icon_cancel',
                    scope   : this,
                    handler : function() {
                        if (this.sw.items.items[0].getForm().isDirty()) {
                            Goliat.Msg.confirm('¿Desea cerrar el formulario sin guardar los cambios?', this, function(btn) {
                                if (btn == 'yes') {
                                    this.sw.close();
                                }
                                else {
                                    return;
                                }
                            });
                        }
                        else {
                            this.sw.close();
                        } 
                    }
                }
            ],
            getForm : function() {
                return this.items.items[0];
            }
        }).show();
    },
    
    onModifyFederacion : function() {        
        this.showConfigWizard();        
    },
    
    onEditSecretario : function() {
        
    },
    
    onNewSecretario : function(win) {
        if(this.getSindicatosList().areRecords()) {
            this.sw = new Ext.Window({
                layout      : 'fit',
                modal       : true,
                width       : 320,
                height      : 150,
                resizable   : false,
                draggable   : true,
                center      : true,
                closable    : false,
                title       : 'Añadir secretarie',
                iconCls     : 'icon_user',            
                items       : [
                    new GsCNT.view.SecretarioForm()
                ],
                buttons     : [            
                    {
                        text    : 'Guardar',
                        iconCls : 'icon_accept',
                        scope   : this,
                        handler : this.secretarioSaveButton_onClick
                    },
                    {
                        text    : 'Cerrar',
                        iconCls : 'icon_cancel',
                        scope   : this,
                        handler : function() {
                            if (this.sw.items.items[0].getForm().isDirty()) {
                                Goliat.Msg.confirm('¿Desea cerrar el formulario sin guardar los cambios?', this, function(btn) {
                                    if (btn == 'yes') {
                                        this.sw.close();
                                    }
                                    else {
                                        return;
                                    }
                                });
                            }
                            else {
                                this.sw.close();
                            } 
                        }
                    }
                ],
                getForm : function() {
                    return this.items.items[0];
                }
            }).show();
        }
        else {
            Goliat.Msg.confirm('Actualmente no existen sindicatos federados a esta Federación Local.<br />¿Desea federar un nuevo sindicato ahora?', this, function(btn) {
                if (btn == 'yes') {
                    this.onNewSindicato();
                }
            });
        }        
    },
    
    onRemoveSecretario : function() {
        
    },
    
    onModifyFederacionComite : function() {
        if (!GsCNT.workspace.getSession().federacionData) {
            Goliat.Msg.alert('No existen datos de la Federación Local, primero debe configurarla.', this);
        }
        else {
            new GsCNT.view.FederacionConfigWindow({
                listeners   : {
                    scope           : this,
                    editsecretario  : this.onEditSecretario,
                    newsecretario   : this.onNewSecretario,
                    removesecretario: this.onRemoveSecretario 
                }
            }).show();
        }                
    },
    
    secretarioSaveButton_onClick : function() {
        if(this.sw.getForm().isValid()) {
            Ext.getBody().mask('Guardando Secretarie', 'x-mask-loading');
            
            f = GsCNT.workspace.getSession().federacionData;
            this.sw.getForm().getForm().submit({
                url     : 'federacionmanager/save_secretario',                
                scope   : this,
                success : function() {
                    Ext.getBody().unmask();
                    this.sw.close();                    
                },
                failure : function() {
                    Ext.getBody().unmask();
                    Goliat.Msg.error('Se produjo un error al intentar guardar los datos.', this);
                }
            });
        } 
        else {
            Goliat.Msg.error('El formulario contiene errores.', this);
        }        
    },
    
    sindicatoSaveButton_onClick : function() {
        if(this.sw.getForm().isValid()) {            
            Ext.getBody().mask('Guardando Sindicato', 'x-mask-loading');
            
            this.sw.getForm().getForm().submit({
                url     : 'sindicatomanager/save',
                scope   : this,
                success : this.onSindicatoSaveSuccess,
                failure : this.onSindicatoSaveFail
            });
        } else {
            Goliat.Msg.error('El formulario contiene errores.', this);
        }        
    },
    
    onSindicatoSaveSuccess : function(form, action) {        
        Ext.getBody().unmask();
        this.sw.close();
        this.getSindicatosList().refreshView();
    },
    
    onSindicatoSaveFail : function() {
        Ext.getBody().unmask();                
        Goliat.Msg.error('Se produjo un error al intentar guardar los datos del sindicato.', this);
    },
    
    showConfigWizard : function() {
        session = GsCNT.workspace.getSession();
        name = (GsCNT.workspace.getSession().federacionData) ? GsCNT.workspace.getSession().federacionData.name : '';        
        var wizard = new Ext.ux.Wiz({
            title           : 'Asistente de Configuración de Federación Local',            
            headerConfig    : {
                title   : 'Configure su Federación Local'
            },
            cardPanelConfig : {
                itemId  : 'cardPanel',
                defaults: {
                    baseCls     : 'x-small-editor',
                    bodyStyle   : 'padding:40px 15px 5px 120px;background: #F6F6F6 url(media/gatonegro_mini.png) no-repeat scroll 16px 22px;',
                    border   : false
                }
            },
            cards           : [
                new Ext.ux.Wiz.Card({
                    title   : 'Ayuda',
                    items   : [
                        {
                            border      : false,
                            bodyStyle   : 'background: none;',
                            html        : 'Bienvenido al asistente de <b>Configuración de Federación Local</b>, '+
                                'siga las instrucciones que iran apareciendo a lo largo del proceso.<br />'+
                                'Haga click en el botón \'Siguiente\''                            
                        }                        
                    ]
                }),
                
                new Ext.ux.Wiz.Card({
                    id          : 'cardname',
                    itemId      : 'cardName',
                    title       : 'Introduzca el nombre de la Federación Local',
                    monitorValid: true,
                    defaults    : {
                        labelStyle  : 'font-size: 11px;'
                    },
                    items       : [
                        {
                            border      : false,
                            bodyStyle   : 'background:none;padding-bottom:30px;',
                            html        : 'Por favor, introduzca el nombre de la Federación Local que está configurando. '+
                                '(El nombre puede modificarse en el futuro).'+
                                ' Cuando haya finalizado haga click en el botón \'Siguiente\'.'
                        },
                        new Ext.form.TextField({
                            id          : 'name',
                            itemId      : 'nameField',
                            fieldLabel  : 'Nombre',
                            hiddenName  : 'name',
                            value       : name,
                            emptyText   : 'Introduzca un nombre...',
                            blankText   : 'Debes introducir un nombre.',
                            width       : 200,
                            allowBlank  : false
                        })
                    ]
                }),
                
                new Ext.ux.Wiz.Card({
                    id          : 'cardgrupo',
                    itemId      : 'cardGrupo',
                    title       : 'Configure el grupo que acogerá a los miembros del Comité',
                    monitorValid: true,
                    items   : [
                        {
                            border      : false,
                            bodyStyle   : 'background:none;padding-bottom:30px;',
                            html        : 'Configure el grupo de usuarios que englobará al Comité de esta Federación Local.<br />'+
                                'Cuando haya acabado haga click en el botón \'Finalizar\''                                                            
                        },
                        new Ext.form.TextField({
                            id          : 'gname',
                            itemId      : 'groupNameField',
                            fieldLabel  : 'Nombre del Grupo',
                            hiddenName  : 'group_name',
                            value       : (session.federacionData) ? session.federacionData.group.name : '',
                            emptyText   : 'Inroduzca un nombre...',
                            blankText   : 'Debes introducir un nombre.',
                            width       : 200,                            
                            allowBlank  : false
                        }),                        
                        new Ext.form.TextArea({
                            id          : 'gdesc',
                            itemId      : 'groupDescField',
                            fieldLabel  : 'Descripción',
                            hiddenName  : 'desc',
                            value       : (session.federacionData) ? session.federacionData.group.desc : '',
                            emptyText   : 'Inroduzca una descripción...',
                            blankText   : 'Debes introducir una descripción.',                            
                            anchor      : '100% 40%',                            
                            allowBlank  : false
                        }),
                        new Ext.form.Hidden({
                            id          : 'gid',
                            itemId      : 'groupIdField',
                            hiddenName  : 'group_id',
                            value       : (session.federacionData) ? session.federacionData.group.id : 0,
                        })                        
                    ]
                })
            ]
        });
        
        wizard.on('finish', this.stepOne, this);
        wizard.show();
    },
    
    stepOne : function(wiz, data) {        
        var name = data.cardname.name;
        var gname = data.cardgrupo.gname;
        var desc = data.cardgrupo.gdesc;
        var gid = data.cardgrupo.gid;
        
        Goliat.data.JsonRequest({
            method      : 'POST',
            url         : '/federacionmanager/save',
            data        : {
                name        : name,
                group_name  : gname,
                group_desc  : desc,
                group_id    : gid
            },
            scope       : this                        
        }, function() {
            Goliat.data.JsonRequest({
                method      : 'GET',
                url         : '/federacionmanager/read',
                data        : {},
                scope       : this                        
            }, function(jsonData, options) { 
                   this.onCheckFederacion(jsonData, options);                    
            });             
        });        
    },
    
    getSindicatosList : function() {
        return this.getComponent('sindicatosList');
    }
});

Ext.reg('federacionmanager', GsCNT.view.FederacionManager);
