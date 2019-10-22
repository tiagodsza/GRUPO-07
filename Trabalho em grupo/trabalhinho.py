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

@app.route('/menu')
def menu():
    return render_template('menu.html', titulo = titulo)

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
            return render_template('politica_uso.html', titulo=titulo)
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

def salvar_produto_alterado(produto_alterado):
    conexao = MySQLdb.connect(host="mysql.zuplae.com", user="zuplae12", passwd="grupo07", database="zuplae12")
    cursor = conexao.cursor()
    cursor.execute("UPDATE eletrodomestico SET tipo='{}', marca='{}',modelo='{}',data_fabric='{}', preco='{}' WHERE serie={}".format(produto_alterado.tipo, produto_alterado.marca, produto_alterado.modelo, produto_alterado.data_fabric, produto_alterado.preco,produto_alterado.serie))
    conexao.commit()
    conexao.close()

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
    return redirect('/lista_compras_join')

# @app.route('/lista_compras')
# def lista_compras():
#     return render_template('lista_compras_join.html', lista = listar_compras_db())

# def deletar_compra_db(serie_fk):
#     conexao = MySQLdb.connect(host="mysql.zuplae.com", user="zuplae12", passwd="grupo07", database="zuplae12")
#     cursor = conexao.cursor()
#     cursor.execute("DELETE FROM compra WHERE serie_fk={}".format(serie_fk))
#     conexao.commit()
#     conexao.close()

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

def deletar_produto_db(serie):
    conexao = MySQLdb.connect(host="mysql.zuplae.com", user="zuplae12", passwd="grupo07", database="zuplae12")
    lista = listar_compras_db()  
    cursor = conexao.cursor()
    for i in lista: 
        if int(serie) == i.serie_fk:
            return render_template('erro_compra.html')   
    cursor.execute("DELETE FROM eletrodomestico WHERE serie={}".format(serie))
    conexao.commit()
    return redirect('/lista_produto')    
#selecionar a coluna do id indicado e com um if se existir serie_fk não excluir, senão excluir.

# def deletar_produto_db(serie):
#     conexao = MySQLdb.connect(host="mysql.zuplae.com", user="zuplae12", passwd="grupo07", database="zuplae12")
#     lista = listar_compras_db()  
#     cursor = conexao.cursor()
#     if serie == i.serie_fk:
#         return render_template('erro_compra.html')   
#     cursor.execute("DELETE FROM eletrodomestico WHERE serie={}".format(serie))
#     return redirect('/lista_produto')  

def listar_compras_db_join():
    conexao = MySQLdb.connect(host="mysql.zuplae.com", user="zuplae12", passwd="grupo07", database="zuplae12")
    cursor = conexao.cursor()
    cursor.execute("select c.nome, c.cpf, c.endereco, e.tipo, e.marca, e.modelo, e.data_fabric, e.preco, e.serie from compra as c join eletrodomestico as e ON c.serie_fk = e.serie;")
    lista_compra_join = []
    for e in cursor.fetchall():
        eletro = Eletrodomesticos(e[3], e[4], e[5], e[6], e[7])
        eletro.nome = e[0]
        eletro.cpf = e[1]
        eletro.endereco = e[2]
        eletro.serie = e[8]
        lista_compra_join.append(eletro)
    conexao.close()
    return lista_compra_join

@app.route('/cad_produto')
def cadastrar():
    return render_template('cad_produto.html', titulo = titulo)

@app.route('/lista_produto')
def listar_produtos():
    return render_template('lista_produto.html', lista = listar_eletro_db())

@app.route('/lista_produto/delete')
def deletar_produto():
    serie = request.args['serie']
    deletar_produto_db(serie)
    return redirect ('/lista_produto')

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

@app.route('/efetuar_compra')
def efetuar_compra():
    return render_template('efetuar_compra.html', titulo = titulo, lista = listar_eletro_db())

# @app.route('/alterar_produto')
# def alterar_produto():
#     serie = request.args['serie']
#     tipo = request.args['tipo']
#     marca = request.args['marca']
#     modelo = request.args['modelo']
#     data_fabricacao = request.args['data_fabric']
#     preco = request.args['preco'] 
#     produto_alterado = Eletrodomesticos(tipo, marca, modelo, data_fabricacao, preco)
#     produto_alterado.serie = serie
#     return render_template('alterar_produto.html', atualizar_produto = produto_alterado)

# @app.route('/alterar_produto/salvar', methods = ['POST'])
# def alterar_produto_salvar():
#     return redirect('lista_produto.html')

# @app.route('/lista_compras_join/delete')
# def deletar_compra():
#     serie_fk = request.args['serie']
#     deletar_compra_db(serie_fk)
#     return redirect ('/lista_compras_join')

@app.route('/politica_uso')
def politica_usuario():
    return render_template('politica_uso.html', titulo = titulo)

@app.route('/lista_compras_join')
def listar_produtos_join():
    return render_template('lista_compras_join.html', lista = listar_compras_db_join())

@app.route('/cad_produto/alterar')
def alterar_produto():
    serie = request.args['serie']
    tipo = request.args['tipo']
    marca = request.args['marca']
    modelo = request.args['modelo']
    data_fabricacao = request.args['data_fabric']
    preco = request.args['preco'] 
    produto_alterado = Eletrodomesticos(tipo, marca, modelo, data_fabricacao, preco)
    produto_alterado.serie = serie
    return render_template('alterar_produto.html', produto = produto_alterado)

@app.route('/alterar_produto/salvar', methods = ['POST'])
def alterar_produto_salvar343():
    tipo = request.form['tipo']
    marca = request.form['marca']
    modelo = request.form['modelo']
    data = request.form['data_fabric']
    preco = request.form['preco']
    serie = request.form['serie']
    produto = Eletrodomesticos(tipo, marca, modelo, data, preco)
    produto.serie = serie
    salvar_produto_alterado(produto)
    return redirect('/lista_produto')

app.run(debug=True)