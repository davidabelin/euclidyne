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

