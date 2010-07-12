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

GsCNT.view.Portlet = Ext.extend(Ext.Panel, {
    anchor : '100%',
    frame : true,
    collapsible : true,
    draggable : true,
    cls : 'gscnt-escritorio-portlet'
});

Ext.reg('portlet', GsCNT.view.Portlet);

GsCNT.view.Portlet.Tools = [
    {
        id:'gear',
        handler: function(){
            Ext.Msg.alert('Message', 'The Settings tool was clicked.');
        }
    },
    {
        id:'close',
        handler: function(e, target, panel){
            panel.ownerCt.remove(panel, true);
        }
    }
];