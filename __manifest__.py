{
    'name': "OT Module",
    'version': '1.0',
    'depends': ['base', 'mail'],
    'author': "Nguyen Van Quoc",
    'category': 'Category',
    'description': """
    Description text
    """,
    # data files always loaded at installation
    'data': [
        'data/data.xml',
        'security/ir.model.access.csv',
        'security/security_access.xml',
        'views/ot_registration_view.xml',
        'views/ot_registration_line_view.xml',
        'views/ot_registration_project_view.xml',
    ],
}
