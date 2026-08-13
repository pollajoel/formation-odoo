/** @odoo-module **/

import { Component, useState, onWillStart } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

export class RegistrationList extends Component {
  static template = "training_management.RegistrationList";
  static props = {};

  setup() {
    this.registrationService = useService("registrationService");
    this.state = useState({
      registrations: [],
    });

    onWillStart(async () => {
      this.state.registrations = await this.registrationService.getRegistrationsData();
    });
  }

  openRegistration(registrationId) {
    this.registrationService.openRegistration(registrationId);
  }

  getStateLabel(state) {
    const labels = {
      draft: "Brouillon",
      waiting: "En attente de validation",
      confirm: "En attente de paiement",
      paid: "Payé",
      done: "Formation validée",
      cancel: "Terminée",
    };
    return labels[state] || state;
  }
}
