(function () {
  var activePortal = null;

  function attach(icon) {
    var wrap = icon.closest(".info-tooltip-wrap");
    if (!wrap) return;
    var panel = wrap.querySelector(".info-tooltip-panel");
    if (!panel) return;

    icon.addEventListener("mouseenter", function () {
      remove();

      var clone = panel.cloneNode(true);
      clone.id = "tooltip-portal-active";

      clone.style.cssText = [
        "position: fixed",
        "display: block",
        "visibility: hidden",
        "z-index: 99999",
        "pointer-events: none",
        "width: 300px",
        "max-width: 90vw",
      ].join(";");

      document.body.appendChild(clone);

      var iconRect = icon.getBoundingClientRect();
      var panelRect = clone.getBoundingClientRect();
      var viewportW = window.innerWidth;
      var viewportH = window.innerHeight;

      var leftCandidate = iconRect.right + 8;
      if (leftCandidate + panelRect.width > viewportW - 8) {
        leftCandidate = iconRect.left - panelRect.width - 8;
      }

      var topCandidate = iconRect.top;
      topCandidate = Math.max(
        8,
        Math.min(topCandidate, viewportH - panelRect.height - 8),
      );

      clone.style.left = leftCandidate + "px";
      clone.style.top = topCandidate + "px";
      clone.style.visibility = "visible";

      activePortal = clone;
    });

    icon.addEventListener("mouseleave", remove);
  }

  function remove() {
    if (activePortal && activePortal.parentNode) {
      activePortal.parentNode.removeChild(activePortal);
    }
    activePortal = null;
  }

  function init() {
    document.querySelectorAll(".info-tooltip-icon").forEach(attach);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }

  var observer = new MutationObserver(function (mutations) {
    mutations.forEach(function (m) {
      m.addedNodes.forEach(function (node) {
        if (node.nodeType !== 1) return;
        if (node.classList && node.classList.contains("info-tooltip-icon")) {
          attach(node);
        }
        node.querySelectorAll &&
          node.querySelectorAll(".info-tooltip-icon").forEach(attach);
      });
    });
  });

  observer.observe(document.body, { childList: true, subtree: true });
})();
