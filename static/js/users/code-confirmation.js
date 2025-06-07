document.addEventListener("DOMContentLoaded", function () {
  const inputs = document.querySelectorAll(".code-input");
  const hiddenInput = document.getElementById("code-hidden");
  const form = document.getElementById("code-form");

  inputs.forEach((input, index) => {
    input.addEventListener("input", () => {
      if (input.value.length === 1 && index < inputs.length - 1) {
        inputs[index + 1].focus();
      }
    });

    input.addEventListener("keydown", (e) => {
      if (e.key === "Backspace" && input.value === "" && index > 0) {
        inputs[index - 1].focus();
      }
    });
  });

  form.addEventListener("submit", (e) => {
    const code = Array.from(inputs).map((input) => input.value).join("");
    hiddenInput.value = code;
  });
});
