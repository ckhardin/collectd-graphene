import React, { Component, PureComponent } from 'react';
import {
  LineChart, Line, AreaChart, Area,
  XAxis, YAxis, CartesianGrid, Tooltip, Legend,
} from 'recharts';
import moment from 'moment';


class CustomizedTimeTick extends PureComponent {
  render() {
    const {
      x, y, stroke, payload,
    } = this.props;

    return (
      <g transform={`translate(${x},${y})`}>
        <text x={0} y={0} dy={16}
              textAnchor="end" fill="#666" transform="rotate(-35)">
          {moment.unix(payload.value).toISOString().split('.')[0]+"Z"}
        </text>
      </g>
    );
  }
}

class ChartRenderer extends Component {
  static propTypes = {
    plugin: React.PropTypes.string,
    instance: React.PropTypes.string,
    series: React.PropTypes.array,
  };

  renderPlugin(plugin, instance, series) {
    const w = Math.max(window.innerWidth || 0,
                       document.documentElement.clientWidth);
    const h = Math.max(window.innerHeight || 0,
                       document.documentElement.clientHeight);
    const margin = { 'left': 80, 'right': 50, 'top': 50, 'bottom': 100 };
    let data = [];
    let dnames;

    switch(plugin) {
      case 'cpu':
        for (let i = 0; i < series[0].sequence.length; i++) {
          dnames = { 't': series[0].sequence[i].t };
          for (let j = 0; j < series.length; j++) {
            dnames[series[j].name] = series[j].sequence[i].v;
          }
          data[data.length] = dnames;
        }

        return (
          <AreaChart width={w} height={h} margin={margin} data={data}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis name="Time" dataKey="t" type="number" scale="time"
                   tick={<CustomizedTimeTick />}
                   domain={['dataMin', 'dataMax']} />
            <YAxis type="number" domain={['auto', 'auto']} />
            <Tooltip />
            <Area dataKey="steal-value" stackId="1" name="steal"
                  type="monotone" stroke="#000000" fill="#000000" />
            <Area dataKey="interrupt-value" stackId="1" name="interrupt"
                  type="monotone" stroke="#a000a0" fill="#a000a0" />
            <Area dataKey="softirq-value" stackId="1" name="softirq"
                  type="monotone" stroke="#ff00ff" fill="#ff00ff" />
            <Area dataKey="system-value" stackId="1" name="system"
                  type="monotone" stroke="#ff0000" fill="#ff0000" />
            <Area dataKey="wait-value" stackId="1" name="wait"
                  type="monotone" stroke="#ffb000" fill="#ffb000" />
            <Area dataKey="user-value" stackId="1" name="user"
                  type="monotone" stroke="#0000ff" fill="#0000ff" />
            <Area dataKey="nice-value" stackId="1" name="nice"
                  type="monotone" stroke="#00e000" fill="#00e000" />
            <Area dataKey="idle-value" stackId="1" name="idle"
                  type="monotone" stroke="#ffffff" fill="#ffffff" />
          </AreaChart>
        )

      case 'memory':
        for (let i = 0; i < series[0].sequence.length; i++) {
          dnames = { 't': series[0].sequence[i].t };
          for (let j = 0; j < series.length; j++) {
            dnames[series[j].name] = series[j].sequence[i].v;
          }
          data[data.length] = dnames;
        }

        return (
          <AreaChart width={w} height={h} margin={margin} data={data}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis name="Time" dataKey="t" type="number" scale="time"
                   tick={<CustomizedTimeTick />}
                   domain={['dataMin', 'dataMax']} />
            <YAxis type="number" domain={['auto', 'auto']} />
            <Tooltip />
            <Area dataKey="free-value" stackId="1" name="free"
                  type="monotone" stroke="#00ff00" fill="#008800" />
            <Area dataKey="cached-value" stackId="1" name="cached"
                  type="monotone" stroke="#0000ff" fill="#000088" />
            <Area dataKey="buffered-value" stackId="1" name="buffered"
                  type="monotone" stroke="#ffff00" fill="#888800" />
            <Area dataKey="used-value" stackId="1" name="used"
                  type="monotone" stroke="#ff0000" fill="#880000" />
          </AreaChart>
        )

      default:
        return (
          <LineChart width={w} height={h} margin={margin}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis name="Time" dataKey="t" type="number" scale="time"
                   tick={<CustomizedTimeTick />}
                   domain={['dataMin', 'dataMax']} />
            <YAxis dataKey="v" type="number" domain={['auto', 'auto']} />
            <Tooltip />
            <Legend />
            {series.map(s => (
              <Line dataKey="v" data={s.sequence} name={s.name} key={s.name} />
            ))}
          </LineChart>
        )
    }
  }

  render () {
    const plugin = this.props.plugin || 'none';
    const instance = this.props.instance || 'none';
    const series = this.props.series || [];

    if (!Array.isArray(series) || !series.length) {
      return (<div className="chart-container" />)
    }

    return (
      <div className="chart-container">
        {this.renderPlugin(plugin, instance, series)}
      </div>
    )
  }
}

export default ChartRenderer;
