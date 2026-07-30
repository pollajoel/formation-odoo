/** @odoo-module */
import { Component } from "@odoo/owl";

export class AppTile extends Component {
    static template = "training_management.appTile";
    static props = {
        name: String,
        iconUrl: { optional: true },
        onClick: { type: Function, optional: true },
    };
}
