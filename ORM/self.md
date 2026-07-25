## `self` et `self.env`

**`self`** : le recordset courant — l'ensemble des enregistrements sur lesquels la méthode s'exécute.

**`self.env`** : l'environnement Odoo (`Environment`) associé à ce recordset.

## Qu'est-ce que `env` ?

`env` contient tout le contexte d'exécution :

- l'accès aux modèles
- l'utilisateur connecté
- la société active
- le contexte
- le curseur (connexion à la base de données)

```
self
└── env
    ├── user      # utilisateur connecté
    ├── company   # société active
    ├── context   # contexte (lang, tz, valeurs par défaut...)
    ├── cr        # curseur SQL
    └── models    # accès aux modèles : self.env['res.partner']
```

## Accéder aux éléments de `env`

```python
user = self.env.user          # utilisateur courant (res.users)
company = self.env.company    # société courante (res.company)
context = self.env.context    # contexte (dict)
cr = self.env.cr              # curseur SQL
partner = self.env['res.partner']  # accès à un modèle
```

## Changer d'utilisateur ou de contexte

Important : `env` est **immuable**. On ne fait jamais `self.env.user = ...` directement — ça ne fonctionne pas et ce n'est pas la logique Odoo. Il faut créer un **nouveau recordset** avec un environnement modifié :

```python
# Exécuter en tant qu'un autre utilisateur
self.with_user(other_user).action_confirm()

# Exécuter avec un contexte modifié
self.with_context(lang='en_US').read(['name'])

# Exécuter avec les droits superutilisateur (bypass des règles d'accès)
self.sudo().unlink()
```

Chacune de ces méthodes renvoie une **copie** du recordset liée à un environnement différent — `self` lui-même n'est jamais modifié.
