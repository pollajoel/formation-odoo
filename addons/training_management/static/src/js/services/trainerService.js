/** @odoo-module **/

import { registry } from "@web/core/registry";

const trainerService = {
  dependencies: ["orm", "action"],

  start(env, { orm, action }) {
    return {
      async getTrainersData() {
        const trainersData = await orm.call(
          "training.trainer",
          "get_trainers_data",
          [],
        );
        return trainersData;
      },

      async openTrainers() {
        await action.doAction({
          type: "ir.actions.act_window",
          name: "Formateurs",
          res_model: "training.trainer",
          views: [
            [false, "list"],
            [false, "form"],
          ],
        });
      },
      create(){
        return action.doAction({
          type: "ir.actions.act_window",
          name: "Nouveau formateur",
          res_model: "training.trainer",
          target:"new",
          views: [
              [false, "form"],
          ],
        });
      }

    };
  },
};

registry.category("services").add("trainerService", trainerService);
