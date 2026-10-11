/* Progressive enhancement: all portfolio content and links work without JavaScript. */
(() => {
  "use strict";
  const button = document.querySelector(".nav-toggle");
  const navigation = document.getElementById("primary-nav");
  if (!button || !navigation) return;

  document.documentElement.classList.add("js");
  button.hidden = false;
  const narrow = window.matchMedia("(max-width: 800px)");

  function setOpen(open, returnFocus = false) {
    navigation.classList.toggle("is-open", open);
    button.setAttribute("aria-expanded", String(open));
    button.querySelector("span").textContent = open ? "Close" : "Menu";
    if (returnFocus) button.focus();
  }

  function updateSize() {
    button.hidden = !narrow.matches;
    setOpen(false);
  }

  button.addEventListener("click", () => {
    setOpen(button.getAttribute("aria-expanded") !== "true");
  });

  navigation.addEventListener("click", (event) => {
    if (event.target.closest("a") && narrow.matches) setOpen(false, true);
  });

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && button.getAttribute("aria-expanded") === "true") {
      setOpen(false, true);
    }
  });

  if (typeof narrow.addEventListener === "function") {
    narrow.addEventListener("change", updateSize);
  } else {
    narrow.addListener(updateSize);
  }
  updateSize();
})();
