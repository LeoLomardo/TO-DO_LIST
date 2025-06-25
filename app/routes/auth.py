from flask import Blueprint, render_template, request, redirect, url_for, session
from domain.user import User
from use_cases.add_user import AddUserUseCase
from use_cases.find_user_by_email import FindUserByEmailUseCase


def create_auth_blueprint(add_uc: AddUserUseCase, find_uc: FindUserByEmailUseCase) -> Blueprint:
    bp = Blueprint('auth', __name__)

    @bp.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            name = request.form['name']
            email = request.form['email']
            user = add_uc.execute(User(id=0, name=name, email=email))
            session['user_id'] = user.id
            return redirect(url_for('pages.index'))
        return render_template('register.html')

    @bp.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            email = request.form['email']
            user = find_uc.execute(email)
            if user:
                session['user_id'] = user.id
                return redirect(url_for('pages.index'))
            return render_template('login.html', error='Usuário não encontrado')
        return render_template('login.html')

    @bp.route('/logout')
    def logout():
        session.pop('user_id', None)
        return redirect(url_for('auth.login'))

    return bp
