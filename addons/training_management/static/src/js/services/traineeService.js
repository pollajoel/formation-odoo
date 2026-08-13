/** @odoo-module **/

import { registry } from "@web/core/registry";

const traineeService = {
  dependencies: ["orm", "action"],

  start(env, { orm, action }) {
    return {
      create(){
        return action.doAction({
          type: "ir.actions.act_window",
          name: "Nouveau participant",
          res_model: "training.trainee",
          target:"new",
          views: [
              [false, "form"],
          ],
        });
      }

    };
  },
};

registry.category("services").add("traineeService", traineeService);
