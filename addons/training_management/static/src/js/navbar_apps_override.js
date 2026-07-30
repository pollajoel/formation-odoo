/** @odoo-module */

import { registry } from  "@web/core/registry"


const navbarAppsOverrideService = {
    dependencies: ["action"],
    start(env){
        document.addEventListener(
            "click",
            (ev) => {
                const button = ev.target.closest(".o_navbar_apps_menu button");
                if( button ){
                    ev.preventDefault();
                    ev.stopPropagation();
                    env.services.action.doAction("training_management.action_training_dashboard")
                }
            },
            true // true = phase de capture
        )
    }
}

registry
    .category("services")
    .add("training_management.navbar_apps_override", navbarAppsOverrideService)


