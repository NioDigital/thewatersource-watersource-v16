odoo.define('pos_extend_receipt_app.pos', function(require){
	'use strict';

	const PaymentScreen = require('point_of_sale.PaymentScreen');
	const Registries = require('point_of_sale.Registries');
	const OrderReceipt = require('point_of_sale.OrderReceipt');
	const ReprintReceiptButton = require('point_of_sale.ReprintReceiptButton');
	const { isConnectionError } = require('point_of_sale.utils');


	const PosInvOrderReceipt = (OrderReceipt) =>
		class extends OrderReceipt {
			setup() {
				super.setup();
			}
			get barcode(){
				var order = this.env.pos.get_order();
				var barcode = '/report/barcode/Code128/' + this.receiptEnv.order.uid;
				return barcode
			}
			get qrcode() {
				var order = this.env.pos.get_order();
				var qrcode = '/report/barcode/QR/' + this.receiptEnv.order.uid;
				return qrcode
			}
		};

	Registries.Component.extend(OrderReceipt, PosInvOrderReceipt);

	const PosInvPaymentScreen = (PaymentScreen) =>
		class extends PaymentScreen {
			setup() {
				super.setup();
			}

			async _finalizeValidation() {
				var self = this;
				if ((this.currentOrder.is_paid_with_cash() || this.currentOrder.get_change()) && this.env.pos.config.iface_cashdrawer) {
	                this.env.proxy.printer.open_cashbox();
	            }

	            var domain = [['pos_reference', '=', this.currentOrder['name']]]
				var fields = ['account_move'];
	            this.currentOrder.initialize_validation_date();
	            this.currentOrder.finalized = true;

	            let syncOrderResult, hasError;

	            try {
	                // 1. Save order to server.
	                syncOrderResult = await this.env.pos.push_single_order(this.currentOrder);

	                // 2. Invoice.
	                if (this.currentOrder.is_to_invoice	()) {
	                    if (syncOrderResult.length) {
	                        await this.env.legacyActionManager.do_action('account.account_invoices', {
	                            additional_context: {
	                                active_ids: [syncOrderResult[0].account_move],
	                            },
	                        });
	                    } else {
	                        throw { code: 401, message: 'Backend Invoice', data: { order: this.currentOrder } };
	                    }
	                }
	                // 3. Post process.
	                if (syncOrderResult.length && this.currentOrder.wait_for_push_order()) {
	                    const postPushResult = await this._postPushOrderResolve(
	                        this.currentOrder,
	                        syncOrderResult.map((res) => res.id)
	                    );
	                    if (!postPushResult) {
	                        this.showPopup('ErrorPopup', {
	                            title: this.env._t('Error: no internet connection.'),
	                            body: this.env._t('Some, if not all, post-processing after syncing order failed.'),
	                        });
	                    }
	                }
	                
	            } catch (error) {
	                if (error.code == 700 || error.code == 701)
	                    this.error = true;

	                if ('code' in error) {
	                    // We started putting `code` in the rejected object for invoicing error.
	                    // We can continue with that convention such that when the error has `code`,
	                    // then it is an error when invoicing. Besides, _handlePushOrderError was
	                    // introduce to handle invoicing error logic.
	                    await this._handlePushOrderError(error);
	                } else {
	                    // We don't block for connection error. But we rethrow for any other errors.
	                    if (isConnectionError(error)) {
	                        this.showPopup('OfflineErrorPopup', {
	                            title: this.env._t('Connection Error'),
	                            body: this.env._t('Order is not synced. Check your internet connection'),
	                        });
	                    } else {
	                        throw error;
	                    }
	                }
	            } finally {
	                // Always show the next screen regardless of error since pos has to
	                // continue working even offline.
	                if (this.currentOrder.is_to_invoice()) {
						this.rpc({
							model: 'pos.order',
							method: 'search_read',
							args: [domain, fields],
						})
						.then(function (output) {
							var inv_print = output[0]['account_move'][1].split(" ")[0]
							self.currentOrder.invoice_number = inv_print
							self.showScreen(self.nextScreen);
						})
					}
					else{
						this.showScreen(this.nextScreen);
					}
	                // Remove the order from the local storage so that when we refresh the page, the order
	                // won't be there
	                this.env.pos.db.remove_unpaid_order(this.currentOrder);

	                // Ask the user to sync the remaining unsynced orders.
	                if (!hasError && syncOrderResult && this.env.pos.db.get_orders().length) {
	                    const { confirmed } = await this.showPopup('ConfirmPopup', {
	                        title: this.env._t('Remaining unsynced orders'),
	                        body: this.env._t(
	                            'There are unsynced orders. Do you want to sync these orders?'
	                        ),
	                    });
	                    if (confirmed) {
	                        // NOTE: Not yet sure if this should be awaited or not.
	                        // If awaited, some operations like changing screen
	                        // might not work.
	                        this.env.pos.push_orders();
	                    }
	                }
	            }
				
			}
		};

	Registries.Component.extend(PaymentScreen, PosInvPaymentScreen);

	const PosReprintReceiptButton = ReprintReceiptButton =>
        class extends ReprintReceiptButton {
            setup() {
                super.setup();
            }
            async _onClick() {
            	var self = this
               	const order = this.props.order;
               	let invoice_number = false
               	const fields_domain = ['name']
                if (this.env.pos.config.invoice_number){
                    if(order.account_move){
               			let pos_domain = [['id','=',order.account_move]];
                        await self.rpc({
							model: 'account.move',
							method: 'search_read',
							args: [pos_domain,fields_domain],
						}).then(function(output1) {
               				invoice_number = output1
							order.set_invoice_number(output1[0].name)
						});
                    }
                }
                this.showScreen('ReprintReceiptScreen', { order: order,});
                
            }
        };
    Registries.Component.extend(ReprintReceiptButton, PosReprintReceiptButton);

	return {
		PosInvPaymentScreen,
		PosInvOrderReceipt,
		PosReprintReceiptButton
	};
});
