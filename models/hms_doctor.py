from odoo import models,fields


class hmsDoctor(models.Model):
    _name='hms.doctor'
    _rec_name='firstName'

    firstName=fields.Char()
    lastName=fields.Char()
    image=fields.Image()
    