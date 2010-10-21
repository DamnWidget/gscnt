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

GsCNT.view.CargoForm = Ext.extend(Goliat.base.FormPanel, {
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
        
        GsCNT.view.CargoForm.superclass.initComponent.call(this);
        
        this.addEvents({
            save    : true
        });
    },
    
    buildFormItems : function() {
        var nameContainer       = this.buildNameContainer();       
           
        return [
            {
                xtype   : 'hidden',
                name    : 'id'
            },
            nameContainer            
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
    }   
    
});

Ext.reg('cargoform', GsCNT.view.CargoForm);


GsCNT.view.CargoFormWindow = Ext.extend(Ext.Window, {
    layout      : 'fit',
    modal       : true,
    width       : 320,
    height      : 112,
    resizable   : false,
    draggable   : true,
    center      : true,
    closable    : false,
    title       : 'Crear nuevo Cargo',
    iconCls     : 'icon_tag',     
    
    initComponent : function() {        
        this.items = this.buildForm();
        this.buttons = this.buildButtons();        
        GsCNT.view.CargoFormWindow.superclass.initComponent.call(this);
        
        this.addEvents('save');
    },
    
    buildForm : function() {
        return [
            {
                xtype   : 'cargoform',
                itemId  : 'cargoForm'
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
        form = this.getComponent('cargoForm');
        if(form.isValid()) {
            this.fireEvent('save', form.getValues());
            form.reset();
            this.hide();
        }
        else {
            Goliat.Msg.error('El formulario contiene errores.', this);
        }       
    }    
     
});
