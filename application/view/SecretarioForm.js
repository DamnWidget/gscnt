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

GsCNT.view.SecretarioForm = Ext.extend(Goliat.base.FormPanel, {
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
        
        GsCNT.view.SecretarioForm.superclass.initComponent.call(this);
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
                        xtype           : 'ajax',
                        id              : 'cargo_name',
                        url             : '/cargomanager',
                        fieldLabel      : 'Cargo',
                        hiddenName      : 'cargo_id',
                        valueField      : 'id',
                        displayField    : 'name',
                        relationModel   : 'Cargo',
                        ajaxManager     : GsCNT.view.CargoFormWindow,     
                        hideRemove      : false,                                           
                        anchor          : '-10',
                        emptyText       : 'Selecciona un Cargo',
                        allowBLank      : false,
                        fields          : ['id', 'name'],
                        columns         : [
                            {
                                id          : 'id',
                                header      : 'ID',
                                sortable    : true,
                                hidden      : true,
                                dataIndex   : 'id'
                            },                            
                            {
                                id          : 'name',
                                header      : 'Nombre',
                                sortable    : true,
                                dataIndex   : 'name'  
                            }                            
                        ],
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
                        xtype           : 'ajax',
                        id              : 'afiliado_name',
                        url             : '/afiliadomanager',
                        fieldLabel      : 'Afiliade',
                        hiddenName      : 'afiliado_id',
                        valueField      : 'id',
                        displayField    : 'name',
                        relationModel   : 'Afiliade a la CNT-AIT',     
                        hideRemove      : true,                                           
                        anchor          : '-10',
                        emptyText       : 'Selecciona un Afiliade',
                        allowBLank      : false,
                        fields          : ['id', 'user_id', 'name', 'nia'],
                        columns         : [
                            {
                                id          : 'id',
                                header      : 'ID',
                                sortable    : true,
                                hidden      : true,
                                dataIndex   : 'id'
                            },
                            {
                                id          : 'user_id',
                                header      : 'User ID',
                                sortable    : true,
                                hidden      : true,
                                dataIndex   : 'user_id'
                            },
                            {
                                id          : 'username',
                                header      : 'Nombre',
                                sortable    : true,
                                dataIndex   : 'name'  
                            },
                            {
                                id          : 'nia',
                                header      : 'Carné Confederal',
                                sortable    : true,
                                dataIndex   : 'nia'
                            }                            
                        ],
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

Ext.reg('secretarioform', GsCNT.view.SecretarioForm);
