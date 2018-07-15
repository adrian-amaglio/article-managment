#!flask/bin/python
from flask import Flask
from flask_jwt import JWT, jwt_required, current_identity
from werkzeug.security import safe_str_cmp
from flask_restful import Api, Resource
import psycopg2, json


###############################################################################
#                   Psycopg2
###############################################################################
cur = None
try:
    conn = psycopg2.connect("dbname='test' user='test' host='localhost' password=''")
    cur = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
except:
    print("I am unable to connect to the database")

###############################################################################
#                   JWT
###############################################################################

# do
# curl localhost:5000/auth -X POST -d '{"username":"joe", "password":"pass"}' -H "Content-Type:application/json"
# handle bad password
# curl localhost:5000/protected -H 'Authorization: JWT <jwt>'

class User():
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __str__(self):
        return "User(id='%s')" % self.id

users = [
    User(0, 'guest', ''),
    User(1, 'mc', 'mc'),
    User(2, 'scribus', 'scribus'),
]
steps = [

{'id':0, 'name':'Rédaction', 'next_steps':{1:'Envoyer en relecture'}},
{'id':1, 'name':'Correction', 'next_steps':{2:'Envoyer en mise en page' ,0:'Renvoyer en rédaction'}},
{'id':2, 'name':'Integration', 'next_steps':{3:'Archiver l’article', 1:'Renvoyer en relecture', 0:'Renvoyer en rédaction'}},
{'id':3, 'name':'Archive', 'next_steps':{3:'Archiver l’article', 1:'Renvoyer en relecture', 0:'Renvoyer en rédaction'}},
{'id':10,'name': 'Émission', 'next_steps':{11:'Archiver'}},
{'id':11,'name': 'Archive radio', 'next_steps':{}},
]

username_table = {u.username: u for u in users}
userid_table = {u.id: u for u in users}
steps_table = {u['id']: u for u in steps}

def authenticate(username, password):
    user = username_table.get(username, None)
    if user and safe_str_cmp(user.password.encode('utf-8'), password.encode('utf-8')):
        return user

def identity(payload):
    user_id = payload['identity']
    return userid_table.get(user_id, None)

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'Ìè"ÌRAÛÏ±\Ô95BME;ýG¾Ð¨ÈºÕ3n×ð?pºét)ëXbZ¨¢ê;é&®ÿxq$Æ×.è³å[Mð²xoF»¨î´©dFC¼ÿrÏ4=mX¹{T5Ù«ÑUG¯L#P¦z¬úo±xÓóó»pÐsNC<¹W3úNn&He%n8Þc÷Âä7b(M,ÌD(ËÊäcéÅ~#·ÇÂ/í5øa-³°rÈ3èCã¿bBF¹ÉjÝHü"²¬.nq`Ý¿2ú²¼^¶z)Û;Ëå¸^béWÂìêX!h5¸(Û÷v9·"ø:¨½â>RtÐé"ØÕõÚ¹:E¢Ëàú5xÙ³Þ³RÓ<¡«ÛÖ°oÕeÔºK)àuÈ©8¨b¦¾½;ÍëU£÷oa«âÈv`¯Ftüû3ãÄïG/%"¿¼÷GÒÎ>#SJ§Õ^A@aÀy´!U-Ê°]ª4á}]ðÜê}A÷íÚ»Äv¢yxÓ¤ë#Æoÿóg±p¶°caTs½¶áVr½ÑN`aÐ¸ÊyW°TS6Suø{¬)íEøAëßëäÍÙ!¼F@FÍ*·Û°Ïßó'
api = Api(app)
jwt = JWT(app, authenticate, identity)

# test
@app.route('/protected')
@jwt_required()
def protected():
    return '%s' % current_identity

###############################################################################
#                     Flask REST API
###############################################################################

class ArticleAPI(Resource):
  def get(self, id):
    cur.execute("""select * from articles where id={:d}""".format(id))
    return json.dumps(cur.fetchall(), sort_keys=True, default=str)

  def put(self, id):
    return 'put '+str(id)


class ArticleListAPI(Resource):
  def get(self, step_id):
    cur.execute("""select id,title,format,type,content from articles where step_id={:d}""".format(step_id))
    return {
      "deadline_colors" : [
        {"seconds" : 3600, "color" : "red"},
        {"seconds" : 14400, "color" : "orange"}
      ],
      "step" : {
        "id":step_id,
        "next_steps":steps_table[step_id]['next_steps'],
        "name":steps_table[step_id]['name'],
        "can_create": False,
        "can_edit": True,
        "can_admin" : False,
        "see_login_button" : False,
      },
      "display" : {
        "0" : {
          "additional_string" : "Aujourd’hui",
          "display" : True
        },
        "1" : {
          "additional_string" : "Demain",
          "display" : True
        },
        "default" : {
          "additional_string" : "",
          "display" : False
        }
      },
      "articles" : cur.fetchall()
    }

api_version = 'v1.0'
api.add_resource(ArticleAPI, '/'+api_version+'/article/<int:id>', endpoint = 'article')
api.add_resource(ArticleListAPI, '/'+api_version+'/articles/<int:step_id>', endpoint = 'articles')


if __name__ == '__main__':
    app.run()
