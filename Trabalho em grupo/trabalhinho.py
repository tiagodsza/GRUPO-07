from flask import Flask, render_template, redirect, request
from eletrodomesticos import Eletrodomesticos
from comprar import Comprar
from usuario_senha import Usuario_senha
import MySQLdb

titulo = "Página interna"

app=Flask(__name__)

@app.route('/')

def inicio():
    return render_template('login.html', titulo = titulo)




@app.route('/testar_login', methods=['POST'])
def login():

    conexao = MySQLdb.connect(host="mysql.zuplae.com", user="zuplae12", passwd="grupo07", database="zuplae12")
    cursor = conexao.cursor()
    cursor.execute('SELECT * FROM usuario_senha')
    lista_usuarios = []
    for i in cursor.fetchall():
        usuario = Usuario_senha(i[1],i[2])   
        lista_usuarios.append(usuario)

    usuario1 = request.form['usuario']
    senha1 = request.form['senha']
    user = Usuario_senha(usuario1,senha1)
    for i in range(len(lista_usuarios)):
        var_temp_usuario = lista_usuarios[i]
        if user.senha == var_temp_usuario.senha and user.usuario == var_temp_usuario.usuario:
            return render_template('menu.html', titulo=titulo)

    if user.senha != var_temp_usuario.senha:
            return redirect('/')

    elif user.usuario != var_temp_usuario.usuario:
            return redirect('/')  

def listar_compras_db():
    conexao = MySQLdb.connect(host="mysql.zuplae.com", user="zuplae12", passwd="grupo07", database="zuplae12")
    cursor = conexao.cursor()
    cursor.execute("select * from compra")
    compras_listadas = []
    for i in cursor.fetchall():
        compra = Comprar(i[1], i[2], i[3], i[4])
        compras_listadas.append(compra)
    return compras_listadas

@app.route('/salvar_compras', methods=['POST'])
def salvar_comprar():
    nome = request.form['nome']
    cpf = request.form['cpf']
    endereco = request.form['endereco']
    serie = request.form['serie']
    serie_fatiada = serie.strip().split(',')
#Abaixo, tivemos que criar outra váriavel chamada serie_inteiro para transformar em int o que veio do html
    serie_inteiro = int(serie_fatiada[2])
    sales_order = Comprar(nome, cpf, endereco, serie_inteiro)    
    lista = listar_compras_db()
    for i in lista:
        if sales_order.serie_fk == i.serie_fk:
            return render_template('erro_compra.html', titulo = titulo)
    salvar_compras(sales_order)
    return redirect('/lista_compras')

@app.route('/lista_compras')
def lista_compras():
    return render_template('lista_compras.html', lista = listar_compras_db())
        
def salvar_compras(sales_order):
    conexao = MySQLdb.connect(host="mysql.zuplae.com", user="zuplae12", passwd="grupo07", database="zuplae12")
    cursor = conexao.cursor()
    cursor.execute("INSERT INTO compra (nome,cpf,endereco,serie_fk) VALUES ('{}', '{}', '{}', '{}')".format(sales_order.nome, sales_order.cpf,sales_order.endereco,sales_order.serie_fk))
    conexao.commit()
    conexao.close()

def salvar_eletro(cadastro_geral):
    conexao = MySQLdb.connect(host="mysql.zuplae.com", user="zuplae12", passwd="grupo07", database="zuplae12")
    cursor = conexao.cursor()
    cursor.execute("INSERT INTO eletrodomestico (marca, modelo, data_fabric, preco, serie, tipo)" + 
    " VALUES ('{}','{}', '{}', '{}','{}','{}')".format(cadastro_geral.marca, cadastro_geral.modelo, cadastro_geral.data_fabric, cadastro_geral.preco,cadastro_geral.serie, cadastro_geral.tipo))
    conexao.commit()
    conexao.close()

def listar_eletro_db():
    conexao = MySQLdb.connect(host="mysql.zuplae.com", user="zuplae12", passwd="grupo07", database="zuplae12")
    cursor = conexao.cursor()
    cursor.execute("select * from eletrodomestico") 
    cadastro_geral = []
    for i in cursor.fetchall():
        produto = Eletrodomesticos(i[1], i[2], i[3], i[4], i[5])
        produto.serie = i[0]
        cadastro_geral.append(produto)        
    return cadastro_geral


# @app.route
# def validar_usuario_senha():
#     usuario1 = request.form['usuario']
#     senha1 = request.form['senha']
#     usuario1 = Usuario_senha(usuario1,senha1)
#     for i in range(len(lista_usuarios)):
#         var_temp_usuario= lista_usuarios[i]
#         if usuario1.senha == var_temp_usuario.senha:
#             menu()
#             print('usuario validado com sucesso')
#         else:
#             print("voce digitou a senha errada") 

@app.route('/menu')
def menu():
    return render_template('menu.html', titulo = titulo)

@app.route('/cad_produto')
def cadastrar():
    return render_template('cad_produto.html', titulo = titulo)

@app.route('/lista_produto')
def listar_produtos():
    return render_template('lista_produto.html', lista = listar_eletro_db())
    
@app.route('/cad_produto/salvar', methods=['POST'])
def salvar_eletrodomestico():
    tipo = request.form['tipo']
    marca = request.form['marca']
    modelo = request.form['modelo']
    data_fabric = request.form['data_fabric']
    preco = request.form['preco']
    cadastro_geral = Eletrodomesticos(tipo, marca, modelo, data_fabric, preco)
    salvar_eletro(cadastro_geral)
    return redirect('/lista_produto')

@app.route('/cad_produto/alterar')
def alterar():
    return render_template('lista_produto.html')

@app.route('/efetuar_compra')
def efetuar_compra():
    return render_template('efetuar_compra.html', titulo = titulo, lista = listar_eletro_db())

@app.route('/politica_uso')
def politica_usuario():
    return render_template('politica_uso.html', titulo = titulo)


app.run(debug=True)