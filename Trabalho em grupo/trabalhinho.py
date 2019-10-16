from flask import Flask, render_template, redirect, request

titulo = "Página interna XX Eletrodomésticos"

app=Flask(__name__)

@app.route('/')
def inicio():
    return render_template('login.html', titulo = titulo)

@app.route('/menu')
def menu():
    return render_template('menu.html', titulo=titulo)

@app.route('/cad_produto')
def cad_produto():
    return render_template('cad_produto.html', titulo = titulo)

@app.route('/cad_produto/salvar', methods=['POST'])
def salvar_produto():
    return redirect('/cad_produto/lista_produto')

@app.route('/efetuar_compra')
def efetuar_compra():
    return render_template('efetuar_compra.html', titulo = titulo)

@app.route('/politica_uso')
def politica_usuario():
    return render_template('politica_uso.html', titulo = titulo)



app.run()