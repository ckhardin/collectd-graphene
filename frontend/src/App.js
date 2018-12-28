import React, { Component } from 'react';
import {QueryRenderer} from 'react-relay';
import Chart from './Chart';
import environment from './Environment';
import './App.css';

const graphql = require('babel-plugin-relay/macro');


class App extends Component {
  state = {
          rrdpath: null,
          refresh: null,
  }

  onSubmit = (evt) => {
    evt.preventDefault();
    this.setState({refresh: Math.random()})
  }

  onChange = (evt) => {
    this.setState({[evt.target.name]: evt.target.value})
  }

  render() {
    return (
      <div className="App">
        <header className="App-header">
          <h1 className="App-title">GraphQL and D3 for RRD</h1>
        </header>
        <QueryRenderer
          environment={environment}
          query={graphql`
            query AppQuery {
              rrdfiles {
                id, name, path
              }
            }
          `}
          variables={{}}
          render={({error, props}) => {
            if (error) {
              return <div>Error!</div>;
            }
            if (!props) {
              return <div>Loading...</div>;
            }
            const rrdfiles = props.rrdfiles
            const listoptions = rrdfiles.map((rrdfile, index) =>
                  <option value={rrdfile.path}>{index} - {rrdfile.path}</option>
            );
            return(
              <div className="selector">
                <form onSubmit={this.onSubmit}>
                <label htmlFor="rrdSelect">Select an RRDFile:</label>
                <select id="rrdSelect" name="rrdpath"
                      onChange={this.onChange} value={this.state.rrdpath||"default"}>
                  <option disabled value="default">choose</option>
                  {listoptions}
                </select>
                <button type="submit">reload</button>
                </form>
                <Chart
                  className='rrdchart'
                  rrdpath={this.state.rrdpath}
                  refresh={this.state.refresh}
                />
              </div>
            );
          }}
        />
      </div>
    );
  }
}

export default App;
