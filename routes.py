from flask import Flask, render_template, request, session, url_for, redirect
from app import app
from db import db
from models import User, Search

import cx_Oracle
from dotenv import load_dotenv
import os
from flask_login import current_user




@app.route('/')
def home():
    print("rendering home.html")
    return render_template('index.html', current_user = current_user)



@app.route('/search', methods=['GET'])
def search():
    username = session.get('username')
    search_query = request.args.get('search').strip()
    print(f'Search Query: {search_query}')

    # Load environment variables
    load_dotenv()
    USERNAME = os.getenv('Oracle_Username')
    PASSWORD = os.getenv('Oracle_PW')
    DSN = cx_Oracle.makedsn(
        os.getenv('Oracle_Host'),
        os.getenv('Oracle_Post'),
        service_name=os.getenv('Oracle_SN')
    )

    # Connect to Oracle DB
    conn = cx_Oracle.connect(USERNAME, PASSWORD, DSN)
    cursor = conn.cursor()

    # Prepare and execute query
    query = """
        SELECT iupac_name, molecular_weight, compound_complexity, smiles_isomeric,
               hydrogen_bond_donor, hydrogen_bond_acceptor, charge
        FROM compounds
        WHERE compound_name LIKE :comp_name
    """
    cursor.execute(query, comp_name=f'%{search_query}%')
    compound_data = cursor.fetchone()  # fix for more than one record

    cursor.close()
    conn.close()

    if compound_data:
        keys = ['iupac_name', 'molecular_weight', 'compound_complexity', 'smiles_isomeric',
                'hydrogen_bond_donor', 'hydrogen_bond_acceptor', 'charge']
        compound_info = dict(zip(keys, compound_data))

        # add to link user to search models

        return render_template('compound_info.html', search_query=search_query, compound_info=compound_info, username=username, current_user=current_user)
    else:
        return render_template('return.html', message="No results found.")


