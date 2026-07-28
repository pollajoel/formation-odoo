/** @odoo-module */

import { Component, useState, onWillStart, onMounted } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { KpiCard } from "./KpiCard";
import { useService } from "@web/core/utils/hooks";

export class TrainingManagementDashboard extends Component {
  static template = "training_management.dashboard";
  // recupérer les composants.
  static components = { KpiCard };
  setup() {
    this.orm = useService("orm");  
    this.action = useService("action");
    this.state = useState({
      nbTrainees: 0,
      nbFormations: 0,
      nbTrainers: 0,
      loading: true,
    });

    // Le cylde de vie d'un composant
    onWillStart(async () => {
      await this.loadData();
    });

    onMounted(() => {
      console.log("Composant crée avec succès");
    });
  }

  async loadData() {
    try {
      const traineesData = await this.orm.call(
        "training.trainee",
        "get_trainees_data",
        [],
      );
      const trainersData = await this.orm.call(
        "training.trainer",
        "get_trainers_data",
        [],
      );
      const formationData = await this.orm.call(
        "training.formation",
        "get_formation_data",
        [],
      );
      this.state.nbTrainees = traineesData.nbTrainees || this.state.nbTrainees;
      this.state.nbFormations =
        formationData.nbFormations || this.state.nbFormations;
      this.state.nbTrainers = trainersData.nbTrainers || this.state.nbTrainers;
    } catch (e) {
      console.error("Ereuur de chargement des données", e.message, e.data);
    }
  }

  async openTrainees() {
    await this.action.doAction({
      type: "ir.actions.act_window",
      name: "Apprenants",
      res_model: "training.trainee",
      views: [
        [false, "kanban"],
        [false, "list"],
        [false, "form"],
      ],
    });
  }

  async openTrainers() {
    await this.action.doAction({
      type: "ir.actions.act_window",
      name: "Formateurs",
      res_model: "training.trainer",
      views: [
        [false, "list"],
        [false, "form"],
      ],
    });
  }

  async openTrainings() {
    await this.action.doAction({
      type: "ir.actions.act_window",
      name: "Formations",
      res_model: "training.formation",
      views: [
        [false, "list"],
        [false, "form"],
      ],
    });
  }

  async openSessions() {
    await this.action.doAction("training_management.action_training_session");
  }

  async openBySession(sessionNumber=2){

    await this.action.doAction({
      type: "ir.actions.act_window",
      name: "Formations",
      res_model: "training.session",
      res_id: sessionNumber,
      views: [
        [false, "form"],
      ],
    });



  }

}

registry
  .category("actions")
  .add("training_management.dashboard", TrainingManagementDashboard);
