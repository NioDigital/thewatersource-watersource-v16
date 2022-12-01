odoo.define('pos_extend_receipt_app.model', function(require) {
	"use strict";

	var core = require('web.core');
	var utils = require('web.utils');
	var round_pr = utils.round_precision;
	var field_utils = require('web.field_utils');
	const Registries = require('point_of_sale.Registries');
	var PosDB = require('point_of_sale.DB');
	var { Order, Orderline, PosGlobalState} = require('point_of_sale.models');
	var round_di = utils.round_decimals;
	var PosDB = require('point_of_sale.DB');

	const POSReciptExtend = (PosGlobalState) => class POSReciptExtend extends PosGlobalState {
		async _processData(loadedData) {
			await super._processData(...arguments);
		}
	}
	Registries.Model.extend(PosGlobalState, POSReciptExtend);


	const CustomOrder = (Order) => class CustomOrder extends Order{
		constructor(obj, options){
			super(...arguments);
			this.invoice_number = this.invoice_number || false;
		}
		set_invoice_number(invoice_number){
			this.invoice_number = invoice_number;
		}
		get_invoice_number(){
			return this.invoice_number;
		}

		export_as_JSON(){
			var self=this;
			const loaded = super.export_as_JSON(...arguments);
			loaded.invoice_number = self.get_invoice_number() || false;
			return loaded;
		}
		init_from_JSON(json){
			super.init_from_JSON(...arguments);
			this.invoice_number = json.invoice_number || false;
		}
		export_for_printing(){
			const json = super.export_for_printing(...arguments);
			json.invoice_number = this.get_invoice_number() || 0;
            return json;
		}

	}
	Registries.Model.extend(Order, CustomOrder);

});
