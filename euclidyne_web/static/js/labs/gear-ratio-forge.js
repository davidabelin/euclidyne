import { readPageModel } from "../common.js";

const page = readPageModel();
const model = page?.model;

if (model) {
  const svg = document.getElementById("gearForgeSvg");
  const summary = document.getElementById("gearForgeSummary");
  const candidate = model.candidates.selected;
  const stages = candidate.stages;

  const spacing = 680 / Math.max(stages.length, 1);
  const nodes = stages
    .map((stage, index) => {
      const cxA = 60 + index * spacing;
      const cxB = cxA + 150;
      const cy = 170;
      const scale = 2.4;
      const rA = Math.max(24, stage.driver_teeth / scale);
      const rB = Math.max(24, stage.follower_teeth / scale);
      return `
        <circle cx="${cxA}" cy="${cy}" r="${rA}" fill="#d6eadf" stroke="#1f1f24" stroke-width="2"></circle>
        <circle cx="${cxB}" cy="${cy}" r="${rB}" fill="#f1dfc0" stroke="#1f1f24" stroke-width="2"></circle>
        <line x1="${cxA + rA}" y1="${cy}" x2="${cxB - rB}" y2="${cy}" stroke="#315f82" stroke-width="4"></line>
        <text x="${cxA}" y="${cy + 5}" text-anchor="middle" font-size="15">${stage.driver_teeth}</text>
        <text x="${cxB}" y="${cy + 5}" text-anchor="middle" font-size="15">${stage.follower_teeth}</text>
      `;
    })
    .join("");

  svg.innerHTML = `
    <rect x="0" y="0" width="720" height="360" fill="transparent"></rect>
    <text x="42" y="38" font-size="16" fill="#605c66">Selected fixed-ratio candidate</text>
    ${nodes}
  `;

  summary.innerHTML = `${candidate.label} realizes ${candidate.realized_ratio.numerator}/${candidate.realized_ratio.denominator} with error ${candidate.error_decimal}.`;
}
