import { clamp, readPageModel } from "../common.js";

const page = readPageModel();
const model = page?.model;

if (model) {
  const geometry = model.geometry;
  const stages = geometry.stages;
  const squares = geometry.squares;
  const range = document.getElementById("rectRange");
  const prev = document.getElementById("rectPrev");
  const next = document.getElementById("rectNext");
  const toggle = document.getElementById("rectToggleArcs");
  const stageLabel = document.getElementById("rectStageLabel");
  const stageInfo = document.getElementById("rectStageInfo");
  const svg = document.getElementById("rectGeometry");

  let currentStage = stages.length;
  let showArcs = false;

  function arcPath(square, scale, padding) {
    const x = padding + square.x * scale;
    const y = padding + square.y * scale;
    const size = square.size * scale;
    let startX = x;
    let startY = y;
    let endX = x + size;
    let endY = y + size;

    if (square.arc_hint === "south") {
      startX = x + size;
      startY = y;
      endX = x;
      endY = y + size;
    } else if (square.arc_hint === "west") {
      startX = x + size;
      startY = y + size;
      endX = x;
      endY = y;
    } else if (square.arc_hint === "north") {
      startX = x;
      startY = y + size;
      endX = x + size;
      endY = y;
    }

    return `M ${startX} ${startY} A ${size} ${size} 0 0 1 ${endX} ${endY}`;
  }

  function renderGeometry() {
    const padding = 24;
    const scale = Math.min(
      (720 - padding * 2) / geometry.bounding_box.width,
      (460 - padding * 2) / geometry.bounding_box.height
    );

    const rects = squares
      .map((square) => {
        const visible = square.stage_index <= currentStage;
        return `
          <rect
            x="${padding + square.x * scale}"
            y="${padding + square.y * scale}"
            width="${square.size * scale}"
            height="${square.size * scale}"
            fill="${square.color}"
            fill-opacity="${visible ? 0.72 : 0.1}"
            stroke="#ffffff"
            stroke-width="1.5"
          ></rect>
        `;
      })
      .join("");

    const arcs =
      showArcs && geometry.golden_special.enabled
        ? squares
            .filter((square) => square.stage_index <= currentStage)
            .map(
              (square) =>
                `<path d="${arcPath(square, scale, padding)}" fill="none" stroke="#1f1f24" stroke-width="1.8" opacity="0.54"></path>`
            )
            .join("")
        : "";

    svg.innerHTML = `
      <rect x="0" y="0" width="720" height="460" fill="transparent"></rect>
      <rect
        x="${padding}"
        y="${padding}"
        width="${geometry.bounding_box.width * scale}"
        height="${geometry.bounding_box.height * scale}"
        fill="none"
        stroke="#1f1f24"
        stroke-width="2"
      ></rect>
      ${rects}
      ${arcs}
    `;
  }

  function renderState() {
    const stage = stages[currentStage - 1];
    stageLabel.textContent = `Stage ${currentStage} / ${stages.length}`;
    stageInfo.innerHTML =
      `<strong>Quotient</strong> q${stage.index} = ${stage.quotient}<br>` +
      `<strong>Orientation</strong> ${stage.orientation}<br>` +
      `<strong>Remainder</strong> ${stage.remainder}<br>` +
      `<strong>Square size</strong> ${stage.square_size}`;

    prev.disabled = currentStage === 1;
    next.disabled = currentStage === stages.length;
    range.value = String(currentStage);
    toggle.textContent = geometry.golden_special.enabled
      ? showArcs
        ? "Hide Arcs"
        : "Show Arcs"
      : "Golden Only";
    renderGeometry();
  }

  function goTo(stage) {
    currentStage = clamp(stage, 1, stages.length);
    renderState();
  }

  prev.addEventListener("click", () => goTo(currentStage - 1));
  next.addEventListener("click", () => goTo(currentStage + 1));
  range.addEventListener("input", () => goTo(Number(range.value)));
  toggle.addEventListener("click", () => {
    if (!geometry.golden_special.enabled) {
      return;
    }
    showArcs = !showArcs;
    renderState();
  });

  renderState();
}
