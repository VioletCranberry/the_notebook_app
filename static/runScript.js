/**
 * Run the provided JavaScript code by sending it to the server for evaluation.
 *
 * @param {HTMLButtonElement} button - The button element that was clicked.
 */
function runScript(button) {
  const textarea = button.previousElementSibling;
  const output = button.nextElementSibling.nextElementSibling; // Adjusted to correctly target the output div
  const scriptContent = textarea.value;

  fetch("/run", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ script: scriptContent }),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.error) {
        output.textContent = data.error;
      } else {
        output.textContent = data.result;
      }
    })
    .catch((error) => {
      output.textContent = "Error: " + error.message;
    });
}
