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

GsCNT.view.SindicatoForm = Ext.extend(Goliat.base.FormPanel, {
    border       : true,
    autoScroll   : true,    
    bodyStyle    : "padding: 10px; background: #ffffff url(media/gatonegro_mini.png) no-repeat bottom right;",
    layout       : 'form',
    labelWidth   : 40,
    defaultType  : 'textfield',
    defaults     : {
        width      : 200,
        maxLength  : 255,
        allowBLank : false
    },
    
    initComponent : function() {
        Ext.applyIf(this, {      
            items   : this.buildFormItems()
        });        
        
        GsCNT.view.SindicatoForm.superclass.initComponent.call(this);
    },
    
    buildFormItems : function() {
        var nameContainer       = this.buildNameContainer(),
            descContainer       = this.buildDescContainer(),
            comiteContainer     = this.buildComiteContainer();       
           
        return [
            {
                xtype   : 'hidden',
                name    : 'id'
            },
            nameContainer,
            descContainer,
            comiteContainer
        ];
    },
    
    buildNameContainer : function() {
        return {
            xtype       : 'container',
            layout      : 'column',
            anchor      : '-10',
            defaultType : 'container',
            defaults    : {
                width       : 280,
                labelWidth  : 50,
                layout      : 'form'
            },
            items       : [
                {
                    items   : {
                        xtype       : 'textfield',
                        fieldLabel  : 'Nombre',
                        name        : 'name',
                        anchor      : '-10',
                        allowBlank  : false,
                        maxLength   : 128
                    }
                }
            ]
        };
    },
    
    buildDescContainer : function() {
        return {
            xtype       : 'container',
            title       : 'Descripción',
            flex        : 1,
            bodyStle    : 'padding: 1px; margin: 0px',
            layout      : 'form',
            labelWidth  : 70,
            width       : 270,
            items       : {
                xtype       : 'textarea',
                fieldLabel  : 'Descripción',
                name        : 'description',
                anchor      : '100% 100%',
                allowBlank  : false,                                
            }
        };
    },
    
    buildComiteContainer : function() {
        return {
            xtype       : 'container',
            layout      : 'column',
            anchor      : '-10',
            defaultType : 'container',
            defaults    : {
                width       : 280,
                labelWidth  : 40,
                layout      : 'form'
            },
            items       : [
                {
                    items   : {
                        xtype           : 'relation',
                        id              : 'ignore-me',
                        url             : '/groupsmanager',
                        fieldLabel      : 'Comité',
                        hiddenName      : 'comite_id',
                        valueField      : 'id',
                        displayField    : 'name',
                        relationModel   : 'Grupo de Usuarios',
                        relationManager : GsCNT.view.UsersGroupFormWindow,                        
                        anchor          : '-10',
                        emptyText       : 'Seleccione un Comité',
                        listeners       : {
                            scope           : this,
                            beforewrite     : function(store, action, record) {
                                retval = true;
                                switch(action) {
                                    case 'destroy':
                                        if(record.id == GsCNT.workspace.getSession().federacionData.comite_id) {
                                            retval = false;
                                            Goliat.Msg.alert('No puede eliminar el comite de la Federación Local.', this);
                                        }
                                        break;
                                }
                                
                                return retval;
                            }
                        }                        
                    }
                }
            ]
        };
    },
    
    loadFormAfterRender: function() {
        
        Ext.getCmp('ignore-me').modelStore.on('onload', function() { 
            this.getForm().loadRecord(this.record); 
        }, this);                
        
    }
    
});

Ext.reg('sindicatoform', GsCNT.view.SindicatoForm);
