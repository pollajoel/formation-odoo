
Odoo a besoin qu’une base soit initialisée avec base avant de servir / correctement; sinon la registry ne contient pas ir.http
docker compose run --rm odoo odoo -d app -i base --stop-after-init