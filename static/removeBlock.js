/**
 * Remove the form block from the page, ensuring at least one form block remains.
 *
 * @param {HTMLButtonElement} button - The button element that was clicked.
 */
function removeBlock(button) {
  const container = document.getElementById("form-container");
  if (container.children.length > 1) {
    const block = button.parentElement;
    container.removeChild(block);
  }
}
