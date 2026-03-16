import { readPageModel } from "./common.js";

const model = readPageModel();

if (model) {
  const phase = model.phase;
  const ratio = phase.follower_turns.decimal;
  const range = document.getElementById("phaseRange");
  const play = document.getElementById("phasePlay");
  const reset = document.getElementById("phaseReset");
  const progressLabel = document.getElementById("phaseProgressLabel");
  const svg = document.getElementById("phaseSvg");
  const summary = document.getElementById("phaseSummary");
  const wholeTurnsNode = document.getElementById("phaseWholeTurns");
  const residualNode = document.getElementById("phaseResidual");

  let progress = 1;
  let timer = null;

  function renderDisc(cx, cy, radius, angle, label, color, tickCount) {
    const ticks = [];
    for (let index = 0; index < tickCount; index += 1) {
      const theta = (index / tickCount) * Math.PI * 2;
      const inner = radius - 16;
      const x1 = cx + inner * Math.cos(theta);
      const y1 = cy + inner * Math.sin(theta);
      const x2 = cx + radius * Math.cos(theta);
      const y2 = cy + radius * Math.sin(theta);
      ticks.push(
        `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="#1f1f24" stroke-width="${index % 4 === 0 ? 2 : 1}"></line>`
      );
    }
    return `
      <g transform="rotate(${angle} ${cx} ${cy})">
        <circle cx="${cx}" cy="${cy}" r="${radius}" fill="${color}" opacity="0.88"></circle>
        ${ticks.join("")}
        <line x1="${cx}" y1="${cy}" x2="${cx}" y2="${cy - radius + 18}" stroke="#1f1f24" stroke-width="3"></line>
      </g>
      <text x="${cx}" y="${cy + radius + 26}" text-anchor="middle" font-size="15" fill="#1f1f24">${label}</text>
    `;
  }

  function render() {
    const followerTurns = progress * ratio;
    const wholeTurns = Math.floor(followerTurns + 1e-9);
    const residual = followerTurns - wholeTurns;
    const driverAngle = progress * 360;
    const followerAngle = -followerTurns * 360;

    svg.innerHTML = `
      <rect x="0" y="0" width="720" height="360" fill="transparent"></rect>
      <text x="50" y="36" font-size="16" fill="#605c66">One full driver turn visualized as quotient + residual phase</text>
      ${renderDisc(225, 170, 112, driverAngle, `Driver a = ${phase.dividend}`, "#d6eadf", 24)}
      ${renderDisc(505, 170, 84, followerAngle, `Follower b = ${phase.divisor}`, "#f1dfc0", 20)}
      <line x1="337" y1="170" x2="421" y2="170" stroke="#315f82" stroke-width="4"></line>
      <text x="360" y="146" font-size="15" fill="#1f1f24">ratio = ${phase.dividend}/${phase.divisor}</text>
    `;

    progressLabel.textContent = `${Math.round(progress * 100)}% of one driver turn`;
    wholeTurnsNode.textContent = String(wholeTurns);
    residualNode.textContent = `${phase.remainder}/${phase.divisor} target | current ${residual.toFixed(4)}`;
    summary.innerHTML =
      `${phase.dividend}/${phase.divisor} = <span class="accent-text">${phase.quotient}</span> + ${phase.remainder}/${phase.divisor}<br>` +
      `Follower turns so far: ${followerTurns.toFixed(4)}<br>` +
      `Full turns counted: ${wholeTurns}`;
  }

  function stopPlayback() {
    if (timer !== null) {
      window.clearInterval(timer);
      timer = null;
    }
    play.textContent = "Play";
  }

  range.addEventListener("input", () => {
    progress = Number(range.value) / 1000;
    render();
  });

  play.addEventListener("click", () => {
    if (timer !== null) {
      stopPlayback();
      return;
    }
    progress = 0;
    range.value = "0";
    play.textContent = "Pause";
    timer = window.setInterval(() => {
      progress += 0.01;
      if (progress >= 1) {
        progress = 1;
        range.value = "1000";
        render();
        stopPlayback();
        return;
      }
      range.value = String(Math.round(progress * 1000));
      render();
    }, 26);
  });

  reset.addEventListener("click", () => {
    stopPlayback();
    progress = 1;
    range.value = "1000";
    render();
  });

  render();
}
