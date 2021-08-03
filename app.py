from flask import Flask, render_template, request, jsonify
from flask.json import jsonify
from flask.wrappers import Response
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from jinja2.utils import generate_lorem_ipsum

from flask_marshmallow import Marshmallow



app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///usuarios.db'

db = SQLAlchemy(app)

ma = Marshmallow(app)

class getUsuarios(ma.Schema):
    class Meta:
        fields = ('id','nombre','edad','genero','fecha_creada')

get_usuario = getUsuarios()
get_usuarios = getUsuarios(many=True)


class Usuarios(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200), nullable = False)
    edad = db.Column(db.Integer, nullable = False)
    genero = db.Column(db.String(200), nullable = False)
    fecha_creada = db.Column(db.DateTime,default = datetime.utcnow)
    def __repr__(self):
        return '<Name %r' % self.id
    


@app.route('/')
def index():
    usuarios = Usuarios.query.order_by(Usuarios.fecha_creada)
    return render_template('index.html', usuarios = usuarios)

@app.route('/nuevoUsuario', methods = ['POST', 'GET'])
def nuevoUsuario():
    if request.method== "POST":
        usuario = request.get_json()
        nombre_usuario = usuario['nombre']
        edad_usuario = usuario['edad']
        genero_usuario = usuario['genero']
        response = 'Post logrado con exito'
        print(nombre_usuario, edad_usuario, genero_usuario)
        nuevo_usuario = Usuarios(nombre = nombre_usuario, edad = edad_usuario, genero = genero_usuario)
        try:
            db.session.add(nuevo_usuario)
            db.session.commit()
            print('Agregado a la base de datos')
        except:
            print('NO SE AGREGO EN LA BASE')
        return jsonify(response)
    return print('Hubo un error:(')



@app.route('/eliminarUsuario',methods= ['POST','GET'])
def eliminarUsuario():
    if request.method == "POST":
        usuario_eliminar = request.get_json()
        ID = usuario_eliminar[0]
        print(ID)
        try:
            Usuarios.query.filter_by(id=ID).delete()
            db.session.commit()
            print('Usuario eliminado con EXITO')
        except:
            print('ERROR en ELIMINAR')
        response = "respuesta"
        return jsonify(response)
    return print('Usuario eliminado')

@app.route('/getUser',methods= ['POST','GET'] )
def getUser():
    usuarios = Usuarios.query.order_by(Usuarios.fecha_creada)
    result = get_usuarios.dump(usuarios)
    response=jsonify(result)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

