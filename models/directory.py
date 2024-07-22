# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class Directory(models.Model):
    _name = 'directory.directory'
    _inherit = ['mail.thread','mail.activity.mixin']
    _description = "Directory"
    
    name = fields.Char('Name',required=True)
    user_id = fields.Many2one('res.users',default=lambda self: self.env.user)
    image_1920 = fields.Image("Image")
    visible = fields.Boolean('Visible?', readonly=False, default=True)
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.user.company_id)
    parent_id = fields.Many2one('directory.directory')
    date = fields.Date("Create Date",default=lambda self: fields.Datetime.now())
    tag_ids = fields.Many2many('directory.tags','directory_tags_rel','directory_id','tag_id', string="Tags")
    sub_dir_ids = fields.Many2many('directory.directory','directory_directory_rel','directory_id','sub_id', string="Sub Directory")
    file_ids = fields.Many2many('ir.attachment','directory_document_rel','directory_id','document_id', string="Documents")
    dir_count = fields.Integer(string="Sub Directories", compute='compute_directories')
    file_count = fields.Integer(string="Files", compute='compute_files')

    @api.depends('sub_dir_ids')
    def compute_directories(self):
        for rec in self:
            rec.dir_count = len(rec.sub_dir_ids.ids)

    @api.depends('file_ids')
    def compute_files(self):
        for rec in self:
            rec.file_count = len(rec.file_ids.ids)

    def get_file_list(self):
        documents = self.env['ir.attachment'].sudo().search([('id','in',self.file_ids.ids)])
        action = self.env.ref('document_management_app.action_document').sudo().read()[0]
        if len(documents) > 1:
            action['domain'] = [('id', 'in', documents.ids)]
        elif len(documents) == 1:
            action['domain'] = [('id', 'in', documents.ids)]
            action['res_id'] = documents.ids[0]
        else:
            action = {'type': 'ir.actions.act_window_close'}
        return action
      

    def get_sub_directories(self):
        directory = self.env['directory.directory'].sudo().search([(('id','in',self.sub_dir_ids.ids))])    
        action = self.env.ref('document_management_app.action_directory').sudo().read()[0]
        if len(directory) > 1:
            action['domain'] = [('id', 'in', directory.ids)]
        elif len(directory) == 1:
            action['domain'] = [('id', 'in', directory.ids)]
            action['res_id'] = directory.ids[0]
        else:
            action = {'type': 'ir.actions.act_window_close'}
        return action


class DirectoryTags(models.Model):
    _name = 'directory.tags'
    _description = 'Directory Tags'
    
    name = fields.Char('Name')
    user_id = fields.Many2one('res.users',default=lambda self: self.env.user)
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.user.company_id)