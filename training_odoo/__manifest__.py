# -*- coding: utf-8 -*-
{
    'name': "Training Odoo",

    'summary': """ Modul untuk latihan technical Odoo """,

    'description': """
        Modul ini berfungsi untuk menjalankan technical documentation pada website resmi odoo.com. Bahan yang dipelajari adalah :
        - ORM
        - Berbagai View
        - Report
        - Wizard
        - Dll
    """,

    'author': "PT. Ismata Nusantara Abadi",
    'website': "http://www.ismata.co.id",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mail', 'report_xlsx', 'om_account_budget', 'mrp', 'sale', 'account'],

    # always loaded
    'data': [
        'report/report_training_session.xml',
        'report/report_training_session2.xml',
        'report/report_action.xml',
        'report/report_action2.xml',
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/sequence_data.xml',
        'views/scheduler_data.xml',
        'views/res_partner.xml',
        'views/umroh_airline_view.xml',
        'views/purchase_order_inherit.xml',
        'views/payment_request_inherit.xml',
        'views/umroh_hotel_view.xml',
        'views/umroh_paket_perjalanan.xml',
        'views/views.xml',
        # 'views/views_1.xml',
        'views/partner_views.xml',
        'wizard/training_wizard_views.xml',
        'views/menuitem_views.xml',
        # 'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    
    'application': True,
}