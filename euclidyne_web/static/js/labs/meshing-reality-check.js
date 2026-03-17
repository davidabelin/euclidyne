import { readPageModel } from "../common.js";

const page = readPageModel();
const model = page?.model;

if (model) {
  const svg = document.getElementById("meshingSvg");
  const scale = 3;
  const cxA = 240;
  const cxB = 240 + model.center_distance.working;
  const cy = 180;
  const rA = model.driver.pitch_radius / scale;
  const rB = model.follower.pitch_radius / scale;

  svg.innerHTML = `
    <rect x="0" y="0" width="720" height="360" fill="transparent"></rect>
    <line x1="${cxA}" y1="${cy}" x2="${cxB}" y2="${cy}" stroke="#315f82" stroke-width="4"></line>
    <circle cx="${cxA}" cy="${cy}" r="${rA}" fill="#d6eadf" stroke="#1f1f24" stroke-width="2"></circle>
    <circle cx="${cxB}" cy="${cy}" r="${rB}" fill="#f1dfc0" stroke="#1f1f24" stroke-width="2"></circle>
    <text x="${cxA}" y="${cy + 5}" text-anchor="middle" font-size="15">${model.driver.teeth}</text>
    <text x="${cxB}" y="${cy + 5}" text-anchor="middle" font-size="15">${model.follower.teeth}</text>
  `;
}
