/** @odoo-module **/

import { registry } from "@web/core/registry";

const registrationService = {
  dependencies: ["orm", "action"],

  start(env, { orm, action }) {
    return {
      async getRegistrationsData() {
        return await orm.searchRead(
          "training.registration",
          [],
          [
            "trainee_id",
            "session_id",
            "formation_id",
            "state",
            "sale_order_id",
          ],
        );
      },

      openRegistration(registrationId) {
        return action.doAction({
          type: "ir.actions.act_window",
          name: "Inscription",
          res_model: "training.registration",
          target: "new",
          res_id: registrationId,
          views: [[false, "form"]],
        });
      },

      create() {
        return action.doAction({
          type: "ir.actions.act_window",
          name: "Nouvelle inscription",
          res_model: "training.registration",
          target: "new",
          views: [[false, "form"]],
        });
      },
    };
  },
};

registry.category("services").add("registrationService", registrationService);
