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

GsCNT.view.SindicatosList = Ext.extend(Goliat.base.ListPanel, {
    url     : 'federacionmanager/check_sindicatos',    
    buildListView : function() {
        return {
            xtype       : 'listview',
            cls         : 'GsCNT-SL',                        
            singleSelect: true,
            store       : this.buildStore(),
            columns     : [
                {
                    header      : 'Nombre del Sindicato',
                    dataIndex   : 'name'
                }
            ]
        };
    },
    
    buildStore : function() {
        return {
            xtype       : 'jsonstore',
            autoLoad    : true,
            url         : this.url,
            root        : 'data',
            fields      : ['id', 'name', 'description', 'comite_id'],
            sortInfo    : {
                field       : 'name',
                dir         : 'ASC'
            }
        };
    },
    
    areRecords : function() {
        return (this.getStore().getCount() > 0)
    }
});

Ext.reg('sindicatoslist', GsCNT.view.SindicatosList);
