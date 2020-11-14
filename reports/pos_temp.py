from odoo import api, models


class ReportPosByCategProd(models.AbstractModel):
    _name = 'report.report_pos_by_categ_prod.report_pos_by_categ_prod_temp'

    @api.model
    def render_html(self, docids, data=None):
        docargs =  {
            'doc_ids': data.get('ids'),
            'doc_model': data.get('model'),
            'data': data['form'],
            'start_date': data['start_date'],
            'end_date': data['end_date'],
        }
        print "===================docargs",docargs
        return self.env['report'].render('report_pos_by_categ_prod.report_pos_by_categ_prod_temp', docargs)
