# -*- coding: utf-8 -*-
# from odoo import http


# class EduManagement(http.Controller):
#     @http.route('/edu_management/edu_management', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/edu_management/edu_management/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('edu_management.listing', {
#             'root': '/edu_management/edu_management',
#             'objects': http.request.env['edu_management.edu_management'].search([]),
#         })

#     @http.route('/edu_management/edu_management/objects/<model("edu_management.edu_management"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('edu_management.object', {
#             'object': obj
#         })

