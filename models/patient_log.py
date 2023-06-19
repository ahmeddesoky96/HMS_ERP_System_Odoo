from odoo import models , fields


class HMSPatientLog(models.Model):
    _name = 'patient.log'
    
    description= fields.Text()
    fname=fields.Char()
    lname =fields.Char()
    age=fields.Integer()
    patient_id = fields.Many2one('hms.patient')
    

    
    