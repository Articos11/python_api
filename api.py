from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api, reqparse, fields, marshal_with, abort

# Definições da API, conexão ao banco de dados, etc. 
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/pythonTest'
db = SQLAlchemy(app)
api = Api(app)

# Aqui criados os dados que serão enviados para o banco de dados. 
class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        # Representação do objeto para debug.
        return f"User(name = {self.name}, email = {self.email})"
    
# Definição dos argumentos separados para futuras requisições.     
user_args = reqparse.RequestParser()
user_args.add_argument('name', type=str, required=True, help="Name cannot be blank")
user_args.add_argument('email', type=str, required=True, help="email cannot be blank")


# Os dados do usuário estarão aqui, para serem retornados como um JSON.
userFields = {
    'id': fields.Integer,
    'name': fields.String,
    'email': fields.String
}


# Operações sobre TODOS os usuários. Métodos Get e post. 
class Users(Resource):
    # Metodo get: Recebemos os dados solicitados. 
    @marshal_with(userFields) # Formata a resposta no formato userFields, ou seja, recebemos um JSON.
    def get(self):
        users = UserModel.query.all()
        return users     # Retorna todos os usuários.
    
    # Metodo post: Enviamos os dados fornecidos.
    @marshal_with(userFields)
    def post(self):
        # É criado um novo grupo de dados a partir das informações obtidas.
        args = user_args.parse_args()
        user = UserModel(name=args["name"], email=args["email"])
        db.session.add(user) 
        db.session.commit()
        
        # Retorna a lista atualizada dos usuários. 
        users = UserModel.query.all()
        return users, 201

# Operações sobre somente UM usuário.
class User(Resource):
    # Método Get
    @marshal_with(userFields)
    def get(self, id):
        user = UserModel.query.filter_by(id=id).first()
        if not user:
            abort(404, "User not found")
        return user
    
    # Método Patch: Podemos atualizar os usuários no banco de dados.
    @marshal_with(userFields)
    def patch(self, id):
        args = user_args.parse_args()
        user = UserModel.query.filter_by(id=id).first()
        if not user:
            abort(404, "User not found")
        user.name = args["name"]
        user.email = args["email"]
        db.session.commit()
        return user
    
    # Método delete: Podemos deletar os dados de um usuário caso necessário. 
    @marshal_with(userFields)
    def delete(self, id):
        args = user_args.parse_args()
        user = UserModel.query.filter_by(id=id).first()
        if not user:
            abort(404, "User not found")
        db.session.delete(user)
        db.session.commit()
        users = UserModel.query.all()
        return users
    

# Rotas da API.
api.add_resource(Users, '/api/users/') # Operações sobre todos os usuários.
api.add_resource(User, '/api/users/<int:id>') # Operações sobre somente um usuário.

# Rota padrão do navegador. 
@app.route('/')
def home():
    return '<h1>Flask REST API</h1>'

# Aplicação em modo debug. Deletar isso quando for subir para a produção.
if __name__ == '__main__':
    app.run(debug=True)