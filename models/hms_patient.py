from odoo import models,fields,api
from odoo.exceptions import ValidationError
from datetime import date
import re

class hmsPatient(models.Model):
    _name='hms.patient'
    _rec_name='firstName'
    _defaults = {'current_date': fields.datetime.now()}

    current_date=fields.Datetime()
    firstName=fields.Char(required=True)
    lastName=fields.Char(required=True)
    birthDate=fields.Date()
    patientStatus=fields.Selection([('undetermined','Undetermined'),('good','Good'),('fair','Fair'),('serious','Serious')])
    histroy=fields.Html()
    CR_Ratio=fields.Float()
    blood_type=fields.Selection(['-A','+O'])
    PCR=fields.Boolean()
    image=fields.Image()
    address=fields.Text()
    age=fields.Integer(compute='compute_age')
    department_name=fields.Many2one('hms.department',domain=[('is_opened','=','True')])
    department_capacity=fields.Integer(related='department_name.capacity')
    doctor_name=fields.Many2many(comodel_name='hms.doctor',string='firstName')
    patientLog=fields.One2many('patient.log','patient_id')
    email=fields.Char()
    _sql_constraints=[
           ('email_check','UNIQUE(email)','Email Should Be Unique')
    ]


    @api.onchange('email')
    def validate_mail(self):
        if self.email:
            match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', self.email)
            if match == None:
                raise ValidationError('Email is not Valied  (hint:xxxxx@xxx.xxx)')
            
    @api.depends('birthDate')
    def compute_age(self):
        for rec in self:
            if rec.birthDate:
                today = date.today()
                rec.age = today.year - rec.birthDate.year - (
                        (today.month, today.day) < (rec.birthDate.month, rec.birthDate.day))
            else:
                rec.age = 0

    @api.onchange('patientStatus')
    def change_status(self):
                if self.patientStatus:
                    return{
                        'warning':{
                            'title':'status Changed',
                            'message':'status has changed to %s'%(self.patientStatus)
                        }
                    }
    @api.onchange('age')
    def change_age(self):
                if self.age:
                    if self.age<30:
                        self.PCR=True   
                        return{
                            'warning':{
                                'title':'Age Changed',
                                'message':'PCR has Checked '
                            }
                            
                        }
    @api.onchange('patientStatus')
    def log_status(self):
                if self.patientStatus:
                    vals={
                           'description':'Status has changed to %s'%(self.patientStatus),
                           'patient_id':self.id,
                           'fname':self.firstName,
                           'lname':self.lastName,
                           'age':self.age,

                    }
                    self.env['patient.log'].create(vals)
                    
    
                        
    