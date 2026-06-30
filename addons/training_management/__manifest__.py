# -*- coding: utf-8 -*-
{
    'name': 'training_management',
    'summary': """
        module de gestion des formation    
    """,
    'descripton': """
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
    'depends': ['contacts'],
    'data': ['views/res_partner_views.xml', 'views/training_menu.xml']
}