/** @odoo-module alias=pos_customer_wallet.models **/
// SPDX-FileCopyrightText: 2022 Coop IT Easy SC
//
// SPDX-License-Identifier: AGPL-3.0-or-later

import {Order} from "point_of_sale.models";
import Registries from "point_of_sale.Registries";

const WalletOrder = (Order_) =>
    class extends Order_ {
        export_for_printing() {
            var json = super.export_for_printing(...arguments);
            json.customer_wallet_balance = this.partner
                ? this.partner.customer_wallet_balance
                : 0;
            return json;
        }
    };

Registries.Model.extend(Order, WalletOrder);
export default WalletOrder;
