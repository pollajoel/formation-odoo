FROM  odoo:19
USER root
RUN pip install --no-cache-dir --break-system-packages python-jose[cryptography] PyJWT
# Créer dossier custom addons
RUN mkdir -p /mnt/extra-addons
# Copier ton module dans l'image
COPY ./addons /mnt/extra-addons
# Droits Odoo
RUN chown -R odoo:odoo /mnt/extra-addons
# Retour user odoo
USER odoo
# Port Odoo
EXPOSE 8069