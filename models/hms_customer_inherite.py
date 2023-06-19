from odoo import models,fields,api
from odoo.exceptions import ValidationError
from datetime import date
import re

class CustomerTemplate(models.Model):
    _inherit='res.partner'

    vat=fields.Char(required=True)
    related_patient_id=fields.Many2many('hms.patient')
    website=fields.Char()
    email=fields.Char(related='related_patient_id.email')
    # _sql_constraints=('unique_email', 'CHECK (NOT EXISTS(SELECT 1 FROM res_partner WHERE res_partner.email = email AND res_partner.id != id))', 'Error: This email address is already assigned to another customer.')
    
    
    @api.constrains('related_patient_id')
    def email_check(self):
        for rec in self:
            if rec.email:
                existing_partner = self.env['res.partner'].search([('email', '=', rec.email), ('id', '!=', rec.id)], limit=1)
                if existing_partner:    
                    raise ValidationError("Email can't be for more than one ")


    # @api.constrains('email')
    # def _check_email_unique(self):
    #     for partner in self:
    #         if partner.email:
    #             existing_partner = self.env['res.partner'].search([('email', '=', partner.email), ('id', '!=', partner.id)], limit=1)
    #             if existing_partner:
    #                 raise ValidationError('This email address is already assigned to partner %s' % existing_partner.name)