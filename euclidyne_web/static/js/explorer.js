import { clamp, readPageModel } from "./common.js";

const model = readPageModel();

if (model) {
  const range = document.getElementById("explorerRange");
  const prev = document.getElementById("explorerPrev");
  const next = document.getElementById("explorerNext");
  const play = document.getElementById("explorerPlay");
  const stepLabel = document.getElementById("explorerStepLabel");
  const equation = document.getElementById("explorerEquation");
  const explanation = document.getElementById("explorerExplanation");
  const identity = document.getElementById("explorerIdentity");
  const svg = document.getElementById("explorerBars");
  const stepRows = Array.from(document.querySelectorAll("#explorerStepTable tbody tr"));
  const extendedRows = Array.from(document.querySelectorAll("#explorerRowTable tbody tr"));

  let state = 0;
  let timer = null;

  function renderBars(step) {
    const data = step
      ? [
          { label: "A", value: step.dividend, color: step.color },
          { label: "B", value: step.divisor, color: "#c0822b" },
          { label: "r", value: step.remainder, color: "#315f82" },
        ]
      : [
          { label: "a", value: model.input.a, color: "#0f7b6d" },
          { label: "b", value: model.input.b, color: "#c0822b" },
        ];

    const maxValue = Math.max(...data.map((item) => item.value), 1);
    const bars = data
      .map((item, index) => {
        const width = (item.value / maxValue) * 500;
        const y = 58 + index * 78;
        return `
          <text x="42" y="${y + 22}" font-size="16" fill="#1f1f24">${item.label}</text>
          <rect x="82" y="${y}" width="${width}" height="30" rx="12" fill="${item.color}" opacity="0.82"></rect>
          <text x="${94 + width}" y="${y + 20}" font-size="16" fill="#1f1f24">${item.value}</text>
        `;
      })
      .join("");

    svg.innerHTML = `
      <rect x="0" y="0" width="720" height="280" fill="transparent"></rect>
      <text x="42" y="28" font-size="16" fill="#605c66">Current magnitude comparison</text>
      ${bars}
    `;
  }

  function renderState() {
    const step = state === 0 ? null : model.steps[state - 1];
    const row = state === 0 ? model.rows[1] : model.rows[state + 1];
    stepLabel.textContent = `Step ${state} / ${model.steps.length}`;
    range.value = String(state);

    if (!step) {
      equation.innerHTML = `Start with <span class="accent-text">a = ${model.input.a}</span> and <span class="accent-text">b = ${model.input.b}</span>.`;
      explanation.textContent =
        "Move step by step to watch each quotient and remainder become an extended-Euclid row.";
      identity.textContent = model.rows[1].identity;
    } else {
      equation.innerHTML = `${step.dividend} = ${step.divisor} * <span class="accent-text">${step.quotient}</span> + ${step.remainder}`;
      explanation.textContent =
        `This step extracts quotient ${step.quotient} and passes remainder ${step.remainder} into the next comparison.`;
      identity.textContent = row.identity;
    }

    renderBars(step);

    stepRows.forEach((element) => {
      element.classList.toggle("active", Number(element.dataset.step) === state);
    });
    extendedRows.forEach((element) => {
      element.classList.toggle("row-active", Number(element.dataset.row) === state + 1);
    });

    prev.disabled = state === 0;
    next.disabled = state === model.steps.length;
  }

  function stopPlay() {
    if (timer !== null) {
      window.clearInterval(timer);
      timer = null;
    }
    play.textContent = "Play";
  }

  function goTo(target) {
    state = clamp(target, 0, model.steps.length);
    renderState();
  }

  prev.addEventListener("click", () => goTo(state - 1));
  next.addEventListener("click", () => goTo(state + 1));
  range.addEventListener("input", () => goTo(Number(range.value)));
  play.addEventListener("click", () => {
    if (timer !== null) {
      stopPlay();
      return;
    }
    play.textContent = "Pause";
    timer = window.setInterval(() => {
      if (state >= model.steps.length) {
        stopPlay();
        return;
      }
      goTo(state + 1);
    }, 950);
  });

  renderState();
}

