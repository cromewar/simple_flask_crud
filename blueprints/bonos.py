from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
from database import mysql

bono = Blueprint('bono', __name__, static_folder="../static", template_folder="../templates/bono")

@bono.route('/')
def home():
    cur = mysql.connection.cursor()
    cur.execute('select bono.*,user.nombre from bono left join user on user.id = bono.id_user_id')
    data = cur.fetchall()
    cur.execute('select * from user')
    users = cur.fetchall()
    return render_template('bono_home.html', bono=data, user=users)

@bono.route('/add_bono', methods=['POST'])
def add_bono():
    if request.method == 'POST':
        valor = request.form['valor']
        fecha = request.form['fecha']
        id_user_id = request.form['user']
        
        cur = mysql.connection.cursor()
        cur.execute('insert into bono (valor, fecha, id_user_id) values (%s, %s, %s)', (valor, fecha, id_user_id))
        cur.connection.commit()
        flash('bono agregado de manera satisfactoria')
        return redirect(url_for('bono.home'))


@bono.route('/edit_bono/<id>')
def get_bono(id):
    cur = mysql.connection.cursor()
    cur.execute('select * from bono where id_bono = %s' % id)
    data = cur.fetchall()
    cur.execute('select * from user')
    user = cur.fetchall()
    return render_template('edit_bono.html', bono=data[0], user=user)

@bono.route('/update_bono/<id>', methods=['POST'])
def update_bono(id):
    if request.method == 'POST':
        valor = request.form['valor']
        fecha = request.form['fecha']
        id_user_id = request.form['user']
    
    cur = mysql.connection.cursor()
    cur.execute("""
                UPDATE bono
                set valor = %s,
                fecha = %s,
                id_user_id = %s
                where id_bono = %s
                """, (valor, fecha, id_user_id, id))
    mysql.connection.commit()
    flash('Edicion de bono exitosa')
    return redirect(url_for('bono.home'))


@bono.route('/delete_bono/<string:id>')
def delete_bono(id):
    cur = mysql.connection.cursor()
    cur.execute('delete from bono where id_bono = {0}'.format(id))
    mysql.connection.commit()
    flash("Bono eliminado de manera exitosa")
    return redirect(url_for('bono.home'))