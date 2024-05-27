/**
 * Add a new form block to the page for entering and running JavaScript code.
 */
function addNewBlock() {
  const container = document.getElementById("form-container");
  const newBlock = document.createElement("div");
  newBlock.className = "form-block";
  newBlock.innerHTML = `
        <textarea class="textarea"></textarea>
        <button class="button" onclick="runScript(this)">Run</button>
        <button class="button" onclick="removeBlock(this)">Remove</button>
        <div class="output"></div>
    `;
  container.appendChild(newBlock);
}
