/** @odoo-module */

// SPDX-FileCopyrightText: 2025 Coop IT Easy SC
//
// SPDX-License-Identifier: AGPL-3.0-or-later

import PaymentScreen from "point_of_sale.PaymentScreen";
import Registries from "point_of_sale.Registries";
import {onWillStart} from "@odoo/owl";

const PaymentScreenSolidarityRounding = (PaymentScreen_) =>
    class extends PaymentScreen_ {
        setup() {
            super.setup(...arguments);
            onWillStart(() => {
                this.setSolidarityRoundingTip();
            });
        }

        // On partner change:
        // Tips will have to be removed manually when changing from
        // a customer with rounding enabled to another with rounding
        // disabled, since there is no way to know if the tip was
        // added automatically or manually by the cashier
        async selectPartner() {
            await super.selectPartner(...arguments);
            this.setSolidarityRoundingTip();
        }

        setSolidarityRoundingTip() {
            const order = this.currentOrder;
            const partner = order.get_partner();
            if (partner && partner.enable_solidarity_rounding && !order.tip_exists()) {
                const tip = order.determine_tip();
                order.set_tip(tip);
            }
        }
    };

Registries.Component.extend(PaymentScreen, PaymentScreenSolidarityRounding);
