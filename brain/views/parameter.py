from flask import Blueprint, render_template, redirect, url_for, flash, abort, request
from flask_login import login_required
from ..application import db
from ..models import Client
from ..forms import ClientForm
from ..util.enums import FlashMessagesCategory


parameter = Blueprint('parameter', __name__)


@parameter.errorhandler(404)
def page_not_found(e):
    flash(e, category=FlashMessagesCategory.ERROR.value)
    return render_template('404.html'), 404


@parameter.errorhandler(500)
def internal_server_error(e):
    flash(e, category=FlashMessagesCategory.ERROR.value)
    return render_template('500.html'), 500


@parameter.errorhandler(Exception)
def unhandled_exception(e):
    flash(e, category=FlashMessagesCategory.ERROR.value)
    return render_template('500.html'), 500


@parameter.route('/parameter/client')
@login_required
def list_clients():
    clients = Client.query.all()
    return render_template('parameter/list-client.html', clients=clients)


@parameter.route('/parameter/client/form', methods=['GET', 'POST'])
@login_required
def form_client():
    form = ClientForm()

    if form.validate_on_submit():
        client = Client(name=form.name.data,
                        document_main=form.document_main.data,
                        address_street=form.address_street.data,
                        address_complement=form.address_complement.data,
                        address_zip=form.address_zip.data,
                        address_district=form.address_district.data,
                        address_city=form.address_city.data,
                        address_state=form.address_state.data,
                        date_start=form.date_start.data,
                        date_end=form.date_end.data)

        try:
            db.session.add(client)
            db.session.commit()

            return redirect(url_for('parameter.list_clients'))
        except Exception as e:
            abort(500, e)

    return render_template('parameter/form-client.html', form=form)


@parameter.route('/parameter/client/<uuid:internal>/edit', methods=['GET', 'POST'])
@login_required
def edit_client(internal):
    client = Client.query.filter_by(internal=internal).first()
    form = ClientForm(obj=client)

    if form.validate_on_submit():
        client.name = form.name.data
        client.document_main = form.document_main.data
        client.address_street = form.address_street.data
        client.address_complement = form.address_complement.data
        client.address_zip = form.address_zip.data
        client.address_district = form.address_district.data
        client.address_city = form.address_city.data
        client.address_state = form.address_state.data
        client.date_start = form.date_start.data
        client.date_end = form.date_end.data

        try:
            db.session.commit()

            return redirect(url_for('parameter.list_clients'))
        except Exception as e:
            abort(500, e)

    return render_template('parameter/form-client.html', form=form)


@parameter.route('/parameter/client/delete', methods=['POST'])
@login_required
def delete_client():
    client = Client.query.filter_by(internal=request.form['recordId']).first()

    try:
        db.session.delete(client)
        db.session.commit()

        flash(u'Registro deletado com sucesso.', category=FlashMessagesCategory.INFO.value)
        return redirect(url_for('parameter.list_clients'))
    except Exception as e:
        abort(500, e)
