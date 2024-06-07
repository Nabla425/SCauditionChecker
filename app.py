from flask import Flask, render_template,request,redirect,session,jsonify,url_for,flash
import Init,Game,util
from transfer_class import Passive
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

from transfer_class import Settings,Situation,Memory

#jinja2とvuejsでデリミタが重複しているので変更
class CustomFlask(Flask):
    jinja_options = Flask.jinja_options.copy()
    jinja_options.update(dict(
    block_start_string='(%',
    block_end_string='%)',
    variable_start_string='((',
    variable_end_string='))',
    comment_start_string='(#',
    comment_end_string='#)',
  ))

app = Flask(__name__)
app.secret_key = 'test'
app.config['JSON_SORT_KEYS'] = False
# MySQLの設定
# SQLAlchemyの設定
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:AdminAdmin@localhost/scdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

class Users(db.Model):
    username = db.Column(db.String(20), primary_key=True, nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    oath_lv = db.Column(db.Integer, nullable=False, default=0)
    created = db.Column(db.TIMESTAMP, nullable=False, server_default=db.func.current_timestamp())
 
@app.route("/",methods=['GET','POST'])
def index():
    return render_template("index.html")

@app.route("/audition",methods=['GET','POST'])
def audition():
    return render_template('audition.html')
    
@app.route("/api/turn",methods=["GET","POST"])
def exe_one_turn():
    print('get request!!!!!')
    in_data = request.json
    settings = Settings.settings()
    settings.set_from_json(in_data['settings'])
    situation = Situation.situation()
    situation.set_from_json(in_data['situation'])
    input = dict(request.json['form'])
    #1ターン分の処理
    GM = Game.play(settings,situation)
    isEnd = GM.oneTurnProcess(input)
    data ={'settings':settings.get_dict(),'situation':situation.get_dict(),'isEnd':isEnd,'result':dict(GM.result_dict)}
    return jsonify(data)

@app.route("/api/init",methods=["GET","POST"])
def audition_init():
        audition_name = '歌姫楽宴'
        rival_list,judge_dict = Init.init_audition(audition_name)
        support_keys = ['"櫻木真乃駅線上の日常4凸"','"風野灯織水面を仰いで海の底4凸"','"小宮果穂反撃の狼煙をあげよ！4凸"','"園田智代子kimagure全力ビート！4凸"']
        support_list = []
        for key in support_keys:
            support_list.append(Init.set_support(key))
        trend = {'Vo':1,'Da':2,'Vi':3}
        pweapon_list = Init.set_pweapon()
        '''
        # test_passive
        aquired_passive = [
            Passive.passive("きゅんコメ金",'履歴(まのひお)',3,100,Passive.history_requirement,[["Vi",75]],["櫻木真乃","風野灯織"]),
            Passive.passive("水面を仰いで海の底金",'3t以降',3,100,Passive.after_turn_requirement,[["Da",60],["Vi",30]],3),
            Passive.passive("駅線上の日常白",'3t以前',3,100,Passive.before_turn_requirement,[["Da",30],["Vi",30]],3),
        ]
        '''
        aquired_passive = [
            Passive.passive("きゅんコメ金",'キュンコメ金',3,40,Passive.history_requirement,[["Vi",75]],["櫻木真乃","風野灯織"]),
            Passive.passive("水面を仰いで海の底金",'海金',3,10,Passive.after_turn_requirement,[["Da",60],["Vi",30]],3),
            Passive.passive("水面を仰いで海の底白1",'海白1',3,10,Passive.no_requirement,[["Da",40],["Vi",20]]),
            Passive.passive("駅線上の日常金",'駅金',3,10,Passive.after_turn_requirement,[["Da",65],["Vi",65]],3),
            Passive.passive("駅線上の日常白",'駅白',3,10,Passive.before_turn_requirement,[["Da",30],["Vi",30]],6),
        ]
        
        settings = Settings.settings(
            support_list=support_list,pweapon_list=pweapon_list,audition_name=audition_name[1:-1],
            week=29,trend=trend,rival_list=rival_list,idol='八宮めぐる',memory=Memory.memory(idol_name='八宮めぐる'),
            aquired_passive=aquired_passive)
        settings.set_rival_mem_turn()
        situation=Situation.situation(judge_dict=judge_dict,status={'Vo':300,'Da':500,'Vi':415,'Me':317,'memory_gage':0.1,'star':0},passive_list=aquired_passive)
        #初ターンのパッシブを鳴かせる
        situation.passive_process(settings)
        data ={'settings':settings.get_dict(),'situation':situation.get_dict()}
        return jsonify(data)
        
@app.route('/audition/back')
def back_one_turn():
    if len(session['history'])>0:
        session['situation'] = session['history'].pop()
    return redirect('/audition')

#ログイン関係
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        # ユーザーが既に存在するかチェック
        existing_user = Users.query.filter_by(username=username).first()
        if existing_user:
            flash('ユーザ名はすでに登録されています。', 'error')
            return redirect(url_for('register'))  
        new_user = Users(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        
        return redirect(url_for('login'))
    
    return render_template('/register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password_candidate = request.form['password']
        
        user = Users.query.filter_by(username=username).first()
        
        if user and bcrypt.check_password_hash(user.password, password_candidate):
            session['logged_in'] = True
            session['username'] = username
            session['oath_lv'] = user.oath_lv
            return redirect(url_for('audition'))
        else:
            return 'Invalid username or password'
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('audition'))
    


if __name__ == '__main__':
    app.run(debug=True)


