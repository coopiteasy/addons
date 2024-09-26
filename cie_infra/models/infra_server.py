from odoo import fields, models, api
from odoo.exceptions import Warning


class Server(models.Model):
    _name = 'infra.server'
    _description = 'server'
    name = fields.Char('name', required=True)
    ipv4 = fields.Char('ipv4')
    ipv6 = fields.Char('ipv6')
    datacenter_info = fields.Char('Datacenter info')
    ovh_address = fields.Char('OVH\'s adress', required=True)
    cie_address = fields.Char('cie adress', required=True)
    note = fields.Text('Note')
    datacenter_id = fields.Many2one('infra.datacenter', string='Datacenter')
    shortname_ids = fields.One2many('infra.server.shortname', 'server_id', string='shortname')
    instance_ids = fields.One2many('infra.instance', 'server_id', string='instance')

    @api.multi
    def _check_ipv4(self, IP):
        def isIPv4(s):
            try:
                return str(int(s)) == s and 0 <= int(s) <= 255
            except:
                return False

        if IP.count(".") == 3 and all(isIPv4(i) for i in IP.split(".")):
            return True
        return False

    @api.multi
    def _check_ipv6(self, IP):
        def isIPv6(s):
            if len(s) > 4:
                return False
            try:
                return int(s, 16) >= 0 and s[0] != '-'
            except:
                return False

        if IP.count(":") == 7 and all(isIPv6(i) for i in IP.split(":")):
            return True
        return False

    @api.multi
    def button_check_ipv(self):
        for server in self:
            if not server.ipv4 and not server.ipv6:
                raise Warning('Please provide an ipv4 or ipv6 for %s' % server.name)
            if server.ipv6 and not server._check_ipv6(self.ipv6):
                raise Warning('%s is an invalid ipv6 address' % server.ipv6)
            if server.ipv4 and not server._check_ipv4(self.ipv4):
                raise Warning('%s is an invalid ipv4 address' % server.ipv4)
        return True
