from odoo import api, fields, models
from datetime import timedelta, datetime, date
import datetime


class PaketPerjalanan(models.Model):
    _name = 'paket.perjalanan'
    _description = 'Paket Perjalanan'
    
    name = fields.Char(string='Referensi', readonly=True, default='-')
    tanggal_berangkat = fields.Date('Tanggal Berangkat')
    # tanggal_berangkat = fields.Date('Tanggal Berangkat',default=datetime.datetime.now().date())
    tanggal_kembali = fields.Date('Tanggal  Kembali')
    sale_id = fields.Many2one('product.product', string='Sale')
    package_id = fields.Many2one('product.product', string='Package')
    kuota = fields.Integer('Kuota')
    sisa_kuota = fields.Integer('Sisa Kuota')
    presentasi_kuota = fields.Integer('presentasi_kuota')
    
    #KEY
    hotel_line_id = fields.One2many('hotel.line', 'paket_id', string='hotel_line')
    
class HotelLine(models.Model):
    _name = 'hotel.line'
    _description = 'Hotel Line'
    
    paket_id = fields.Many2one('paket.perjalanan', string='Hotel Line')
    partner_id = fields.Many2one('res.partner', string='Nama')
    check_in_hotel = fields.Date('Check In Hotel')
    check_out_hotel = fields.Date('Check Out Hotel')
    kota = fields.Char(related='partner_id.city',string='Kota')