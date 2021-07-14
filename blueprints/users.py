from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
from database import mysql

user = Blueprint('user', __name__, static_folder="../static", template_folder="../templates/user")

@user.route('/')
def home():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM user')
    data = cur.fetchall()
    return render_template('user_home.html', user=data)


@user.route('/add_user', methods=['POST'])
def add_user():
    if request.method == 'POST':
        nombre = request.form['name']
        cedula = request.form['cedula']
        edad = request.form['edad']

        cur = mysql.connection.cursor()
        cur.execute(
            'INSERT INTO user (nombre, cedula, edad) VALUES (%s, %s, %s)', (nombre, cedula, edad))
        mysql.connection.commit()
        flash('usuario agregado de manera satisfactoria')
        return redirect(url_for('user.home'))
        
@user.route('/edit/<id>')
def get_user(id):
    cur = mysql.connection.cursor()
    cur.execute('select * from user where id = %s' % id)
    data = cur.fetchall()
    return render_template('edit_user.html', user=data[0])

@user.route('/update_user/<id>', methods=['POST'])
def update_user(id):
    if request.method == 'POST':
        nombre = request.form['name']
        cedula = request.form['cedula']
        edad = request.form['edad']
    
    cur = mysql.connection.cursor()
    cur.execute("""
                UPDATE user
                set nombre = %s, 
                cedula = %s,
                edad = %s
                where id = %s 
                """, (nombre, cedula, edad, id))
    mysql.connection.commit()
    flash('edicion exitosa')
    return redirect(url_for('user.home'))

@user.route('/delete_user/<string:id>')
def delete_user(id):
    cur = mysql.connection.cursor()
    cur.execute('delete from user where id = {0}'.format(id))
    mysql.connection.commit()
    flash('Usuario removido de manera exitosa')
    return redirect(url_for('user.home'))