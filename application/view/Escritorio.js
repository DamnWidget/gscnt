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

GsCNT.view.Escritorio = Ext.extend(Ext.Panel, {
    itemId      : 'escritorioPanel',
    layout      : 'column',
    autoScroll  : true,
    cls         : 'gscnt-escritorio',
    defaultType : 'escritoriocolumn',    
    
    initComponent : function(){
        GsCNT.view.Escritorio.superclass.initComponent.call(this);
        this.addEvents({
            validatedrop    : true,
            beforedragover  : true,
            dragover        : true,
            beforedrop      : true,
            drop            : true
        });
        this.buildLayout();
    },
    
    buildLayout : function() {
        for(var i = 0; i < this.pLayout.columns.length; i++) {            
            this.add(
                { 
                    columnWidth : this.pLayout.columns[i].columnWidth,
                    style       :'padding: 10px',
                    items       : this.pLayout.columns[i].items 
                }
            );
        }
    },
    
    addPortlet : function(column, portlet) {
        this.items.items[column].add(portlet);                
    },

    initEvents : function(){
        GsCNT.view.Escritorio.superclass.initEvents.call(this);
        this.dd = new GsCNT.view.Escritorio.DropZone(this, this.dropConfig);
    },
    
    beforeDestroy : function() {        
        if(this.dd) {
            this.dd.unreg();
        }
        GsCNT.view.Escritorio.superclass.beforeDestroy.call(this);
    }
});

Ext.reg('escritorio', GsCNT.view.Escritorio);

GsCNT.view.Escritorio.DropZone = Ext.extend(Ext.dd.DropTarget, {
    
    constructor : function(escritorio, cfg){
        this.escritorio = escritorio;
        Ext.dd.ScrollManager.register(escritorio.body);
        GsCNT.view.Escritorio.DropZone.superclass.constructor.call(this, escritorio.bwrap.dom, cfg);
        escritorio.body.ddScrollConfig = this.ddScrollConfig;
    },
    
    ddScrollConfig : {
        vthresh: 50,
        hthresh: -1,
        animate: true,
        increment: 200
    },

    createEvent : function(dd, e, data, col, c, pos){
        return {
            escritorio: this.escritorio,
            panel: data.panel,
            columnIndex: col,
            column: c,
            position: pos,
            data: data,
            source: dd,
            rawEvent: e,
            status: this.dropAllowed
        };
    },

    notifyOver : function(dd, e, data){
        var xy = e.getXY(), escritorio = this.escritorio, px = dd.proxy;

        // case column widths
        if(!this.grid){
            this.grid = this.getGrid();
        }

        // handle case scroll where scrollbars appear during drag
        var cw = escritorio.body.dom.clientWidth;
        if(!this.lastCW){
            this.lastCW = cw;
        }else if(this.lastCW != cw){
            this.lastCW = cw;
            escritorio.doLayout();
            this.grid = this.getGrid();
        }

        // determine column
        var col = 0, xs = this.grid.columnX, cmatch = false;
        for(var len = xs.length; col < len; col++){
            if(xy[0] < (xs[col].x + xs[col].w)){
                cmatch = true;
                break;
            }
        }
        // no match, fix last index
        if(!cmatch){
            col--;
        }

        // find insert position
        var p, match = false, pos = 0,
            c = escritorio.items.itemAt(col),
            items = c.items.items, overSelf = false;

        for(var len = items.length; pos < len; pos++){
            p = items[pos];
            var h = p.el.getHeight();
            if(h === 0){
                overSelf = true;
            }
            else if((p.el.getY()+(h/2)) > xy[1]){
                match = true;
                break;
            }
        }

        pos = (match && p ? pos : c.items.getCount()) + (overSelf ? -1 : 0);
        var overEvent = this.createEvent(dd, e, data, col, c, pos);

        if(escritorio.fireEvent('validatedrop', overEvent) !== false &&
           escritorio.fireEvent('beforedragover', overEvent) !== false){

            // make sure proxy width is fluid
            px.getProxy().setWidth('auto');

            if(p){
                px.moveProxy(p.el.dom.parentNode, match ? p.el.dom : null);
            }else{
                px.moveProxy(c.el.dom, null);
            }

            this.lastPos = {c: c, col: col, p: overSelf || (match && p) ? pos : false};
            this.scrollPos = escritorio.body.getScroll();

            escritorio.fireEvent('dragover', overEvent);

            return overEvent.status;
        }else{
            return overEvent.status;
        }

    },

    notifyOut : function(){
        delete this.grid;
    },

    notifyDrop : function(dd, e, data){
        delete this.grid;
        if(!this.lastPos){
            return;
        }
        var c = this.lastPos.c, 
            col = this.lastPos.col, 
            pos = this.lastPos.p,
            panel = dd.panel,
            dropEvent = this.createEvent(dd, e, data, col, c,
                pos !== false ? pos : c.items.getCount());

        if(this.escritorio.fireEvent('validatedrop', dropEvent) !== false &&
           this.escritorio.fireEvent('beforedrop', dropEvent) !== false){

            dd.proxy.getProxy().remove();
            panel.el.dom.parentNode.removeChild(dd.panel.el.dom);
            
            if(pos !== false){
                c.insert(pos, panel);
            }else{
                c.add(panel);
            }
            
            c.doLayout();

            this.escritorio.fireEvent('drop', dropEvent);

            // scroll position is lost on drop, fix it
            var st = this.scrollPos.top;
            if(st){
                var d = this.escritorio.body.dom;
                setTimeout(function(){
                    d.scrollTop = st;
                }, 10);
            }

        }
        delete this.lastPos;
    },

    // internal cache of body and column coords
    getGrid : function(){
        var box = this.escritorio.bwrap.getBox();
        box.columnX = [];
        this.escritorio.items.each(function(c){
             box.columnX.push({x: c.el.getX(), w: c.el.getWidth()});
        });
        return box;
    },

    // unregister the dropzone from ScrollManager
    unreg: function() {
        Ext.dd.ScrollManager.unregister(this.escritorio.body);
        GsCNT.view.Escritorio.DropZone.superclass.unreg.call(this);
    }
});
