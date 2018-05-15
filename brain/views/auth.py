from flask import Blueprint, render_template, flash, redirect, url_for, request, abort, session
from flask_login import login_required, login_user, logout_user, current_user
from ..forms import LoginForm, UserForm, UserEditForm, UserChangePasswordForm, AuthApiForm, UserGroupForm
from ..models import User, AuthApi, LoginActivity, UserGroup
from ..application import db, f_images
from ..util.library import generate_secret_key, current_request_ip
from user_agents import parse
from ..util.enums import FlashMessagesCategory


auth = Blueprint('auth', __name__)


@auth.errorhandler(404)
def page_not_found(e):
    flash(e, category=FlashMessagesCategory.ERROR.value)
    return render_template('404.html'), 404


@auth.errorhandler(500)
def internal_server_error(e):
    flash(e, category=FlashMessagesCategory.ERROR.value)
    return render_template('500.html'), 500


@auth.errorhandler(Exception)
def unhandled_exception(e):
    flash(e, category=FlashMessagesCategory.ERROR.value)
    return render_template('500.html'), 500


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    next_url = request.args.get('next')

    if form.validate_on_submit():
        next_url = request.form['next']

        # check if user exists on database
        user = User.query.filter_by(user_email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            # validations over user
            if not user.active:
                flash(u'Usuário não encontra-se ativo', category=FlashMessagesCategory.INFO.value)
            else:
                login_user(user, remember=form.remember_me.data)
                session.permanent = True

                # record activity
                record_login_activity(user, 'login')

                # redirect to dashboard after login
                return redirect(next_url or url_for('website.index'))
        else:
            flash(u'E-mail de usuário ou senha inválidos', category=FlashMessagesCategory.ERROR.value)

    return render_template('auth/login.html', form=form, next=next_url)


@auth.route('/logout', methods=['GET'])
@login_required
def logout():
    # record activity
    record_login_activity(current_user, 'logout')
    logout_user()
    return redirect('login')


def record_login_activity(user, action):
    """Login activities registry"""""

    ip_address = current_request_ip()
    ua_header = request.headers['USER_AGENT']
    ua_device = str(parse(ua_header))

    activity = LoginActivity(user_id=user.id,
                             action=action,
                             ip_address=ip_address,
                             ua_header=ua_header,
                             ua_device=ua_device)

    try:
        db.session.add(activity)
        db.session.commit()

    except Exception as e:
        exception = e  # ignoring, just


@auth.route('/manage/client-secret', methods=['GET'])
@login_required
def list_client_secrets():
    clients = AuthApi.query.all()
    return render_template('manage/list-client-secret.html', clients=clients)


@auth.route('/manage/client-secret/form', methods=['GET', 'POST'])
@login_required
def form_client_secret():
    form = AuthApiForm()

    if form.validate_on_submit():
        client = AuthApi(client_secret=form.client_secret.data,
                         api_key=generate_secret_key())

        try:
            db.session.add(client)
            db.session.commit()

            return redirect(url_for('auth.list_client_secrets'))
        except Exception as e:
            abort(500, e)

    return render_template('manage/form-client-secret.html', form=form)


@auth.route('/manage/client-secret/<uuid:internal>/edit', methods=['GET', 'POST'])
@login_required
def edit_client_secret(internal):
    client = AuthApi.query.filter_by(internal=internal).first()
    form = AuthApiForm(obj=client)

    if form.validate_on_submit():
        client.client_secret = form.client_secret.data

        try:
            db.session.commit()

            return redirect(url_for('auth.list_client_secrets'))
        except Exception as e:
            abort(500, e)

    return render_template('manage/form-client-secret.html', form=form)


@auth.route('/manage/client-secret/delete', methods=['POST'])
@login_required
def delete_client_secret():
    client = AuthApi.query.filter_by(internal=request.form['recordId']).first()

    try:
        db.session.delete(client)
        db.session.commit()

        flash(u'Registro deletado com sucesso.', category=FlashMessagesCategory.INFO.value)
        return redirect(url_for('auth.list_client_secrets'))
    except Exception as e:
        abort(500, e)


@auth.route('/manage/user', methods=['GET'])
@login_required
def list_users():
    users = User.query.all()
    return render_template('manage/list-user.html', users=users)


@auth.route('/manage/user/form', methods=['GET', 'POST'])
@login_required
def form_user():
    form = UserForm()

    if form.validate_on_submit():
        # upload-file
        file = form.photo.data
        file_name = None
        file_url = None

        if file:
            file_folder = 'profile'
            # a = secure_filename(str(time.time()) + file.filename)

            file_name = f_images.save(file, folder=file_folder)
            file_url = f_images.url(file_name)
            # v = s3_upload(file, file_name)

        user = User(active=form.active.data,
                    name=form.name.data,
                    user_name=form.user_email.data.lower(),
                    user_email=form.user_email.data.lower(),
                    password=form.user_password.data,
                    user_group_id=form.groups.data,
                    file_name=file_name,
                    file_url=file_url,
                    company=form.company.data,
                    occupation=form.occupation.data,
                    phone=form.phone.data,
                    document_main=form.document_main.data)

        try:
            db.session.add(user)
            db.session.commit()

            return redirect(url_for('auth.list_users'))
        except Exception as e:
            abort(500, e)

    return render_template('manage/form-user.html', form=form)


@auth.route('/manage/user/<uuid:internal>/edit', methods=['GET', 'POST'])
@login_required
def edit_user(internal):
    user = User.query.filter_by(internal=internal).first()
    form = UserEditForm(obj=user, groups=user.user_group_id)

    file_name = user.file_name if user else ''
    file_url = user.file_url if user else ''

    if form.validate_on_submit():
        # upload-file
        file = form.photo.data

        if file:
            file_folder = 'profile'
            file_name = f_images.save(file, folder=file_folder)
            file_url = f_images.url(file_name)

            user.file_name = file_name
            user.file_url = file_url

        user.name = form.name.data
        user.company = form.company.data
        user.occupation = form.occupation.data
        user.active = form.active.data
        user.user_group_id = form.groups.data
        user.phone = form.phone.data
        user.document_main = form.document_main.data

        try:
            db.session.commit()

            return redirect(url_for('auth.list_users'))
        except Exception as e:
            abort(500, e)

    return render_template('manage/form-user.html',
                           form=form, file_name=file_name, file_url=file_url)


@auth.route('/manage/user/delete', methods=['POST'])
@login_required
def delete_user():
    user = User.query.filter_by(internal=request.form['recordId']).first()

    try:
        db.session.delete(user)
        db.session.commit()

        flash(u'Registro deletado com sucesso.', category=FlashMessagesCategory.INFO.value)
        return redirect(url_for('auth.list_users'))
    except Exception as e:
        abort(500, e)


@auth.route('/manage/user/profile', methods=['GET', 'POST'])
@login_required
def view_profile():
    form = UserChangePasswordForm()

    if form.validate_on_submit():
        user = User.query.filter_by(internal=current_user.internal).first()

        # verificando se senha atual confere
        if not user.verify_password(form.current_password.data):
            flash(u'Senha atual informada está incorreta.', category=FlashMessagesCategory.ERROR.value)
            return render_template('manage/view-profile.html', form=form)

        user.password = form.user_password.data

        try:
            db.session.commit()

            flash(u'Alteração de senha realizada com sucesso. A alteração ocorre apenas uma vez por sessão.',
                  category=FlashMessagesCategory.INFO.value)
            return redirect(url_for('auth.view_profile'))
        except Exception as e:
            abort(500, e)

    return render_template('manage/view-profile.html', form=form)


@auth.route('/manage/group')
@login_required
def list_groups():
    groups = UserGroup.query.all()
    return render_template('manage/list-group.html', groups=groups)


@auth.route('/manage/group/form', methods=['GET', 'POST'])
@login_required
def form_group():
    form = UserGroupForm()

    if form.validate_on_submit():
        group = UserGroup(name=form.name.data,
                          type=form.type.data,
                          description=form.description.data)

        try:
            db.session.add(group)
            db.session.commit()

            return redirect(url_for('auth.list_groups'))
        except Exception as e:
            abort(500, e)

    return render_template('manage/form-group.html', form=form)


@auth.route('/manage/group/<uuid:internal>/edit', methods=['GET', 'POST'])
@login_required
def edit_group(internal):
    group = UserGroup.query.filter_by(internal=internal).first()
    form = UserGroupForm(obj=group)

    if form.validate_on_submit():
        group.name = form.name.data
        group.description = form.description.data

        try:
            db.session.commit()

            return redirect(url_for('auth.list_groups'))
        except Exception as e:
            abort(500, e)

    return render_template('manage/form-group.html', form=form)


@auth.route('/manage/group/delete', methods=['POST'])
@login_required
def delete_group():
    group = UserGroup.query.filter_by(internal=request.form['recordId']).first()

    if group and group.users:
        flash(u'Não é possível deletar o registro, pois está associado a um usuário.',
              category=FlashMessagesCategory.INFO.value)
        return redirect(url_for('auth.list_groups'))

    try:
        db.session.delete(group)
        db.session.commit()

        flash(u'Registro deletado com sucesso.', category=FlashMessagesCategory.INFO.value)
        return redirect(url_for('auth.list_groups'))
    except Exception as e:
        abort(500, e)
