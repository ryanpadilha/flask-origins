from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from .application import db, login_manager
from flask_uuid import uuid
from sqlalchemy_utils import UUIDType
from .util.library import current_timestamp_tz, user_logged_in


class AuditEntity(object):
    created = db.Column(db.DateTime, default=current_timestamp_tz, onupdate=current_timestamp_tz)
    created_user = db.Column(db.String(200), nullable=False, default=user_logged_in)
    modified = db.Column(db.DateTime, onupdate=current_timestamp_tz)
    modified_user = db.Column(db.String(200), onupdate=user_logged_in)


class Client(db.Model, AuditEntity):
    __tablename__ = 'xf_client_global'

    id = db.Column(db.Integer, primary_key=True)
    internal = db.Column(UUIDType(binary=False), index=True, unique=True, default=uuid.uuid4)
    name = db.Column(db.String(200), nullable=False)
    document_main = db.Column(db.String(20), nullable=False)
    address_street = db.Column(db.String(250))
    address_complement = db.Column(db.String(200))
    address_zip = db.Column(db.String(10))
    address_district = db.Column(db.String(100))
    address_city = db.Column(db.String(100))
    address_state = db.Column(db.String(2))
    date_start = db.Column(db.Date, nullable=False, default=current_timestamp_tz)
    date_end = db.Column(db.Date, nullable=False, default=current_timestamp_tz)


class State(db.Model):
    __tablename__ = 'xf_state'

    initials = db.Column(db.String(2), primary_key=True)
    state = db.Column(db.String(100), nullable=False)
    capital = db.Column(db.String(100), nullable=False)
    region = db.Column(db.String(100), nullable=False)


class AuthApi(db.Model, AuditEntity):
    __tablename__ = 'xf_auth_api'

    internal = db.Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
    client_secret = db.Column(db.String(), nullable=False, unique=True)
    api_key = db.Column(db.String(), nullable=False, unique=True)


class LoginActivity(db.Model):
    __tablename__ = 'xf_login_activities'

    internal = db.Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
    created = db.Column(db.DateTime, default=current_timestamp_tz)
    user_id = db.Column(db.Integer, db.ForeignKey('xf_user.id'))
    user = db.relationship('User', backref=db.backref('activities', cascade='all, delete-orphan'), lazy='joined')
    action = db.Column(db.String(), nullable=False)
    ip_address = db.Column(db.String(), nullable=False)
    ua_header = db.Column(db.String(), nullable=False)
    ua_device = db.Column(db.String(), nullable=False)


class UserGroup(db.Model, AuditEntity):
    __tablename__ = 'xf_user_group'

    id = db.Column(db.Integer, primary_key=True)
    internal = db.Column(UUIDType(binary=False), index=True, unique=True, default=uuid.uuid4)
    name = db.Column(db.String(200), nullable=False)
    type = db.Column(db.String(3), nullable=False, unique=True)
    description = db.Column(db.String(200))
    users = db.relationship('User', backref='group', lazy=True)


class User(db.Model, UserMixin, AuditEntity):
    __tablename__ = 'xf_user'
    __table_args__ = {'sqlite_autoincrement': True}

    id = db.Column(db.Integer, primary_key=True)
    internal = db.Column(UUIDType(binary=False), index=True, unique=True, default=uuid.uuid4)
    active = db.Column(db.Boolean, nullable=False, default=False)
    name = db.Column(db.String(200), nullable=False)
    user_name = db.Column(db.String(100), index=True, unique=True)
    user_email = db.Column(db.String(200), index=True, unique=True)
    user_password = db.Column(db.String(200), nullable=False)
    file_name = db.Column(db.String())
    file_url = db.Column(db.String())
    company = db.Column(db.String())
    occupation = db.Column(db.String())
    phone = db.Column(db.String())
    document_main = db.Column(db.String())
    user_group_id = db.Column(db.Integer, db.ForeignKey('xf_user_group.id'))

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
        user_group_id = provider_dict.get('group_id')
        file_name = provider_dict.get('file_name')
        file_url = provider_dict.get('file_url')
        company = provider_dict.get('company')
        occupation = provider_dict.get('occupation')
        phone = provider_dict.get('phone')
        document_main = provider_dict.get('document_main')

        return User(id=id,
                    internal=internal,
                    created=created,
                    active=active,
                    name=name,
                    user_name=user_name,
                    user_email=user_email,
                    password=user_password,
                    user_group_id=user_group_id,
                    file_name=file_name,
                    file_url=file_url,
                    company=company,
                    occupation=occupation,
                    phone=phone,
                    document_main=document_main)

    def __repr__(self):
        return '<User: {}>'.format(self.user_name)


@login_manager.user_loader
def load_user(user_id):
    """
        load user from database to session, using Flask Login
    """
    return User.query.get(int(user_id))
