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

GsCNT.view.FederacionGrid = Ext.extend(Ext.grid.GridPanel, {
    dirty         : false,    
    viewConfig    : { forceFit : true },
    columns       : [
        {
            header    : 'Nombre',
            dataIndex : 'name',
            sortable  : true
        },
        {
            header    : 'NIA',
            dataIndex : 'nia',
            sortable  : true
        },
        {
            header    : 'Título',
            dataIndex : 'title',
            sortable  : true
        },
        {
            header    : 'Sindicato',
            dataIndex : 'sindicato',
            sortable  : true
        }
    ],
    
    initComponent : function() {
        this.store = this.buildStore();
        GsCNT.view.FederacionGrid.superclass.initComponent.call(this);
    },
    
    buildStore : function() {
        return {
            xtype    : 'jsonstore',            
            id       : 'id',                        
            autoLoad : false,
            proxy    : new Ext.data.HttpProxy({                                
                api     : {
                    read    : { url: 'federacionmanager/get_comite', method: 'GET' },
                    update  : { url: 'federacionmanager/set_comite', method: 'POST' }                                        
                }
            }),
            fields   : [
                'id', 'name', 'nia', 'comite', 'title', 'sindicato'
            ],
            sortInfo : {
                field : 'name',
                dir   : 'ASC'
            },
            listeners: {
                scope       : this,
                load        : this.onLoad,
                exception   : this.onException                
            }
        }
    },
    
    loadData : function(d) {
        return this.store.loadData(d);
    },
    
    load : function(o) {
        return this.store.load(o);
    },
    
    removeAll : function() {
        return this.store.removeAll();
    },
    
    getSelected : function() {
        return this.selModel.getSelections();
    },
    
    onLoad : function(proxy, response) {        
    },
    
    onException : function(proxy, type, action, options, response, args) {
        Goliat.Msg.alert(response.raw.message, this);       
    }
});

Ext.reg('federaciongridpanel', GsCNT.view.FederacionGrid);
