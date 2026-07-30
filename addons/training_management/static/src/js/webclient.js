/** @odoo-module */


import { patch }  from "@web/core/utils/patch";
import { WebClient } from "@web/webclient/webclient";
import { browser } from "@web/core/browser/browser";

patch( WebClient.prototype,{
    async _loadDefaultApp()
    {
            // Eviter de lancer l'accueil si une action est déjà dans l'URL
        if( browser.location.hash.includes("action=")){
            return super._loadDefaultApp(...arguments);
        }
        return this.actionService.doAction("training_management.action_training_dashboard", {clearBreadcrumbs: true,})
    }
})