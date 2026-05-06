/**
 * Tooltip portal — escapes sidebar overflow clipping.
 *
 * The sidebar has `overflowY: auto` which implicitly sets `overflowX: hidden`,
 * clipping any absolutely-positioned child that extends beyond the sidebar edge.
 *
 * Fix: on hover, read the icon's viewport coordinates via getBoundingClientRect(),
 * clone the tooltip panel into <body> as `position: fixed`, and position it there.
 * The clone lives outside every overflow ancestor, so it is never clipped.
 */

(function () {
  var activePortal = null;

  function attach(icon) {
    var wrap = icon.closest(".info-tooltip-wrap");
    if (!wrap) return;
    var panel = wrap.querySelector(".info-tooltip-panel");
    if (!panel) return;

    icon.addEventListener("mouseenter", function () {
      // Remove any existing portal first
      remove();

      var clone = panel.cloneNode(true);
      clone.id = "tooltip-portal-active";

      // Make it fixed and invisible for measurement
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

      // Measure icon and portal, then place it
      var iconRect = icon.getBoundingClientRect();
      var panelRect = clone.getBoundingClientRect();
      var viewportW = window.innerWidth;
      var viewportH = window.innerHeight;

      // Prefer placing to the right of the icon; flip left if it would overflow
      var leftCandidate = iconRect.right + 8;
      if (leftCandidate + panelRect.width > viewportW - 8) {
        leftCandidate = iconRect.left - panelRect.width - 8;
      }

      // Align tooltip top-edge to icon top-edge (corner-anchored, not centred);
      // clamp within viewport so it never bleeds off the bottom.
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

  // Run on initial load
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }

  // Re-run after Dash re-renders (Dash updates the DOM without a full page reload)
  var observer = new MutationObserver(function (mutations) {
    mutations.forEach(function (m) {
      m.addedNodes.forEach(function (node) {
        if (node.nodeType !== 1) return;
        // If new icons were added inside the mutated subtree, attach to them
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
