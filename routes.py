from flask import render_template, request, redirect, url_for, session
from app import app
from db import db
from models import User, Search
import requests
from flask_login import current_user




@app.route('/')
def home():
    print("rendering home.html")
    return render_template('index.html', current_user = current_user)



@app.route('/search', methods=['GET'])
def search():
    username = session.get('username')
    search_query = request.args.get('search')
    #added print statements for debugging
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

    # point of improvement - I want to recreate this for loop for easier readability 
    #      property_map = {
    #         ('Allowed', 'IUPAC Name'): 'iupac_name', ....  }
    #     for prop in props:
    #         key = (prop['urn'].get('name', ''), prop['urn'].get('label', '')) ...
    
    

        # Extracting the IUPAC name, charge, molecular weight, compound complexity 
        for prop in props:
            if 'name' in prop['urn'] and prop['urn']['name'] == 'Allowed' and prop['urn']['label'] == 'IUPAC Name':
                compound_data['iupac_name'] = prop['value']['sval']
            elif 'label' in prop['urn'] and prop['urn']['label'] == 'Molecular Weight':
                compound_data['molecular_weight'] = prop['value']['sval'] + ' g/mol'
            elif 'label' in prop['urn'] and prop['urn']['label'] == 'Compound Complexity':
                compound_data['compound_complexity'] = prop['value']['fval']
                compound_data['complexity_datatype'] = prop['urn']['datatype']
            elif 'name' in prop['urn'] and prop['urn']['name'] == 'Hydrogen Bond Donor':
                compound_data['hydrogen_bond_donor'] = prop['value']['ival']
                compound_data['donor_datatype'] = prop['urn']['datatype']
            elif 'name' in prop['urn'] and prop['urn']['name'] == 'Hydrogen Bond Acceptor':
                compound_data['hydrogen_bond_acceptor'] = prop['value']['ival']
                compound_data['acceptor_datatype'] = prop['urn']['datatype']
            elif 'label' in prop['urn'] and prop['urn']['label'] == 'SMILES' and prop['urn']['name'] == 'Isomeric':
                compound_data['smiles_isomeric'] = prop['value']['sval']

        compound_data['charge'] = compound['charge']


    # point of improvement: I want to be able to create a relationship with User and Search for an analytics database 
        # search_result = Search(user_id=username, search_query=search_query, search_result=str(compound_data))
        # db.session.add(search_result)
        # db.session.commit()


        return render_template('compound_info.html', search_query=search_query, compound_info=compound_data, username = username, current_user = current_user)
    else:
        return render_template('return.html')


