from flask import render_template, send_from_directory
import csv, io
from werkzeug.datastructures import Headers
from pendulum import Date
from . import main
from config import basedir
from .forms import CSVUploadForm

@main.route('/', methods=['GET', 'POST'])
def index():
    form = CSVUploadForm()
    if form.validate_on_submit():
        form_input = io.StringIO(form.file.data.stream.read().decode('utf-8'))
        input_csv = csv.reader(form_input, delimiter=',', dialect='excel', lineterminator='\r\n')

        def remove_slash(d):
            return d.replace('/', '')

        def join_date_numb(d, m):
            return d + m

        def format_amount(a):
            a1 = a.replace('$', '')
            a2 = a1.replace('.', '')
            return a2.replace(',', '')

        row_num = 0
        ce_num = 525627
        txt_filename = Date.today().format('%m%d%Y') + '.txt'

        with open(txt_filename, 'w+') as output_text:
            for row in input_csv:
                if row_num >= 1:
                    date = remove_slash(row[0])
                    date_memb = join_date_numb(date, row[2])
                    last_name = row[3].split(',')
                    amount = format_amount(row[7])
                    ce_num_final = str(ce_num) + 'CE'
                    line = '{date_memb} {last_name}{ce_num_final}{amount}\n'.format(date_memb=date_memb.ljust(13),
                                                                                    last_name=last_name[0].ljust(33),
                                                                                    ce_num_final=ce_num_final.ljust(12),
                                                                                    amount=amount)
                    output_text.write(line)
                ce_num += 1
                row_num += 1
            output_text.close()
        headers = Headers()
        headers.set('Content-Disposition', 'attachment', filename=txt_filename)

        return send_from_directory(basedir, txt_filename, mimetype='text/css', as_attachment=True)

    return render_template('index.html', form=form)