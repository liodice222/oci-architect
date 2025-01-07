from flask import Blueprint, render_template, request, session
from app.db import db  # Correct import for db
from app.models.User import User 
from app.models.Search import Search  
import requests
from flask_login import current_user, login_required

# Define a blueprint for routes
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    print("rendering home.html")
    return render_template('index.html', current_user=current_user)

@main_bp.route('/search', methods=['GET'])
@login_required #ensure user is logged in before showing search queries
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

        return render_template('compound_info.html', search_query=search_query, compound_info=compound_data, username=username, current_user=current_user)
    else:
        return render_template('return.html')
