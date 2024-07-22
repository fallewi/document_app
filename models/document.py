# -*- coding: utf-8 -*-
import uuid
import zipfile
from werkzeug.urls import url_encode
from io import BytesIO
from odoo import _, fields,models, api
from odoo.exceptions import UserError

class Attachment(models.Model):
    _name = 'ir.attachment'
    _inherit = ['ir.attachment','portal.mixin','mail.thread','mail.activity.mixin']

    user_id = fields.Many2one('res.users',default=lambda self: self.env.user)
    visible = fields.Boolean('Visible?', readonly=False, default=True)
    tag_ids = fields.Many2many('document.tags','document_tags_rel','document_id','tag_id', string="Tags")
    directory_id = fields.Many2one('directory.directory')

    # ====== send return template 
    def _find_mail_template(self, force_confirmation_template=False):
        template_id = False
        if force_confirmation_template:
            template_id = self.env['ir.model.data']._xmlid_to_res_id('document_management_app.email_template_send_document', raise_if_not_found=False)
        return template_id

    # ====  send document email
    def action_document_send(self):
        ''' Opens a wizard to compose an email, with relevant mail template loaded by default '''
        self.ensure_one()
        template_id = self._find_mail_template()
        lang = self.env.context.get('lang')
        template = self.env['mail.template'].browse(template_id)
        if template.lang:
            lang = template._render_lang(self.ids)[self.id]
        ctx = {
            'default_model': 'ir.attachment',
            'default_res_id': self.ids[0],
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'default_composition_mode': 'comment',
            'mark_so_as_sent': True,
            'custom_layout': "mail.mail_notification_paynow",
            'proforma': self.env.context.get('proforma', False),
            'force_email': True,
            'model_description': self.with_context(lang=lang),
        }
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(False, 'form')],
            'view_id': False,
            'target': 'new',
            'context': ctx,
        }

    # === document export to zip file
    def action_document_download_zip(self):
        items = self.filtered(lambda x: x.type == "binary")
        if not items:
            raise UserError(
                _("Only binary attachments allowed.")
            )
        ids = ",".join(map(str, items.ids))
        return {
            "type": "ir.actions.act_url",
            "url": "/web/document/export_zip?ids=%s" % (ids),
            "target": "self",
        }

    def _create_zip(self):
        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
            for attachment in self:
                attachment.check("read")
                zip_file.writestr(
                    attachment._compute_zip_name(),
                    attachment.raw,
                )
            zip_buffer.seek(0)
            zip_file.close()
        return zip_buffer

    def _compute_zip_name(self):
        """Give a chance of easily changing the name of the file inside the ZIP."""
        self.ensure_one()
        return self.name

    # === Share document action
    @api.model
    def action_share(self):
        action = self.env["ir.actions.actions"]._for_xml_id("portal.portal_share_action")
        action['context'] = {'active_id': self.env.context['active_id'],
                             'active_model': self.env.context['active_model']}
        return action


class DocumentTags(models.Model):
    _name = 'document.tags'
    _description = "Document Tags"
    
    name = fields.Char('Name')
    user_id = fields.Many2one('res.users',default=lambda self: self.env.user)
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.user.company_id)
