from datetime import timedelta
from flask import (
    render_template,
    redirect,
    flash,
    url_for,
    session
)


from flask_bcrypt import check_password_hash

from flask_login import (
    login_user,
    current_user,
    logout_user,
    login_required,
)

from app import create_app, login_manager
from models import User
from forms import login_form


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


app = create_app()
chat_messages = [{'name': 'karst', 'messages': [
    'hello there!', 
    'how we doing!', 
    'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.']},
    {'name': 'test', 'messages': ['hello', 'how we doing', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.']}]


@ app.before_request
def session_handler():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=1)


@ app.route("/", methods=("GET", "POST"), strict_slashes=False)
def index():
    if not current_user.is_authenticated:
        form = login_form()
        if form.validate_on_submit():
            try:
                user = User.query.filter_by(
                    username=form.username.data).first()
                if check_password_hash(user.pwd, form.pwd.data):
                    login_user(user)
                    return redirect(url_for('index'))
                else:
                    flash("Invalid Username or password!", "danger")
            except Exception as e:
                flash(e, "danger")

        return render_template("auth.html",
                               form=form,
                               title="Login",
                               btn_action="Login"
                               )
    else:
        return render_template("index.html", title="Secret Chat", chat_messages=chat_messages)


@ app.route("/logout")
@ login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)
