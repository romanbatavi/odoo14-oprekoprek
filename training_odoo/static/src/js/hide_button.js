odoo.define('nama_modul.FormView', function (require) {
    // 'use strict'
    var FormView = require('web.FormView');
    var Context = require('web.Context');
    var core = require('web.core');
    var FormController = require('web.FormController');
    var FormRenderer = require('web.FormRenderer');
    const { generateID } = require('web.utils');
    var rpc = require('web.rpc');
    var _lt = core._lt;
    var BasicController = require('web.BasicController');
    var Dialog = require('web.Dialog');
    var dialogs = require('web.view_dialogs');
    var qweb = core.qweb;

    FormController.include({
        getState: function () {
            var self = this;
            if (this.viewType === "form" && self.modelName === 'training.session') {
                if (this.controlPanelProps.actionMenus != null) {
                    if (this.controlPanelProps.actionMenus.activeIds[0] != '') {

                        rpc.query({
                            model: 'training.session',
                            method: 'search_read',
                            args: [[['id', '=', this.controlPanelProps.actionMenus.activeIds[0]]], ['id', 'name', 'state']],
                        }).then(function (ev) {
                            if (ev[0]['state'] == 'draft' || ev[0]['state'] == 'paid' || ev[0]['state'] == 'cancel') {
                                $(".o_form_button_edit").css("display", "");
                                $(".o_form_button_create").css("display", "");
                            } else {
                                $(".o_form_button_edit").css("display", "none");
                                $(".o_form_button_create").css("display", "none");
                            }
                        });
                    }
                }
            }
            const state = this._super.apply(this, arguments);
            const env = this.model.get(this.handle, { env: true });
            state.id = env.currentId;
            return state;
        },
    });
    return FormController;
});