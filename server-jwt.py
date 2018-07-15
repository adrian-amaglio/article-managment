#!flask/bin/python
from flask import Flask
from flask_jwt import JWT, jwt_required, current_identity
from werkzeug.security import safe_str_cmp
from flask_restful import Api, Resource
from model import *

###############################################################################
#                   JWT
###############################################################################

# do
# curl localhost:5000/auth -X POST -d '{"username":"joe", "password":"pass"}' -H "Content-Type:application/json"
# handle bad password
# curl localhost:5000/protected -H 'Authorization: JWT <jwt>'


class User(object):
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
  Step(id=0, name='Rédaction', next_step={1:'Envoyer en relecture'}),
  Step(id=1, name='Correction', next_step={2:'Envoyer en mise en page' ,0:'Renvoyer en rédaction'}),
  Step(id=2, name='Integration', next_step={3:'Archiver l’article', 1:'Renvoyer en relecture', 0:'Renvoyer en rédaction'}),
  Step(id=3, name='Archive', next_step={3:'Archiver l’article', 1:'Renvoyer en relecture', 0:'Renvoyer en rédaction'}),

  Step(id=10,name= 'Émission', next_step={11:'Archiver'}),
]

username_table = {u.username: u for u in users}
userid_table = {u.id: u for u in users}
steps_table = {u.id: u for u in steps}

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
    return 'get '+str(id)

  def put(self, id):
    return 'put '+str(id)

  def delete(self, id):
    return 'del '+str(id)


class ArticleListAPI(Resource):
  def post(self, step_id):
    return {
      "deadline_colors" : [
        {"seconds" : 3600, "color" : "red"},
        {"seconds" : 14400, "color" : "orange"}
      ],
      "step" : {
        "id":step_id,
        "next_steps":steps_table[step_id].next_steps,
        "name":steps_table[step_id].name,
        "can_create": False,
        "can_admin" : (True if current_identity.name == 'scribus' else False),

      },
      "display" : {
        "0" : {
          "additional_string" : "Aujourd’hui",
          "display" : true
        },
        "1" : {
          "additional_string" : "Demain",
          "display" : true
        },
        "default" : {
          "additional_string" : "",
          "display" : false
        }
      },
    "articles" : [
        {
  "id" : 192867192,
  "title" : "Il y a 30 ans",
  "format" : "article",
  "type" : "edito",
  "due_date" : 1523741010,
  "exergue" : "Truc !",
  "content" : """Lorem ipsum dolor sit amet iueu npfb efépeéepéhf eép ane ueae upeu peflupeupelau emupefaiu.ijma. i.
auijmezuaeuiemiueiuleui eiuealuimelui eiuemaiue iueeiuemi umae,ufip euple ulnepuesupletsuinletulneodstupeftelupftelp ufeute
unfe uleuaeflte olfeateelpu eauefetae esiaelfnaespésf*e pes épepéeapéEEop*e péepéfepe pée.""",
  "max_length" : 0,
  "min_length" : 550,
  "author" : "Juju et Rose",
  "can_read" : true,
  "can_write" : true,
  "can_create" : false,
  "can_delete" : false,
  "can_validate" : false
}
,
{
  "id" : 192867191,
  "title" : "Miam",
  "format" : "article",
  "type" : "miam",
  "due_date" : 1523808027,
  "exergue" : "Truc !",
  "content" : """Lorem ipsum dolor sit amet iueu npfb efépeéepéhf eép ane ueae upeu peflupeupelau emupefaiu.ijma. i.           
auijmezuaeuiemiueiuleui eiuealuimelui eiuemaiue iueeiuemi umae,ufip euple ulnepuesupletsuinletulneodstupeftelupftelp ufeute  
unfe uleuaeflte olfeateelpu eauefetae esiaelfnaespésf*e pes épepéeapéEEop*e péepéfepe pée.""",
  "max_length" : 600,
  "min_length" : 550,
  "author" : "Rose",
  "can_read" : true,
  "can_write" : true,
  "can_delete" : false,
  "can_validate" : false
}

    ]
    }



api_version = 'v1.0'
api.add_resource(ArticleAPI, '/'+api_version+'/article/<int:id>', endpoint = 'article')
api.add_resource(ArticleListAPI, '/'+api_version+'/article/<int:step_id>', endpoint = 'articles')


if __name__ == '__main__':
    app.run()
