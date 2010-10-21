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
        this.items = this.buildComiteGrid();
        this.buttons = this.buildButtons();        
        GsCNT.view.FederacionConfigWindow.superclass.initComponent.call(this);
        
        this.addEvents(
            'editsecretario',
            'newsecretario',
            'removesecretario'            
        );
        this.getComponent('federacionGrid').load({});  
    },
    
    buildComiteGrid : function() {        
        var tbar = [
            '<b>Secretari@s</b>',
            '->',
            {
                text    : 'Nueve Secretarie',
                iconCls : 'icon_user',
                scope   : this,
                handler : this.onNewSecretario
            },
            '-',
            {
                text    : 'Eliminar Secretarie',
                iconCls : 'icon_cancel',
                scope   : this,
                handler : this.onRemoveSecretario
            }
        ];
        
        return {
            xtype       : 'federaciongridpanel',
            itemId      : 'federacionGrid',
            flex        : 1,
            loadMask    : true,
            tbar        : tbar,            
            listeners   : {
                scope       : this,
                rowdblclcik : this.onGridRowDblClick
            }
        };
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
                handler : this.cancelButton_onClick
            }
        ];
    },
    
    cancelButton_onClick : function() {
        Goliat.Msg.confirm('¿Está seguro de que quiere cerrar el formulario?<br />Cualquier cambio será irrecuperable una vez cerrado si no ha guardado previamente.', this, function(btn) {
            if (btn == 'yes') this.close();
        });         
    },
    
    saveButton_onClick : function() {
            
    },
    
    onGridRowDblClick : function(grid, rowIndex) {
        var record = grid.store.getAt(rowIndex);

        this.fireEvent('editsecretario', this, grid, record);
    },
    
    onNewSecretario : function() {
        this.fireEvent('newsecretario', this);
    },
    
    onRemoveSecretario : function() {
        
    },
    
    getGrid : function() {
        return this.getComponent('federacionGrid');
    }
});
