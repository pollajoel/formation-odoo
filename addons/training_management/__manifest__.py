# -*- coding: utf-8 -*-
{
    'name': 'training_management',
    'summary': """
        module de gestion des formation    
    """,
    'description': """
        ce module va permettre de gérer les formations en mettant en relations 
        les formateurs et les apprenants
    """,
    'installable': True,
    'application': True,
    'author': 'joël',
    'category': 'training',
    'version': '0.1',
    'license': 'LGPL-3', # OEEL-1 =>module entreprise, OPL-1=> Licence propietaire
    'auto_install': False,
    'depends': ['base', 'contacts', 'point_of_sale', 'sale_management', 'product'],
    'data': [ 
        'views/training_menu.xml', 
        'views/training_trainee_views.xml', 
        'views/training_trainer_views.xml',
        'views/training_training_formation_views.xml',
        'views/training_session_views.xml',
        'security/ir.model.access.csv']
}