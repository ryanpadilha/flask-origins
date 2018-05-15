import uuid

from flask import Flask, g, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


class MultiTenantSQLAlchemy(SQLAlchemy):
    def choose_tenant(self, bind_key):
        if hasattr(g, 'tenant'):
            raise RuntimeError('Switching tenant in the middle of the request.')
        g.tenant = bind_key

    def get_engine(self, app=None, bind=None):
        if bind is None:
            if not hasattr(g, 'tenant'):
                raise RuntimeError('No tenant chosen.')
            bind = g.tenant
        return super().get_engine(app=app, bind=bind)


application = Flask(__name__)
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
application.config['SQLALCHEMY_BINDS'] = {
    'dev': 'postgresql://origins:origins@localhost:5432/dev_origins',
    'stg': 'postgresql://origins:origins@localhost:5432/stg_origins'
}

db = MultiTenantSQLAlchemy(application)


@application.before_request
def before_request():
    tenant = request.args.get('tenant')
    if not tenant:
        tenant = 'dev'
    db.choose_tenant(tenant)


@application.route("/")
def list_users():
    return repr(list(User.query.all()))


@application.route("/add", methods=["POST"])
def add_user():
    user = User(request.form['username'], request.form['email'])
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('list_users'))


class User(UserMixin, db.Model):
    __tablename__ = 'xf_user'

    id = db.Column(db.Integer, primary_key=True)
    internal = db.Column(db.String(200), index=True, unique=True, default=uuid.uuid4())
    created = db.Column(db.DateTime, default=datetime.utcnow)
    active = db.Column(db.Boolean, nullable=False, default=False)
    name = db.Column(db.String(200), nullable=False)
    user_name = db.Column(db.String(100), index=True, unique=True)
    user_email = db.Column(db.String(200), index=True, unique=True)
    user_password = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    file_name = db.Column(db.String())
    file_url = db.Column(db.String())
    company = db.Column(db.String())
    occupation = db.Column(db.String())

    @property
    def password(self):
        # Prevent password from being accessed
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        self.user_password = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.user_password, password)

    @classmethod
    def from_dict(cls, provider_dict):
        id = provider_dict.get('id')
        internal = provider_dict.get('internal')
        created = provider_dict.get('created')
        active = provider_dict.get('active')
        name = provider_dict.get('name')
        user_name = provider_dict.get('user_email').lower()
        user_email = provider_dict.get('user_email').lower()
        user_password = provider_dict.get('user_password')
        is_admin = provider_dict.get('is_admin')
        file_name = provider_dict.get('file_name')
        file_url = provider_dict.get('file_url')
        company = provider_dict.get('company')
        occupation = provider_dict.get('occupation')

        return User(id=id,
                    internal=internal,
                    created=created,
                    active=active,
                    name=name,
                    user_name=user_name,
                    user_email=user_email,
                    password=user_password,
                    is_admin=is_admin,
                    file_name=file_name,
                    file_url=file_url,
                    company=company,
                    occupation=occupation)

    def __repr__(self):
        return '<User: {}>'.format(self.user_name)


if __name__ == "__main__":
    application.run(debug=True)