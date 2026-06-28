* Qu’est-ce que Docker ?
* Qu’est-ce qu’un conteneur ?
* Pourquoi utiliser Docker plutôt qu’une installation classique ?
    * Installation rapide
    * Isolation de l’environnement
    * Reproductibilité
    * Facilité de mise à jour
    * Compatible développement et production

Machine hôte
│
├── Docker
│   ├── Conteneur Odoo
│   └── Conteneur PostgreSQL
│
└── Volumes de données

2. architecture d’Odoo

Odoo a besoin de :
  * Un serveur Odoo
  * Une base PostgreSQL

Navigateur
     │
     ▼
   Odoo
     │
     ▼
 PostgreSQL

> Prérequis
  - Montrer rapidement :
    * Docker installé
    * Docker Compose disponible

> Commande :
  - docker --version
  - docker compose version