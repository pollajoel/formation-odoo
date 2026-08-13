/** @odoo-module  */

import { Component, useState, onWillStart } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

export class SessionKanban extends Component {
  static template = "training_management.SesionKanban";
      static props = {
        openSession: { type: Function, optional: true },
        sessionState: { type: String, optional: true },
    };

  setup() {
    this.orm = useService("orm");
    this.action = useService("action");
    this.state = useState({
      sessions: [],
    });

    onWillStart(async () => {
      this.loadSessions();
    });
  }

  async loadSessions() {
    this.state.sessions = await this.orm.searchRead(
      "training.session",
      [["state", "=", this.props.sessionState]],
      [
        "state",
        "trainer_id",
        "registration_ids",
        "trainer_id",
        "start_date",
        "state",
        "name",
        "formation_id",
      ],
    );
  }

//   openSession(sessionId) {
//     this.action.doAction({
//       type: "ir.actions.client",
//       tag: "training_session_detail",
//       params: {
//         sessionId: sessionId,
//       },
//     });
//   }

  getStateIcon(state) {
    const icons = {
      draft: "fa-pencil",
      confirmed: "fa-check-circle",
      done: "fa-flag-checkered",
      cancel: "fa-times-circle",
    };
    return icons[state] || "fa-circle";
  }
}
