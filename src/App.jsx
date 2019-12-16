import React, { Component } from 'react'
import * as d3 from 'd3';
import data from './data/a-60-5500-15';
import colors from './colors';
import './App.css';

const margin = {top: 10, right: 30, bottom: 30, left: 40};

class App extends Component {
  constructor(props) {
    super(props);
    this.container = null;
    this.state = {
      width: window.innerWidth,
      height: window.innerHeight,
      data: {}
    }
  }

  componentDidMount() {
    this.updateDimention()
    window.addEventListener('resize', this.updateDimention)
    this.setupComponents()
  }

  componentWillUnmount() {
    window.removeEventListener('resize', this.updateDimention)
  }

  updateDimention = () => {
    this.setState({ width: window.innerWidth, height: window.innerHeight })
  }

  setupComponents = () => {
    const { width, height } = this.state;

    this.svg = d3.select(this.container)
      .append("svg")
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom)
      .append("g")
      .attr("transform", `translate(${margin.left},${margin.top})`)

    this.link = this.svg
        .selectAll("line")
        .data(data.links)
        .enter()
        .append("line")
        .style("stroke", "#999999");

    this.circle = this.svg
      .selectAll("circle")
      .data(data.nodes)
      .enter()
      .append("circle")
        .attr("r", 20);

    this.label = this.svg.append("g")
        .attr("class", "labels")
        .selectAll("text")
        .data(data.nodes)
        .enter().append("text")
          .attr("class", "label")
          .text(d => d.id);


    d3.forceSimulation(data.nodes)
        .force("link", d3.forceLink()
              .id((d) => d.id)
              .links(data.links)
        )
        .force("charge", d3.forceManyBody().strength(-7000))
        .force("center", d3.forceCenter(width / 2, height / 2))
        .on("end", this.draw);
  }

  draw = ()=> {
    this.link
        .attr("x1", d =>  d.source.x)
        .attr("y1", d =>  d.source.y)
        .attr("x2", d => d.target.x)
        .attr("y2", d => d.target.y)
        .attr("stroke-width", d => d.source.relations[d.target.id] * 0.1);

    this.circle
         .attr("cx", d => d.x+6)
         .attr("cy", d => d.y-6)
          .style("fill", (d) => colors[d.group]);

    this.label
    		.attr("x", d => d.x)
            .attr("y", d => d.y)
            .style("font-size", "20px")
            .style("fill", "#333333");
  }

  render() {
    return(
      <div
        className="main-container"
        ref={container => this.container = container}/>
    )
  }
}

export default App;
