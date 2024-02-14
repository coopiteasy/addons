/** @odoo-module */
// SPDX-FileCopyrightText: 2024 Coop IT Easy SC
//
// SPDX-License-Identifier: AGPL-3.0-or-later

// This must be imported here to ensure that the menu items are added before
// being removed by this module.
import "@web/webclient/user_menu/user_menu_items";
import {registry} from "@web/core/registry";

const userMenuRegistry = registry.category("user_menuitems");

for (const item of [
    "documentation",
    "support",
    "shortcuts",
    "separator",
    "odoo_account",
]) {
    userMenuRegistry.remove(item);
}
