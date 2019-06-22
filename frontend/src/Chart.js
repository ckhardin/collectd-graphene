import React, { Component } from 'react';
import {QueryRenderer} from 'react-relay';
import ChartRenderer from './ChartRenderer';
import environment from './Environment';

const graphql = require('babel-plugin-relay/macro');


class Chart extends Component {
  static propTypes = {
    pluginpath: React.PropTypes.string,
    refresh: React.PropTypes.number,
  };

  render() {
    return (
      <QueryRenderer
        environment={environment}
        query={graphql`
          query ChartQuery($pluginpath: String) {
            plugindata(path: $pluginpath) {
              plugin, instance, series { name, sequence {t, v} }
            }
          }
        `}
        variables={{ pluginpath: this.props.pluginpath,
                     refresh: this.props.refresh
        }}
        render={({error, props}) => {
          if (error) {
            return <div>Error!</div>;
          }
          if (props && props.plugindata) {
            return <ChartRenderer plugin={props.plugindata.plugin}
                                  instance={props.plugindata.instance}
                                  series={props.plugindata.series} />;
          }
          return <div/>;
        }}
      />
    );
  }
}

export default Chart;
