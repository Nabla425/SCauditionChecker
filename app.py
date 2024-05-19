from flask import Flask, render_template,request,redirect,session
import Init,Game,util
import pickle
from datetime import timedelta

from transfer_class import Settings,Situation

app = Flask(__name__)
app.secret_key = 'test'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=1)
 
@app.route("/",methods=['GET','POST'])
def index():
    session.clear()
    print(session)
    return render_template("index.html")
    
@app.route("/audition",methods=['GET','POST'])
def audition():
    if not any(session):
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
        session['settings'] = pickle.dumps(settings)
        session['situation'] = pickle.dumps(situation)
        session['history'] = []
        return render_template(
            "audition.html",rival_list=settings.rival_list,judge_dict=situation.judge_dict,settings=settings,situation=situation
            )
    else:
        settings = pickle.loads(session.get('settings'))
        situation = pickle.loads(session.get('situation'))
        # util.test_rival_mem_turn(settings)
        #対面判定のset
        settings.set_rival_critical(situation.turn)
        rival = settings.rival_list[0]
        rival.set_aim(settings.trend,situation.turn,situation.get_judge_alive_dict())
        return render_template(
            "audition.html",rival_list=settings.rival_list,judge_dict=situation.judge_dict,settings=settings,situation=situation
            )
    
@app.route("/audition/turn",methods=["GET","POST"])
def exe_one_turn():
    session['history'].append(session.get('situation'))
    settings = pickle.loads(session.get('settings'))
    situation = pickle.loads(session.get('situation'))
    GM = Game.play(settings,situation)
    GM.oneTurnProcess(dict(request.form))
    situation.turn += 1
    session['settings'] = pickle.dumps(settings)
    session['situation'] = pickle.dumps(situation)
    return redirect('/audition')

#オーディションをリセット　settionをリセット
@app.route('/audition/reset')
def init_audition():
    if 'situation' in session.keys():
        session.pop('situation')
    rival_list,judge_dict = Init.init_audition('"歌姫楽宴"')
    situation=Situation.situation(judge_dict,{'Vo':300,'Da':500,'Vi':415,'Me':317,'memory_gage':0.1})
    session['situation'] = pickle.dumps(situation)
    session['history'] = []
    return redirect('/audition')

@app.route('/audition/back')
def back_one_turn():
    if len(session['history'])>0:
        session['situation'] = session['history'].pop()
    return redirect('/audition')
    

# @app.route("/create",methods=["GET","POST"])
# def create():
#     if request.method == "POST":
#         title = request.form.get('title')
#         body = request.form.get('body')
#         return redirect('/')
#     else:
#         return render_template("create.html")



