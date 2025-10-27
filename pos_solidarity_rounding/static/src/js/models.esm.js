/** @odoo-module */

// SPDX-FileCopyrightText: 2025 Coop IT Easy SC
//
// SPDX-License-Identifier: AGPL-3.0-or-later

import {Order} from "point_of_sale.models";
import Registries from "point_of_sale.Registries";

const OrderRounding = (OriginalOrder) =>
    class extends OriginalOrder {
        determine_tip() {
            const amount = this.get_total_with_tax();
            const target_amount = Math.ceil(amount);
            return target_amount - amount;
        }
        tip_exists() {
            const lines = this.get_orderlines();
            const tip_product = this.pos.db.get_product_by_id(
                this.pos.config.tip_product_id[0]
            );

            if (tip_product) {
                if (lines.some((line) => line.get_product() === tip_product)) {
                    return true;
                }
            }
            return false;
        }
    };

Registries.Model.extend(Order, OrderRounding);
