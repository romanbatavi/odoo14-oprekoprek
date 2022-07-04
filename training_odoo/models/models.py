from asyncore import write
from random import randint, seed
from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from datetime import timedelta, datetime, date
from lxml import etree


class TrainingCourse(models.Model):
    _name = 'training.course'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Training Kursus'

    def get_default_color(self):
        return randint(1, 11)
    
    def name_get(self):
        result = []
        for account in self:
            name = account.ref + ' ' + account.name
            result.append((account.id, name))
        return result
    
    name = fields.Char(string='Judul', required=True, tracking=True)
    description = fields.Text(string='Keterangan', tracking=True)
    user_id = fields.Many2one('res.users', string="Penanggung Jawab", tracking=True)
    session_line = fields.One2many('training.session', 'course_id', string='Sesi')
    product_ids = fields.Many2many('product.product', 'course_product_rel', 'course_id', 'product_id', 'Cendera Mata', tracking=True)
    ref = fields.Char(string='Referensi', readonly=True, default='/')
    level = fields.Selection([('basic', 'Dasar'), ('advanced', 'Lanjutan')], string='Tingkatan', default='basic')
    color = fields.Integer('Warna', default=get_default_color)
    email = fields.Char(string="Email", related='user_id.login')
    active = fields.Boolean('active', default=True)
    company_id = fields.Many2one('res.company', string='Company')
    harga_kursus = fields.Float('Harga Kursus Satuan(Rp).')
    
    active = fields.Boolean('Active', default=True)
    
    #QUEST 1
    attendee_ids = fields.Many2many('training.attendee', compute='_compute_peserta', string='Peserta')
    
    def _compute_peserta(self):
        data = []
        for rec in self.session_line:
            for x in rec.attendee_ids:
                data.append(x.id)
        self.attendee_ids = data
        
    # attendee_ids = fields.Many2many('training.session', string='Attendee')
    

    # #COMPUTE KURSI
    jumlah_kursi_kursus = fields.Float(compute='_compute_jumlah_kursi_kursus', string='Jumlah Kursi Kursus')
    
    # #COMPUTE HARI
    jumlah_hari_kursus = fields.Float(compute='_compute_jumlah_hari_kursus', string='Jumlah Hari Kursus')
    
    # #COMPUTE PESERTA
    jumlah_peserta = fields.Float(compute='_compute_jumlah_peserta', string='Jumlah Peserta')
    
    #COMPUTE JUMLAH HARGA KURSUS
    jumlah_harga_kursus = fields.Float(compute='_compute_jumlah_harga_kursus', string='Jumlah Harga Kursus Satuan(Rp).')
    
    
    #BIKIN TOTAL HARGA
    @api.depends('harga_kursus', 'jumlah_peserta')
    def _compute_jumlah_harga_kursus(self):
        for rec in self:
            rec.jumlah_harga_kursus = 0
            if rec.harga_kursus and rec.jumlah_peserta:
                rec.jumlah_harga_kursus = rec.harga_kursus * rec.jumlah_peserta
                if rec.jumlah_harga_kursus > 300000:
                    rec.jumlah_harga_kursus = rec.jumlah_harga_kursus * 70/100
                elif rec.jumlah_harga_kursus > 600000:
                    rec.jumlah_harga_kursus = rec.jumlah_harga_kursus * 62/100
                elif rec.jumlah_harga_kursus > 750000:
                    rec.jumlah_harga_kursus = rec.jumlah_harga_kursus * 60/100
                elif rec.jumlah_harga_kursus > 950000:
                    rec.jumlah_harga_kursus = rec.jumlah_harga_kursus * 58/100
    
    #COMPUTE PESERTA
    @api.depends('session_line')
    def _compute_jumlah_peserta(self):
        for rec in self:
            if rec.session_line:
                list_peserta = rec.session_line.mapped('attendees_count')
                rec.jumlah_peserta = sum(list_peserta) if list_peserta else 0
            else:
                rec.jumlah_peserta = 0
    
    # #COMPUTE HARI
    @api.depends('session_line')
    def _compute_jumlah_hari_kursus(self):
        for rec in self:
            if rec.session_line:
                list_hari = rec.session_line.mapped('duration')                
                # rec.jumlah_hari_kursus = (rec.end_date - rec.start_date).days
                rec.jumlah_hari_kursus = sum(list_hari) if list_hari else 0
            else:
                rec.jumlah_hari_kursus = 0
    
    # #COMPUTE KURSI
    @api.depends('session_line')
    def _compute_jumlah_kursi_kursus(self):
        for rec in self:
            if rec.session_line:
                list_kursi = rec.session_line.mapped('seats')                
                rec.jumlah_kursi_kursus = sum(list_kursi) if list_kursi else 0
            else:
                rec.jumlah_kursi_kursus = 0
    
    view_id = fields.Reference(selection=[('sale.order', 'Sale'), ('purchase.order', 'Purchase')], string='Refrensi Dokumen')
    # document_id = fields.Reference(selection=lambda self: self._get_document_types(), string='Dokumen Referensi')
    
    # model_id = fields.Many2one('ir.model', string='model')
    
    # @api.model
    # def _get_document_types(self):
    #     selection = []
    #     for i in self.env['master.document.reference'].search([]):
    #         selection.append((i.model_id.model, i.name))
    #     return selection

    _sql_constraints = [
        ('nama_kursus_unik', 'UNIQUE(name)', 'Judul kursus harus unik'),
        ('nama_keterangan_cek', 'CHECK(name != description)', 'Judul kursus dan keterangan tidak boleh sama ')
    ]

    @api.model
    def create(self, vals):
        vals['ref'] = self.env['ir.sequence'].next_by_code('training.course')
        return super(TrainingCourse, self).create(vals)

    def copy(self, default=None):
        default = dict(default or {})
        default.update(name=("%s (copy)") % (self.name or ''))
        return super(TrainingCourse, self).copy(default)

    def action_print_course(self):
        return self.env.ref('training_odoo.report_training_course_action').report_action(self)
    
    def action_print_course2(self):
        return self.env.ref('training_odoo.report_training_course_action2').report_action(self)
    
    def action_update(self):
        for rec in self:
            for x in rec.session_line:
                print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",rec.session_line)
                x.course_id = self.id
    
    # @api.model
    # def fields_view_get(self, view_id=None, view_type="form", toolbar=False, submenu=False):
    #     result = super(TrainingCourse, self).fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu)
    #     doc = etree.XML(result["arch"])
    #     if view_type == "tree" or view_type == "form" or view_type == "kanban":
    #         if not self.user_has_groups("training_odoo.group_user_cud_training_course"):
    #             for node_form in doc.xpath("//form"):
    #                 node_form.set("create", "0")
    #                 node_form.set("delete", "0")
    #                 node_form.set("edit", "0")
    #             for tree in doc.xpath("//tree"):
    #                 tree.set("create", "0")
    #                 tree.set("delete", "0")
    #                 tree.set("edit", "0")
    #             for form in doc.xpath("//kanban"):
    #                 form.set("create", "0")
    #                 form.set("delete", "0")
    #                 form.set("edit", "0")

    #     result["arch"] = etree.tostring(doc, encoding="unicode")
    #     return result
    
    @api.model_create_multi
    def create(self, vals):
        if not self.user_has_groups('training_odoo.group_user_cud_training_course'):
            raise UserError(('ANDA TIDAK MEMILIKI AKSES UNTUK MEMBUAT COURSE'))
        return super(TrainingCourse, self).create(vals)

    def unlink(self):
        for rec in self:
            if not rec.user_has_groups('training_odoo.group_user_cud_training_course'):
                raise UserError(('ANDA TIDAK MEMILIKI AKSES UNTUK HAPUS COURSE'))
        return super(TrainingCourse, self).unlink()
    
    def write(self, vals):
        res = super(TrainingCourse, self).write(vals)
        for rec in self:
            if not rec.user_has_groups('training_odoo.group_user_cud_training_course'):
                raise UserError(('ANDA TIDAK MEMILIKI AKSES UNTUK SUNTING COURSE'))
        return res

class TrainingSession(models.Model):
    _name = 'training.session'
    _description = 'Training Sesi'
    
    # ceklis = fields.Boolean(string = 'Ceklis',default = True)
    
    def write(self, vals):
        # print("=====================",self.name, '', self.level)
        # print("=====================", vals)
        return super().write(vals)

    def default_partner_id(self):
        instruktur = self.env['res.partner'].search(['|', ('instructor', '=', True), ('category_id.name', 'ilike', 'Pengajar')], limit=1)
        return instruktur

    @api.depends('start_date', 'duration')
    def get_end_date(self):
        for sesi in self:
            if not sesi.start_date: 
                sesi.end_date = sesi.start_date
                # self.env['sale.order'].name_function()
                continue

            start = fields.Date.from_string(sesi.start_date)
            sesi.end_date = start + timedelta(days=sesi.duration)
        
    def set_end_date(self):
        for sesi in self:
            if not (sesi.start_date and sesi.end_date):
                continue
            
            start_date = fields.Datetime.from_string(sesi.start_date)
            end_date = fields.Datetime.from_string(sesi.end_date)
            sesi.duration = (end_date - start_date).days + 1
            
    course_id = fields.Many2one('training.course', string='Judul Kursus', required=True, ondelete='cascade', readonly=True, states={'draft': [('readonly', False)]}, check_company=True)
    tingkatan = fields.Selection(related='course_id.level', string='Tingkatan', readonly=True, states={'draft': [('readonly', False)]})
    name = fields.Char(string='Nama', required=True, readonly=True, states={'draft': [('readonly', False)]})
    start_date = fields.Date(string='Tanggal', default=fields.Date.context_today, readonly=True, states={'draft': [('readonly', False)]})
    duration = fields.Float(string='Durasi', help='Jumlah Hari Training', default=9, readonly=True, states={'draft': [('readonly', False)]})
    seats = fields.Integer(string='Kursi', help='Jumlah Kuota Kursi', default=10, readonly=True, states={'draft': [('readonly', False)]})
    partner_id = fields.Many2one('res.partner', string='Instruktur', domain=['|', ('instructor', '=', True), ('category_id.name', 'ilike', 'Pengajar')], default=default_partner_id, readonly=True, states={'draft': [('readonly', False)]})
    attendee_ids = fields.Many2many('training.attendee', 'session_attendee_rel', 'session_id', 'attendee_id', 'Peserta', readonly=True, states={'draft': [('readonly', False)]})
    end_date = fields.Date(string="Tanggal Selesai", compute='get_end_date', inverse='set_end_date', store=True, readonly=True, states={'draft': [('readonly', False)]})
    taken_seats = fields.Float(string="Kursi Terisi", compute='compute_taken_seats')
    attendees_count = fields.Integer(string="Jumlah Peserta", compute='get_attendees_count', store=True)
    color = fields.Integer('Index Warna', default=0)
    level = fields.Selection(string='Tingkatan', related='course_id.level', readonly=True, states={'draft': [('readonly', False)]})
    state = fields.Selection([('draft', 'Draft'), ('open', 'Open'), ('done', 'Done')], string='Status', readonly=True, default='draft')
    company_id = fields.Many2one('res.company', string='Company', readonly=True, states={'draft': [('readonly', False)]})
    
    #QUEST 2
    course_ids = fields.Many2many(related="course_id.attendee_ids", string='Peserta Berdasarkan Kursus')
    
    #QUEST 2 TAPI PAKE COMPUTE
    # course2_ids = fields.Many2many('training.attendee',compute='_compute_attendesss_ids', string='Peserta Berdasarkan Kursus Pake Compute')
    
    # def _compute_attendesss_ids(self):
    #     data = []
    #     for rec in self.course_id:
    #         for x in rec.attendee_ids:
    #             data.append(x.id)
    #     self.course2_ids = data
    #==================================================================================================================#
    
    #QUEST 3
    gatau = fields.Many2many('training.attendee',compute='_compute_attendesss_ids', string='Peserta Disemua Kursus')
    entahlah_ids = fields.Many2many('training.course', string='Entahlah')
    
    def _compute_attendesss_ids(self):
        for rec in self:
            data = []
            for x in rec.entahlah_ids.attendee_ids:
                data.append(x.id)
        self.gatau = data
    
    #COMPUTE KURSI
    jumlah_kursi_kursus = fields.Integer(compute='_compute_jumlah_kursi_kursus', string='Jumlah Kursi Kursus')
    
    #COMPUTE HARI
    jumlah_hari_kursus = fields.Float(compute='_compute_jumlah_hari_kursus', string='Jumlah Hari Kursus')
    
    #COMPUTE PESERTA
    jumlah_peserta = fields.Char(compute='_compute_jumlah_peserta', string='Jumlah Peserta')
    
    # COMPUTE PESERTA
    @api.depends('course_id')
    def _compute_jumlah_peserta(self):
        for rec in self:
            if rec.course_id:
                list_peserta = rec.course_id.session_line.mapped('attendees_count')
                rec.jumlah_peserta = sum(list_peserta) if list_peserta else 0
            else:
                rec.jumlah_peserta = 0
    
    #COMPUTE HARI
    @api.depends('course_id')
    def _compute_jumlah_hari_kursus(self):
        for rec in self:
            if rec.course_id:
                list_hari = rec.course_id.session_line.mapped('duration')                
                # rec.jumlah_hari_kursus = (rec.end_date - rec.start_date).days
                rec.jumlah_hari_kursus = sum(list_hari) if list_hari else 0
            else:
                rec.jumlah_hari_kursus = 0
    
    #COMPUTE KURSI
    @api.depends('course_id')
    def _compute_jumlah_kursi_kursus(self):
        for rec in self:
            if rec.course_id:
                list_kursi = rec.course_id.session_line.mapped('seats')                
                rec.jumlah_kursi_kursus = sum(list_kursi) if list_kursi else 0
            else:
                rec.jumlah_kursi_kursus = 0
    
    # @api.onchange('course_id')
    # def _onchange_course_id(self):
    #     for rec in self:
    #         for i in rec.course_id.session_line:
    #             i.name = 'ABCDEFG'
    #             i.write({
    #                 'name': 'Annas YNWA',
    #             })
                
                
            # if rec.course_id:
            #     print('===========================', rec.course_id.session_line.name)
            # rec.name = rec.course_id.ref + ' ' + rec.course_id.name if rec.course_id else False
    # def unlink(self):
    #     if self.status != 'approve':
    #         return super().unlink()
    #     else:
    #         raise ValidationError("gaboleh ngapus")

    def action_print_session(self):
        return self.env.ref('training_odoo.report_training_session_action').report_action(self)
    
    def action_print_session2(self):
        return self.env.ref('training_odoo.report_training_session_action2').report_action(self)

    def action_confirm(self):
        self.write({'state': 'open'})
    
    def action_cancel(self):
        self.write({'state': 'draft'})
    
    def action_close(self):
        self.write({'state': 'done'})

    @api.depends('attendee_ids')
    def get_attendees_count(self):
        for sesi in self:
            sesi.attendees_count = len(sesi.attendee_ids)

    @api.depends('seats', 'attendee_ids')
    def compute_taken_seats(self):
        for sesi in self:
            sesi.taken_seats = 0
            if sesi.seats and sesi.attendee_ids :
                sesi.taken_seats = 100 * len(sesi.attendee_ids) / sesi.seats

    @api.constrains('seats', 'attendee_ids')
    def check_seats_and_attendees(self):
        for r in self:
            if r.seats < len(r.attendee_ids): 
                raise ValidationError("Jumlah Peserta Melebihi Kuota Yang Disediakan")
    

    @api.onchange('duration')
    def verify_valid_duration(self):
        if self.duration <= 0:
            self.duration = 1
            return {'warning': {'title': 'Perhatian', 'message': 'Durasi Hari Training Tidak Boleh 0 Atau Negatif'}}
    
    #RND
    @api.constrains('end_date','start_date')
    def check_end_date(self):
        for x in self:
            if x.end_date < x.start_date: 
                raise ValidationError("Tanggal Selesai Tidak Boleh Kurang Dari Tanggal Sekarang!!")
    # RND
    @api.constrains('seats')
    def check_valid_seats5(self):
        for x in self:
            if x.seats < 5: 
                raise ValidationError("Untuk Membuat Sesi Minimal Menyediakan 5 Slot Kursi")
    
    #RND
    @api.onchange('end_date')
    def verify_valid_end_date(self):
        if self.start_date >= self.end_date:
            return {'warning': {'title': 'Perhatian', 'message': 'Tanggal Selesai Tidak Boleh Kurang Dari Tanggal Sekarang!!'}}
        
    #RND
    @api.onchange('seats')
    def verify_valid_seats(self):
        if self.seats <= 5:
            return {'warning': {'title': 'Perhatian', 'message': 'Untuk Membuat Sesi Minimal Menyediakan 5 Slot Kursi'}}

    def cron_expire_session(self):
        now = fields.Date.today()
        expired_ids = self.search([('end_date', '<', now), ('state', '=', 'open')])
        expired_ids.write({'state': 'done'})


class TrainingAttendee(models.Model):
    _name = 'training.attendee'
    _description = 'Training Peserta'
    _inherits = {'res.partner': 'partner_id'}

    partner_id = fields.Many2one('res.partner', 'Partner', required=True, ondelete='cascade')
    name = fields.Char(string='Nama', required=True, inherited=True)
    sex = fields.Selection([('male', 'Pria'), ('female', 'Wanita')], string='Kelamin', required=True, help='Jenis Kelamin')
    marital = fields.Selection([
        ('single', 'Belum Menikah'),
        ('married', 'Menikah'),
        ('divorced', 'Cerai')],
        string='Pernikahan', help='Status Pernikahan')
    session_ids = fields.Many2many('training.session', 'session_attendee_rel', 'attendee_id', 'session_id', 'Sesi')

    marital = fields.Selection(selection = '_get_marital_selection', string='Marital', default=lambda self: self._get_default_martal())
    
    def _get_default_martal(self):
        session = self.env['training.session'].search([], order='create_date desc', limit=1)
        for s in session:
            return s.name
    
    def _get_marital_selection(self):
        session = self.env['training.session'].search([])
        result = []
        for s in session:
            result.append((s.name, s.name))
        return result
        # return [
        #     ('single', 'Belum Menikah'),
        #     ('married', 'Menikah'),
        #     ('divorced', 'Cerai')
        # ]
        

class IrAttachment(models.Model):
    _inherit = 'ir.attachment'
    _description = 'Ir Attachment'
        
    @api.constrains('file_size')
    def _check_attachments(self):
        limit_size = 10
        
        for attachment in self:
            if attachment.file_size > limit_size * 1024 * 1024:
                raise ValidationError("Ukuran file lampiran tidak boleh lebih besar dari {} MB".format(limit_size))
            
    """
    fungsi context:
        - ngasih nilai default:
            {'default_nama_field': 'nilai_default'}
        - sebagai parsing data, untuk pegecekan atau dikelola lagi data nya
    """
    
    # COMPUTE MAS AHMAD
    @api.depends(
        'unit_cost_line.total_rent_fuel_monthly', 
        'production_plan_ore_monthly', 
        'production_plan_quarry_monthly',
        'unit_cost_line.activity_id', 
        'operator_convert_currency',
        'consumption_cost_name',
        'is_use_consumption',
        'consumption_days',
        'salary_cost_name',
        'safety_factor',
        'is_use_salary', 
        'hr_line.amount_total',
        'hr_line.sdm_qty',
        'ore_price', 
        'income', 
        'kurs', 
    )
    def _compute_project_cost_line(self):
        activities = {}
        summary = []
        cost_converted = 0
        for rec in self:
            for cost in rec.unit_cost_line:
                if cost.activity_id not in activities:
                    activities[cost.activity_id] = cost.total_rent_fuel_monthly
                else:
                    activities[cost.activity_id] += cost.total_rent_fuel_monthly

            for act, value in activities.items():
                cost_converted = 0
                if rec.operator_convert_currency == 'x':
                    cost_converted = value * rec.kurs if rec.currency_id != rec.convert_currency_id else value
                else:
                    cost_converted = value / rec.kurs if rec.currency_id != rec.convert_currency_id and rec.kurs != 0 else value
                summary.append((0, 0, {
                    'activity_id': act.id,
                    'cost': value,
                    'cost_converted': cost_converted
                }))

            if rec.is_use_salary:
                salary_activity = rec.env['project.activity'].create({'name': rec.salary_cost_name})

                convert_to_current = sum([record.amount_total for record in rec.hr_line])
                if rec.currency_id.id != rec.convert_currency_id.id:
                    if rec.operator_convert_currency == 'x':
                        convert_to_current = convert_to_current * rec.convert_currency_id.rate if rec.currency_id != rec.convert_currency_id else convert_to_current
                    else:
                        convert_to_current = convert_to_current / rec.convert_currency_id.rate if rec.currency_id != rec.convert_currency_id else convert_to_current
                summary.append((0, 0, {
                    'activity_id': salary_activity.id,
                    'cost': sum([record.amount_total for record in rec.hr_line]),
                    'cost_converted': convert_to_current,
                }))

            if rec.is_use_consumption:
                consumption_activity = rec.env['project.activity'].create({'name': rec.consumption_cost_name})
                convert_to_current = 0
                convert_to_current = sum([record.sdm_qty for record in rec.hr_line]) * rec.consumption_days * rec.working_day_schedule

                if rec.currency_id != rec.convert_currency_id:
                    if rec.operator_convert_currency == 'x':
                        convert_to_current = convert_to_current * rec.convert_currency_id.rate
                    else:
                        convert_to_current = convert_to_current / rec.convert_currency_id.rate if rec.convert_currency_id.rate != 0 else convert_to_current
                    
                summary.append((0, 0, {
                    'activity_id': consumption_activity.id,
                    'cost': sum([record.sdm_qty for record in rec.hr_line]) * rec.consumption_days * rec.working_day_schedule,
                    'cost_converted': convert_to_current,
                })) 

            rec.project_cost_line = [(5, 0, 0)]
            rec.project_cost_line = summary

            price_income = rec.safety_factor * rec.ore_price
            rec.income = price_income
            if rec.currency_id.id != rec.convert_currency_id.id:
                rec.income = price_income * rec.convert_currency_id.rate
                # if rec.operator_convert_currency == 'x':
                #     rec.income = price_income * rec.convert_currency_id.rate
                # else:
                #     rec.income = price_income / rec.convert_currency_id.rate

            rec.cost = sum([record.cost for record in rec.project_cost_line]) if rec.project_cost_line else 0
            rec.total = rec.income - rec.cost