document
  .getElementById("transaction-form")
  .addEventListener("submit", function (event) {
    const contaId = this.getAttribute("data-conta-id");
    const natureza = document.getElementById("natureza").value;

    if (natureza === "Saque") {
      this.action = `/contas/${contaId}/sacar`;
    } else if (natureza === "Deposito") {
      this.action = `/contas/${contaId}/depositar`;
    }
  });

const modal = document.getElementById("transaction-modal");
const btn = document.getElementById("new-transaction-btn");
const span = document.querySelector(".modal .close");

btn.onclick = () => (modal.style.display = "flex");
span.onclick = () => (modal.style.display = "none");
window.onclick = (event) => {
  if (event.target == modal) modal.style.display = "none";
};
