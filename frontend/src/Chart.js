import React, { Component } from 'react';
import {QueryRenderer} from 'react-relay';
import ChartRenderer from './ChartRenderer';
import environment from './Environment';

const graphql = require('babel-plugin-relay/macro');


class Chart extends Component {
  static propTypes = {
    rrdpath: React.PropTypes.string,
    refresh: React.PropTypes.number,
  };

  render() {
    return (
      <QueryRenderer
        environment={environment}
        query={graphql`
          query ChartQuery($rrdpath: String) {
            rrdseries(path: $rrdpath) {
              label, sequence {t, v}
            }
          }
        `}
        variables={{ rrdpath: this.props.rrdpath,
                     refresh: this.props.refresh
        }}
        render={({error, props}) => {
          if (error) {
            return <div>Error!</div>;
          }
          return <ChartRenderer data={props} />;
        }}
      />
    );
  }
}

export default Chart;
