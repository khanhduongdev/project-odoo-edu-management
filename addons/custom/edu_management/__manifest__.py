# -*- coding: utf-8 -*-
{
    'name': "edu_management",

    'summary': "Module quản lý lớp học, khóa học Odoo 17",

    'description': """
        Module quản lý đào tạo bao gồm:
        - Quản lý khóa học
        - Quản lý lớp học
        - Quản lý giảng viên/học viên
        - Báo cáo thống kê
    """,

    'author': "Your Name",
    'website': "https://www.yourcompany.com",
    'category': 'Education',
    'version': '0.1',

    # Dependencies
    'depends': ['base', 'product', 'mail'],

    # Always loaded
    'data': [
        'security/edu_security.xml',
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'views/edu_course_views.xml',
        'views/edu_subject_views.xml',
        'views/edu_classroom_views.xml',
        'views/edu_session_views.xml',
        'views/res_partner_views.xml',
        'views/menus.xml',
    ],
    # Demo data
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
