var data = [
  {
    className: "germany", // optional, can be used for styling
    axes: [
      { axis: "strength", value: 13, yOffset: 10 },
      { axis: "intelligence", value: 6 },
      { axis: "charisma", value: 5 },
      { axis: "dexterity", value: 9 },
      { axis: "luck", value: 2, xOffset: -20 },
    ],
  },
  {
    className: "argentina",
    axes: [
      { axis: "strength", value: 6 },
      { axis: "intelligence", value: 7 },
      { axis: "charisma", value: 10 },
      { axis: "dexterity", value: 13 },
      { axis: "luck", value: 9 },
    ],
  },
];

var chart = RadarChart.chart();
var svg = d3
  .select("body")
  .append("svg")
  .attr("width", 600)
  .attr("height", 800);

// draw one
svg.append("g").classed("focus", 1).datum(data).call(chart);

// draw many radars
var game = svg.selectAll("g.game").data([data, data, data, data]);
game.enter().append("g").classed("game", 1);
game
  .attr("transform", function (d, i) {
    return "translate(150,600)";
  })
  .call(chart);

// retrieve config
chart.config();
// all options with default values
chart.config({
  containerClass: "radar-chart", // target with css, the default stylesheet targets .radar-chart
  w: 600,
  h: 600,
  factor: 0.95,
  factorLegend: 1,
  levels: 3,
  maxValue: 0,
  minValue: 0,
  radians: 2 * Math.PI,
  color: d3.scale.category10(), // pass a noop (function() {}) to decide color via css
  axisLine: true,
  axisText: true,
  circles: true,
  radius: 5,
  open: false, // whether or not the last axis value should connect back to the first axis value
  // if true, consider modifying the chart opacity (see "Style with CSS" section above)
  axisJoin: function (d, i) {
    return d.className || i;
  },
  tooltipFormatValue: function (d) {
    return d;
  },
  tooltipFormatClass: function (d) {
    return d;
  },
  transitionDuration: 300,
});

// var chart = RadarChart.chart();
// var svg = d3
//   .select("body")
//   .append("svg")
//   .attr("width", 600)
//   .attr("height", 800);

// // draw one
// svg.append("g").classed("focus", 1).datum(data).call(chart);

// // draw many radars
// var game = svg.selectAll("g.game").data([data, data, data, data]);
// game.enter().append("g").classed("game", 1);
// game
//   .attr("transform", function (d, i) {
//     return "translate(150,600)";
//   })
//   .call(chart);
