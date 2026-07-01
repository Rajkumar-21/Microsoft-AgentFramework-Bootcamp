#!/usr/bin/env python3
"""Convert .drawio (mxGraph XML) files to SVG.

Parses mxCell elements, resolves parent–child geometry offsets,
renders shapes as SVG <rect> + <text>, and draws edges between
connected cells.
"""
import xml.etree.ElementTree as ET
import os, re, html

DIAGRAMS_DIR = os.path.join(os.path.dirname(__file__), "..", "docs", "architecture", "diagrams")

# ── helpers ──────────────────────────────────────────────────────────

def parse_style(raw: str) -> dict:
    """Parse 'key=value;key2=value2;...' into a dict."""
    d = {}
    if not raw:
        return d
    for part in raw.split(";"):
        if "=" in part:
            k, v = part.split("=", 1)
            d[k.strip()] = v.strip()
        elif part.strip():
            d[part.strip()] = True
    return d


def lighten(hex_color: str, factor: float = 0.15) -> str:
    """Return a slightly lighter version of a hex colour."""
    hc = hex_color.lstrip("#")
    if len(hc) != 6:
        return hex_color
    r, g, b = int(hc[0:2], 16), int(hc[2:4], 16), int(hc[4:6], 16)
    r = min(255, int(r + (255 - r) * factor))
    g = min(255, int(g + (255 - g) * factor))
    b = min(255, int(b + (255 - b) * factor))
    return f"#{r:02x}{g:02x}{b:02x}"


def escape(text: str) -> str:
    return html.escape(text).replace("&#xa;", "\n").replace("&amp;", "&amp;")


# ── converter ────────────────────────────────────────────────────────

class DrawioToSvg:
    def __init__(self, path: str):
        self.tree = ET.parse(path)
        self.root_model = self.tree.getroot()
        self.cells: dict[str, ET.Element] = {}
        self.vertices: dict[str, dict] = {}
        self.edges: list[dict] = []
        self._parse()

    # ── parse ────────────────────────────────────────────────────────

    def _parse(self):
        for cell in self.root_model.iter("mxCell"):
            cid = cell.get("id", "")
            self.cells[cid] = cell

        # first pass — vertices
        for cid, cell in self.cells.items():
            if cell.get("vertex") != "1":
                continue
            geo = cell.find("mxGeometry")
            if geo is None:
                continue
            x = float(geo.get("x", 0))
            y = float(geo.get("y", 0))
            w = float(geo.get("width", 0))
            h = float(geo.get("height", 0))
            style = parse_style(cell.get("style", ""))
            value = cell.get("value", "") or ""
            parent = cell.get("parent", "1")
            self.vertices[cid] = dict(
                x=x, y=y, w=w, h=h,
                style=style, value=value,
                parent=parent, id=cid,
            )

        # resolve absolute positions (parent offsets)
        for v in self.vertices.values():
            self._resolve_abs(v)

        # second pass — edges
        for cell in self.cells.values():
            if cell.get("edge") != "1":
                continue
            src = cell.get("source", "")
            tgt = cell.get("target", "")
            style = parse_style(cell.get("style", ""))
            value = cell.get("value", "") or ""
            parent = cell.get("parent", "1")
            self.edges.append(dict(source=src, target=tgt, style=style, value=value, parent=parent))

    def _resolve_abs(self, v: dict):
        """Compute absolute (x,y) by walking parent chain."""
        pid = v["parent"]
        if pid in ("0", "1"):
            v["abs_x"] = v["x"]
            v["abs_y"] = v["y"]
        elif pid in self.vertices:
            pv = self.vertices[pid]
            if "abs_x" not in pv:
                self._resolve_abs(pv)
            v["abs_x"] = pv["abs_x"] + v["x"]
            v["abs_y"] = pv["abs_y"] + v["y"]
        else:
            v["abs_x"] = v["x"]
            v["abs_y"] = v["y"]

    # ── render SVG ───────────────────────────────────────────────────

    def render(self) -> str:
        # compute bounding box
        min_x = min_y = float("inf")
        max_x = max_y = float("-inf")
        for v in self.vertices.values():
            min_x = min(min_x, v["abs_x"])
            min_y = min(min_y, v["abs_y"])
            max_x = max(max_x, v["abs_x"] + v["w"])
            max_y = max(max_y, v["abs_y"] + v["h"])

        pad = 30
        vb_x = min_x - pad
        vb_y = min_y - pad
        vb_w = (max_x - min_x) + 2 * pad
        vb_h = (max_y - min_y) + 2 * pad

        parts = []
        parts.append(
            f'<svg xmlns="http://www.w3.org/2000/svg" '
            f'viewBox="{vb_x:.0f} {vb_y:.0f} {vb_w:.0f} {vb_h:.0f}" '
            f'width="100%" height="100%" '
            f'style="font-family:Segoe UI,Inter,system-ui,sans-serif;background:#fff">'
        )
        parts.append("<defs>")
        parts.append(
            '<marker id="arrowhead" markerWidth="8" markerHeight="6" '
            'refX="8" refY="3" orient="auto"><polygon points="0 0, 8 3, 0 6" fill="#666"/></marker>'
        )
        parts.append("</defs>")

        # draw swimlanes first (they are parents)
        swimlanes = [v for v in self.vertices.values() if v["style"].get("swimlane")]
        others = [v for v in self.vertices.values() if not v["style"].get("swimlane")]

        for v in swimlanes:
            parts.append(self._render_swimlane(v))
        for v in others:
            parts.append(self._render_vertex(v))
        for e in self.edges:
            parts.append(self._render_edge(e))

        parts.append("</svg>")
        return "\n".join(parts)

    def _render_swimlane(self, v: dict) -> str:
        x, y, w, h = v["abs_x"], v["abs_y"], v["w"], v["h"]
        s = v["style"]
        fill = s.get("fillColor", "#f5f5f5")
        stroke = s.get("strokeColor", "#666")
        sw = s.get("strokeWidth", "2")
        start_size = int(s.get("startSize", 28))
        r = 8 if s.get("rounded") else 0
        value = v["value"]
        font_size = s.get("fontSize", "12")
        font_color = s.get("fontColor", "#333")

        svg = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" '
        svg += f'fill="{lighten(fill, 0.3)}" stroke="{stroke}" stroke-width="{sw}" />\n'
        # header bar
        svg += f'<rect x="{x}" y="{y}" width="{w}" height="{start_size}" rx="{r}" '
        svg += f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}" />\n'
        # title
        if value:
            clean = value.replace("&#xa;", " ").replace("\n", " ")
            svg += (
                f'<text x="{x + w / 2}" y="{y + start_size / 2 + 1}" '
                f'text-anchor="middle" dominant-baseline="central" '
                f'font-size="{font_size}" font-weight="bold" fill="{font_color}">'
                f'{escape(clean)}</text>\n'
            )
        return svg

    def _render_vertex(self, v: dict) -> str:
        x, y, w, h = v["abs_x"], v["abs_y"], v["w"], v["h"]
        s = v["style"]

        # skip pure "0" root cells
        if v["id"] in ("0", "1"):
            return ""

        # text-only cells
        if s.get("text") is True or (s.get("shape") is None and s.get("fillColor") == "none"):
            return self._render_text_cell(v)

        # image cells (Azure icons) — render as a simple labelled box
        if s.get("image") or s.get("shape") == "image":
            return ""  # skip icon images, we show their labels

        # actor shape
        if s.get("shape") == "actor":
            return self._render_actor(v)

        # ellipse (numbered badge)
        if s.get("ellipse") is True:
            return self._render_ellipse(v)

        fill = s.get("fillColor", "#fff")
        stroke = s.get("strokeColor", "#999")
        sw = s.get("strokeWidth", "1")
        r = 6 if s.get("rounded") else 0
        font_size = s.get("fontSize", "11")
        font_color = s.get("fontColor", "#333")
        font_weight = "bold" if s.get("fontStyle") in ("1", "3", 1, 3) else "normal"
        value = v["value"]

        if not value and fill == "none" and stroke == "none":
            return ""

        svg = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" '
        svg += f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}" />\n'

        if value:
            lines = value.replace("&#xa;", "\n").replace("&amp;", "&").split("\n")
            lines = [l.strip() for l in lines if l.strip()]
            total_h = len(lines) * (int(font_size) + 4)
            start_y = y + (h - total_h) / 2 + int(font_size)
            for i, line in enumerate(lines):
                ly = start_y + i * (int(font_size) + 4)
                svg += (
                    f'<text x="{x + w / 2}" y="{ly}" '
                    f'text-anchor="middle" dominant-baseline="central" '
                    f'font-size="{font_size}" font-weight="{font_weight}" fill="{font_color}">'
                    f'{html.escape(line)}</text>\n'
                )
        return svg

    def _render_text_cell(self, v: dict) -> str:
        x, y, w, h = v["abs_x"], v["abs_y"], v["w"], v["h"]
        s = v["style"]
        font_size = s.get("fontSize", "11")
        font_color = s.get("fontColor", "#333")
        font_weight = "bold" if s.get("fontStyle") in ("1", "3", 1, 3) else "normal"
        font_style_css = "italic" if s.get("fontStyle") in ("2", 2) else "normal"
        value = v["value"]
        if not value:
            return ""
        align = s.get("align", "center")
        anchor = {"left": "start", "right": "end"}.get(align, "middle")
        tx = {"start": x, "end": x + w}.get(anchor, x + w / 2)
        lines = value.replace("&#xa;", "\n").replace("&amp;", "&").split("\n")
        lines = [l.strip() for l in lines if l.strip()]
        svg = ""
        for i, line in enumerate(lines):
            ly = y + h / 2 + i * (int(font_size) + 2)
            svg += (
                f'<text x="{tx}" y="{ly}" '
                f'text-anchor="{anchor}" dominant-baseline="central" '
                f'font-size="{font_size}" font-weight="{font_weight}" '
                f'font-style="{font_style_css}" fill="{font_color}">'
                f'{html.escape(line)}</text>\n'
            )
        return svg

    def _render_ellipse(self, v: dict) -> str:
        x, y, w, h = v["abs_x"], v["abs_y"], v["w"], v["h"]
        s = v["style"]
        fill = s.get("fillColor", "#6B4FBB")
        stroke = s.get("strokeColor", "none")
        font_color = s.get("fontColor", "#fff")
        cx, cy = x + w / 2, y + h / 2
        svg = f'<ellipse cx="{cx}" cy="{cy}" rx="{w / 2}" ry="{h / 2}" fill="{fill}" stroke="{stroke}" />\n'
        if v["value"]:
            svg += (
                f'<text x="{cx}" y="{cy}" text-anchor="middle" dominant-baseline="central" '
                f'font-size="12" font-weight="bold" fill="{font_color}">{html.escape(v["value"])}</text>\n'
            )
        return svg

    def _render_actor(self, v: dict) -> str:
        x, y, w, h = v["abs_x"], v["abs_y"], v["w"], v["h"]
        s = v["style"]
        fill = s.get("fillColor", "#dae8fc")
        stroke = s.get("strokeColor", "#6c8ebf")
        cx, cy = x + w / 2, y + h * 0.35
        # simple circle head
        svg = f'<circle cx="{cx}" cy="{cy}" r="{min(w, h) * 0.2}" fill="{fill}" stroke="{stroke}" stroke-width="2" />\n'
        if v["value"]:
            svg += (
                f'<text x="{cx}" y="{y + h + 14}" text-anchor="middle" '
                f'font-size="12" font-weight="bold" fill="#333">{html.escape(v["value"])}</text>\n'
            )
        return svg

    def _render_edge(self, e: dict) -> str:
        src_id = e["source"]
        tgt_id = e["target"]
        src = self.vertices.get(src_id)
        tgt = self.vertices.get(tgt_id)
        if not src or not tgt:
            return ""
        sx = src["abs_x"] + src["w"] / 2
        sy = src["abs_y"] + src["h"] / 2
        tx = tgt["abs_x"] + tgt["w"] / 2
        ty = tgt["abs_y"] + tgt["h"] / 2

        # clip to edge of source/target rect
        sx2, sy2 = self._clip_to_rect(sx, sy, tx, ty, src)
        tx2, ty2 = self._clip_to_rect(tx, ty, sx, sy, tgt)

        s = e["style"]
        color = s.get("strokeColor", "#666")
        sw = s.get("strokeWidth", "2")
        dashed = 'stroke-dasharray="6,4"' if s.get("dashed") in ("1", True) else ""

        svg = (
            f'<line x1="{sx2}" y1="{sy2}" x2="{tx2}" y2="{ty2}" '
            f'stroke="{color}" stroke-width="{sw}" {dashed} '
            f'marker-end="url(#arrowhead)" />\n'
        )

        # label
        label = e["value"]
        if label:
            mx, my = (sx2 + tx2) / 2, (sy2 + ty2) / 2 - 6
            font_color = s.get("fontColor", color)
            svg += (
                f'<text x="{mx}" y="{my}" text-anchor="middle" '
                f'font-size="9" fill="{font_color}">{html.escape(label)}</text>\n'
            )
        return svg

    @staticmethod
    def _clip_to_rect(fx, fy, tx, ty, v):
        """Clip point (fx,fy) to the nearest edge of v's rectangle towards (tx,ty)."""
        cx, cy = v["abs_x"] + v["w"] / 2, v["abs_y"] + v["h"] / 2
        dx, dy = tx - cx, ty - cy
        if dx == 0 and dy == 0:
            return fx, fy
        hw, hh = v["w"] / 2, v["h"] / 2
        # scale
        if abs(dx) * hh > abs(dy) * hw:
            # exits left or right
            s = hw / abs(dx) if dx != 0 else 1
        else:
            s = hh / abs(dy) if dy != 0 else 1
        return cx + dx * s, cy + dy * s


# ── main ─────────────────────────────────────────────────────────────

def main():
    diagrams_dir = os.path.abspath(DIAGRAMS_DIR)
    for fname in sorted(os.listdir(diagrams_dir)):
        if not fname.endswith(".drawio"):
            continue
        src = os.path.join(diagrams_dir, fname)
        dst = os.path.join(diagrams_dir, fname.replace(".drawio", ".svg"))
        print(f"Converting {fname} → {os.path.basename(dst)}")
        converter = DrawioToSvg(src)
        svg_content = converter.render()
        with open(dst, "w", encoding="utf-8") as f:
            f.write(svg_content)
    print("Done!")


if __name__ == "__main__":
    main()
