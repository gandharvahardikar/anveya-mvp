"""Build the Startup Buildathon India 2026 submission deck directly on the official template."""

from __future__ import annotations

import json
from pathlib import Path
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.util import Inches, Pt

TEMPLATE = Path(
    r"C:\Users\Asus\.gemini\antigravity\brain\b1cf372c-7679-404e-b29e-16a7b706dfd3\.user_uploaded\media_1795208613523_dd2f9c20.pptx"
)
ASSETS = Path(r"d:\Work\anveya-mvp\submission\assets")
OUT_PPTX = Path(r"d:\Work\anveya-mvp\submission\Anveya_Labs_Startup_Buildathon_2026.pptx")

# Palette (Anveya Labs crisp light editorial + Startup Buildathon harmony)
C_INK = RGBColor(0x11, 0x11, 0x11)
C_MUTED = RGBColor(0x4B, 0x55, 0x63)
C_WHITE = RGBColor(0xFF, 0xFF, 0xFF)
C_PANEL = RGBColor(0xFA, 0xFA, 0xFA)
C_SUNKEN = RGBColor(0xF3, 0xF4, 0xF6)
C_LINE = RGBColor(0xE5, 0xE7, 0xEB)
C_ORANGE = RGBColor(0xF5, 0x82, 0x20)
C_ORANGE_DK = RGBColor(0xC2, 0x56, 0x08)
C_ORANGE_BG = RGBColor(0xFF, 0xF7, 0xED)
C_GREEN = RGBColor(0x1F, 0x7A, 0x63)
C_GREEN_BG = RGBColor(0xF0, 0xFD, 0xF4)
C_RED = RGBColor(0xB4, 0x40, 0x1C)
C_RED_BG = RGBColor(0xFE, 0xF2, 0xF2)
C_BLUE = RGBColor(0x1A, 0x73, 0xE8)
C_BLUE_BG = RGBColor(0xEF, 0xF6, 0xFF)

FONT_HEAD = "Segoe UI"
FONT_BODY = "Segoe UI"
FONT_MONO = "Consolas"


def delete_slide(prs: Presentation, index: int) -> None:
    """Remove slide at 0-based index cleanly."""
    sld_id_lst = prs.slides._sldIdLst
    sld_id = list(sld_id_lst)[index]
    r_id = sld_id.rId
    prs.part.drop_rel(r_id)
    sld_id_lst.remove(sld_id)


def remove_non_header_textboxes(slide) -> None:
    """Remove template placeholder textboxes (keeping top banner image)."""
    to_remove = [s for s in slide.shapes if s.has_text_frame]
    for s in to_remove:
        sp = s._element
        sp.getparent().remove(sp)


def add_header_title(slide, eyebrow: str, title: str, right_badge: str = "") -> None:
    """Add crisp Anveya Labs eyebrow + bold title + subtle divider right under official top banner."""
    # Eyebrow
    tb_e = slide.shapes.add_textbox(Inches(0.35), Inches(0.76), Inches(6.5), Inches(0.20))
    tf_e = tb_e.text_frame
    tf_e.word_wrap = True
    tf_e.margin_left = tf_e.margin_top = tf_e.margin_right = tf_e.margin_bottom = 0
    p_e = tf_e.paragraphs[0]
    r_e = p_e.add_run()
    r_e.text = eyebrow
    r_e.font.name = FONT_MONO
    r_e.font.size = Pt(8.5)
    r_e.font.bold = True
    r_e.font.color.rgb = C_ORANGE_DK

    # Title (single-line crisp editorial heading)
    tb_t = slide.shapes.add_textbox(Inches(0.35), Inches(0.96), Inches(7.10), Inches(0.34))
    tf_t = tb_t.text_frame
    tf_t.word_wrap = False
    tf_t.margin_left = tf_t.margin_top = tf_t.margin_right = tf_t.margin_bottom = 0
    p_t = tf_t.paragraphs[0]
    r_t = p_t.add_run()
    r_t.text = title
    r_t.font.name = FONT_HEAD
    r_t.font.size = Pt(16.0)
    r_t.font.bold = True
    r_t.font.color.rgb = C_INK

    if right_badge:
        pill = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.55), Inches(0.86), Inches(2.10), Inches(0.32)
        )
        pill.adjustments[0] = 0.5
        pill.shadow.inherit = False
        pill.fill.solid()
        pill.fill.fore_color.rgb = C_ORANGE_BG
        pill.line.color.rgb = C_ORANGE
        pill.line.width = Pt(1)
        tf_p = pill.text_frame
        tf_p.vertical_anchor = MSO_ANCHOR.MIDDLE
        tf_p.margin_left = tf_p.margin_right = Inches(0.08)
        tf_p.margin_top = tf_p.margin_bottom = 0
        pp = tf_p.paragraphs[0]
        pp.alignment = PP_ALIGN.CENTER
        rp = pp.add_run()
        rp.text = right_badge
        rp.font.name = FONT_MONO
        rp.font.size = Pt(8.0)
        rp.font.bold = True
        rp.font.color.rgb = C_ORANGE_DK

    # Hairline divider
    line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.35), Inches(1.33), Inches(9.30), Inches(0.015))
    line.shadow.inherit = False
    line.fill.solid()
    line.fill.fore_color.rgb = C_LINE
    line.line.fill.background()


def add_card(
    slide,
    x: float,
    y: float,
    w: float,
    h: float,
    *,
    fill: RGBColor = C_PANEL,
    border: RGBColor = C_LINE,
    border_pt: float = 1.0,
    radius: float = 0.08,
):
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    shape.adjustments[0] = radius
    shape.shadow.inherit = False
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill
    shape.line.color.rgb = border
    shape.line.width = Pt(border_pt)
    return shape


def add_textbox(
    slide,
    x: float,
    y: float,
    w: float,
    h: float,
    text: str = "",
    *,
    font: str = FONT_BODY,
    size: float = 10.5,
    bold: bool = False,
    color: RGBColor = C_INK,
    align=PP_ALIGN.LEFT,
    line_spacing: float = 1.18,
):
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    if text:
        for i, line in enumerate(text.split("\n")):
            p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            p.alignment = align
            p.line_spacing = line_spacing
            r = p.add_run()
            r.text = line
            r.font.name = font
            r.font.size = Pt(size)
            r.font.bold = bold
            r.font.color.rgb = color
    return tb


def add_kpi_tile(
    slide,
    x: float,
    y: float,
    w: float,
    h: float,
    number: str,
    label: str,
    sub: str = "",
    *,
    accent: RGBColor = C_ORANGE_DK,
    bg: RGBColor = C_PANEL,
    border: RGBColor = C_LINE,
):
    add_card(slide, x, y, w, h, fill=bg, border=border, border_pt=1.0, radius=0.10)
    add_textbox(slide, x + 0.14, y + 0.10, w - 0.28, 0.42, number, font=FONT_MONO, size=20, bold=True, color=accent)
    add_textbox(slide, x + 0.14, y + 0.52, w - 0.28, 0.24, label, font=FONT_HEAD, size=9.5, bold=True, color=C_INK)
    if sub:
        add_textbox(slide, x + 0.14, y + 0.74, w - 0.28, h - 0.80, sub, font=FONT_BODY, size=8.0, color=C_MUTED, line_spacing=1.15)


def add_bullets(slide, x: float, y: float, w: float, h: float, items: list[tuple[str, str]], size: float = 9.5):
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    for idx, (lead, body) in enumerate(items):
        p = tf.paragraphs[0] if idx == 0 else tf.add_paragraph()
        p.space_after = Pt(5)
        p.line_spacing = 1.18
        r0 = p.add_run()
        r0.text = "▪  "
        r0.font.name = FONT_BODY
        r0.font.size = Pt(size)
        r0.font.bold = True
        r0.font.color.rgb = C_ORANGE_DK
        if lead:
            r1 = p.add_run()
            r1.text = lead + " "
            r1.font.name = FONT_HEAD
            r1.font.size = Pt(size)
            r1.font.bold = True
            r1.font.color.rgb = C_INK
        r2 = p.add_run()
        r2.text = body
        r2.font.name = FONT_BODY
        r2.font.size = Pt(size)
        r2.font.color.rgb = C_MUTED


def add_footer_note(slide, text: str) -> None:
    add_textbox(
        slide, 0.35, 5.34, 9.30, 0.22, text, font=FONT_MONO, size=7.5, color=C_MUTED, align=PP_ALIGN.RIGHT
    )


def main() -> None:
    bench = json.loads((ASSETS / "benchmark_live.json").read_text(encoding="utf-8"))
    prs = Presentation(str(TEMPLATE))

    # Remove template Slide 1 (download note) and blank template Slides 14 & 15 (0-based: 14, 13, 0 in reverse order!)
    for idx in (14, 13, 0):
        delete_slide(prs, idx)

    # Now prs.slides has exactly 13 slides:
    # 0: Cover
    # 1: Brief about the idea
    # 2: Opportunities / USP
    # 3: List of features
    # 4: Process flow diagram
    # 5: Wireframes / Mock diagrams
    # 6: Architecture diagram
    # 7: Technologies used
    # 8: Estimated implementation cost
    # 9: Snapshots of the prototype
    # 10: Prototype Performance report / Benchmarking
    # 11: Additional Details / Future Development
    # 12: Thank you

    # ------------------------------------------------------------------
    # SLIDE 1 (Cover)
    # ------------------------------------------------------------------
    s1 = prs.slides[0]
    remove_non_header_textboxes(s1)

    # Left: Team & Problem details
    add_textbox(s1, 0.55, 3.22, 5.55, 0.26, "ANVEYA LABS · CONTINUOUS LLM ASSURANCE", font=FONT_MONO, size=9, bold=True, color=C_ORANGE_DK)

    tb_meta = s1.shapes.add_textbox(Inches(0.55), Inches(3.52), Inches(5.65), Inches(1.85))
    tf_m = tb_meta.text_frame
    tf_m.word_wrap = True
    tf_m.margin_left = tf_m.margin_right = tf_m.margin_top = tf_m.margin_bottom = 0
    rows_cover = [
        ("Team Name: ", "Anveya Labs (अन्वय)"),
        ("Team Size: ", "1 (Core Engineering Founder)"),
        ("Problem Statement: ", "Production LLM apps silently leak confidential instructions and tokens, fail safety guardrails, and regress on accuracy when prompts are patched blindly — with no fast, unbiased way to prove safety before shipping."),
    ]
    for i, (k, v) in enumerate(rows_cover):
        p = tf_m.paragraphs[0] if i == 0 else tf_m.add_paragraph()
        p.space_after = Pt(6)
        p.line_spacing = 1.2
        rk = p.add_run()
        rk.text = k
        rk.font.name = FONT_HEAD
        rk.font.size = Pt(11.5)
        rk.font.bold = True
        rk.font.color.rgb = C_INK
        rv = p.add_run()
        rv.text = v
        rv.font.name = FONT_BODY
        rv.font.size = Pt(11.0 if i < 2 else 10.2)
        rv.font.color.rgb = C_MUTED if i == 2 else C_INK

    # Right: Live Proof Card
    add_card(s1, 6.45, 3.22, 3.15, 2.10, fill=C_PANEL, border=C_ORANGE, border_pt=1.3, radius=0.08)
    add_textbox(s1, 6.62, 3.34, 2.85, 0.22, "LIVE DEPLOYED PROTOTYPE", font=FONT_MONO, size=8.0, bold=True, color=C_ORANGE_DK)
    add_textbox(s1, 6.62, 3.58, 2.85, 0.34, "anveya-266974009969\n.asia-south1.run.app", font=FONT_MONO, size=8.5, bold=True, color=C_BLUE)
    add_textbox(s1, 6.62, 4.02, 2.85, 1.20,
                "• 12 Live Models across 5 Labs\n• 60% of v1 models failed security\n• 70 → 100 avg security uplift (v2)\n• 4.6s fastest full evaluation\n• < $0.002 / run · Keyless IAM",
                font=FONT_BODY, size=8.8, color=C_INK, line_spacing=1.28)

    # ------------------------------------------------------------------
    # SLIDE 2 (Brief about the idea)
    # ------------------------------------------------------------------
    s2 = prs.slides[1]
    remove_non_header_textboxes(s2)
    add_header_title(s2, "01 / BRIEF ABOUT THE IDEA", "Prove your LLM app is accurate, safe & secure before shipping.", "LIVE ON CLOUD RUN")

    # Left column: Narrative + 3 steps
    add_textbox(
        s2, 0.35, 1.46, 5.15, 0.90,
        "Anveya Labs is a single-service LLM Assurance platform on Google Cloud Run & Vertex AI. "
        "It tests bots across Quality, Safety & Security, catches secret leaks in <1 ms, generates copyable prompt fixes "
        "via an independent cross-vendor judge, and proves v1 → v2 gains with zero regressions.",
        font=FONT_BODY, size=9.6, color=C_MUTED, line_spacing=1.24,
    )

    steps = [
        ("01 // PLANT", "Embed confidential canary token ANV-7F3K inside the system prompt as an unforgeable tripwire."),
        ("02 // ATTACK & JUDGE", "Run Quality, Safety & Prompt-Injection tests concurrently; check via <1 ms rules + temp=0 independent judge."),
        ("03 // FIX & PROVE", "Apply suggested prompt fixes to v2, re-run the suite, and verify exact v1 → v2 deltas & zero regressions."),
    ]
    for i, (tag, desc) in enumerate(steps):
        yy = 2.48 + i * 0.90
        add_card(s2, 0.35, yy, 5.15, 0.78, fill=C_PANEL, border=C_LINE, radius=0.10)
        add_textbox(s2, 0.50, yy + 0.08, 4.85, 0.22, tag, font=FONT_MONO, size=8.5, bold=True, color=C_ORANGE_DK)
        add_textbox(s2, 0.50, yy + 0.31, 4.85, 0.42, desc, font=FONT_BODY, size=9.0, color=C_INK, line_spacing=1.18)

    # Right column: 2x2 Headline Metrics Grid
    add_kpi_tile(s2, 5.75, 1.48, 1.88, 1.78, "60%", "v1 Models Vulnerable", "3 of 5 live models failed security on v1; Gemma 4 26B leaked ANV-7F3K.", accent=C_RED, bg=C_RED_BG, border=C_RED)
    add_kpi_tile(s2, 7.77, 1.48, 1.88, 1.78, "+30 pts", "Avg Security Uplift", "70 → 100 average Security score on v2 (+50 pts on every failing model).", accent=C_GREEN, bg=C_GREEN_BG, border=C_GREEN)
    add_kpi_tile(s2, 5.75, 3.40, 1.88, 1.78, "12", "Live Vertex Models", "5 labs: DeepSeek, OpenAI GPT-OSS, Z.ai GLM, Gemma 4, Gemini 3.1 Pro.", accent=C_BLUE, bg=C_BLUE_BG, border=C_BLUE)
    add_kpi_tile(s2, 7.77, 3.40, 1.88, 1.78, "4.6 s", "Fastest Full Run", "10 concurrent LLM calls on Cloud Run Mumbai for < $0.002 / run.", accent=C_ORANGE_DK, bg=C_ORANGE_BG, border=C_ORANGE)

    add_footer_note(s2, "Anveya Labs · Evaluate · Secure · Monitor · Measured live on Cloud Run (asia-south1)")

    # ------------------------------------------------------------------
    # SLIDE 3 (Opportunities, Differentiation & USP)
    # ------------------------------------------------------------------
    s3 = prs.slides[2]
    remove_non_header_textboxes(s3)
    add_header_title(s3, "02 / OPPORTUNITIES & USP", "Eliminating self-eval bias and silent regressions in production AI.", "144 MODEL PAIRS")

    cols = [
        (
            "HOW IS IT DIFFERENT?",
            C_ORANGE_DK,
            C_ORANGE_BG,
            C_ORANGE,
            [
                ("Cross-vendor judging:", "Evaluate DeepSeek, OpenAI GPT-OSS, GLM, or Gemma using an independent Gemini 3.1 Pro judge (and warn on same-model bias)."),
                ("Zero-latency rules layer:", "Deterministic plain + Base64 canary scan catches secret leaks in <1 ms with 0% LLM hallucination risk."),
                ("One-click fixes:", "Not just red/green scores — every failure outputs an exact copy-ready system prompt rule."),
            ],
        ),
        (
            "HOW IT SOLVES THE PROBLEM",
            C_BLUE,
            C_BLUE_BG,
            C_BLUE,
            [
                ("Replaces manual red-teaming:", "Cuts ad-hoc prompt audits from hours to 4.6–12 seconds with 5× bounded concurrency."),
                ("Catches over-hardening:", "Our live benchmark caught DeepSeek v4.1 Flash dropping 100 → 50 on Quality in v2 while hardening Security."),
                ("Live custom adversarial cases:", "Engineers or security reviewers add new domain attacks on the fly without redeploying."),
            ],
        ),
        (
            "USP OF ANVEYA LABS",
            C_GREEN,
            C_GREEN_BG,
            C_GREEN,
            [
                ("Prove before you ship:", "Aligned v1 vs v2 Signal Strips show Fixed IDs, Regressed IDs, and engine deltas in one view."),
                ("Serverless & keyless:", "Single ~120 KB frontend + FastAPI container on Cloud Run using Vertex AI IAM — zero static API keys."),
                ("99.5% cost reduction:", "< $0.002 (~₹0.17) per run vs ₹1.5L+ manual AI security audits or costly data-leak incidents."),
            ],
        ),
    ]
    for idx, (heading, hc, bgc, bc, items) in enumerate(cols):
        cx = 0.35 + idx * 3.16
        add_card(s3, cx, 1.50, 2.98, 3.68, fill=C_PANEL, border=C_LINE, radius=0.06)
        hdr = add_card(s3, cx, 1.50, 2.98, 0.42, fill=bgc, border=bc, border_pt=1.0, radius=0.06)
        add_textbox(s3, cx + 0.12, 1.60, 2.74, 0.24, heading, font=FONT_MONO, size=8.5, bold=True, color=hc)
        add_bullets(s3, cx + 0.14, 2.06, 2.70, 3.00, items, size=9.1)

    add_footer_note(s3, "Market opportunity: Global LLM evaluation & AI security governance · Built for Indian & global AI startups")

    # ------------------------------------------------------------------
    # SLIDE 4 (List of features)
    # ------------------------------------------------------------------
    s4 = prs.slides[3]
    remove_non_header_textboxes(s4)
    add_header_title(s4, "03 / FEATURES", "End-to-end LLM assurance in one lightweight workspace.", "6 CORE CAPABILITIES")

    feats = [
        ("01 // DUAL-LAYER ASSURANCE", "Rules + Independent Judge", "Deterministic canary scan (plain, lowercase, Base64, embedded Base64 in <1 ms) combined with structured JSON LLM judging at temp=0 across Quality, Safety & Security."),
        ("02 // 12-MODEL LIVE MATRIX", "Cross-Vendor Switchers", "Pick any of 12 verified live Vertex AI models across 5 labs (DeepSeek, OpenAI GPT-OSS, Z.ai GLM, Gemma 4, Gemini 3.x) as Target or Judge with live self-bias warnings."),
        ("03 // EVIDENCE-FIRST UI", "Chat Exhibits & Copy Fixes", "Side-by-side prompt/reply chat bubbles, red <mark> highlighting on leaked tokens, layer attribution ('Caught by rules' / 'Gemini judge'), and 1-click Copy Fix."),
        ("04 // REGRESSION PROOF", "v1 → v2 Compare & Deltas", "Expandable aligned dual Signal Strips with per-bar 'fixed' ticks, animated engine score deltas, and explicit Fixed & Regressed case ID tracking."),
        ("05 // EXTENSIBLE SUITE", "5 Defaults + 7 Presets + Custom", "Starts fast with 5 high-signal tests (~5s), offers 1-click presets (Base64 leak, DevMode jailbreak, customer PII), and live custom test creation via UI or REST API."),
        ("06 // STAGE & ACCESSIBILITY", "Dual Theme + Keyboard Nav", "Matches Anveya Labs light editorial UI + instant Dark Stage Presenter Mode (P key), keyboard shortcuts (R/C/1/2/←/→), reduced-motion support, and 390px mobile responsiveness."),
    ]
    for i, (num, title, desc) in enumerate(feats):
        col = i % 3
        row = i // 3
        fx = 0.35 + col * 3.16
        fy = 1.50 + row * 1.88
        add_card(s4, fx, fy, 2.98, 1.72, fill=C_PANEL, border=C_LINE, radius=0.07)
        add_textbox(s4, fx + 0.14, fy + 0.12, 2.70, 0.20, num, font=FONT_MONO, size=7.8, bold=True, color=C_ORANGE_DK)
        add_textbox(s4, fx + 0.14, fy + 0.34, 2.70, 0.28, title, font=FONT_HEAD, size=11.0, bold=True, color=C_INK)
        add_textbox(s4, fx + 0.14, fy + 0.66, 2.70, 0.96, desc, font=FONT_BODY, size=8.6, color=C_MUTED, line_spacing=1.22)

    add_footer_note(s4, "All 6 capabilities live today · Zero external JS frameworks · ~120 KB single-file UI")

    # ------------------------------------------------------------------
    # SLIDE 5 (Process flow diagram)
    # ------------------------------------------------------------------
    s5 = prs.slides[4]
    remove_non_header_textboxes(s5)
    add_header_title(s5, "04 / PROCESS FLOW", "Closed-loop Plant → Attack → Judge → Fix → Prove workflow.", "ASYNC · 5× CONCURRENT")
    s5.shapes.add_picture(str(ASSETS / "diag_process_flow.png"), Inches(0.35), Inches(1.42), width=Inches(9.30))
    add_card(s5, 0.35, 5.18, 9.30, 0.32, fill=C_SUNKEN, border=C_LINE, radius=0.25)
    add_textbox(
        s5, 0.48, 5.24, 9.04, 0.20,
        "Per-case error isolation guarantees 1 API failure never crashes a run · Exponential 429/503 retry backoff · Results cached in memory & browser localStorage",
        font=FONT_MONO, size=7.6, color=C_MUTED, align=PP_ALIGN.CENTER,
    )

    # ------------------------------------------------------------------
    # SLIDE 6 (Wireframes / UX & Dual-Theme Layout)
    # ------------------------------------------------------------------
    s6 = prs.slides[5]
    remove_non_header_textboxes(s6)
    add_header_title(s6, "05 / INTERFACE & WIREFRAME ZONES", "Evidence-first UI from empty state to all-held verdict.", "WCAG AA ≥ 4.5:1")

    # Left visual: Empty / Ready State (settled reduced-motion capture)
    add_card(s6, 0.35, 1.46, 4.52, 2.95, fill=C_WHITE, border=C_LINE, radius=0.05)
    s6.shapes.add_picture(str(ASSETS / "card_empty_clean.png"), Inches(0.48), Inches(1.52), height=Inches(2.60))
    add_textbox(s6, 0.42, 4.18, 4.38, 0.20, "Ready State · Canary Planted + Model Pickers + Dashed Signal Slots", font=FONT_MONO, size=7.5, bold=True, color=C_MUTED, align=PP_ALIGN.CENTER)

    # Right visual: All-Held Green State
    add_card(s6, 5.12, 1.46, 4.52, 2.95, fill=C_WHITE, border=C_GREEN, radius=0.05)
    s6.shapes.add_picture(str(ASSETS / "card_pass_clean.png"), Inches(5.26), Inches(1.52), height=Inches(2.60))
    add_textbox(s6, 5.18, 4.18, 4.40, 0.20, "Hardened v2 Verdict · Canary Silent + All Bars Held + Success Banner", font=FONT_MONO, size=7.5, bold=True, color=C_GREEN, align=PP_ALIGN.CENTER)

    # Bottom 4 UX zone callouts
    zones = [
        ("ZONE 01 · HEADER", "12-model Target & Judge chips + Presenter mode (P)"),
        ("ZONE 02 · VERDICT", "Plain-English verdict, Canary Ring & SVG Seismograph"),
        ("ZONE 03 · STRIP", "Quality / Safety / Security bars + Compare v1 → v2"),
        ("ZONE 04 · LEDGER", "Chat-bubble exhibits, copyable fixes & 0-100 scores"),
    ]
    for i, (z_t, z_b) in enumerate(zones):
        zx = 0.35 + i * 2.36
        add_card(s6, zx, 4.54, 2.22, 0.76, fill=C_PANEL, border=C_LINE, radius=0.10)
        add_textbox(s6, zx + 0.10, 4.61, 2.02, 0.18, z_t, font=FONT_MONO, size=7.2, bold=True, color=C_ORANGE_DK)
        add_textbox(s6, zx + 0.10, 4.81, 2.02, 0.44, z_b, font=FONT_BODY, size=7.8, color=C_INK, line_spacing=1.15)

    # ------------------------------------------------------------------
    # SLIDE 7 (Architecture diagram)
    # ------------------------------------------------------------------
    s7 = prs.slides[6]
    remove_non_header_textboxes(s7)
    add_header_title(s7, "06 / ARCHITECTURE", "Keyless serverless stack on Cloud Run and Vertex AI.", "MUMBAI · asia-south1")
    s7.shapes.add_picture(str(ASSETS / "diag_architecture.png"), Inches(0.35), Inches(1.42), width=Inches(9.30))
    add_card(s7, 0.35, 5.18, 9.30, 0.32, fill=C_BLUE_BG, border=C_BLUE, radius=0.25)
    add_textbox(
        s7, 0.48, 5.24, 9.04, 0.20,
        "Zero static credentials in production · Deployed from source via Cloud Build + Artifact Registry · Automatic HTTPS + Scale-to-Zero",
        font=FONT_MONO, size=7.6, color=C_BLUE, align=PP_ALIGN.CENTER,
    )

    # ------------------------------------------------------------------
    # SLIDE 8 (Technologies used)
    # ------------------------------------------------------------------
    s8 = prs.slides[7]
    remove_non_header_textboxes(s8)
    add_header_title(s8, "07 / TECHNOLOGY STACK", "Production Google Cloud AI stack with zero bloat.", "SINGLE SERVICE")

    stack = [
        ("GOOGLE CLOUD & AI", C_BLUE, C_BLUE_BG, [
            ("Vertex AI (global):", "Unified routing to 8 Gemini 3.x models & 4 Model Garden MaaS models."),
            ("google-genai SDK v3.6:", "Native typed Pydantic JSON Schema judging at temperature=0."),
            ("Model Garden MaaS:", "OpenAI-compatible REST for DeepSeek, GPT-OSS 120B, GLM 5.2, Gemma 4."),
        ]),
        ("BACKEND ENGINE", C_ORANGE_DK, C_ORANGE_BG, [
            ("Python 3.12 + FastAPI:", "Async REST endpoints (/api/run, /api/compare, /api/cases, /api/config)."),
            ("Asyncio Concurrency:", "Bounded Semaphore(5) + to_thread runs 10 LLM calls in 4.6s."),
            ("Deterministic Rules:", "Plain, case-insensitive, Base64 & embedded-Base64 canary scanner."),
        ]),
        ("FRONTEND & MOTION", C_INK, C_SUNKEN, [
            ("Vanilla HTML/CSS/JS:", "Zero React/npm build step; single ~120 KB file served by FastAPI."),
            ("SVG & rAF Engine:", "Single requestAnimationFrame loop driving seismograph & count-ups."),
            ("Accessible UX:", "WCAG AA ≥4.5:1, keyboard shortcuts, reduced-motion & 390px mobile."),
        ]),
        ("CLOUD & DEVOPS", C_GREEN, C_GREEN_BG, [
            ("Cloud Run (asia-south1):", "Docker python:3.12-slim container listening on $PORT, scale-to-zero."),
            ("Keyless IAM Auth:", "Compute SA granted roles/aiplatform.user — zero secrets in container."),
            ("CI-Ready Source:", "Cloud Build + Artifact Registry + GitHub version control (.env ignored)."),
        ]),
    ]
    for i, (head, hc, bgc, items) in enumerate(stack):
        sx = 0.35 + i * 2.36
        add_card(s8, sx, 1.50, 2.22, 3.68, fill=C_PANEL, border=C_LINE, radius=0.06)
        add_card(s8, sx, 1.50, 2.22, 0.40, fill=bgc, border=hc, border_pt=1.0, radius=0.06)
        add_textbox(s8, sx + 0.10, 1.60, 2.02, 0.20, head, font=FONT_MONO, size=7.8, bold=True, color=hc, align=PP_ALIGN.CENTER)
        add_bullets(s8, sx + 0.10, 2.02, 2.02, 3.05, items, size=8.4)

    add_footer_note(s8, "Total runtime dependencies: fastapi, uvicorn, google-genai, google-auth, requests, python-dotenv (6 packages)")

    # ------------------------------------------------------------------
    # SLIDE 9 (Estimated implementation cost)
    # ------------------------------------------------------------------
    s9 = prs.slides[8]
    remove_non_header_textboxes(s9)
    add_header_title(s9, "08 / ESTIMATED IMPLEMENTATION COST", "Serverless economics: ₹0.17 per run, $0/month idle.", ">99% CHEAPER THAN AUDITS")

    # Top 3 bold unit economics KPIs
    add_kpi_tile(s9, 0.35, 1.48, 2.98, 1.25, "$0.002", "Cost per 5-Test Run (~₹0.17)", "~3.5K input + ~1.5K output tokens across Target & Judge on Vertex AI.", accent=C_ORANGE_DK, bg=C_ORANGE_BG, border=C_ORANGE)
    add_kpi_tile(s9, 3.51, 1.48, 2.98, 1.25, "$0 / mo", "Idle Infrastructure Cost", "Cloud Run scales cleanly to zero instances when no tests are running.", accent=C_GREEN, bg=C_GREEN_BG, border=C_GREEN)
    add_kpi_tile(s9, 6.67, 1.48, 2.98, 1.25, "~$2–$4", "1,000 CI/CD Runs / Month", "~₹170–₹340/mo vs ₹1.5L–₹5L for a single manual AI security audit.", accent=C_BLUE, bg=C_BLUE_BG, border=C_BLUE)

    # Clean cost breakdown table
    tbl_shape = s9.shapes.add_table(5, 4, Inches(0.35), Inches(2.92), Inches(9.30), Inches(2.22))
    tbl = tbl_shape.table
    tbl.columns[0].width = Inches(2.35)
    tbl.columns[1].width = Inches(3.25)
    tbl.columns[2].width = Inches(1.85)
    tbl.columns[3].width = Inches(1.85)

    headers_cost = ["Component", "Usage Assumption (Monthly)", "MVP (100 runs)", "Scale (1,000 runs)"]
    rows_cost = [
        ["Vertex AI Target + Judge Tokens", "5 tests × 2 calls/test (~5K total tokens/run)", "$0.15 – $0.40", "$1.50 – $4.00"],
        ["Cloud Run (asia-south1, 512 MiB)", "Scale-to-zero; ~6s active CPU per run", "$0.00 (Free Tier)", "$0.00 – $0.50"],
        ["Cloud Build & Artifact Registry", "Container image (< 180 MB) + occasional builds", "$0.00 (Free Tier)", "< $0.20"],
        ["Total Estimated Monthly Cost", "100% serverless · Zero GPU or license fees", "< $0.50 (₹42)", "$1.70 – $4.70 (₹145–₹400)"],
    ]
    for c_i, h_txt in enumerate(headers_cost):
        cell = tbl.cell(0, c_i)
        cell.fill.solid()
        cell.fill.fore_color.rgb = C_INK
        cell.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = cell.text_frame.paragraphs[0]
        r = p.add_run()
        r.text = h_txt
        r.font.name = FONT_MONO
        r.font.size = Pt(8.5)
        r.font.bold = True
        r.font.color.rgb = C_WHITE

    for r_i, r_vals in enumerate(rows_cost, 1):
        is_total = r_i == len(rows_cost)
        for c_i, val in enumerate(r_vals):
            cell = tbl.cell(r_i, c_i)
            cell.fill.solid()
            cell.fill.fore_color.rgb = C_ORANGE_BG if is_total else (C_WHITE if r_i % 2 == 1 else C_PANEL)
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            p = cell.text_frame.paragraphs[0]
            r = p.add_run()
            r.text = val
            r.font.name = FONT_MONO if c_i >= 2 else FONT_BODY
            r.font.size = Pt(8.8)
            r.font.bold = is_total or c_i == 0
            r.font.color.rgb = C_ORANGE_DK if (is_total and c_i >= 2) else C_INK

    add_footer_note(s9, "Pricing based on Google Cloud Run asia-south1 free tier & Vertex AI pay-as-you-go token rates (USD 1 ≈ ₹85)")

    # ------------------------------------------------------------------
    # SLIDE 10 (Snapshots of the prototype)
    # ------------------------------------------------------------------
    s10 = prs.slides[9]
    remove_non_header_textboxes(s10)
    add_header_title(s10, "09 / PROTOTYPE SNAPSHOTS", "Live UI screenshots from Cloud Run (asia-south1).", "PRODUCTION UI")

    # Left top: Verdict + Leak Signal Strip
    add_card(s10, 0.35, 1.44, 4.55, 2.02, fill=C_WHITE, border=C_LINE, radius=0.04)
    s10.shapes.add_picture(str(ASSETS / "card_leak_verdict.png"), Inches(0.45), Inches(1.48), height=Inches(1.74))
    add_textbox(s10, 0.42, 3.24, 4.40, 0.18, "1. Canary Leak Verdict · Seismograph Spike & ANV-7F3K Bar Flag", font=FONT_MONO, size=7.2, bold=True, color=C_RED, align=PP_ALIGN.CENTER)

    # Left bottom: Chat Evidence & Copyable Fix
    add_card(s10, 0.35, 3.56, 4.55, 1.78, fill=C_WHITE, border=C_LINE, radius=0.04)
    s10.shapes.add_picture(str(ASSETS / "card_leak_evidence.png"), Inches(0.48), Inches(3.60), height=Inches(1.50))
    add_textbox(s10, 0.42, 5.12, 4.40, 0.18, "2. Chat Exhibit · Red <mark> Leak Highlight & 1-Click Copy Fix", font=FONT_MONO, size=7.2, bold=True, color=C_ORANGE_DK, align=PP_ALIGN.CENTER)

    # Right full height: v1 -> v2 Compare
    add_card(s10, 5.08, 1.44, 4.57, 3.90, fill=C_WHITE, border=C_GREEN, radius=0.04)
    s10.shapes.add_picture(str(ASSETS / "card_compare.png"), Inches(5.16), Inches(1.56), width=Inches(4.41))
    add_textbox(s10, 5.16, 4.30, 4.41, 0.22, "3. Side-by-Side v1 → v2 Compare & Delta Proof", font=FONT_MONO, size=8.0, bold=True, color=C_GREEN, align=PP_ALIGN.CENTER)
    add_textbox(
        s10, 5.22, 4.55, 4.28, 0.72,
        "• Aligned dual strips mark every fixed v1 test ('fixed' tick)\n"
        "• Count-up deltas: Security 0 → 100 ↑ Improved\n"
        "• Explicit Fixed (SC-01, SC-02) & Regressed (0) audit lists",
        font=FONT_BODY, size=8.4, color=C_MUTED, line_spacing=1.22,
    )

    # ------------------------------------------------------------------
    # SLIDE 11 (Prototype Performance Report / Benchmarking)
    # ------------------------------------------------------------------
    s11 = prs.slides[10]
    remove_non_header_textboxes(s11)
    add_header_title(s11, "10 / PERFORMANCE & BENCHMARKING", "Live Cloud Run benchmark across 5 models from 4 labs.", "50 LIVE EXECUTIONS")

    # Left: Real Matplotlib Chart
    add_card(s11, 0.35, 1.44, 5.25, 3.42, fill=C_WHITE, border=C_LINE, radius=0.05)
    s11.shapes.add_picture(str(ASSETS / "chart_benchmark.png"), Inches(0.42), Inches(1.50), width=Inches(5.11))

    # Right top: Real Measured Data Table
    btbl_shape = s11.shapes.add_table(6, 5, Inches(5.72), Inches(1.44), Inches(3.93), Inches(2.05))
    btbl = btbl_shape.table
    btbl.columns[0].width = Inches(1.38)
    btbl.columns[1].width = Inches(0.62)
    btbl.columns[2].width = Inches(0.62)
    btbl.columns[3].width = Inches(0.65)
    btbl.columns[4].width = Inches(0.66)

    b_headers = ["Target Model", "v1 Sec", "v2 Sec", "v2 Qual", "v1 Time"]
    for ci, ht in enumerate(b_headers):
        cell = btbl.cell(0, ci)
        cell.fill.solid()
        cell.fill.fore_color.rgb = C_INK
        cell.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = cell.text_frame.paragraphs[0]
        r = p.add_run()
        r.text = ht
        r.font.name = FONT_MONO
        r.font.size = Pt(7.4)
        r.font.bold = True
        r.font.color.rgb = C_WHITE

    for ri, b in enumerate(bench, 1):
        v1, v2 = b["v1"], b["v2"]
        v1_sc = f"{v1['scores']['security']}" + ("*" if v1["leaks"] else "")
        v2_sc = f"{v2['scores']['security']}"
        v2_q = f"{v2['scores']['quality']}"
        v1_t = f"{v1['duration_s']:.1f}s"
        vals = [b["label"], v1_sc, v2_sc, v2_q, v1_t]
        for ci, val in enumerate(vals):
            cell = btbl.cell(ri, ci)
            cell.fill.solid()
            cell.fill.fore_color.rgb = C_WHITE if ri % 2 == 1 else C_PANEL
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            p = cell.text_frame.paragraphs[0]
            r = p.add_run()
            r.text = val
            r.font.name = FONT_MONO if ci > 0 else FONT_BODY
            r.font.size = Pt(7.5)
            r.font.bold = ci == 0 or (ci == 1 and v1["scores"]["security"] < 80) or (ci == 3 and v2["scores"]["quality"] < 80)
            if ci == 1 and v1["leaks"]:
                r.font.color.rgb = C_RED
            elif ci == 1 and v1["scores"]["security"] < 80:
                r.font.color.rgb = C_ORANGE_DK
            elif ci == 2:
                r.font.color.rgb = C_GREEN
            elif ci == 3 and v2["scores"]["quality"] < 80:
                r.font.color.rgb = C_RED
            else:
                r.font.color.rgb = C_INK

    # Right bottom: Key Findings Card
    add_card(s11, 5.72, 3.60, 3.93, 1.26, fill=C_ORANGE_BG, border=C_ORANGE, radius=0.08)
    add_textbox(s11, 5.84, 3.68, 3.70, 0.18, "KEY BENCHMARK INSIGHTS", font=FONT_MONO, size=7.8, bold=True, color=C_ORANGE_DK)
    add_textbox(
        s11, 5.84, 3.88, 3.70, 0.94,
        "• 60% of v1 models failed Security; Gemma 4 leaked ANV-7F3K (<1 ms rule catch).\n"
        "• v2 raised avg Security 70 → 100 (+30 pts) with 0 leaks.\n"
        "• Caught real DeepSeek v2 Quality regression (100 → 50) — proving regression gates are mandatory.",
        font=FONT_BODY, size=7.9, color=C_INK, line_spacing=1.22,
    )

    # Bottom stat strip
    add_card(s11, 0.35, 4.98, 9.30, 0.36, fill=C_SUNKEN, border=C_LINE, radius=0.25)
    add_textbox(
        s11, 0.45, 5.06, 9.10, 0.20,
        "Measured live on Cloud Run (anveya-00007-kjx, asia-south1) · Independent Judge: Gemini 3.7 Flash · Fastest run: 4.60s · 0 server crashes",
        font=FONT_MONO, size=7.6, color=C_MUTED, align=PP_ALIGN.CENTER,
    )

    # ------------------------------------------------------------------
    # SLIDE 12 (Additional Details / Future Development)
    # ------------------------------------------------------------------
    s12 = prs.slides[11]
    remove_non_header_textboxes(s12)
    add_header_title(s12, "11 / ROADMAP & FUTURE DEVELOPMENT", "From live MVP to CI/CD LLM assurance at scale.", "3-PHASE PLAN")

    phases = [
        ("PHASE 1 · LIVE NOW (MVP)", C_GREEN, C_GREEN_BG, [
            ("12 Live Vertex AI Models:", "Cross-vendor Target × Judge assurance across 5 frontier & open-weight labs."),
            ("Dual Detection Engine:", "Deterministic canary rules (<1 ms) + temp=0 structured JSON judging."),
            ("Production Cloud Run:", "Live public URL in Mumbai (asia-south1) with keyless IAM & custom tests."),
        ]),
        ("PHASE 2 · NEXT 30–60 DAYS", C_ORANGE_DK, C_ORANGE_BG, [
            ("Bring-Your-Own Endpoint:", "Point Anveya at any staging chatbot HTTP/OpenAI webhook URL in 1 click."),
            ("GitHub Actions PR Gate:", "Fail CI builds automatically if Security < 80, Quality regresses, or a canary leaks."),
            ("Firestore Persistence:", "Save org test suites, prompt history, and longitudinal score trends across releases."),
        ]),
        ("PHASE 3 · ENTERPRISE SCALE", C_BLUE, C_BLUE_BG, [
            ("OWASP LLM & India DPDP:", "Pre-built compliance packs for Aadhaar/PAN PII leakage, DPDP Act & OWASP Top 10."),
            ("Multi-Turn Red-Teaming:", "Autonomous multi-turn attacker agents probing tool-use and RAG pipelines."),
            ("Continuous Monitoring:", "Sample live production traffic for drift, hallucinations, and shadow prompt attacks."),
        ]),
    ]
    for i, (p_title, pc, pbg, pitems) in enumerate(phases):
        px = 0.35 + i * 3.16
        add_card(s12, px, 1.50, 2.98, 3.25, fill=C_PANEL, border=C_LINE, radius=0.06)
        add_card(s12, px, 1.50, 2.98, 0.40, fill=pbg, border=pc, border_pt=1.0, radius=0.06)
        add_textbox(s12, px + 0.12, 1.60, 2.74, 0.20, p_title, font=FONT_MONO, size=8.0, bold=True, color=pc)
        add_bullets(s12, px + 0.14, 2.02, 2.70, 2.60, pitems, size=9.0)

    # Bottom links bar
    add_card(s12, 0.35, 4.90, 9.30, 0.42, fill=C_WHITE, border=C_ORANGE, border_pt=1.2, radius=0.20)
    add_textbox(
        s12, 0.50, 5.00, 9.00, 0.22,
        "Live Prototype: https://anveya-266974009969.asia-south1.run.app   ·   Preview Mode: /?preview   ·   Repo: github.com/gandharvahardikar/anveya-mvp",
        font=FONT_MONO, size=7.8, bold=True, color=C_INK, align=PP_ALIGN.CENTER,
    )

    # ------------------------------------------------------------------
    # SLIDE 13 (Official Thank You Slide + Clean Anveya Contact Footer)
    # ------------------------------------------------------------------
    s13 = prs.slides[12]
    add_textbox(
        s13, 0.55, 5.14, 5.70, 0.30,
        "Anveya Labs (अन्वय)  ·  Live: https://anveya-266974009969.asia-south1.run.app",
        font=FONT_MONO, size=8.3, bold=True, color=C_ORANGE_DK,
    )

    prs.save(str(OUT_PPTX))
    print(f"SAVED_DECK: {OUT_PPTX} ({len(prs.slides)} slides)")


if __name__ == "__main__":
    main()
