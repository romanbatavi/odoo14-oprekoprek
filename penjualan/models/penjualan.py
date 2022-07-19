from odoo import api, fields, models
from datetime import timedelta, datetime, date
from odoo.exceptions import ValidationError, UserError
import datetime

class BarangMasuk(models.Model):
    _name = 'barang.masuk'
    _description = 'Barang Masuk'
    
    date = fields.Date('Tanggal',readonly=True,default=date.today())
    product_name = fields.Char('Product Name',readonly=True, states={'ready': [('readonly', False)]})
    code = fields.Char('Code',readonly=True, states={'ready': [('readonly', False)]})
    product_type = fields.Char('Product Type',readonly=True, states={'ready': [('readonly', False)]})
    specification = fields.Char('Specification',readonly=True, states={'ready': [('readonly', False)]})
    purchase_price = fields.Integer('Purchase Price',readonly=True, states={'ready': [('readonly', False)]})
    advertising = fields.Integer('Advertising', readonly=True,states={'ready': [('readonly', False)]})
    operational = fields.Integer('Operational', readonly=True,states={'ready': [('readonly', False)]})
    cashback = fields.Integer('Cashback', readonly=True, states={'ready': [('readonly', False)]})
    note = fields.Char('Note', readonly=True, states={'ready': [('readonly', False)]})
    state = fields.Selection([
        ('ready', 'Ready'),
        ('sold', 'Sold')
    ], string='Status',default='ready')
    total = fields.Integer(compute='_compute_total', string='Total')
    
    @api.depends('purchase_price','advertising','operational','cashback')
    def _compute_total(self):
        for t in self:
            penjumlahan = t.purchase_price + t.advertising + t.operational - t.cashback
            t.total = penjumlahan
    
    def name_get(self):
        result = []
        for x in self:
            name = x.code + " "  + "-" + " " + x.product_name
            result.append((x.id, name))
        return result
    
class BarangKeluar(models.Model):
    _name = 'barang.keluar'
    _description = 'Barang Keluar'
    
    date = fields.Date('Tanggal',default=date.today())
    masuk_id = fields.Many2one('barang.masuk', string='Product Name', readonly=True, required=True, states={'ready': [('readonly', False)]})
    product_type = fields.Char('Product Type',related="masuk_id.product_type")
    code = fields.Char('Code',related="masuk_id.code")
    product_name = fields.Char('Product Name',related="masuk_id.product_name")
    purchase_price = fields.Integer('Purchase Price',related="masuk_id.purchase_price")
    selling_price = fields.Integer('Selling Price', readonly=True, required=True, states={'ready': [('readonly', False)]})
    operational = fields.Integer('Operational')
    address = fields.Char('Address')
    profit = fields.Char(compute='_compute_profit', string='Profit')
    state = fields.Selection([
        ('ready', 'Ready'),
        ('sold', 'Sold')
    ], string='Status',default='ready')

    @api.depends('purchase_price','selling_price','operational')
    def _compute_profit(self):
        for x in self:
            prof = x.purchase_price + x.operational - x.selling_price
            x.profit = prof
            
    def name_get(self):
        result = []
        for x in self:
            name = x.code + " "  + "-" + " " + x.product_name
            result.append((x.id, name))
        return result
    
    def action_confirm(self):
        for x in self:
            x.state = 'sold'
            x.masuk_id.state = 'sold'

    # @api.model
    # def create(self, vals):
    #     for change in self:
    #         if change.date == change.masuk_id.date:
    #             raise UserError(("wkwkwkwwkwkwkwkwk"))
    #     makan_nasi =  super(BarangKeluar, self).create(vals)
    #     return makan_nasi