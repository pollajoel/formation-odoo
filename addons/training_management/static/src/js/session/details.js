import { Component, useState, onWillStart } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { SelectCreateDialog } from "@web/views/view_dialogs/select_create_dialog";

//
import { ConfirmationDialog, AlertDialog } from "@web/core/confirmation_dialog/confirmation_dialog";
import { Dropdown } from "@web/core/dropdown/dropdown";
import { DropdownItem } from "@web/core/dropdown/dropdown_item";

export class SessionDetail extends Component {
    static template = "training_management.SesionDetail";
    static components = { Dropdown, DropdownItem };

    static props = {
        sessionId: Number,
        onBack: { type: Function, optional: true },
    }

    setup() {
        this.orm = useService("orm");
        this.action = useService("action")
        this.dialog = useService("dialog")
        this.notification = useService("notification")
        this.traineeService = useService("traineeService")

        this.state = useState({
            session: {},
            registration_ids : [],
            trainee_ids: []
        })

        onWillStart( async () => {
            await this.loadData()
        })
    }

    async loadData(){
        const [session] = await this.orm.read("training.session",
            [this.props.sessionId],
            [
                "name",
                "formation_id",
                "start_date",
                "registration_ids"
            ]
        );

        this.state.session = session;

        if( session.registration_ids.length){
            const registrations = await this.orm.read("training.registration",
                session.registration_ids,
                ["trainee_id"]
            );
            this.state.trainee_ids = registrations.map((r) => r.trainee_id[0]);
            this.state.registration_ids = await this.orm.read("training.trainee",
                this.state.trainee_ids,
                [
                    "name",
                    "email"
                ]
            )
        } else {
            this.state.trainee_ids = [];
            this.state.registration_ids = [];
        }
    }

    addTrainee(){
        this.dialog.add(
            SelectCreateDialog,
            {
                resModel: "training.trainee",
                title: "Ajouter des Participants",
                multiSelect: true,
                domain: [["id", "not in", this.state.trainee_ids]],
                onSelected: async (selectedIds) => {
                    await this.orm.create(
                        "training.registration",
                        selectedIds.map((traineeId) => ({
                            session_id: this.props.sessionId,
                            trainee_id: traineeId,
                        }))
                    )
                    await this.loadData()
                    this.notification.add("Participants ajoutés avec succès", {type: "success"})
                }
            }
        )
    }

    async confirmSession() {
        await this.orm.call("training.session", "action_confirm", [this.props.sessionId]);
        this.notification.add("Session confirmée", { type: "success" });
    }

    async doneSession() {
        await this.orm.call("training.session", "action_done", [this.props.sessionId]);
        this.notification.add("Session marquée comme terminée", { type: "success" });
    }

    async cancelSession() {
        await this.orm.call("training.session", "action_cancel", [this.props.sessionId]);
        this.notification.add("Session annulée", { type: "warning" });
    }

    async generateAttendanceSheet() {
                       // env["training.session"].browse([sessionId]).action_done()
        const result = await this.orm.call("training.session", "action_generate_attendance_sheet", [this.props.sessionId]);
        if (result) {
            await this.action.doAction(result);
        }
    }

    async sendAttendanceRequests() {
        await this.orm.call("training.session", "action_send_attendance_requests", [this.props.sessionId]);
        this.notification.add("Convocations envoyées", { type: "success" });
    }

    removeTrainee(traineeId){
        // warning, info, succees, danger
        this.dialog.add(
            AlertDialog,
            {
                body: "Êtes-vous sûr de vouloir retirer ce participant de la session ?",
            })
        
    }



}


// Notebook, Dropdown, Checkbox, Pager, SelectMen, TagList, ColorList, ActionSwiper