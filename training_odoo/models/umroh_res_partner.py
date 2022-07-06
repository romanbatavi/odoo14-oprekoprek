from odoo import api, fields, models

class ResPartnerInherit(models.Model):
    _inherit = 'res.partner'
    _description = 'INHERIT DARI RES PARTNER'
    
    # ADDICTIONAL INFORMATION
    ktp = fields.Char(string='No.KTP')
    ayah = fields.Char(string='Nama Ayah')
    pekerjaan_ayah = fields.Char(string='Pekerjaan Ayah')
    tempat_lahir = fields.Char(string='Tempat Lahir')
    pendidikan = fields.Selection([
        ('sd', 'Sekolah Dasar'), 
        ('smp', 'Sekolah Menengah Pertama'), 
        ('sma', 'Sekolah Menengah Atas/Kejuruan'),
        ('d3', 'Diploma 3'), 
        ('s1', 'S1'), 
        ('s2', 'S2'), 
        ('s3', 'S3')], 
        string='Pendidikan', help='Pendidikan Terakhir')
    status_hubungan = fields.Selection([
        ('single', 'Belum Menikah'), 
        ('married', 'Menikah'), 
        ('divorced', 'Cerai')], 
        string='Status Pernikahan', help='Status Pernikahan')
    jenis_kelamin = fields.Selection([
        ('Laki-Laki', 'Laki-Laki'), 
        ('perempuan', 'Perempuan')], 
        string='Jenis Kelamin', help='Gender')
    ibu = fields.Char(string='Nama Ibu')
    pekerjaan_ibu = fields.Char(string='Pekerjaan Ibu')
    tanggal_lahir = fields.Date(string='Tanggal Lahir')
    golongan_darah = fields.Selection([
        ('a', 'A'), 
        ('b', 'B'), 
        ('ab', 'AB'), 
        ('o', 'O')], 
        string='Golongan Darah', help='Golongan Darah')
    ukuran_baju = fields.Selection([
        ('xs', 'XS'), 
        ('s', 'S'), 
        ('m', 'M'), 
        ('l', 'L'), 
        ('xl', 'XL'), 
        ('xxl', 'XXL'), 
        ('xxxl', 'XXXL'), 
        ('4l', '4L')], 
        string='Ukuran Baju', help='Ukuran Baju')
    umur = fields.Char(compute='_compute_umur' ,string='Umur')
    
    # PASSPOR INFORMATION
    no_passpor = fields.Char(string='No.Passpor')
    tanggal_berlaku = fields.Date(string='Tanggal Berlaku')
    imigrasi = fields.Char(string='Imigrasi')
    nama_passpor = fields.Char(string='Nama Passpor')
    tanggal_habis = fields.Date(string='Tanggal Habis')
    
    # SCAN DOCUMENT
    gambar_passpor = fields.Image(string="Scan Passpor")
    gambar_ktp = fields.Image(string="Scan KTP")
    gambar_bukuk_nikah = fields.Image(string="Scan Buku Nikah")
    gambar_kartu_keluarga = fields.Image(string="Scan Kartu Keluarga")
    
    #LOGIC CHECKBOX
    airlines = fields.Boolean(string='Airlines')
    hotels = fields.Boolean(string='Hotel')
    
    #ROMAN
    braga = fields.Char(string='Ke Braga')
    asia_afrika = fields.Char(string='Ke Asia-Afrika')
    stasiun = fields.Char(string='Ke Stasiun')
    alun_alun = fields.Char(string='Ke Alun-Alun')
    harga = fields.Integer('Harga')