# -*- coding: utf-8 -*-
from odoo import _, http
from odoo.http import request

class AttachmentDocument(http.Controller):
    @http.route("/web/document/export_zip", type="http", auth="user")
    def export_zip(self, ids=None, debug=0):
        ids = [] if not ids else ids
        if len(ids) == 0:
            return
        list_ids = map(int, ids.split(","))
        out_file = request.env["ir.attachment"].browse(list_ids)._create_zip()

        return http.send_file(
            filepath_or_fp=out_file,
            mimetype="application/zip",
            as_attachment=True,
            filename=_("export_documents.zip"),
        )
