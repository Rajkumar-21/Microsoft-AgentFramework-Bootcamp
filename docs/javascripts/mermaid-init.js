/**
 * Mermaid fallback initializer.
 *
 * Material for MkDocs dynamically loads mermaid from CDN (unpkg),
 * but that load can fail silently in some environments.
 * This script ensures mermaid renders all diagrams by:
 *   1. Waiting for the `mermaid` global to be available
 *   2. Checking for any unrendered `pre.mermaid` elements
 *   3. Calling mermaid.run() as a safety net
 */
;(function () {
  "use strict"

  var MAX_WAIT = 15000 /* ms — max time to wait for mermaid library */
  var POLL = 300 /* ms — poll interval */
  var waited = 0

  function tryInit() {
    /* mermaid not loaded yet — keep waiting */
    if (typeof mermaid === "undefined" || mermaid instanceof Element) {
      waited += POLL
      if (waited < MAX_WAIT) {
        setTimeout(tryInit, POLL)
      }
      return
    }

    /* Find all pre.mermaid elements that still contain raw text (no SVG) */
    var unrendered = document.querySelectorAll("pre.mermaid")
    if (unrendered.length === 0) return /* nothing to do */

    /* Check if any of them are still unrendered (Material strips .mermaid
       class on successful render, so pre.mermaid = not yet processed) */
    var needsRender = false
    unrendered.forEach(function (el) {
      if (!el.querySelector("svg")) needsRender = true
    })

    if (!needsRender) return /* Material already rendered them */

    /* Initialize mermaid and render all unprocessed elements */
    try {
      mermaid.initialize({
        startOnLoad: false,
        theme: "default",
        sequence: {
          actorFontSize: "16px",
          messageFontSize: "16px",
          noteFontSize: "16px"
        }
      })
      mermaid.run({ querySelector: "pre.mermaid" })
    } catch (e) {
      /* mermaid.run() might not exist in older versions — try contentLoaded */
      try {
        mermaid.contentLoaded()
      } catch (e2) {
        console.warn("[mermaid-init] Failed to render:", e2)
      }
    }
  }

  /* Start checking after DOM is ready */
  function start() {
    /* Give Material 2 seconds to do its thing first */
    setTimeout(tryInit, 2000)
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", start)
  } else {
    start()
  }

  /* Re-run on instant navigation */
  if (typeof document$ !== "undefined") {
    document$.subscribe(function () {
      waited = 0
      setTimeout(tryInit, 2000)
    })
  }
})()
