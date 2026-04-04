/**
 * Diagram Zoom — click-to-expand fullscreen overlay for Mermaid diagrams,
 * SVG images, and architecture preview images.
 *
 * Features:
 *   - Click any diagram → opens fullscreen modal with pan & zoom
 *   - Mouse-wheel zoom / pinch-to-zoom
 *   - Click-and-drag pan
 *   - "Expand" button hint on hover
 *   - Escape / click backdrop to close
 *   - Robust mermaid handling: waits for rendering, re-renders if needed
 */
;(function () {
  "use strict"

  /* ---- Helpers ---- */
  var MERMAID_RE = /^(sequenceDiagram|graph |flowchart |classDiagram|stateDiagram|erDiagram|gantt|pie|gitGraph|journey|mindmap|timeline|sankey|block|C4Context|C4Container)/m

  /** Extract raw mermaid text from a pre/code element */
  function getMermaidText(el) {
    var code = el.querySelector("code")
    var text = code ? code.textContent : el.textContent
    return text ? text.trim() : ""
  }

  /** Check whether an element contains a rendered SVG */
  function hasRenderedSvg(el) {
    return !!el.querySelector("svg")
  }

  /* ---- Create modal once ---- */
  var overlay = document.createElement("div")
  overlay.className = "diagram-zoom-overlay"
  overlay.innerHTML =
    '<div class="diagram-zoom-backdrop"></div>' +
    '<div class="diagram-zoom-container">' +
    '  <div class="diagram-zoom-toolbar">' +
    '    <button class="diagram-zoom-btn" data-action="zoom-in" title="Zoom in">+</button>' +
    '    <button class="diagram-zoom-btn" data-action="zoom-out" title="Zoom out">&minus;</button>' +
    '    <button class="diagram-zoom-btn" data-action="reset" title="Reset">↻</button>' +
    '    <button class="diagram-zoom-btn diagram-zoom-close" data-action="close" title="Close (Esc)">✕</button>' +
    "  </div>" +
    '  <div class="diagram-zoom-viewport"></div>' +
    "</div>"
  document.body.appendChild(overlay)

  var backdrop = overlay.querySelector(".diagram-zoom-backdrop")
  var viewport = overlay.querySelector(".diagram-zoom-viewport")
  var toolbar = overlay.querySelector(".diagram-zoom-toolbar")

  var scale = 1
  var panX = 0
  var panY = 0
  var dragging = false
  var lastX = 0
  var lastY = 0

  function setTransform() {
    var el = viewport.querySelector(".diagram-zoom-content")
    if (el) el.style.transform = "translate(" + panX + "px," + panY + "px) scale(" + scale + ")"
  }

  /** Create the standard wrapper for modal content */
  function makeWrapper() {
    var w = document.createElement("div")
    w.className = "diagram-zoom-content"
    w.style.transformOrigin = "center center"
    w.style.transition = "transform 0.15s ease"
    w.style.cursor = "grab"
    return w
  }

  /** Place the wrapper in the viewport and show the modal */
  function showModal(wrapper) {
    viewport.appendChild(wrapper)
    setTransform()
    overlay.classList.add("active")
    document.body.style.overflow = "hidden"
  }

  /** Clone an SVG element for display in the modal */
  function cloneSvgForModal(svg) {
    var svgClone = svg.cloneNode(true)
    svgClone.style.maxWidth = "none"
    svgClone.style.maxHeight = "none"
    svgClone.style.width = ""
    svgClone.style.height = ""
    svgClone.removeAttribute("id")
    // Ensure viewBox
    if (!svgClone.getAttribute("viewBox")) {
      var bbox = svg.getBBox ? svg.getBBox() : null
      if (bbox && bbox.width && bbox.height) {
        svgClone.setAttribute("viewBox", bbox.x + " " + bbox.y + " " + bbox.width + " " + bbox.height)
      }
    }
    svgClone.setAttribute("width", "100%")
    svgClone.setAttribute("height", "100%")
    svgClone.style.display = "block"
    return svgClone
  }

  /** Attempt to render mermaid text into SVG using the global mermaid API */
  function renderMermaidSvg(text, callback) {
    // mermaid v10+ (used by Material) exposes a global with .render()
    if (typeof mermaid === "undefined" || !mermaid.render) {
      callback(null)
      return
    }
    var id = "zoom-mm-" + Date.now()
    try {
      var result = mermaid.render(id, text)
      if (result && typeof result.then === "function") {
        // Promise-based (mermaid v10+)
        result.then(function (r) { callback(r.svg || null) })
              .catch(function () { callback(null) })
      } else if (typeof result === "string") {
        callback(result)
      } else {
        callback(null)
      }
    } catch (e) {
      callback(null)
    }
  }

  function openModal(sourceEl) {
    viewport.innerHTML = ""
    scale = 1
    panX = 0
    panY = 0

    var wrapper = makeWrapper()

    /* 1. Rendered SVG present inside the element */
    var svg = sourceEl.querySelector("svg")
    if (svg) {
      wrapper.appendChild(cloneSvgForModal(svg))
      showModal(wrapper)
      return
    }

    /* 2. <img> element (architecture diagram cards) */
    var img = sourceEl.querySelector("img")
    if (img) {
      var imgClone = img.cloneNode(true)
      imgClone.style.maxWidth = "88vw"
      imgClone.style.maxHeight = "82vh"
      imgClone.style.width = "auto"
      imgClone.style.height = "auto"
      wrapper.appendChild(imgClone)
      showModal(wrapper)
      return
    }

    /* 3. Raw mermaid text — render it dynamically */
    var text = getMermaidText(sourceEl)
    if (text && MERMAID_RE.test(text)) {
      // Show a loading placeholder while rendering
      wrapper.innerHTML = '<div style="color:#888;font-size:1.2rem;padding:2rem">Rendering diagram…</div>'
      showModal(wrapper)

      renderMermaidSvg(text, function (svgHtml) {
        if (svgHtml) {
          wrapper.innerHTML = svgHtml
          var rendered = wrapper.querySelector("svg")
          if (rendered) {
            rendered.setAttribute("width", "100%")
            rendered.setAttribute("height", "100%")
            rendered.style.display = "block"
            rendered.style.maxWidth = "none"
            rendered.style.maxHeight = "none"
          }
        } else {
          // mermaid API unavailable — show formatted text as last resort
          var pre = document.createElement("pre")
          pre.style.color = "#ddd"
          pre.style.padding = "2rem"
          pre.style.whiteSpace = "pre-wrap"
          pre.style.fontFamily = "monospace"
          pre.textContent = text
          wrapper.innerHTML = ""
          wrapper.appendChild(pre)
        }
        setTransform()
      })
      return
    }

    /* 4. Fallback — clone the source element */
    var clone = sourceEl.cloneNode(true)
    clone.style.maxWidth = "none"
    clone.style.maxHeight = "none"
    wrapper.appendChild(clone)
    showModal(wrapper)
  }

  function closeModal() {
    overlay.classList.remove("active")
    document.body.style.overflow = ""
    viewport.innerHTML = ""
  }

  /* ---- Toolbar buttons ---- */
  toolbar.addEventListener("click", function (e) {
    var btn = e.target.closest("[data-action]")
    if (!btn) return
    var action = btn.dataset.action
    if (action === "zoom-in") {
      scale = Math.min(scale * 1.3, 8)
    } else if (action === "zoom-out") {
      scale = Math.max(scale / 1.3, 0.2)
    } else if (action === "reset") {
      scale = 1
      panX = 0
      panY = 0
    } else if (action === "close") {
      closeModal()
      return
    }
    setTransform()
  })

  /* ---- Backdrop close ---- */
  backdrop.addEventListener("click", closeModal)

  /* ---- Escape key ---- */
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && overlay.classList.contains("active")) closeModal()
  })

  /* ---- Mouse-wheel zoom ---- */
  viewport.addEventListener(
    "wheel",
    function (e) {
      e.preventDefault()
      var factor = e.deltaY < 0 ? 1.12 : 1 / 1.12
      scale = Math.max(0.2, Math.min(8, scale * factor))
      setTransform()
    },
    { passive: false }
  )

  /* ---- Pan via drag ---- */
  viewport.addEventListener("mousedown", function (e) {
    dragging = true
    lastX = e.clientX
    lastY = e.clientY
    viewport.style.cursor = "grabbing"
  })
  document.addEventListener("mousemove", function (e) {
    if (!dragging) return
    panX += e.clientX - lastX
    panY += e.clientY - lastY
    lastX = e.clientX
    lastY = e.clientY
    var el = viewport.querySelector(".diagram-zoom-content")
    if (el) {
      el.style.transition = "none"
      setTransform()
    }
  })
  document.addEventListener("mouseup", function () {
    dragging = false
    viewport.style.cursor = ""
    var el = viewport.querySelector(".diagram-zoom-content")
    if (el) el.style.transition = "transform 0.15s ease"
  })

  /* ---- Attach to diagrams (with retry for mermaid rendering) ---- */
  var retryCount = 0
  var MAX_RETRIES = 30 /* retry up to ~15 seconds */

  function attachZoom() {
    var unboundMermaid = 0

    /* Mermaid diagrams — only bind once SVG is rendered */
    document.querySelectorAll(".mermaid:not([data-zoom-bound])").forEach(function (el) {
      if (!hasRenderedSvg(el)) {
        unboundMermaid++
        return /* skip — mermaid hasn't rendered this one yet */
      }
      el.setAttribute("data-zoom-bound", "true")
      el.classList.add("diagram-zoomable")
      el.addEventListener("click", function (e) {
        e.stopPropagation()
        openModal(el)
      })
    })

    /* If there are still unrendered mermaid elements, retry */
    if (unboundMermaid > 0 && retryCount < MAX_RETRIES) {
      retryCount++
      setTimeout(attachZoom, 500)
    }

    /* Architecture preview cards (with <img> inside) */
    document.querySelectorAll(".diagram-preview:not([data-zoom-bound])").forEach(function (el) {
      el.setAttribute("data-zoom-bound", "true")
      el.addEventListener("click", function (e) {
        e.stopPropagation()
        openModal(el)
      })
    })

    /* Any explicit .diagram-zoomable-img wrapper */
    document.querySelectorAll(".diagram-zoomable-img:not([data-zoom-bound])").forEach(function (el) {
      el.setAttribute("data-zoom-bound", "true")
      el.classList.add("diagram-zoomable")
      el.addEventListener("click", function (e) {
        e.stopPropagation()
        openModal(el)
      })
    })
  }

  /* Run after page load — use a longer initial delay for mermaid to render */
  function scheduleAttach() {
    retryCount = 0
    setTimeout(attachZoom, 1200)
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", scheduleAttach)
  } else {
    scheduleAttach()
  }

  /* MkDocs Material instant navigation support */
  document.addEventListener("DOMContentSwitch", function () {
    retryCount = 0
    setTimeout(attachZoom, 1200)
  })
  /* Also works with newer material versions */
  if (typeof document$ !== "undefined") {
    document$.subscribe(function () {
      retryCount = 0
      setTimeout(attachZoom, 1200)
    })
  }
})()
