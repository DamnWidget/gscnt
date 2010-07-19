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
    url           : 'federacionmanager/get_comite',
    viewConfig    : { forceFit : true },
    columns       : [
        {
            header    : 'Nombre',
            dataIndex : 'name',
            sortable  : true
        },
        {
            header    : 'First Name',
            dataIndex : 'firstName',
            sortable  : true
        },
        {
            header    : 'Email',
            dataIndex : 'email',
            sortable  : true
        },
        {
            header    : 'Date Hired',
            dataIndex : 'dateHired',
            sortable  : true
        },
        {
            header    : 'Rate',
            dataIndex : 'rate',
            sortable  : true,
            renderer  : Ext.util.Format.usMoney
        }
    ],
    
    initComponent : function() {
        this.store = this.buildStore();
        GsCNT.view.FederacionGrid.superclass.initComponent.call(this);
    },
    
    buildStore : function() {
        return {
            xtype    : 'jsonstore',
            url      : this.url,
            autoLoad : false,
            fields   : [
                'id', 'name', 'nia', 'comite', 'title'
            ],
            sortInfo : {
                field : 'name',
                dir   : 'ASC'
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
    }
});

Ext.reg('federaciongridpanel', GsCNT.view.FederacionGrid);
