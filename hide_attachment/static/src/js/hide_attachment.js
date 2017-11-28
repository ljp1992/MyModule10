odoo.define('document.document', function(require) {
"use strict";

var core = require('web.core');
var Sidebar = require('web.Sidebar');

var _t = core._t;

Sidebar.include({
    init : function(){
        this._super.apply(this, arguments);
        var view = this.getParent();
        if (view.fields_view && view.fields_view.type === "form") {//隐藏附件按钮
            var del_index = 0;
            for (var i=0;i<this.sections.length;i++){
                if (this.sections[i].label === '附件'){
                    del_index = i;
                }
            }
            this.sections.splice(del_index, 1);
        }
    },
});

});
