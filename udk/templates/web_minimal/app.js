// Minimal Web Starter Logic
document.addEventListener("DOMContentLoaded", () => {
  const input = document.getElementById("user-input");
  const button = document.getElementById("action-btn");
  const output = document.getElementById("output-box");

  if (button && input && output) {
    button.addEventListener("click", () => {
      const val = input.value.trim();
      if (!val) {
        output.textContent = "Please enter some text first.";
        output.classList.add("warn");
      } else {
        output.textContent = `Processed: ${val.toUpperCase()} (${val.length} chars)`;
        output.classList.remove("warn");
      }
    });
  }
});
