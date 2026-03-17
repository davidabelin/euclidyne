export function readPageModel() {
  const node = document.getElementById("page-model");
  if (!node) {
    return null;
  }
  return JSON.parse(node.textContent);
}

export function clamp(value, minimum, maximum) {
  return Math.min(maximum, Math.max(minimum, value));
}

export function prefersReducedMotion() {
  return window.matchMedia("(prefers-reduced-motion: reduce)").matches;
}

export function renderMath(root = document.body) {
  if (typeof window.renderMathInElement !== "function") {
    return;
  }
  window.renderMathInElement(root, {
    delimiters: [
      { left: "$$", right: "$$", display: true },
      { left: "$", right: "$", display: false },
    ],
    throwOnError: false,
  });
}

renderMath();
