from odoo import models, fields, api

class BarangMasuk(models.Model):
    _name = 'barang.masuk'
    _description = 'Barang Masuk'
    
    product_name = fields.Char('Product Name',required=True)
    code = fields.Char('Code',required=True)
    product_type = fields.Char('Product Type',required=True)
    specification = fields.Char('Specification',required=True)
    purchase_price = fields.Integer('Purchase Price',required=True)
    advertising = fields.Integer('Advertising',)
    operational = fields.Integer('Operational')
    cashback = fields.Integer('Cashback')
    note = fields.Char('Note')
    month = fields.Selection([
        ('jan', 'January'),
        ('feb', 'February'),
        ('mar', 'March'),
        ('apr', 'April'),
        ('may', 'May'),
        ('jun', 'June'),
        ('jul', 'July'),
        ('aug', 'August'),
        ('sep', 'September'),
        ('oct', 'October'),
        ('nov', 'November'),
        ('dec', 'December')
    ], string='Month',required=True)
    date = fields.Selection([
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
        ('7', '7'),
        ('8', '8'),
        ('9', '9'),
        ('10', '10'),
        ('11', '11'),
        ('12', '12'),
        ('13', '13'),
        ('14', '14'),
        ('15', '15'),
        ('16', '16'),
        ('17', '17'),
        ('18', '18'),
        ('19', '19'),
        ('20', '20'),
        ('21', '21'),
        ('22', '22'),
        ('23', '23'),
        ('24', '24'),
        ('25', '25'),
        ('26', '26'),
        ('27', '27'),
        ('28', '28'),
        ('29', '29'),
        ('30', '30'),
        ('31', '31')
    ], string='Date',required=True)
    total = fields.Integer(compute='_compute_total', string='Total')
    
    @api.depends('purchase_price','advertising','operational','cashback')
    def _compute_total(self):
        for t in self:
            penjumlahan = t.purchase_price + t.advertising + t.operational - t.cashback
            t.total = penjumlahan
    
    def name_get(self):
        result = []
        for x in self:
            name = x.product_name
            result.append((x.id, name))
        return result
    
class BarangKeluar(models.Model):
    _name = 'barang.keluar'
    _description = 'Barang Keluar'
    
    masuk_id = fields.Many2one('barang.masuk', string='Product Name')
    product_type = fields.Char('Product Type',related="masuk_id.product_type")
    month = fields.Selection('Month')
    date = fields.Selection('Date')
    code = fields.Char('Code',related="masuk_id.code")
    purchase_price = fields.Integer('Purchase Price',related="masuk_id.purchase_price")
    selling_price = fields.Integer('Selling Price')
    operational = fields.Integer('Operational')
    address = fields.Char('Address')
    profit = fields.Char(compute='_compute_profit', string='Profit')

    
    @api.depends('purchase_price','selling_price','operational')
    def _compute_profit(self):
        for x in self:
            prof = x.purchase_price + x.operational - x.selling_price
            x.profit = prof
    