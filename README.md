# 🐋 Environnement Odoo 19 & PostgreSQL 16 avec Docker Compose

Ce dépôt contient la configuration prête à l'emploi pour lancer instantanément un environnement de développement ou de test pour **Odoo 19**, propulsé par une base de données **PostgreSQL 16** entièrement conteneurisée.

---

## ✨ Fonctionnalités

- 🟢 **Odoo 19.0** — dernière version majeure, optimisée pour Python 3.11+
- 🐘 **PostgreSQL 16** — performances de requêtage accrues
- 💾 **Persistance totale des données** — volumes Docker pour la base de données et les filestores
- 🔄 **Hot-reload des modules** — dossier `./addons` synchronisé en temps réel avec le conteneur
- 🌐 **Réseau isolé** — communication sécurisée entre les services via un réseau Docker dédié

---

## 🛠️ Prérequis

Avant de lancer le projet, assurez-vous d'avoir :

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installé et démarré
- Un terminal (Bash, Zsh ou PowerShell)
- Git (optionnel, pour cloner le dépôt)

---

## 📁 Structure du Projet

```text
📂 mon-projet-odoo19/
├── 📂 addons/             # Vos modules Odoo 19 personnalisés
├── 📄 docker-compose.yml  # Orchestration des services
└── 📄 README.md           # Documentation
```

---

## 🚀 Démarrage en 3 étapes

### Étape 1 — Cloner ou créer le projet

```bash
# Cloner le dépôt
git clone https://github.com/votre-repo/mon-projet-odoo19.git
cd mon-projet-odoo19

# Ou créer manuellement
mkdir mon-projet-odoo19 && cd mon-projet-odoo19
mkdir -p addons
```

### Étape 2 — Lancer les conteneurs

```bash
docker compose up -d
```

Docker Compose va automatiquement :
- 📥 Télécharger les images `odoo:19` et `postgres:16`
- 🌐 Créer un réseau virtuel isolé entre les services
- 💾 Monter les volumes persistants pour les données