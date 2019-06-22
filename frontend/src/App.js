import React, { Component } from 'react';
import {QueryRenderer} from 'react-relay';
import Chart from './Chart';
import environment from './Environment';
import './App.css';

const graphql = require('babel-plugin-relay/macro');


class App extends Component {
  state = {
          pluginpath: null,
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
          <h1 className="App-title">GraphQL and React for RRD</h1>
        </header>
        <QueryRenderer
          environment={environment}
          query={graphql`
            query AppQuery {
              plugins {
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
            const plugins = props.plugins
            const listoptions = plugins.map((plugin, index) =>
                  <option value={plugin.path}>{index} - {plugin.path}</option>
            );
            return(
              <div className="selector">
                <form onSubmit={this.onSubmit}>
                <label htmlFor="pluginSelect">Select a Collectd Plugin:</label>
                <select id="pluginSelect" name="pluginpath"
                      onChange={this.onChange}
                      value={this.state.plugininstnace||"default"}>
                  <option disabled value="default">choose</option>
                  {listoptions}
                </select>
                <button type="submit">reload</button>
                </form>
                <Chart
                  className='pluginchart'
                  pluginpath={this.state.pluginpath}
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
