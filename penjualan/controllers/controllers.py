# -*- coding: utf-8 -*-
# from odoo import http


# class Penjualan(http.Controller):
#     @http.route('/penjualan/penjualan/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/penjualan/penjualan/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('penjualan.listing', {
#             'root': '/penjualan/penjualan',
#             'objects': http.request.env['penjualan.penjualan'].search([]),
#         })

#     @http.route('/penjualan/penjualan/objects/<model("penjualan.penjualan"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('penjualan.object', {
#             'object': obj
#         })
