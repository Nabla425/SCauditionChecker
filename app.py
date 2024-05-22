from flask import Flask, render_template,request,redirect,session,jsonify
import Init,Game,util
import pickle

from transfer_class import Settings,Situation

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
# app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=1)
 
@app.route("/",methods=['GET','POST'])
def index():
    return render_template("index.html")

@app.route("/audition",methods=['GET','POST'])
def audition():
    return render_template('audition.html')
    
@app.route("/api/turn",methods=["GET","POST"])
def exe_one_turn():
    in_data = request.json
    settings = Settings.settings()
    settings.set_from_json(in_data['settings'])
    situation = Situation.situation()
    situation.set_from_json(in_data['situation'])
    input = dict(request.json['form'])
    #1ターン分の処理
    GM = Game.play(settings,situation)
    GM.oneTurnProcess(input)
    data ={'settings':settings.get_dict(),'situation':situation.get_dict()}
    print(data)
    return jsonify(data)

@app.route("/api/init",methods=["GET","POST"])
def audition_init():
        audition_name = '"歌姫楽宴"'
        rival_list,judge_dict = Init.init_audition(audition_name)
        support_keys = ['"櫻木真乃駅線上の日常4凸"','"風野灯織水面を仰いで海の底4凸"','"小宮果穂反撃の狼煙をあげよ！4凸"','"園田智代子kimagure全力ビート！4凸"']
        support_list = []
        for key in support_keys:
            support_list.append(Init.set_support(key))
        trend = {'Vo':1,'Da':2,'Vi':3}
        pweapon_list = Init.set_pweapon()
        settings = Settings.settings(support_list,pweapon_list,audition_name[1:-1],29,trend,rival_list)
        settings.set_rival_mem_turn()
        situation=Situation.situation(judge_dict,{'Vo':300,'Da':500,'Vi':415,'Me':317,'memory_gage':0.1})
        data ={'settings':settings.get_dict(),'situation':situation.get_dict()}
        print(situation.judge_dict)
        return jsonify(data)
        
#オーディションをリセット　settionをリセット
@app.route('/audition/reset')
def init_audition():
    if 'situation' in session.keys():
        session.pop('situation')
    rival_list,judge_dict = Init.init_audition('"歌姫楽宴"')
    situation=Situation.situation(judge_dict,{'Vo':300,'Da':500,'Vi':415,'Me':317,'memory_gage':0.1})
    return redirect('/audition')

@app.route('/audition/back')
def back_one_turn():
    if len(session['history'])>0:
        session['situation'] = session['history'].pop()
    return redirect('/audition')
    
@app.route('/api/hello')
def test():
    print('api required')
    return{'message':'testAPI'}



