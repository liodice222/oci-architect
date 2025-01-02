import React from 'react'
import reactDOM from 'react-dom'
'use strict';

const e = React.createElement;

class SearchBar extends React.Component {
  constructor(props) {
    super(props);
    this.state = { search: '', results: [] };

    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleChange(event) {
    this.setState({search: event.target.value});
  }

  handleSubmit(event) {
    event.preventDefault();
    fetch(`/search?search=${this.state.search}`)
      .then(response => response.json())
      .then(data => this.setState({ 
        results: data.compound_info, 
        username: data.username,
        search_query: data.search_query
      }));
  }

  render() {
    return (
      <div>
        <form onSubmit={this.handleSubmit}>
          <input type="text" value={this.state.search} onChange={this.handleChange} placeholder="Search" />
          <input type="submit" value="Search" />
        </form>
        <div>
        {this.state.username && (
          <div >
            <h2>{this.state.username}</h2>
            <p>Search query: {this.state.search_query}</p>
            <p>IUPAC Name: {this.state.results.iupac_name}</p>
            <p>Molecular Weight: {this.state.results.molecular_weight}</p>
          </div>
)}
        </div>
      </div>
    );
  }
}

const domContainer = document.querySelector('#search-container');
const root = ReactDOM.createRoot(domContainer);
root.render(<SearchBar />);
