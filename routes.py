from flask import render_template, request, redirect, url_for, session
from app import app
from db import db
from models import User, Search
import requests
from flask_login import current_user

@app.route('/')
def home():
    print("rendering home.html")
    return render_template('index.html', current_user=current_user)

@app.route('/search', methods=['GET'])
def search():
    username = session.get('username')
    search_query = request.args.get('search')
    
    # Debugging print statement
    print(f'Search Query: {search_query}')
    
    try:
        response = requests.get(f'https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{search_query}/JSON')
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f'An error occurred: {e}')
        response = None

    compound_info = response.json() if response and response.status_code == 200 else None
    compound_data = {}

    if compound_info:
        compound = compound_info['PC_Compounds'][0]
        props = compound['props']

        # Extracting compound properties
        property_map = {
            ('Allowed', 'IUPAC Name'): 'iupac_name',
            ('', 'Molecular Weight'): 'molecular_weight',
            ('', 'Compound Complexity'): 'compound_complexity',
            ('Hydrogen Bond Donor', ''): 'hydrogen_bond_donor',
            ('Hydrogen Bond Acceptor', ''): 'hydrogen_bond_acceptor',
            ('Isomeric', 'SMILES'): 'smiles_isomeric'
        }

        for prop in props:
            key = (prop['urn'].get('name', ''), prop['urn'].get('label', ''))
            if key in property_map:
                field_name = property_map[key]
                compound_data[field_name] = prop['value'].get('sval') or prop['value'].get('fval') or prop['value'].get('ival')
                if field_name == 'molecular_weight':
                    compound_data[field_name] += ' g/mol'

        compound_data['charge'] = compound['charge']

        # TODO: Create a relationship with User and Search for an analytics database
        # search_result = Search(user_id=username, search_query=search_query, search_result=str(compound_data))
        # db.session.add(search_result)
        # db.session.commit()

        return render_template('compound_info.html', search_query=search_query, compound_info=compound_data, username=username, current_user=current_user)
    else:
        return render_template('return.html')
