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

GsCNT.view.AfiliadoForm = Ext.extend(Goliat.base.FormPanel, {
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
        
        GsCNT.view.AfiliadoForm.superclass.initComponent.call(this);
    },
    
    buildFormItems : function() {
        var cargoContainer       = this.buildCargoContainer(),            
            afiliadoContainer    = this.buildAfiliadoContainer();       
           
        return [
            {
                xtype   : 'hidden',
                name    : 'id'
            },
            afiliadoContainer,
            cargoContainer
        ];
    },
    
    buildCargoContainer : function() {
        var cargos = [
            ['SG', 'Secretarie General'],
            ['SO', 'Secretarie de Organización'],
            ['ST', 'Secretarie de Tesorería'],
            ['SP', 'Secretarie de Prensa y Propaganda'],
            ['SASI', 'Secretarie de Acción Sindical'],
            ['SASO', 'Secretarie de Acción Social'],
            ['SJYP', 'Secretarie de Jurídica y Pro-Preses'],
            ['SPP', 'Secretarie de Patrimonio']
        ];
        
        var store = new Ext.data.ArrayStore({
            fields  : ['abbr', 'nombre'],
            data    : cargos
        });
        
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
                        xtype           : 'combo',
                        store           : store,
                        displayField    : 'nombre',                        
                        fieldLabel      : 'Cargo',
                        typeAhead       : true,
                        mode            : 'local',
                        forceSelection  : true,
                        triggerAction   : 'all',
                        emptyText       : 'Selecciona un cargo...',
                        selectOnFocus   : true,
                        name            : 'cargo',
                        anchor          : '-10',
                        allowBlank      : false                        
                    }
                }
            ]
        };
    },
    
    buildAfiliadoContainer : function() {
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
                        url             : '/afiliadomanager',
                        fieldLabel      : 'Afiliade',
                        hiddenName      : 'afiliado_id',
                        valueField      : 'id',
                        displayField    : 'name',
                        relationModel   : 'Afiliade a la CNT-AIT',
                        relationManager : GsCNT.view.AfiliadoFormWindow,                        
                        anchor          : '-10',
                        emptyText       : 'Selecciona un Afiliade',
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
    }
    
});

Ext.reg('afiliadoform', GsCNT.view.AfiliadoForm);

GsCNT.view.AfiliadoFormWindow = Ext.extend(Ext.Window, {
    layout      : 'fit',
    modal       : true,
    width       : 320,
    height      : 210,
    resizable   : false,
    draggable   : true,
    center      : true,
    closable    : false,
    title       : 'Crear nueve Afiliade',
    iconCls     : 'icon_user',     
    
    initComponent : function() {        
        this.items = this.buildForm();
        this.buttons = this.buildButtons();        
        GsCNT.view.UsersGroupFormWindow.superclass.initComponent.call(this);
    },
    
    buildForm : function() {
        return [
            {
                xtype   : 'afiliadoform'
            }
        ];
    },
    
    buildButtons : function() {
        return [            
            {
                text    : 'Guardar',
                iconCls : 'icon_accept',
                scope   : this,
                handler : this.saveButton_onClick
            },
            {
                text    : 'Cerrar',
                iconCls : 'icon_cancel',
                scope   : this,
                handler : function() {                    
                    if (this.items.items[0].getForm().isDirty()) {
                        Goliat.Msg.confirm('¿Desea cerrar el formulario sin guardar los cambios?', this, function(btn) {
                            if (btn == 'yes') {
                                this.close();
                            }
                            else {
                                return;
                            }
                        });
                    }
                    else {
                        this.close();
                    } 
                }
            }
        ];
    },
    
    saveButton_onClick : function() {
        
    }
});
