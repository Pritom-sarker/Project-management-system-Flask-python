#   importing necesary file from flask
from flask import Flask,session,send_file
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from flask import request
from flask import flash
from flask import redirect
from flask import url_for
from forms import searchFile
import os
from werkzeug.utils import secure_filename
import pandas as pd
import datetime
import mail

UPLOAD_FOLDER = '/uploads'
ALLOWED_EXTENSIONS = { 'rar', 'zip'}



app = Flask(__name__)
db = SQLAlchemy(app)

#   generate a secret key for forms
app.config['SECRET_KEY'] = '94692de71c05d2759ecc4bfd5d5ec4f0'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['TEXT_FILE_UPLOAD'] = '/uploads'
app.config['ALLOWED_IMAGE_EXTENSION'] = 'ZIP'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def insert_project_with_team(t,p,a):
    if t== '0':
        return 0
    row = project(
        team=t,
        project=p,
        amount=a,
        status='Active'
    )

    db.session.add(row)


class files(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.String())
    team = db.Column(db.String())
    date = db.Column(db.String())
    file_name = db.Column(db.String())

    def __repr__(self):
        return f"people('{self.ID}','{self.order_id}','{self.team}','{self.date}','{self.file_name})"

class work(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    Date = db.Column(db.String())
    Work = db.Column(db.String())
    notes = db.Column(db.String())
    Owner = db.Column(db.String())
    Budget = db.Column(db.String())
    Team = db.Column(db.String())
    Cost = db.Column(db.String())
    Total_Earning = db.Column(db.String())
    Des = db.Column(db.String())
    Status = db.Column(db.String())
    deadline = db.Column(db.String())
    end_time = db.Column(db.String())
    def __repr__(self):
        return f"stock('{self.ID}','{self.Date}','{self.Work}','{self.Date}','{self.Owner}','" \
               f"{self.Budget}','{self.Team}','{self.Cost}','{self.Total_Earning}','{self.Des}','{self.Status}','{self.deadline}','{self.end_time}','{self.notes})"



class people(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    position = db.Column(db.String())
    user = db.Column(db.String())
    email = db.Column(db.String())
    password = db.Column(db.String())
    earning=db.Column(db.String())
    paid = db.Column(db.String())

    def __repr__(self):
        return f"people('{self.position}','{self.user}','{self.email}','{self.password})"

class project(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    team = db.Column(db.Integer)
    project = db.Column(db.Integer)
    amount = db.Column(db.Integer)
    status = db.Column(db.String())

    def __repr__(self):
        return f"people('{self.team}','{self.project}','{self.amount}','{self.status})"


class money(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer)
    amount = db.Column(db.String())
    date = db.Column(db.String())

    def __repr__(self):
        return f"people('{self.ID}','{self.team}','{self.amount}','{self.date})"

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def check_login():
    try:
        print(session['id'] , session['Type'])
        if session['id'] and session['Type']=='owner' :
            return True
    except:
        print('Err')
        return False

def check_login_team():
    try:
        print(session['id'] , session['Type'])
        if session['id'] and session['Type']=='Team' :
            print('login')
            return True
    except:
        print('Err')
        return False

@app.route('/', methods=['GET', 'POST'], defaults={"page_num": 1})
def index(page_num):

    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST' and 'user' in request.form and 'pass' in request.form:
        user = (request.form["user"])
        pas = (request.form["pass"])
        per = people.query.filter_by(email=user).first()
        if not per:
            flash('Please input a valid username!!', 'danger')
        else:
            if str(per.password) == pas:
                print('Bingoooooooooooo!!!!')
                session['id'] = per.ID
                session['Type'] = per.position
                session['name']=per.user
                if per.position =='owner':
                    flash('Your login successfully', 'success')
                    return redirect(url_for('owner'))
                else:
                    return redirect(url_for('team'))
            else:
                flash('Please input a valid Login!!', 'danger')
                return render_template('index.html')
    else:
        flash('Please input a valid Login!!', 'danger')
        return render_template('index.html')


# team dash
@app.route('/team', methods=['GET', 'POST'], defaults={"page_num": 1})
@app.route('/team/<int:page_num>', methods=['GET', 'POST'])
def team(page_num):
    if not check_login_team():
        return  render_template('index.html')

    date_1 = datetime.datetime.now()
    dead = date_1.strftime('%b')
    form = searchFile()

    # take all the projects

    all_project= project.query.filter_by(team=session['name'])
    projects_by_him=[]
    for proj in all_project:
        projects_by_him.append([proj.project,proj.amount])


    complete_proj=0
    complete_money=0


    running_proj=0
    running_money=0

    running_work=[]
    for proj in projects_by_him:
        temp = work.query.filter_by(ID=proj[0])
        if temp[0].Status == 'Active' or temp[0].Status == 'Rivision' :
            print(temp[0])
            running_work.append(temp[0])
            running_proj+=1
            running_money+=float(proj[1])

        elif temp[0].Status == 'Complete':
            complete_proj+=1
            complete_money+=float(proj[1])

    mon = money.query.filter_by(team_id=session['id'])

    total_paid=0
    for m in mon:
        total_paid+=float(m.amount)

    balance = complete_money-total_paid
    return render_template('team_dash.html',threads=running_work,  over=(complete_proj,complete_money,running_proj,running_money,total_paid,balance),form=form)


@app.route('/owner', methods=['GET', 'POST'], defaults={"page_num": 1})
@app.route('/owner/<int:page_num>', methods=['GET', 'POST'])
def owner(page_num):
    if not check_login():
        return  render_template('index.html')

    date_1 = datetime.datetime.now()
    dead = date_1.strftime('%b')
    form = searchFile()

    all_project=work.query.filter((work.end_time.like('%{}%'.format(dead))))


    com_price=0
    com_order=0
    for proj in all_project:
        if 'Com' in proj.Status:
            com_order+=1
            com_price+=float(proj.Total_Earning)

    all_project=work.query.filter((work.Status=='Active') |(work.Status=='Rivision')).order_by(work.Date.desc())

    total_running = 0
    total_order=0
    for proj in all_project:
            total_order+=1
            total_running+=float(proj.Total_Earning)



    threads = work.query.filter((work.Status=='Active') |(work.Status=='Rivision') ).paginate(per_page=10, page=page_num)

    return render_template('owner.html', threads=threads, over=(com_price,com_order,total_running,total_order),form=form)



@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if not check_login():
        return render_template('index.html')
    form = searchFile()

    return render_template('add_user.html', form=form)


@app.route('/add_money', methods=['GET', 'POST'])
def add_money():
    if not check_login():
        return render_template('index.html')
    form = searchFile()
    team = request.form["team"]
    pas = request.form["amnt"]
    row = money(team_id=team,
                 date=datetime.datetime.now().strftime('%b %d,%Y %H:%M'),
                 amount=pas)

    db.session.add(row)
    db.session.commit()

    return redirect(url_for('user_list'))



@app.route('/files_upload', methods=['GET', 'POST'])
def files_upload():
    print('Here')
    ind = (request.args.get('q'))
    if request.files:
        text = request.files["files"]

        if text.filename == '':
            flash('Your file do not have a name, please resubmit', 'danger')

        if not allowed_file(text.filename):
            flash('Please upload a valid .txt file', 'danger')

        else:
            filename = secure_filename(text.filename)
            try:
                os.mkdir('/uploads/{}'.format(ind))
            except:
                pass

            text.save(os.path.join(app.config['TEXT_FILE_UPLOAD'],ind, filename))
            flash('Your file submitted successfully', 'success')
            row = files(order_id=ind,
                         team=session['name'],
                         date=datetime.datetime.now().strftime('%b %d,%Y %H:%M'),
                         file_name=os.path.join(app.config['TEXT_FILE_UPLOAD'],ind, filename))

            db.session.add(row)
            db.session.commit()

    if  check_login():
        return redirect(('/order_owner?q='+ind))
    else:
        return redirect(('/order_team?q=' + ind))

@app.route('/add_notes', methods=['GET', 'POST'])
def add_notes():
    # if check_login():
    #     return render_template('index.html')

    ind = (request.args.get('q'))

    thread = work.query.filter_by(ID=ind)
    try:
        date_1 = datetime.datetime.strptime(thread[0].deadline, '%b %d,%Y %H:%M:%S')
        d = date_1 + datetime.timedelta(days=int(request.form["time"]))
        dead = d.strftime('%b %d,%Y %H:%M:%S')

        thread[0].deadline = dead
    except:
        pass
    #print(thread[0].notes)
    try:
        thread[0].notes += '+' + request.form["note"]
    except:

        thread[0].notes = request.form["note"]+ '+'

    db.session.commit()


    return redirect(('/order_owner?q='+ind))

@app.route('/add_new_user', methods=['GET', 'POST'], defaults={"page_num": 1})
def add_new_user(page_num):
    if not check_login():
        return render_template('index.html')
    form = searchFile()
    return render_template('add_user.html', form=form)

@app.route('/logout', methods=['GET', 'POST'], defaults={"page_num": 1})
def logout(page_num):
    session.pop('id', None)
    session.pop('name', None)
    session.pop('Type', None)
    return render_template('index.html')

@app.route('/insert_new_user', methods=['GET', 'POST'], defaults={"page_num": 1})
def insert_new_user(page_num):
    if not check_login():
        return render_template('index.html')
    form = searchFile()
    if request.method == 'POST' and 'name' in request.form and 'email' in request.form  and 'password' in request.form:
        name = request.form["name"]
        email = request.form["email"]
        pas = request.form["password"]
        radio = request.form["r1"]
        try:
            check = request.form["check"]
        except:
            check=''




        print(name,email,pas,radio,check)
        row = people(position=radio,
                     user=name,
                     email = email,
                     password= pas)

        db.session.add(row)
        db.session.commit()
        flash('{}  Added as a {}'.format(name,radio), 'success')
    else:
        print(request.form["name"])
    return redirect(url_for('add_new_user'))




@app.route('/add_new_order', methods=['GET', 'POST'], defaults={"page_num": 1})
def add_new_order(page_num):
    if not check_login():
        return render_template('index.html')
    form = searchFile()
    threads = people.query.filter_by(position='Buyer')
    threads1 = people.query.filter_by(position='Team')
    return render_template('add_new_order.html', buyer=threads, team=threads1,form=form)



@app.route('/insert_new_order', methods=['GET', 'POST'], defaults={"page_num": 1})
def insert_new_order(page_num):
    if not check_login():
        return render_template('index.html')
    if request.method == 'POST' :
        name = request.form["title"]
        budget = request.form["budget"]
        pas = request.form["buyer"]
        team=''
        try:
            T1 = request.form["T1"]
            team+=T1+','
        except:
            pass
        try:
            T2 = request.form["T2"]
            team+=T2+','
        except:
            pass
        try:
            T3 = request.form["T3"]
            team+=T2+','
        except:
            pass

        cost=0
        try:
            P1 = request.form["P1"]
            cost+=int(P1)
        except:
            pass

        try:
            P2 = request.form["P2"]
            cost+=int(P2)
        except:
            pass

        try:
            P3 = request.form["P3"]
            cost+=int(P3)
        except:
            pass
        des = request.form["des"]


        date_1 = datetime.datetime.now()
        d= date_1 + datetime.timedelta(days=int(request.form["dead"]))
        dead = d.strftime('%b %d,%Y %H:%M:%S')


        new_time  = datetime.datetime.now().strftime('%b %d,%Y %H:%M')
        try:
            final= str(float(budget) - float(cost))
        except:
            final = str(float(budget))
        row = work(Date=str( new_time),
                           Work=name,
                           Owner=pas,
                           Budget=budget,
                           Team=team ,
                           Cost=cost,
                           Total_Earning=final,
                           Des=des,
                           deadline=dead,
                           Status='Active')

        db.session.add(row)
        db.session.commit()
        if request.files:
            text = request.files["file"]


            if not allowed_file(text.filename):
                flash('Please upload a valid .zip file', 'danger')

            else:
                filename = secure_filename(text.filename)
                text.save(os.path.join(app.config['TEXT_FILE_UPLOAD'], filename))
                flash('Your file submitted successfully', 'success')

        temp1 =  work.query.filter_by(Date=new_time)

        try:
            insert_project_with_team(T1,temp1[0].ID,P1)
            temp = people.query.filter_by(user=T1)
            print(temp[0].email)
            s = '{},\nWork Title: {}\n Budget: {}\n\nFor more information please login\nLink: https://accountbook.xyz/\nEmail: {}\nPassword: {}'.format(T1,name,str(P1)
                                                                                                                                                   ,str(temp[0].email)
                                                                                                                                                       ,str(temp[0].password))
            mail.send_email(temp[0].email,'Congratulation!! You got a new order',s)

        except:
            pass


        try:
            insert_project_with_team(T2,temp1[0].ID,P2)
            temp = people.query.filter_by(user=T2)
            print(temp[0].email)
            s = '{},\nWork Title: {}\n Budget: {}\n\nFor more information please login\nLink: https://accountbook.xyz/\nEmail: {}\nPassword: {}'.format(
                T2, name, str(P2)
                , str(temp[0].email)
                , str(temp[0].password))
            mail.send_email(temp[0].email, 'Congratulation!! You got a new order', s)
        except:
            pass

        try:
            insert_project_with_team(T3,temp1[0].ID,P3)
            temp = people.query.filter_by(user=T3)
            print(temp[0].email)
            s = '{},\nWork Title: {}\n Budget: {}\n\nFor more information please login\nLink: https://accountbook.xyz/\nEmail: {}\nPassword: {}'.format(
                T3, name, str(P3)
                , str(temp[0].email)
                , str(temp[0].password))
            mail.send_email(temp[0].email, 'Congratulation!! You got a new order', s)
        except:
            pass

        db.session.commit()


        #flash('{}  Added as a {}'.format(name,radio), 'success')
    else:
        print('else')

    return redirect(url_for('add_new_order'))


@app.route('/download')
def downloadFile ():

    date = datetime.datetime.now().strftime('%b_%d_%Y_%H_%M')

    ind = (request.args.get('q'))
    print(ind)
    path = r"{}".format(str(ind[2:]).replace('/','\\'))
    return send_file(path, as_attachment=True)



@app.route('/order_team', methods=['GET', 'POST'], defaults={"page_num": 1})
def order_team(page_num):
    
    if not check_login_team():
        if check_login():
            return redirect("/order_owner?q=" + (request.args.get('q')))
        return render_template('index.html')
    form = searchFile()
    ind = (request.args.get('q'))
    threads = work.query.filter_by(ID=ind)
    user = project.query.filter((project.project==ind) & (project.team==session['name']))
    all_user=people.query.filter_by(position='Team')

    fils = files.query.filter_by(order_id=ind)
    return render_template('team_order.html', work=threads[0],user=user,all_user = all_user,form=form,down=fils)


@app.route('/order_owner', methods=['GET', 'POST'])
def order_owner():
    if not check_login():
        return render_template('index.html')
    form = searchFile()
    ind = (request.args.get('q'))
    threads = work.query.filter_by(ID=ind)
    user = project.query.filter_by(project=ind )
    all_user=people.query.filter_by(position='Team')

    fils = files.query.filter_by(order_id=ind)
    ntes = str(threads[0].notes).split('+')
    return render_template('owner_order.html', work=threads[0],user=user,all_user = all_user,form=form,down=fils,notes=ntes)

@app.route('/update_order_status', methods=['GET', 'POST'], defaults={"page_num": 1})
def update_order_status(page_num):
    if not check_login():
        return render_template('index.html')
    form = searchFile()
    ind = (request.args.get('id'))
    threads = work.query.get(ind)
    threads.Status=request.form["T3"]
    if 'Com' in request.form["T3"]:
        threads.end_time = datetime.datetime.now().strftime('%b %d,%Y %H:%M')
        db.session.commit()
    else:
        threads.end_time = ''
        db.session.commit()

    flash('Order Marked as {}'.format(request.form["T3"]), 'success')
    return redirect(url_for('owner'))


@app.route('/User_list', methods=['GET', 'POST'], defaults={"page_num": 1})
@app.route('/User_list/<int:page_num>', methods=['GET', 'POST'])
def user_list(page_num):
    if not check_login():
        return render_template('index.html')
    form = searchFile()

    threads = people.query.filter_by().paginate(per_page=10, page=page_num)
    print(threads.items)
    return render_template('user_list.html', threads=threads)

@app.route('/delete_user', methods=['GET', 'POST'], defaults={"page_num": 1})
def delete_user(page_num):
    if not check_login():
        return render_template('index.html')
    form = searchFile()
    ind = (request.args.get('q'))

    threads = people.query.filter_by(ID=ind)
    db.session.delete(threads[0])
    db.session.commit()
    return redirect(url_for('user_list'))


@app.route('/all_order', methods=['GET', 'POST'], defaults={"page_num": 1})
@app.route('/all_order/<int:page_num>', methods=['GET', 'POST'])
def all_order(page_num):
    if not check_login():
        return render_template('index.html')
    form = searchFile()
    threads = work.query.filter_by().order_by(work.Date.asc()).paginate(per_page=10, page=page_num)
    return render_template('all_orders.html', threads=threads)




@app.route('/all_order_team', methods=['GET', 'POST'], defaults={"page_num": 1})
@app.route('/all_order_team/<int:page_num>', methods=['GET', 'POST'])
def all_order_team(page_num):
    if not check_login_team():
        return render_template('index.html')

    # take all the projects

    all_project= project.query.filter_by(team=session["name"]).order_by(project.ID.desc())
    projects_by_him=[]
    for proj in all_project:
        projects_by_him.append([proj.project,proj.amount])

    thread=[]
    for proj in projects_by_him:
        data = proj
        temp = work.query.filter_by(ID=proj[0])
        data.append(temp[0].Work)
        data.append(temp[0].Status)
        data.append(proj[0])
        data.append(temp[0].Date)
        thread.append(data)

    return render_template('all_order_team.html',threads=thread)


@app.route('/Transaction', methods=['GET', 'POST'], defaults={"page_num": 1})
@app.route('/Transaction/<int:page_num>', methods=['GET', 'POST'])
def Transaction(page_num):
    if not check_login_team():
        return render_template('index.html')

    # take all the projects

    all_project= money.query.filter_by(team_id=session["id"]).paginate(per_page=10, page=page_num)

    # monthly curve


    return render_template('trancetion.html',threads=all_project)



@app.route('/add_budget', methods=['GET', 'POST'], defaults={"page_num": 1})
def change_order_price(page_num):
    if not check_login():
        return render_template('index.html')
    form = searchFile()
    ind = (request.args.get('id'))

    threads = work.query.filter_by(ID=ind)
    threads[0].Budget=request.form['budget']
    threads[0].Total_Earning=int(request.form['budget'])-int(threads[0].Cost)

    db.session.commit()

    return redirect(('order_owner?q='+ind))

@app.route('/add_team', methods=['GET', 'POST'], defaults={"page_num": 1})
def add_team(page_num):
    if not check_login():
        return render_template('index.html')
    form = searchFile()
    ind = (request.args.get('id'))

    threads = work.query.filter_by(ID=ind)
    threads[0].Team += ','+request.form['buyer']
    threads[0].Cost = float(threads[0].Cost) + int(request.form['budget'])
    threads[0].Total_Earning= float(threads[0].Total_Earning)- int(request.form['budget'])


    insert_project_with_team(request.form['buyer'], ind, request.form['budget'])
    db.session.commit()

    return redirect(('order_owner?q='+ind))


@app.route('/delete_team', methods=['GET', 'POST'], defaults={"page_num": 1})
def delete_team(page_num):
    if not check_login():
        return render_template('index.html')
    form = searchFile()
    ind = (request.args.get('id'))

    name = (request.args.get('name'))
    amnt = (request.args.get('amount'))
    threads = work.query.filter_by(ID=ind)

    threads[0].Team = str(threads[0].Team ).replace(name,'').replace(',,',',')
    threads[0].Cost = float(threads[0].Cost) - float(amnt)
    threads[0].Total_Earning= float(threads[0].Total_Earning) + float(amnt)

    peo = project.query.filter((project.team==name) & (project.project==ind))

    db.session.delete(peo[0])


    db.session.commit()

    return redirect(('order_owner?q='+ind))



@app.route('/team_person', methods=['GET', 'POST'], defaults={"page_num": 1})
def team_person(page_num):
    date_1 = datetime.datetime.now()
    dead = date_1.strftime('%b')
    form = searchFile()
    id =(request.args.get('id'))
    name = (request.args.get('name'))
    # take all the projects

    all_project = project.query.filter_by(team=name)
    projects_by_him = []
    for proj in all_project:
        projects_by_him.append([proj.project, proj.amount])

    complete_proj = 0
    complete_money = 0

    running_proj = 0
    running_money = 0

    running_work = []
    for proj in projects_by_him:
        temp = work.query.filter_by(ID=proj[0])
        if temp[0].Status == 'Active' or temp[0].Status == 'Rivision':
            print(temp[0])
            running_work.append(temp[0])
            running_proj += 1
            running_money += float(proj[1])

        elif temp[0].Status == 'Complete':
            complete_proj += 1
            complete_money += float(proj[1])

    mon = money.query.filter_by(team_id=id)

    total_paid = 0
    for m in mon:
        total_paid += float(m.amount)

    balance = complete_money - total_paid
    return render_template('team_dash.html', threads=running_work,
                           over=(complete_proj, complete_money, running_proj, running_money, total_paid, balance),
                           form=form)


if __name__ == "__main__":
    app.run(debug=True)