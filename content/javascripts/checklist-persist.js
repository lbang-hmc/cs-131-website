// Persists the checked state of task-list checkboxes (`- [ ] ...`) to
// localStorage, keyed by page path + item text, so a student's progress
// through a lab/HW checklist survives a reload. Not shared across devices
// or browsers, and not submitted anywhere -- purely a local convenience.
(function () {
  function storageKey(text) {
    return "cs131-checklist:" + location.pathname + ":" + text.slice(0, 200);
  }

  function initChecklists() {
    var boxes = document.querySelectorAll(
      '.md-content li.task-list-item input[type="checkbox"]'
    );

    boxes.forEach(function (box) {
      if (box.dataset.checklistBound) return;
      box.dataset.checklistBound = "true";

      var li = box.closest("li");
      var text = li ? li.textContent.trim() : "";
      var key = storageKey(text);

      try {
        var saved = localStorage.getItem(key);
        if (saved !== null) {
          box.checked = saved === "true";
        }
      } catch (e) {
        // localStorage unavailable (private browsing, disabled, etc.) -- skip persistence.
      }

      box.addEventListener("change", function () {
        try {
          localStorage.setItem(key, box.checked);
        } catch (e) {
          // Ignore -- nothing to do if storage isn't available.
        }
      });
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initChecklists);
  } else {
    initChecklists();
  }

  // Material's "instant navigation" feature (if ever enabled) swaps page
  // content without a full reload; re-bind checkboxes after each swap.
  if (window.document$ && typeof window.document$.subscribe === "function") {
    window.document$.subscribe(initChecklists);
  }
})();
