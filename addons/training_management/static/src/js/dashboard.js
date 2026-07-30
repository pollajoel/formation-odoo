/** @odoo-module */

import { Component, useState, onWillStart, onMounted } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { KpiCard } from "./KpiCard";
import { AppTile } from "./AppTile";
import { useService } from "@web/core/utils/hooks";
import { user } from "@web/core/user";

export class TrainingManagementDashboard extends Component {
  static template = "training_management.dashboard";
  // recupérer les composants.
  static components = { KpiCard, AppTile };
  setup() {
    this.orm = useService("orm");
    this.action = useService("action");
    this.menu = useService("menu");
    this.apps = this.menu.getApps().map((app) => ({
      id: app.id,
      name: app.name,
      iconUrl: this.getAppIconUrl(app),
    }));
    this.state = useState({
      currentPage: "dashboard",
      nbTrainees: 0,
      nbFormations: 0,
      nbTrainers: 0,
      loading: true,
      trainingMenuOpen: false,
      sessionMenuOpen: false,
      company: null,
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
    const companyId = user.activeCompany.id;
    const [company, traineesData, trainersData, formationData] =
      await Promise.all([
        this.orm.read("res.company", [companyId], ["name", "logo"]),
        this.orm.call("training.trainee", "get_trainees_data", []),
        this.orm.call("training.trainer", "get_trainers_data", []),
        this.orm.call("training.formation", "get_formation_data", []),
      ]);

    this.state.company = company[0];
    this.state.nbTrainees = traineesData.nbTrainees || this.state.nbTrainees;
    this.state.nbFormations = formationData.nbFormations || this.state.nbFormations;
    this.state.nbTrainers = trainersData.nbTrainers || this.state.nbTrainers;
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

  async openBySession(sessionNumber = 2) {
    await this.action.doAction({
      type: "ir.actions.act_window",
      name: "Formations",
      res_model: "training.session",
      res_id: sessionNumber,
      views: [[false, "form"]],
    });
  }

  openPageChange(pageName) {
    this.state.currentPage = pageName;
  }

  toggleMenu(menu) {
    this.state.trainingMenuOpen =
      menu === "training" ? !this.state.trainingMenuOpen : false;
    this.state.sessionMenuOpen =
      menu === "session" ? !this.state.sessionMenuOpen : false;
  }

  getAppIconUrl(app) {
    if (!app.webIconData) {
      return null;
    }
    if (app.webIconData.startsWith("data:")) {
      return app.webIconData;
    }
    const prefix = app.webIconData.startsWith("P")
      ? "data:image/svg+xml;base64,"
      : "data:image/png;base64,";
    return prefix + app.webIconData;
  }

  openApp(appId) {
    this.menu.selectMenu(appId);
  }
}

registry
  .category("actions")
  .add("training_management.dashboard", TrainingManagementDashboard);
