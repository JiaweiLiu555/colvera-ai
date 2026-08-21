"""Inline, synthetic imaging-style visualizations for the Colvera demo.

They are intentionally abstract SVG illustrations, not clinical images and not
model overlays.  Keeping them as generated markup avoids unknown image rights
and makes the demo self-contained.
"""

from __future__ import annotations

from html import escape

from .patient import DemoVisit


def exam_visual(visit: DemoVisit, modality: str, show_overlay: bool = True) -> str:
    """Return a self-contained synthetic MRI or endoscopy visualization."""
    current = visit.role == "Current"
    label = "MRI · T2 / DWI" if modality == "MRI" else "Endoscopy · white light"
    accent = "#9B7CFF" if current and show_overlay else "#32C7D9"
    annotation = escape(visit.mri_annotation if modality == "MRI" else visit.endoscopy_annotation)
    if modality == "MRI":
        anatomy = """
          <ellipse cx='300' cy='193' rx='175' ry='127' fill='url(#body)' opacity='.86'/>
          <ellipse cx='300' cy='193' rx='108' ry='83' fill='none' stroke='#90A2AA' stroke-width='2' opacity='.35'/>
          <ellipse cx='300' cy='193' rx='58' ry='42' fill='#263F4B' opacity='.9'/>
          <path d='M228 190 C249 154 282 145 304 163 C322 177 343 176 368 150' fill='none' stroke='#C4D3D8' stroke-width='8' opacity='.24'/>
          <path d='M231 220 C266 248 327 253 373 218' fill='none' stroke='#63828D' stroke-width='13' opacity='.25'/>
        """
        region = "<ellipse cx='333' cy='174' rx='20' ry='14' fill='#9B7CFF' fill-opacity='.44' stroke='#D8CEFF' stroke-width='2'/>" if current and show_overlay else ""
    else:
        anatomy = """
          <circle cx='300' cy='189' r='141' fill='url(#endo)'/>
          <path d='M161 170 C194 92 294 86 383 124 C431 145 444 218 393 274 C317 332 216 304 177 250 C160 228 150 196 161 170Z' fill='#9E5849' opacity='.42'/>
          <path d='M188 251 C222 211 245 253 283 228 C319 202 337 242 385 220' fill='none' stroke='#F3B28C' stroke-width='8' opacity='.45'/>
          <path d='M190 142 C231 169 250 137 292 157 C330 176 351 143 403 169' fill='none' stroke='#F4C2A0' stroke-width='7' opacity='.28'/>
        """
        region = "<ellipse cx='352' cy='178' rx='23' ry='17' fill='#A98CFF' fill-opacity='.43' stroke='#E0D5FF' stroke-width='2'/>" if current and show_overlay else ""
    overlay = "Change overlay shown" if show_overlay and current else "Reference view"
    markup = f"""
    <div class='exam-visual' aria-label='Synthetic {escape(modality)} visualization for {escape(visit.short_date)}'>
      <svg viewBox='0 0 600 330' role='img' xmlns='http://www.w3.org/2000/svg'>
        <defs>
          <linearGradient id='scene' x1='0' y1='0' x2='1' y2='1'><stop stop-color='#182554'/><stop offset='1' stop-color='#0A102D'/></linearGradient>
          <radialGradient id='body'><stop stop-color='#A9BBC0'/><stop offset='.55' stop-color='#59717B'/><stop offset='1' stop-color='#23343B'/></radialGradient>
          <radialGradient id='endo'><stop stop-color='#E5A379'/><stop offset='.55' stop-color='#A75847'/><stop offset='1' stop-color='#572A31'/></radialGradient>
          <filter id='blur'><feGaussianBlur stdDeviation='10'/></filter>
        </defs>
        <rect width='600' height='330' rx='18' fill='url(#scene)'/>
        <circle cx='300' cy='192' r='150' fill='{accent}' opacity='.10' filter='url(#blur)'/>
        {anatomy}
        {region}
        <rect x='20' y='18' width='130' height='28' rx='14' fill='#FFFFFF' fill-opacity='.10'/>
        <text x='34' y='37' fill='#EAF0F1' font-size='13' font-family='Arial, sans-serif'>{label}</text>
        <rect x='393' y='274' width='187' height='34' rx='8' fill='#0D171B' fill-opacity='.84' stroke='#FFFFFF' stroke-opacity='.13'/>
        <text x='406' y='296' fill='#DDE7E8' font-size='12' font-family='Arial, sans-serif'>{annotation}</text>
      </svg>
      <div class='exam-visual-caption'><span>{escape(visit.short_date)}</span><span>{overlay}</span></div>
    </div>
    """
    # Streamlit's Markdown parser treats a blank line inside an HTML SVG block
    # as a code fence.  Keep the generated illustration in one HTML block.
    return "".join(line.strip() for line in markup.splitlines())


def trend_chart(title: str, labels: tuple[str, ...], values: tuple[float, ...], color: str, unit: str) -> str:
    """Return a compact, presentation-ready SVG trend chart without a data backend."""
    width, height = 560, 238
    left, right, top, bottom = 43, 20, 31, 44
    chart_width, chart_height = width - left - right, height - top - bottom
    floor, ceiling = min(0.0, min(values) * 0.78), max(values) * 1.16
    span = ceiling - floor or 1
    points = []
    for index, value in enumerate(values):
        x = left + chart_width * index / max(len(values) - 1, 1)
        y = top + (ceiling - value) / span * chart_height
        points.append((x, y))
    point_string = " ".join(f"{x:.1f},{y:.1f}" for x, y in points)
    grid = "".join(
        f"<line x1='{left}' x2='{width-right}' y1='{top + chart_height * row / 3:.1f}' y2='{top + chart_height * row / 3:.1f}' stroke='#E3EAF4' stroke-width='1'/>"
        for row in range(4)
    )
    markers = "".join(f"<circle cx='{x:.1f}' cy='{y:.1f}' r='5.3' fill='{color}' stroke='white' stroke-width='3'/>" for x, y in points)
    x_labels = "".join(
        f"<text x='{x:.1f}' y='{height-16}' text-anchor='middle' fill='#687895' font-size='11' font-family='Arial, sans-serif'>{label}</text>"
        for (x, _), label in zip(points, labels)
    )
    first_value, last_value = values[0], values[-1]
    return f"""
    <div class='trend-panel'>
      <div class='trend-title'><span>{title}</span><strong>{first_value:g} → {last_value:g} {unit}</strong></div>
      <svg class='trend-svg' viewBox='0 0 {width} {height}' role='img' aria-label='{title} synthetic demonstration trend'>
        {grid}
        <polyline points='{point_string}' fill='none' stroke='{color}' stroke-width='3.2' stroke-linecap='round' stroke-linejoin='round'/>
        {markers}{x_labels}
      </svg>
    </div>
    """
