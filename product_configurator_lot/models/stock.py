# -*- coding: utf-8 -*-

from openerp import models, fields, api


class StockLot(models.Model):
    _inherit = 'stock.production.lot'

    product_id = fields.Many2one(domain=[('config_ok', '=', False)])
    description = fields.Text('Description')

    @api.multi
    def reconfigure_product(self):
        """ Creates and launches a product configurator wizard with a linked
        template and variant in order to re-configure a existing product. It is
        esetially a shortcut to pre-fill configuration data of a variant"""

        wizard_obj = self.env['product.configurator']
        wizard = wizard_obj.create({
            'product_tmpl_id': self.product_id.product_tmpl_id.id,
            'prodlot_id': self.id,
        })

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'product.configurator',
            'name': "Configure Product",
            'view_mode': 'form',
            'context': dict(
                self.env.context,
                wizard_id=wizard.id,
            ),
            'target': 'new',
            'res_id': wizard.id,
        }
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
