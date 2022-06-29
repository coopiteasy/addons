# Copyright 2014-2017 GRAP (http://www.grap.coop)
#   - Sylvain LE GAL (https://twitter.com/legalsylvain)
# Copyright 2017-Today Coop IT Easy SC
#   - Houssine BAKKALI <houssine@coopiteasy.be>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import codecs
import logging
import os
from datetime import datetime

from odoo import api, fields, models, tools

_logger = logging.getLogger(__name__)

try:
    from ftplib import FTP
except ImportError:
    _logger.warning(
        "Cannot import 'ftplib' Python Library. 'product_to_bizerba_scale' "
        "module will not work properly. "
    )


class ProductScaleLog(models.Model):
    _name = "product.scale.log"
    _inherit = "mail.activity.mixin"
    _order = "log_date desc, id desc"

    _EXTERNAL_SIZE_ID_RIGHT = 4

    _DELIMITER = "#"

    _ACTION_SELECTION = [
        ("create", "Creation"),
        ("write", "Update"),
        ("unlink", "Deletion"),
    ]

    _ACTION_MAPPING = {"create": "C", "write": "C", "unlink": "S"}

    _ENCODING_MAPPING = {"iso-8859-1": "\r\n", "cp1252": "\n", "utf-8": "\n"}

    _EXTERNAL_TEXT_ACTION_CODE = "C"

    _EXTERNAL_TEXT_DELIMITER = "#"

    log_date = fields.Datetime(string="Log Date", required=True)
    scale_system_id = fields.Many2one(
        comodel_name="product.scale.system",
        string="Scale System",
        required=True,
    )
    send_product_image = fields.Boolean(string="Send product image")
    product_id = fields.Many2one("product.template", string="Product")
    product_text = fields.Text(
        compute="_compute_text", string="Product Text", store=True
    )
    external_text = fields.Text(
        compute="_compute_text", string="External Text", store=True
    )
    external_text_display = fields.Text(
        compute="_compute_text", string="External Text (Display)", store=True
    )
    action = fields.Selection(
        selection=_ACTION_SELECTION, string="Action", required=True
    )
    sent = fields.Boolean(string="Is Sent")
    last_send_date = fields.Datetime(string="Last Send Date")

    @api.noguess
    def _auto_init(self):
        # FIXME on install -> psycopg2.ProgrammingError: relation
        #  "product_scale_log" does not exist self.env.cr.execute("DELETE
        #  FROM product_scale_log")
        res = super(ProductScaleLog, self)._auto_init()
        return res

    # Private Section
    def _clean_value(self, value, product_line):
        if not value:
            return ""
        elif product_line.multiline_length:
            res = ""
            current_val = value
            while current_val:
                res += current_val[: product_line.multiline_length]
                current_val = current_val[product_line.multiline_length :]
                if current_val:
                    res += product_line.multiline_separator
        else:
            res = value
        if product_line.delimiter:
            return res.replace(product_line.delimiter, "")
        else:
            return res

    def _generate_external_text(self, value, product_line, external_id, log):
        external_text_list = [
            self._EXTERNAL_TEXT_ACTION_CODE,  # WALO Code
            log.product_id.scale_group_id.external_identity,  # ABNR Code
            external_id,  # TXNR Code
            self._clean_value(value, product_line),  # TEXT Code
        ]
        return self._EXTERNAL_TEXT_DELIMITER.join(external_text_list)

    # Compute Section
    @api.multi  # noqa: C901 (method too complex)
    @api.depends("scale_system_id", "product_id")
    def _compute_text(self):  # noqa: C901 (method too complex)
        for log in self:

            group = log.product_id.scale_group_id
            product_text = self._ACTION_MAPPING[log.action] + self._DELIMITER
            external_texts = []

            # Set custom fields
            for product_line in group.scale_system_id.product_line_ids:
                if product_line.field_id:
                    value = getattr(log.product_id, product_line.field_id.name)

                if product_line.type == "id":
                    product_text += str(log.product_id.id)

                elif product_line.type == "numeric":
                    value = tools.float_round(
                        value * product_line.numeric_coefficient,
                        precision_rounding=product_line.numeric_round,
                    )
                    product_text += str(value).replace(".0", "")

                elif product_line.type == "text":
                    product_text += self._clean_value(value, product_line)

                elif product_line.type == "external_text":
                    external_id = str(log.product_id.id) + str(product_line.id).rjust(
                        self._EXTERNAL_SIZE_ID_RIGHT, "0"
                    )
                    external_texts.append(
                        self._generate_external_text(
                            value, product_line, external_id, log
                        )
                    )
                    product_text += external_id

                elif product_line.type == "constant":
                    product_text += self._clean_value(
                        product_line.constant_value, product_line
                    )

                elif product_line.type == "external_constant":
                    # Constant Value are like product ID = 0
                    external_id = str(product_line.id)

                    external_texts.append(
                        self._generate_external_text(
                            product_line.constant_value,
                            product_line,
                            external_id,
                            log,
                        )
                    )
                    product_text += external_id

                elif product_line.type == "many2one":
                    # If the many2one is defined
                    if value and not product_line.related_field_id:
                        product_text += value.id
                    elif value and product_line.related_field_id:
                        item_value = getattr(value, product_line.related_field_id.name)
                        product_text += item_value and str(item_value) or ""

                elif product_line.type == "many2many":
                    # Select one value, depending of x2many_range
                    if product_line.x2many_range < len(value):
                        item = value[product_line.x2many_range - 1]
                        if product_line.related_field_id:
                            item_value = getattr(
                                item, product_line.related_field_id.name
                            )
                        else:
                            item_value = item.id
                        product_text += self._clean_value(item_value, product_line)

                elif product_line.type == "product_image":
                    product_text += str(log.product_id.id) + product_line.suffix

                if product_line.delimiter:
                    product_text += product_line.delimiter
            break_line = self._ENCODING_MAPPING[log.scale_system_id.encoding]
            log.product_text = product_text + break_line
            log.external_text = break_line.join(external_texts) + break_line
            log.external_text_display = "\n".join(
                [x.replace("\n", "") for x in external_texts]
            )

    # View Section
    @api.model
    def _needaction_count(self):
        return len(self.search([("sent", "=", False)]))

    @api.model
    def ftp_connection_open(self, scale_system):
        """Return a new FTP connection with found parameters."""
        _logger.info(
            "Trying to connect to ftp://%s@%s"
            % (scale_system.ftp_login, scale_system.ftp_url)
        )
        try:
            ftp = FTP(scale_system.ftp_url)
            if scale_system.ftp_login:
                ftp.login(scale_system.ftp_login, scale_system.ftp_password)
            else:
                ftp.login()
            return ftp
        except:  # noqa: E722,B001 do not use bare 'except' fixme
            _logger.error(
                "Connection to ftp://%s@%s failed."
                % (scale_system.ftp_login, scale_system.ftp_url)
            )
            return False

    @api.model
    def ftp_connection_close(self, ftp):
        try:
            ftp.quit()
        except:  # noqa: E722,B001 do not use bare 'except' fixme
            pass

    @api.model
    def ftp_connection_push_text_file(
        self,
        ftp,
        distant_folder_path,
        local_folder_path,
        pattern,
        lines,
        encoding,
    ):
        if lines:
            # Generate temporary file
            f_name = datetime.now().strftime(pattern)
            local_path = os.path.join(local_folder_path, f_name)
            distant_path = os.path.join(distant_folder_path, f_name)
            f = open(local_path, "wb")
            for line in lines:
                f.write(line.encode(encoding))
            f.close()

            # Send File by FTP
            f = open(local_path, "rb")
            ftp.storbinary("STOR " + distant_path, f)
            f.close()
            # Delete temporary file
            os.remove(local_path)

    @api.model
    def action_send_product_image(
        self, ftp, distant_folder_path, local_folder_path, product_lst
    ):
        if not ftp:
            return False

        for product in product_lst:
            f_name = str(product.id) + ".jpeg"
            datas = codecs.decode(product.image, "base64")
            local_path = os.path.join(local_folder_path, f_name)
            distant_path = os.path.join(distant_folder_path, f_name)
            f = open(local_path, "wb")
            f.write(datas)
            f.close()
            # Send File by FTP
            f = open(local_path, "rb")
            ftp.storbinary("STOR " + distant_path, f)
            f.close()
            # Delete temporary file
            os.remove(local_path)
        return True

    @api.multi
    def send_log(self, context=None, domain=None, order=None):
        folder_path = (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("bizerba.local_folder_path")
        )
        system_map = {}
        if domain and order:  # cron_send_to_scale
            logs = self.search(domain, order=order)
        else:
            logs = self.browse(self.ids)

        for log in logs:
            if log.scale_system_id in list(system_map.keys()):
                system_map[log.scale_system_id].append(log)
            else:
                system_map[log.scale_system_id] = [log]

        for scale_system, logs in system_map.items():

            # Open FTP Connection
            ftp = self.ftp_connection_open(logs[0].scale_system_id)
            if not ftp:
                return False

            # Generate and Send Files
            product_image_lst = []
            product_text_lst = []
            external_text_lst = []

            for log in logs:
                if log.send_product_image and log.product_id.image:
                    product_image_lst.append(log.product_id)
                if log.product_text:
                    product_text_lst.append(log.product_text)
                if log.external_text:
                    external_text_lst.append(log.external_text)
            self.action_send_product_image(
                ftp,
                scale_system.product_image_relative_path,
                folder_path,
                product_image_lst,
            )
            self.ftp_connection_push_text_file(
                ftp,
                scale_system.csv_relative_path,
                folder_path,
                scale_system.external_text_file_pattern,
                external_text_lst,
                scale_system.encoding,
            )
            self.ftp_connection_push_text_file(
                ftp,
                scale_system.csv_relative_path,
                folder_path,
                scale_system.product_text_file_pattern,
                product_text_lst,
                scale_system.encoding,
            )

            # Close FTP Connection
            self.ftp_connection_close(ftp)

            # Mark logs as sent
            now = fields.Datetime.now()
            for log in logs:
                log.write({"sent": True, "last_send_date": now})
        return True

    @api.model
    def cron_send_to_scale(self):
        domain = [("sent", "=", False)]
        order = "log_date"
        self.send_log(domain=domain, order=order)
