#! /usr/bin/python

import click
import pickle
import os
from datetime import date
from api_connector import ApiConnector
from config import Config

names = Config().get('NAMES').split(',')

YEAR_MIN = 2020
NAME_TYPE = click.Choice(names, case_sensitive=False)

filepath = 'config.pkl'
if os.path.exists(filepath):
    f = open('config.pkl', 'rb')
    config = pickle.load(f)
    f.close()
else:
    config = {}

def deactivate_prompts(ctx, param, value):
    if value:
        for p in ctx.command.params:
            if isinstance(p, click.Option) and p.prompt is not None:
                p.prompt = None
    return value

@click.group(invoke_without_command=True)
def main():
    check_name()

@main.command('add')
@click.option('--quiet', '-q', default=False, is_eager=True, is_flag=True, callback=deactivate_prompts,  help='Run the script in non-interactive mode')
@click.option('--name', '-n', type=NAME_TYPE, help='Who paid?')
@click.option('--month', '-m', type=click.IntRange(1, 12), help='Month that the expense happened')
@click.option('--year', '-y', type=click.IntRange(YEAR_MIN, date.today().year), help='Year that the expense happened')
@click.option('--amount', '-a', required=True, type=click.FLOAT, prompt=True, help='The amount that was paid')
@click.option('--purpose', '-p', type=click.STRING, default='Zakupy', help='What was the purpose?')
@click.option('--shared', '-s', is_flag=True, default=True, help='Was it a shared expense, or rather paying for someone?')
def add_expense(quiet, name, month, year, amount, purpose, shared):
    if name is None:
        name = check_name()

    if month is None:
        month = date.today().month

    if year is None:
        year = date.today().year

    time =  '{0:0>2}{1:0>2}'.format(year, month)

    print('\n')
    print('*'*15, 'EXPENSE SUMMARY', '*'*15, end='\n\n')
    print('Name:', name)
    print('Date:', '{0}.{1}'.format(month, year))
    print('Amount:', '{0:.2f}'.format(amount), 'zł')
    print('Purpose:', purpose)
    print('Shared:', shared, end='\n\n')

    if quiet or click.confirm('Do you confirm adding the expense?', default=True):
        expense_data = {'name': name, 'purpose': purpose, 'shared': shared, 'time': time, 'amount': amount}
        connector = ApiConnector()
        connector.add_expense(expense_data)

@main.command('get')
@click.option('--id', '-i', required=True, type=click.INT, help='Expense ID')
def get_expense(id):
    connector = ApiConnector()
    connector.get_expense(id)

@main.command('list')
def get_expenses():
    connector = ApiConnector()
    connector.get_expenses()

@main.command('delete')
@click.option('--id', '-i', required=True, type=click.INT, help='Expense ID')
def delete_expense(id):
    connector = ApiConnector()
    connector.delete_expense(id)

def check_name():
    global config
    if not config.get('name', ''):
        config['name'] = click.prompt('Your name', type=NAME_TYPE)
        f = open('config.pkl', 'wb')
        pickle.dump(config, f)

    return config['name']


if __name__ == '__main__':
    main()
