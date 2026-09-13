# -*- coding: utf-8 -*-
# from odoo import http


# class NtiVehicleRental(http.Controller):
#     @http.route('/nti_vehicle_rental/nti_vehicle_rental', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/nti_vehicle_rental/nti_vehicle_rental/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('nti_vehicle_rental.listing', {
#             'root': '/nti_vehicle_rental/nti_vehicle_rental',
#             'objects': http.request.env['nti_vehicle_rental.nti_vehicle_rental'].search([]),
#         })

#     @http.route('/nti_vehicle_rental/nti_vehicle_rental/objects/<model("nti_vehicle_rental.nti_vehicle_rental"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('nti_vehicle_rental.object', {
#             'object': obj
#         })

