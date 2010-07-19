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
            border      : false,
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
        session = GsCNT.workspace.getSession();
        if(session.hasGroup('admin') || session.hasGroup('org')) {
            federacionBtn = {
                text    : 'Configuración de la Federación Local',
                iconCls : 'icon_config',
                scope   : this,
                handler : this.onModifyFederacion
            };
        } 
        return [
            '->',
            federacionBtn,
            {
                text    : 'Registrar nuevo Sindicato',
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
        
    },
    
    onModifyFederacion : function() {
        new GsCNT.view.FederacionConfigWindow().show();
        /*Goliat.data.JsonRequest({
            method      : 'GET',
            url         : '/federacionmanager/get_comite',
            data        : {},
            scope       : this                        
        }, this.showConfigWizard);*/
    },
    
    /*showConfigWizard : function(jsonData, options) {
        name = (GsCNT.workspace.getSession().federacionData.name) ? GsCNT.workspace.getSession().federacionData.name : '';
        console.debug(jsonData);
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
                            itemId      : 'nameField',
                            fieldLabel  : 'Nombre',
                            hiidenName  : 'name',
                            value       : name,
                            emptyText   : 'Introduzca un nombre...',
                            blankText   : 'Debes introducir un nombre.',
                            width       : 200,
                            allowBlank  : false
                        })
                    ]
                }),
                
                new Ext.ux.Wiz.Card({
                    itemId      : 'cardGrupo',
                    title       : 'Configure el grupo que acojerá a los miembros del Comité',
                    monitorValid: true,
                    items   : [
                        {
                            border      : false,
                            bodyStyle   : 'background:none;padding-bottom:30px;',
                            html        : 'Configure el grupo de usuarios que englobará al Comité de esta Federación Local.<br />'+
                                'Cuando haya acabado haga click en el botón \'Finalizar\''                                                            
                        },
                        new Ext.form.TextField({
                            itemId      : 'groupNameField',
                            fieldLabel  : 'Nombre del Grupo',
                            hiddenName  : 'group_name',
                            value       : jsonData.group.name,
                            emptyText   : 'Inroduzca un nombre...',
                            blankText   : 'Debes introducir un nombre.',
                            width       : 200,                            
                            allowBlank  : false
                        }),                        
                        new Ext.form.TextArea({
                            itemId      : 'groupDescField',
                            fieldLabel  : 'Descripción',
                            hiddenName  : 'desc',
                            value       : jsonData.group.desc,
                            emptyText   : 'Inroduzca una descripción...',
                            blankText   : 'Debes introducir una descripción.',                            
                            anchor      : '100% 40%',                            
                            allowBlank  : false
                        }),
                        new Ext.form.Hidden({
                            itemId      : 'groupIdField',
                            hiddenName  : 'group_id',
                            value       : jsonData.group.id
                        })                        
                    ]
                })
            ]
        });
        
        wizard.on('finish', this.stepOne, this);
        wizard.show();
    },
    
    stepOne : function(wiz, data) {        
        var name = data[wiz.getComponent('cardPanel').getComponent('cardName').id].name;
        var gname = data[wiz.getComponent('cardPanel').getComponent('cardGrupo').id].group_name;
        var desc = data[wiz.getComponent('cardPanel').getComponent('cardGrupo').id].desc;
        var gid = data[wiz.getComponent('cardPanel').getComponent('cardGrupo').id].group_id;   
        console.debug(name);     
    }*/
});

Ext.reg('federacionmanager', GsCNT.view.FederacionManager);
