import React, { Component } from 'react';
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend,
} from 'recharts';


class ChartRenderer extends Component {
  static propTypes = {
    data: React.PropTypes.array,
  };

  render () {
    const w = Math.max(document.documentElement.clientWidth, window.innerWidth || 0);
    const h = Math.max(document.documentElement.clientHeight, window.innerHeight || 0);
    const margin = { 'left': 50, 'right': 50, 'top': 50, 'bottom': 50 };
    const data = this.props.data || { 'rrdseries': [] }

    if (!Array.isArray(data.rrdseries) || !data.rrdseries.length) {
      return (<div className="chart-container" />)
    }

    return (
      <div className="chart-container">
        <LineChart width={w} height={h}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="t" type="number" domain={['dataMin', 'dataMax']}
                 padding={{ left: margin.left, right: margin.right }} />
          <YAxis dataKey="v" type="number" domain={['auto', 'auto']}
                 padding={{ top: margin.top, bottom: margin.bottom}} />
          <Tooltip />
          <Legend />
          {data.rrdseries.map(s => (
            <Line dataKey="v" data={s.sequence} name={s.name} key={s.name} />
          ))}
        </LineChart>
      </div>
    )
  }
}

export default ChartRenderer;
