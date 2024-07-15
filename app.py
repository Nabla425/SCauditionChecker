import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from flask import Flask, render_template,request,redirect,session,jsonify,url_for,flash, jsonify
import Init,Game,util
from transfer_class import Passive
from flask_bcrypt import Bcrypt
import DataHandler as DH
from transfer_class import Support,P_weapon
import Entity
import os
from transfer_class import Settings,Situation,Memory


app = Flask(__name__)

app.secret_key = 'test'

# 環境変数の取得
db_user = os.getenv('DB_USER', 'Nabla')
db_password = os.getenv('DB_PASSWORD', 'AdminAdmin')
db_host = os.getenv('DB_HOST', 'Nabla.mysql.pythonanywhere-services.com')
db_name = os.getenv('DB_NAME', 'Nabla$scdb')

# データベース接続情報の設定
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}'
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 280}

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

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


@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template('index.html')

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
    print('initing!!!!!!!!!!!!!')
    audition_name = '歌姫楽宴'
    rival_list,judge_dict = Init.init_audition(audition_name)
    support_list = Init.set_support()
    trend = {'Vo':1,'Da':2,'Vi':3}
    pweapon_list = Init.set_pweapon()

    # test_passive
    aquired_passive = [
        Passive.passive("きゅんコメ","金1",'きゅんコメ金1',3,40,Passive.history_requirement,[["Vi",75]],["櫻木真乃","風野灯織"]),
        Passive.passive("水面を仰いで海の底",'金1','海金',3,10,Passive.after_turn_requirement,[["Da",60],["Vi",30]],[3]),
        Passive.passive("駅線上の日常",'白1','駅白',3,10,Passive.before_turn_requirement,[["Da",30],["Vi",30]],[3]),
    ]
    passive_list =[
        {'name':p._name,'rest':p._times,'isActive':False,
            'text':p.get_text(),'short_name':p._short_name} for p in aquired_passive
    ]

    settings = Settings.settings(
        support_list=support_list,pweapon_list=pweapon_list,audition_name=audition_name,
        week=29,trend=trend,rival_list=rival_list,idol='八宮めぐる',produce_card='きゅんコメ',memory=Memory.memory(idol_name='八宮めぐる'),
        aquired_passive=aquired_passive)
    settings.set_rival_mem_turn()
    situation=Situation.situation(judge_dict=judge_dict,status={'Vo':300,'Da':500,'Vi':415,'Me':317,'memory_gage':0.1,'star':0},passive_list=passive_list)

    #初ターンのパッシブを鳴かせる
    situation.passive_process(settings)
    data ={'settings':settings.get_dict(),'situation':situation.get_dict()}
    return jsonify(data)

@app.route("/api/reload_audition",methods=["GET","POST"])
def reload_audition():
    settings_in = request.json['settings']
    audiiton_name = settings_in['audition_name']
    situation_in = request.json['situation']
    passive_list = util.changePassive(settings_in['aquired_passive'])
    rival_list,judge_dict = Init.init_audition(audiiton_name)
    settings_in['rival_list'] = [r.info for r in rival_list]
    situation_in['judge_dict'] = {k:v.info for (k,v) in judge_dict.items()}
    situation_in['passive_list'] = passive_list

    settings = Settings.settings()
    settings.set_from_json(settings_in)
    situation = Situation.situation()
    situation.set_from_json(situation_in)
    #対面の判定と狙い先設定
    settings.set_rival_mem_turn()
    settings.set_rival_critical(2)
    settings.set_rival_aim(settings.trend,1,{'Vo':True,'Da':True,'Vi':True})

    return jsonify({'settings':settings.get_dict(),'situation':situation.get_dict()})

@app.route("/api/session",methods=["GET","POST"])
def get_session():
    return jsonify(session)

@app.route('/api/pushSupport',methods=["GET","POST"])
def pushSupport():
    support = Support.support(dict(request.json))
    message=support.push2DB(session)
    return jsonify({"message": message})

@app.route('/api/pushPcard',methods=["GET","POST"])
def pushPcard():
    input = dict(request.json)
    # print(dict(request.json))
    entity = Entity.ProduceCard()
    entity.idol = input['idol']
    entity.card_name = input['cardname']
    message =  DH.push2DB(entity,session)
    return jsonify({"message": message})

@app.route('/api/pushDeck',methods=["GET","POST"])
def pushDeck():
    print(dict(request.json))
    message = DH.pushDeck(dict(request.json),session)
    return jsonify({"message": message})

@app.route('/api/pushPweapon',methods=["GET","POST"])
def pushpweapon():
    pweapon = P_weapon.pweapon(dict(request.json))
    message=pweapon.push2DB(session)
    return jsonify({"message": message})

@app.route('/api/pushPassive',methods=["GET","POST"])
def pushpassive():
    input = dict(request.json)
    print(input)
    passive = Passive.passive()
    passive.set_from_json(input)
    message = passive.push2DB(session)
    print(message)
    return jsonify({"message": message})

@app.route("/api/fetchPweaponPaassive",methods=["GET","POST"])
def get_passive():
    ret = DH.fetchPweaponPassive(request.json)
    return jsonify(ret)

@app.route('/api/all_support')
def all_support():
    all_supports = []
    support_entities = DH.session.query(Entity.Support).filter_by(created_by='admin').all().copy()
    if len(session)>0:
        username = session['username']
        if username != 'admin':
            support_entities += DH.session.query(Entity.Support).filter_by(created_by=username).all().copy()

    for support in support_entities:
        sup_dict = {
        'card_type':'S','idol_name':support.idol,'card_name':support.name,
        'totu':str(support.totu)+'凸','status':{'Vo':support.Vo,'Da':support.Da,'Vi':support.Vi},
        'appeal':{'Vo':support.Vo_rate,'Da':support.Da_rate,'Vi':support.Vi_rate,'Ex':support.Ex_rate},
        'ATKtype':'single','buff':[],'key':support.idol+support.name+str(support.totu)+'凸'
        }
        if support.buff_relations:
            for buff in support.buff_relations:
                sup_dict['buff'].append( {
                    'color':buff.color,'buff':buff.rate,'turn':buff.turn,
                    'val':None,'name':support.name + '(S)'
                })
        all_supports.append(sup_dict)
    return jsonify(all_supports)

@app.route("/api/all_deck")
def get_decks():
    deck_list = []
    deck_list += DH.session.query(Entity.Deck).filter_by(created_by='admin').all().copy()
    if len(session)>0:
        username = session['username']
        if username != 'admin':
            deck_list += DH.session.query(Entity.Deck).filter_by(created_by=username).all().copy()
    ret_list = [{
        'deck_id': deck.id,
        'name': deck.name,
        'produce_idol': deck.produce_card.idol,
        'produce_card': deck.produce_card.card_name,
        'support1': {'idol': deck.supports[0].idol, 'name': deck.supports[0].name, 'totu': deck.supports[0].totu} if len(deck.supports) > 0 else {'idol': '櫻木真乃', 'name': '駅線上の日常', 'totu': 4},
        'support2': {'idol': deck.supports[1].idol, 'name': deck.supports[1].name, 'totu': deck.supports[1].totu} if len(deck.supports) > 1 else {'idol': '櫻木真乃', 'name': '駅線上の日常', 'totu': 4},
        'support3': {'idol': deck.supports[2].idol, 'name': deck.supports[2].name, 'totu': deck.supports[2].totu} if len(deck.supports) > 2 else {'idol': '櫻木真乃', 'name': '駅線上の日常', 'totu': 4},
        'support4': {'idol': deck.supports[3].idol, 'name': deck.supports[3].name, 'totu': deck.supports[3].totu} if len(deck.supports) > 3 else {'idol': '櫻木真乃', 'name': '駅線上の日常', 'totu': 4}
    } for deck in deck_list]

    DH.session.close()
    return jsonify(ret_list)

@app.route("/api/setDeck/<int:id>")
def set_deck(id):
    deck_dict,passive_list = DH.setDeck(id)
    return jsonify({'settings':deck_dict,'passive_list':passive_list})

@app.route("/api/deleteDeck/<int:id>")
def delete_deck(id):
    from Entity import Deck,deck_passive,deck_pweapon,deck_support
    delete_deck = DH.session.query(Deck).filter_by(id=id).first()

    DH.session.query(deck_pweapon).filter(deck_pweapon.c.deck_id == id).delete()
    DH.session.query(deck_support).filter(deck_support.c.deck_id == id).delete()
    DH.session.query(deck_passive).filter(deck_passive.c.deck_id == id).delete()
    DH.session.delete(delete_deck)
    DH.session.commit()
    DH.session.close()
    return jsonify({'massege':'削除しました'})

#settingsの獲得パッシブ情報からシミュレーションで使うpassive_listを生成
@app.route('/api/changePassive',methods=['GET','POSt'])
def changePassive():
    passive_list=util.changePassive(list(request.json))
    return jsonify(passive_list)

@app.route('/edit',methods=['GET','POSt'])
def edit():
    return render_template('/deckEdit.html')

#ログイン関係
@app.route('/register', methods=['GET', 'POST'])
def register():
    from Entity import Users
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        # ユーザーが既に存在するかチェック
        existing_user = DH.session.query(Users).filter_by(username=username).first()
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
    from Entity import Users
    if request.method == 'POST':
        username = request.form['username']
        password_candidate = request.form['password']

        user = DH.session.query(Users).filter_by(username=username).first()

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

@app.route('/test')
def testpage():
    return render_template('test.html')

@app.route('/api/hello')
def apitest():
    print('get_request')
    return jsonify({'message':'API連携成功'})




if __name__ == '__main__':
    app.run(debug=True)
    # os.environ['FLASK_DEBUG'] = '1'
    session['logged_in'] = False
