import click
import random

from datetime import datetime

from faker import Faker

from mrsservice.app import create_app
from mrsservice.extensions import db
from mrsservice.blueprints.user.models import User
from mrsservice.blueprints.billing.models.invoice import Invoice

import os

# Create an app context for the database connection.
app = create_app()
db.app = app

fake = Faker()

from string import ascii_uppercase
import random
from itertools import islice


def random_chars(size, chars=ascii_uppercase):
    selection = iter(lambda: random.choice(chars), object())
    while True:
        yield ''.join(islice(selection, size))


def _log_status(count, model_label):
    """
    Log the output of how many records were created.

    :param count: Amount created
    :type count: int
    :param model_label: Name of the model
    :type model_label: str
    :return: None
    """
    click.echo('Created {0} {1}'.format(count, model_label))

    return None


def _bulk_insert(model, data, label):
    """
    Bulk insert data to a specific model and log it. This is much more
    efficient than adding 1 row at a time in a loop.

    :param model: Model being affected
    :type model: SQLAlchemy
    :param data: Data to be saved
    :type data: list
    :param label: Label for the output
    :type label: str
    :param skip_delete: Optionally delete previous records
    :type skip_delete: bool
    :return: None
    """
    size = 10000
    with app.app_context():
        model.query.delete()

        db.session.commit()
        db.engine.execute(model.__table__.insert(), data)

        _log_status(model.query.count(), label)

    return None


@click.group()
def cli():
    """ Add items to the database. """
    pass


@click.command()
def users():
    """
    Generate fake users.
    """
    random_emails = []
    data = []

    click.echo('Working...')

    # Ensure we get about 100 unique random emails.
    user_number = os.getenv('MAX_DEV_USER', 100)
    for i in range(0, user_number):
        random_emails.append(fake.email())

    random_emails.append(app.config['SEED_ADMIN_EMAIL'])
    random_emails = list(set(random_emails))

    thepassword = User.encrypt_password('password'),

    username_list = {}
    while True:
        if len(random_emails) == 0:
            break

        fake_datetime = fake.date_time_between(
            start_date='-1y', end_date='now').strftime('%s')

        created_on = datetime.utcfromtimestamp(
            float(fake_datetime)).strftime('%Y-%m-%dT%H:%M:%S Z')

        random_percent = random.random()

        role = 'member'

        email = random_emails.pop()

        # random_percent = random.random()
        #
        # if random_percent >= 0.5:
        #     random_trail = str(int(round((random.random() * 1000))))
        #     username = fake.first_name() + random_trail
        # else:
        #     username = None

        username = '{}'.format(random.randint(200000000, 300000000))
        # avoid duplication
        while username_list.get(username, 0):
            username = '{}'.format(random.randint(200000000, 300000000))
        username_list[username] = 1

        fake_datetime = fake.date_time_between(
            start_date='-1y', end_date='now').strftime('%s')

        current_sign_in_on = datetime.utcfromtimestamp(
            float(fake_datetime)).strftime('%Y-%m-%dT%H:%M:%S Z')

        params = {
            'created_on': created_on,
            'updated_on': created_on,
            'role': role,
            'email': email,
            'username': username,
            'password': thepassword,
            'sign_in_count': random.random() * 100,
            'name': fake.name(),
            'address': fake.address(),
            'current_sign_in_on': current_sign_in_on,
            'current_sign_in_ip': fake.ipv4(),
            'last_sign_in_on': current_sign_in_on,
            'last_sign_in_ip': fake.ipv4()
        }

        # Ensure the seeded admin is always an admin with the seeded password.
        if email == app.config['SEED_ADMIN_EMAIL']:
            password = User.encrypt_password(app.config['SEED_ADMIN_PASSWORD'])

            params['role'] = 'admin'
            params['password'] = password

        data.append(params)

    return _bulk_insert(User, data, 'users')


@click.command()
def invoices():
    """
    Generate random invoices.
    """
    _start_year = 2005
    _end_year = 2018

    for year in range(_start_year, _end_year):
        click.echo('Year: {}'.format(year))
        data = []
        start_year = year
        end_year = year + 1
        users = db.session.query(User).all()
        meter_number = {}

        for user in users:
            meter_number[user.id] = {}
            for y in range(start_year, end_year):
                meter_number[user.id][y] = {}
                for m in range(1, 13):

                    reference = random_chars(10)

                    period = '{}-{}'.format(m, y)
                    total_volume = random.randint(10, 200)

                    if y == start_year and m == 1:
                        last_meter_number = random.randint(1, 1000)
                    elif m == 1:
                        last_meter_number = meter_number[user.id][y - 1][12]
                    else:
                        last_meter_number = meter_number[user.id][y][m - 1]

                    current_meter_number = last_meter_number + total_volume
                    meter_number[user.id][y][m] = current_meter_number

                    currency = 'vnd'
                    amount = total_volume * 12000
                    tax = total_volume * 240
                    environment_fee = total_volume * 240
                    waste_treatment_fee = total_volume * 240
                    total = amount + tax + environment_fee + waste_treatment_fee
                    payment_state = 'paid'
                    if y == 2017 and m == 12:
                        payment_state = random.choice(['paid', 'unpaid'])

                    params = {
                        'user_id': user.id,
                        'reference': next(reference),
                        'period': period,
                        'last_meter_number': last_meter_number,
                        'current_meter_number': current_meter_number,
                        'total_volume': total_volume,

                        'currency': currency,
                        'amount': amount,
                        'tax': tax,
                        'environment_fee': environment_fee,
                        'waste_treatment_fee': waste_treatment_fee,
                        'total': total,
                        'payment_state': payment_state,
                    }

                    data.append(params)
        _bulk_insert(Invoice, data, 'invoices')
    return True

    #return _bulk_insert(Invoice, data, 'invoices')


@click.command()
@click.pass_context
def all(ctx):
    """
    Generate all data.

    :param ctx:
    :return: None
    """
    ctx.invoke(users)
    ctx.invoke(invoices)

    return None


cli.add_command(users)
cli.add_command(invoices)
cli.add_command(all)
