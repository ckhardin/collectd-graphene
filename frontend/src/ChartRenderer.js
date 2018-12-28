import * as d3 from 'd3';
import React, { Component } from 'react';
import { withFauxDOM } from 'react-faux-dom';


class ChartRenderer extends Component {
  static propTypes = {
    data: React.PropTypes.array,
  };

  render () {
    const faux = this.props.connectFauxDOM('div', 'chart', true);
    const w = Math.max(document.documentElement.clientWidth, window.innerWidth || 0);
    const h = Math.max(document.documentElement.clientHeight, window.innerHeight || 0);
    const padding = 40;
    const data = this.props.data || { 'rrdseries': [] }

    const sequence = [];

    if (!Array.isArray(data.rrdseries) || !data.rrdseries.length) {
      return (<div className="chart-container" />)
    }

    // D3 Code to create the chart using faux as container
    const el = d3.select(faux).append('svg')
        .attr('width', w)
        .attr('height', h)
        .attr('data', null);

    data.rrdseries.forEach((series) => {
      sequence.push.apply(sequence, series.sequence)
    })

    const extent_x = d3.extent(sequence, (d) => d.t)
    const x = d3.scaleTime()
      .range([padding, w - padding])
      .domain([extent_x[0], extent_x[1]]);

    const extent_y = d3.extent(sequence, (d) => d.v)
    const y = d3.scaleLinear()
      .range([h - padding, padding])
      .domain([(extent_y[0] > 0) ? 0 : extent_y[0], 1.1 * extent_y[1]]);

    const area = d3.area()
      .x((d) => x(d.t))
      .y1((d) => y(d.v))
      .y0((d) => y(0));

    const line = d3.line()
      .x((d) => x(d.t))
      .y((d) => y(d.v));

    if (data.rrdseries.length === 1) {
      el.append('path')
        .attr('className', 'rrdchart')
        .attr('key', 'rrdchart')
        .attr('d', area(sequence));
    } else {
      const g_path = el.append("g")
        .attr('className', 'rrdchart')
        .attr('key', 'rrdchart')
        .attr("fill", "none")
        .attr("stroke", "steelblue")
        .attr("stroke-width", 1.5)
        .attr("stroke-linejoin", "round")
        .attr("stroke-linecap", "round");
      data.rrdseries.forEach((series) => {
        g_path.append('path')
          .style("mix-blend-mode", "multiply")
          .attr('d', line(series.sequence));
      })
    }

    // x-axis
    el.append('g')
      .attr("transform", `translate(0, ${h - padding})`)
      .call(d3.axisBottom(x));

    return (<div className="chart-container">{this.props.chart}</div>)
  }
}

export default withFauxDOM(ChartRenderer);
