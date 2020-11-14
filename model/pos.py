from odoo import api, fields, models
import logging

_logger = logging.getLogger(__name__)

class ReportPosProd(models.TransientModel):
    _name = 'report.pos.prod'

    start_date = fields.Date("Tanggal Awal", required=True) 
    end_date = fields.Date("Tanggal Akhir", required=True) 

    @api.multi
    def print_report_pos_by_categ_prod(self):
        sessions = self.env['pos.session'].search(
            [ 
                ('stop_at', '<=', self.end_date),
                ('stop_at', '>=', self.start_date),
                ('state', '=', 'closed'),
            ], 
            order="stop_at asc")

        final_dict = {}

        for session in sessions:
            transactions = self.env['pos.order'].search(
                [
                    ('session_id', '=', session.name),
                    ('state', '=', 'done'),
                ]
            )
            for transaction in transactions:
                for line in transaction.lines:
                    category = line.product_id.categ_id

                    uom = line.uom_id.name
                    ratio_uom = line.product_id.product_tmpl_id.uom_id.factor

                    purchase_uom = line.uom_id.factor_inv
                    qty = line.qty
                    if(uom != False):
                        qty = line.qty*ratio_uom*purchase_uom
                    
                    if category.name not in final_dict.keys():                    
                        final_dict[category.name] = {}

                    data_of_cat = final_dict[category.name]

                    if line.product_id.id in data_of_cat.keys():
                        data_of_prod = data_of_cat[line.product_id.id]
                        data_of_prod[2] += qty
                        data_of_prod[4] += line.price_subtotal_incl

                    else:
                        data_of_cat[line.product_id.id] = []
                        data_of_cat[line.product_id.id].append(line.product_id.default_code)
                        data_of_cat[line.product_id.id].append(line.product_id.name)
                        data_of_cat[line.product_id.id].append(qty)
                        data_of_cat[line.product_id.id].append(line.product_id.product_tmpl_id.uom_id.name)
                        data_of_cat[line.product_id.id].append(line.price_subtotal_incl)

        datas = {
            'ids': self.ids,
            'model': 'report.pos.prod',
            'form': final_dict,
            'start_date': self.start_date,
            'end_date': self.end_date,

        }
        return self.env['report'].get_action(self,'report_pos_by_categ_prod.report_pos_by_categ_prod_temp', data=datas)
