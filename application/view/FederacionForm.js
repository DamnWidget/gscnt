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

GsCNT.view.FederacionForm = Ext.extend(Goliat.base.FormPanel, {    
    layout        : {
        type  : 'vbox',
        align : 'stretch'
    },
    
    initComponent : function() {        
        this.items = [
            {
                xtype       : 'panel',
                bodyStyle   : 'text-align: center; margin: 10px; font-size: 18px; font-weight: bold;',
                html        : 'Grupo de usuarios del Comité',
                border      : false                    
            },
            this.buildGeneralInfoForm(),
            this.buildComiteGrid()
        ];
        GsCNT.view.FederacionForm.superclass.initComponent.call(this);        
    },
    
    buildGeneralInfoForm : function() {
        var rightHalf = {
            xtype      : 'container',
            title      : 'Descripción',
            flex       : 1,
            bodyStyle  : 'padding: 1px; margin: 0px;',
            layout     : 'form',
            labelWidth : 70,
            items      : {
                xtype      : 'textarea',
                fieldLabel : 'Descripción',
                name       : 'description',
                anchor     : '100% 100%'
            }
        };
        
        var leftHalf = {
            xtype       : 'container',
            layout      : 'form',
            flex        : 1,
            labelWidth  : 60,
            defaultType : 'textfield',
            defaults    : { anchor: '-10' },
            items       : [
                {
                    xtype      : 'hidden',
                    name       : 'id'
                },
                {
                    fieldLabel : 'Nombre',
                    name       : 'name',
                    allowBlank : false,
                    maxLength  : 255
                },
                {
                    xtype      : 'checkbox',
                    fieldLabel : 'Activo',
                    name        : 'active'
                }
            ]
        };
        
        return {          
            layout       : 'hbox',
            height       : 100,
            bodyStyle    : 'padding: 10px',
            layoutConfig : { align : 'stretch' },
            border       : false,
            items        : [                
                leftHalf,
                rightHalf
            ]
        };
    },
    
    buildComiteGrid : function() {        
        var tbar = [
            '<b>Secretari@s</b>',
            '->',
            {
                text    : 'Nuevo Secretario',
                iconCls : 'icon_user',
                scope   : this,
                handler : this.onNewSecretario
            },
            '-',
            {
                text    : 'Eliminar Secretario',
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
    
    onGridRowDblClick : function(grid, rowIndex) {
        var record = grid.store.getAt(rowIndex);

        this.fireEvent('editsecretario', this, grid, record);
    },
    
    onNewSecretario : function() {
        
    },
    
    onRemoveSecretario : function() {
        
    }
    
});

Ext.reg('federacionform', GsCNT.view.FederacionForm);
