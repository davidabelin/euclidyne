import { readPageModel } from "../common.js";

const page = readPageModel();
const model = page?.model;
const Tone = window.Tone;

if (model) {
  const svg = document.getElementById("rhythmSvg");
  const play = document.getElementById("rhythmPlay");
  const stop = document.getElementById("rhythmStop");

  function render(activeIndex = -1) {
    const cx = 360;
    const cy = 180;
    const radius = 118;
    const nodes = model.events
      .map((event) => {
        const theta = (event.angle_deg - 90) * (Math.PI / 180);
        const x = cx + radius * Math.cos(theta);
        const y = cy + radius * Math.sin(theta);
        const fill = !event.active ? "#f1e9db" : event.index === activeIndex ? "#923f36" : "#0f7b6d";
        return `<circle cx="${x}" cy="${y}" r="18" fill="${fill}" stroke="#1f1f24" stroke-width="2"></circle>`;
      })
      .join("");
    svg.innerHTML = `
      <rect x="0" y="0" width="720" height="360" fill="transparent"></rect>
      <circle cx="${cx}" cy="${cy}" r="${radius}" fill="none" stroke="#1f1f24" stroke-width="2"></circle>
      ${nodes}
    `;
  }

  let synth = null;
  let timer = null;

  async function startPlayback() {
    render();
    if (!Tone) {
      return;
    }
    await Tone.start();
    if (!synth) {
      synth = new Tone.MembraneSynth().toDestination();
    }
    let index = 0;
    const duration = model.audio.step_duration * 1000;
    timer = window.setInterval(() => {
      const event = model.events[index];
      render(index);
      if (event.active) {
        synth.triggerAttackRelease("C2", "8n");
      }
      index = (index + 1) % model.events.length;
    }, duration);
  }

  play.addEventListener("click", async () => {
    if (timer !== null) {
      return;
    }
    await startPlayback();
  });

  stop.addEventListener("click", () => {
    if (timer !== null) {
      window.clearInterval(timer);
      timer = null;
    }
    render();
  });

  render();
}
