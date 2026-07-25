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
    'depends': ['base', 'contacts', 'sale_management', 'product', 'mail', 'digest'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/mail_template_attendance_signature.xml',
        'views/attendance_signature_templates.xml',
        'report/report_training_certificate.xml',
        'report/training_certificate_report.xml',
        'views/portal_templates.xml',
        'views/training_menu.xml',
        'views/training_trainee_views.xml',
        'views/training_trainer_views.xml',
        'views/training_training_formation_views.xml',
        'views/training_session_views.xml',
        'views/training_registration_views.xml',
        'views/training_attendance_views.xml',
        'views/training_attendance_sheet_views.xml',
        'views/training_certificate_views.xml',
        'views/digest_views.xml',
        'views/wizards/add_trainee_wizard_view.xml',
        'demo/training_trainee.demo.xml',
        'demo/training_trainer.demo.xml',
        'demo/training_formation.demo.xml',
        'demo/training_session.demo.xml',
        ]
}