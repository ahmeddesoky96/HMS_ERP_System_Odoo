from odoo import models,fields



class hmsDepartment(models.Model):
    _name='hms.department'
    name=fields.Char()
    capacity=fields.Integer()
    is_opened=fields.Boolean()
    patients=fields.One2many('hms.patient','department_name',readonly=True)