#   importing necesary file from flask
from flask import Flask
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from flask import request
from flask import flash
from flask import redirect
from flask import url_for
from forms import searchFile

import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
db = SQLAlchemy(app)

#   generate a secret key for forms
app.config['SECRET_KEY'] = '94692de71c05d2759ecc4bfd5d5ec4f0'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['TEXT_FILE_UPLOAD'] = './static/text_files'
app.config['ALLOWED_IMAGE_EXTENSION'] = 'TXT'


class stock(db.Model):
    index = db.Column(db.Integer, primary_key=True)
    SNO = db.Column(db.String())
    STOCK_Symbol = db.Column(db.String())
    Date = db.Column(db.String())
    Company_Name = db.Column(db.String())
    CD = db.Column(db.String())
    OLD_CE = db.Column(db.String())
    NW_ST1_CE = db.Column(db.String())
    ST2_CE = db.Column(db.String())
    ST3_CE = db.Column(db.String())
    ST4_CE = db.Column(db.String())
    ST5_CE = db.Column(db.String())
    OLD_VOL = db.Column(db.String())
    NW_ST1_VOL = db.Column(db.String())
    ST2_VOL = db.Column(db.String())
    ST3_VOL = db.Column(db.String())
    ST4_VOL = db.Column(db.String())
    ST5_VOL = db.Column(db.String())
    HG_PR = db.Column(db.String())
    CL_PR = db.Column(db.String())
    DIFF_ = db.Column(db.String())
    VOL_ = db.Column(db.String())
    VOL = db.Column(db.String())
    LOT = db.Column(db.String())
    PRM_PR = db.Column(db.String())
    INV_AMT = db.Column(db.String())
    NET_PRFT = db.Column(db.String())
    D_I_HV_HW = db.Column(db.String())
    AVERGAE_PRICE_5_DAYS = db.Column(db.String())
    AVERGAE_PRICE_10_DAYS = db.Column(db.String())
    AVERGAE_PRICE_15_DAYS = db.Column(db.String())
    AVERGAE_PRICE_20_DAYS = db.Column(db.String())
    AVERGAE_PRICE_50_DAYS = db.Column(db.String())
    WK_HG_1 = db.Column(db.String())
    WK_HG_2 = db.Column(db.String())
    WK_HG_3 = db.Column(db.String())
    MTH_HG_1 = db.Column(db.String())
    MTH_HG_2 = db.Column(db.String())

    def __repr__(self):
        return f"stock('{self.SNO}','{self.STOCK_Symbol}','{self.Date}','{self.Company_Name}','{self.CD}','{self.OLD_CE}','{self.NW_ST1_CE}','{self.ST2_CE}','{self.ST3_CE}','{self.ST4_CE}','{self.ST5_CE}','{self.OLD_VOL}','{self.NW_ST1_VOL}','{self.ST2_VOL}','{self.ST3_VOL}','{self.ST4_VOL}','{self.ST5_VOL}','{self.HG_PR}','{self.CL_PR}','{self.DIFF_}','{self.VOL_}','{self.VOL}','{self.LOT}','{self.PRM_PR}','{self.INV_AMT}','{self.NET_PRFT}','{self.D_I_HV_HW}','{self.AVERGAE_PRICE_5_DAYS}','{self.AVERGAE_PRICE_10_DAYS}','{self.AVERGAE_PRICE_15_DAYS}','{self.AVERGAE_PRICE_20_DAYS}','{self.AVERGAE_PRICE_50_DAYS}','{self.WK_HG_1}','{self.WK_HG_2}','{self.WK_HG_3}','{self.MTH_HG_1}','{self.MTH_HG_2}')"


def extract_data_from_text(text_file):
    print('reload')
    f = open('./static/text_files/{}'.format(text_file), 'r')
    st = ''
    for i in f:
        st += (i)
    f.close()
    lines = st.replace('===================R', '').replace('=', '').split('\n')
    print(len(lines))
    all_data = []
    for line in range(6, len(lines), 2):
        temp = str(lines[line]).split('|')[1:]
        temp1 = str(lines[line + 1]).split('|')[1:-1]
        temp3 = [i for i in list(str(temp[1]).split('  ')) if len(i) > 0]
        temp3.append(temp1[0])
        new_arr = (list(temp[0][-1]) + temp3 + temp[2:9] + temp1[2:] + temp[9:-1])

        # print(new_arr)
        all_data.append(new_arr)

    for data in all_data:
        row= stock(SNO=data[0],
        STOCK_Symbol=data[1],
        Date=data[2],
        Company_Name=data[3],
        CD=data[4],
        OLD_CE=data[5],
        NW_ST1_CE=data[6],
        ST2_CE=data[7],
        ST3_CE=data[8],
        ST4_CE=data[9],
        ST5_CE=data[10],
        OLD_VOL=data[11],
        NW_ST1_VOL=data[12],
        ST2_VOL=data[13],
        ST3_VOL=data[14],
        ST4_VOL=data[15],
        ST5_VOL=data[16],
        HG_PR=data[17],
        CL_PR=data[18],
        DIFF_=data[19],
        VOL_=data[20],
        VOL=data[21],
        LOT=data[22],
        PRM_PR=data[23],
        INV_AMT=data[24],
        NET_PRFT=data[25],
        D_I_HV_HW=data[26],
        AVERGAE_PRICE_5_DAYS=data[27],
        AVERGAE_PRICE_10_DAYS=data[28],
        AVERGAE_PRICE_15_DAYS=data[29],
        AVERGAE_PRICE_20_DAYS=data[30],
        AVERGAE_PRICE_50_DAYS=data[31],
        WK_HG_1=data[32],
        WK_HG_2=data[33],
        WK_HG_3=data[34],
        MTH_HG_1=data[35],
        MTH_HG_2=data[36])

        db.session.add(row)
    db.session.commit()

    try:
        os.remove('./static/text_files/{}'.format(text_file))
    except:
        pass


    return all_data


def allowed_file(filename):
    if not '.' in filename:
        return False

    ext = filename.rsplit('.', 1)[1]

    if ext.upper() in app.config['ALLOWED_IMAGE_EXTENSION']:
        return True
    else:
        return False


@app.route('/', methods=['GET', 'POST'], defaults={"page_num": 1})
@app.route('/<int:page_num>', methods=['GET', 'POST'])
def index(page_num):
    form = searchFile()
    threads = stock.query.order_by(stock.index.desc()).paginate(per_page=50, page=page_num, error_out=True)



    if request.method == 'POST' and 'tag' in request.form:
        tag = request.form["tag"]
        search = "%{}%".format(tag)
        threads = stock.query.filter(stock.STOCK_Symbol.like(search)).paginate(per_page=50, page=page_num, error_out=True)
        return render_template('index.html', threads=threads, form=form, tag=tag)

    return render_template('index.html', threads=threads, form=form)


@app.route('/add_data', methods=['GET', 'POST'])
def add_data():
    if request.method == "POST":
        if request.files:
            text = request.files["text"]

            if text.filename == '':
                flash('Your file do not have a name, please resubmit', 'danger')

            if not allowed_file(text.filename):
                flash('Please upload a valid .txt file', 'danger')

            else:
                filename = secure_filename(text.filename)
                text.save(os.path.join(app.config['TEXT_FILE_UPLOAD'], filename))
                extract_data_from_text(filename)
                flash('Your file submitted successfully', 'success')


    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)