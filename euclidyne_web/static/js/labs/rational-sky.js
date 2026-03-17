import { readPageModel } from "../common.js";

const page = readPageModel();
const model = page?.model;
const d3 = window.d3;

if (model && d3) {
  const svg = d3.select("#rationalSkySvg");
  svg.selectAll("*").remove();

  if (model.view === "orchard") {
    svg
      .append("g")
      .selectAll("circle")
      .data(model.orchard.points)
      .join("circle")
      .attr("cx", (d) => 40 + d.x * 70)
      .attr("cy", (d) => 430 - d.y * 40)
      .attr("r", 6)
      .attr("fill", (d) => (d.visible ? "#0f7b6d" : "#cbbfad"))
      .attr("opacity", 0.82);
  } else if (model.view === "farey") {
    svg
      .append("line")
      .attr("x1", 40)
      .attr("x2", 680)
      .attr("y1", 220)
      .attr("y2", 220)
      .attr("stroke", "#1f1f24")
      .attr("stroke-width", 2);
    svg
      .append("g")
      .selectAll("circle")
      .data(model.farey.fractions)
      .join("circle")
      .attr("cx", (d) => 40 + d.decimal * 640)
      .attr("cy", 220)
      .attr("r", (d) => (d.is_selected ? 9 : 6))
      .attr("fill", (d) => (d.is_selected ? "#923f36" : "#22577a"));
  } else if (model.view === "ford") {
    svg
      .append("g")
      .selectAll("circle")
      .data(model.ford.circles)
      .join("circle")
      .attr("cx", (d) => 40 + d.x * 640)
      .attr("cy", (d) => 420 - d.radius * 1800)
      .attr("r", (d) => Math.max(3, d.radius * 1800))
      .attr("fill", "none")
      .attr("stroke", (d) => (d.is_selected ? "#923f36" : "#315f82"))
      .attr("stroke-width", 2);
  } else {
    svg
      .append("g")
      .selectAll("text")
      .data(model.stern_brocot.path)
      .join("text")
      .attr("x", 40)
      .attr("y", (_, index) => 44 + index * 28)
      .attr("font-size", 15)
      .text((d) => `${d.move} : ${d.mediant}`);
  }
}
