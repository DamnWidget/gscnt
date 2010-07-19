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

GsCNT.view.FederacionConfigWindow = Ext.extend(Ext.Window, {
    layout      : 'fit',
    modal       : true,
    width       : 820,
    height      : 655,
    resizable   : false,
    draggable   : true,
    center      : true,
    closable    : false,
    
    initComponent : function() {
        this.title = 'Configuración de la Federación Local';
        this.iconCls = 'icon_federacion';
        this.items = this.buildForm();
        this.buttons = this.buildButtons();
        GsCNT.view.FederacionConfigWindow.superclass.initComponent.call(this);
    },
    
    buildForm : function() {
        return {
            xtype   : 'federacionform',
            border  : false,
            itemId  : 'federacionForm',
            tbar    : null
        }
    },
    
    buildButtons : function() {
        return [
            {
                text    : 'Cancelar',
                iconCls : 'icon_cancel',
                scope   : this,
                handler : this.cancelButton_onClick
            },
            {
                text    : 'Guardar',
                iconCls : 'icon_accept',
                scope   : this,
                handler : this.saveButton_onClick
            }
        ];
    },
    
    cancelButton_onClick : function() {
        this.close();
    },
    
    saveButton_onClick : function() {
        
    }
});
