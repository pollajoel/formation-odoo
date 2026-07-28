/** @odoo-module */
import { Component } from "@odoo/owl";

export class KpiCard extends Component {
    static template = "training_management.kpiCard";
    // definir les props
    static props = {
        value: Number,
        title: String,
        onClick: { type: Function, optional: true}
    }
}