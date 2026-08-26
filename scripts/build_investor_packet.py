from __future__ import annotations

import argparse
import shutil
import subprocess
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "norynthe-investor-packet.pdf"


def asset(name: str) -> str:
    return (ROOT / name).resolve().as_uri()


def find_chrome() -> str:
    candidates = [
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/Applications/Chromium.app/Contents/MacOS/Chromium",
        shutil.which("google-chrome"),
        shutil.which("chromium"),
        shutil.which("chromium-browser"),
    ]
    for candidate in candidates:
        if candidate and Path(candidate).exists():
            return str(candidate)
    raise RuntimeError("Google Chrome or Chromium is required to render the investor PDF.")


def stop_renderer(process: subprocess.Popen, profile_path: Path) -> None:
    try:
        process.terminate()
    except ProcessLookupError:
        return
    except PermissionError:
        pass
    try:
        process.wait(timeout=2)
        return
    except subprocess.TimeoutExpired:
        pass
    except PermissionError:
        pass

    for signal_name in ("-TERM", "-KILL"):
        subprocess.run(
            ["pkill", signal_name, "-f", str(profile_path)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        )
        try:
            process.wait(timeout=2)
            return
        except subprocess.TimeoutExpired:
            continue
        except PermissionError:
            return


CSS = r"""
@page {
  size: 11in 8.5in;
  margin: 0;
}

* {
  box-sizing: border-box;
}

html,
body {
  margin: 0;
  padding: 0;
}

body {
  color: #0f1115;
  font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  background: #e9edf2;
  -webkit-print-color-adjust: exact;
  print-color-adjust: exact;
}

.slide {
  position: relative;
  width: 11in;
  height: 8.5in;
  overflow: hidden;
  break-inside: avoid-page;
  page-break-inside: avoid;
  page-break-after: auto;
  padding: 0.45in 0.54in 0.42in;
  background:
    radial-gradient(circle at 78% 14%, rgba(143, 177, 203, 0.24), transparent 29%),
    radial-gradient(circle at 22% 88%, rgba(154, 124, 57, 0.12), transparent 25%),
    radial-gradient(circle at 46% 50%, rgba(255, 255, 255, 0.72), transparent 44%),
    linear-gradient(180deg, #f1f5f7 0%, #e9edf2 48%, #eef2f6 100%);
}

.slide + .slide {
  break-before: page;
  page-break-before: always;
}

.slide::before {
  content: "";
  position: absolute;
  inset: 0;
  background-image:
    linear-gradient(rgba(15, 17, 21, 0.025) 1px, transparent 1px),
    linear-gradient(90deg, rgba(15, 17, 21, 0.025) 1px, transparent 1px);
  background-size: 72px 72px;
  opacity: 0.68;
}

.slide::after {
  content: "";
  position: absolute;
  inset: 0.25in;
  border: 1px solid rgba(15, 17, 21, 0.085);
  border-radius: 20px;
  pointer-events: none;
}

.content {
  position: relative;
  z-index: 1;
  display: flex;
  flex-direction: column;
  height: 100%;
  min-height: 0;
}

.topbar {
  display: flex;
  flex: 0 0 0.45in;
  align-items: center;
  justify-content: space-between;
  min-height: 0.45in;
  padding-bottom: 0.16in;
  border-bottom: 1px solid rgba(15, 17, 21, 0.11);
}

.brand {
  display: flex;
  align-items: center;
  width: 1.72in;
  height: 0.32in;
}

.brand img {
  display: block;
  width: 100%;
  height: auto;
}

.meta {
  color: #596571;
  font-size: 9px;
  font-weight: 780;
  letter-spacing: 0.16em;
  line-height: 1;
  text-transform: uppercase;
}

.cover .topbar {
  border-bottom: 0;
}

.body {
  flex: 1;
  min-height: 0;
  overflow: hidden;
  padding-top: 0.34in;
}

.cover .body {
  padding-top: 0.25in;
}

.eyebrow {
  margin: 0 0 0.13in;
  color: #7a3030;
  font-size: 9.2px;
  font-weight: 820;
  letter-spacing: 0.2em;
  line-height: 1.25;
  text-transform: uppercase;
}

.title {
  margin: 0;
  color: #0f1115;
  font-size: 36px;
  font-weight: 760;
  letter-spacing: 0;
  line-height: 0.98;
  max-width: 9.1in;
}

.title.compact {
  max-width: 6.9in;
  font-size: 33px;
}

.cover-title {
  max-width: 4.9in;
  font-size: 61px;
  line-height: 0.91;
}

.lede {
  margin: 0.22in 0 0;
  max-width: 6.6in;
  color: #36414e;
  font-size: 15.5px;
  font-weight: 480;
  line-height: 1.47;
}

.small {
  color: #596571;
  font-size: 11.5px;
  line-height: 1.45;
}

.cover-grid {
  display: grid;
  grid-template-columns: 4.55in minmax(0, 1fr);
  gap: 0.46in;
  align-items: stretch;
  height: 6.75in;
}

.cover .lede {
  max-width: 4.35in;
}

.metrics {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 0.14in;
  margin-top: 0.48in;
}

.metric {
  min-height: 0.9in;
  padding: 0.17in 0.15in 0.15in;
  border: 1px solid rgba(15, 17, 21, 0.09);
  border-radius: 14px;
  background:
    linear-gradient(180deg, rgba(255, 255, 255, 0.92), rgba(250, 252, 253, 0.76)),
    radial-gradient(circle at top right, rgba(51, 75, 110, 0.07), transparent 38%);
  box-shadow: 0 14px 34px rgba(15, 17, 21, 0.045);
}

.metric-label {
  color: #7a3030;
  font-size: 8px;
  font-weight: 820;
  letter-spacing: 0.16em;
  line-height: 1.2;
  text-transform: uppercase;
}

.metric-value {
  margin-top: 0.06in;
  color: #0f1115;
  font-size: 20px;
  font-weight: 760;
  letter-spacing: 0;
  line-height: 1;
}

.metric-note {
  margin-top: 0.08in;
  color: #596571;
  font-size: 10.5px;
  line-height: 1.36;
}

.collage {
  position: relative;
  min-height: 0;
}

.cover-board {
  display: grid;
  grid-template-rows: 0.82in 3.28in 1.58in;
  gap: 0.16in;
  height: 6.0in;
  margin-top: 0.13in;
}

.cover-score-row {
  display: grid;
  grid-template-columns: 1.14in minmax(0, 1fr);
  gap: 0.14in;
}

.cover-score {
  display: grid;
  place-items: center;
  border-radius: 16px;
  color: #ffffff;
  background:
    radial-gradient(circle at top right, rgba(255, 255, 255, 0.14), transparent 42%),
    linear-gradient(145deg, #101820, #2b3a49);
  box-shadow: 0 22px 56px rgba(15, 17, 21, 0.14);
}

.cover-score strong {
  display: block;
  font-size: 31px;
  font-weight: 760;
  line-height: 0.9;
  text-align: center;
}

.cover-score span {
  display: block;
  margin-top: 0.05in;
  color: rgba(255, 255, 255, 0.68);
  font-size: 6.6px;
  font-weight: 820;
  letter-spacing: 0.16em;
  text-align: center;
  text-transform: uppercase;
}

.cover-board-note {
  padding: 0.14in 0.17in;
  border: 1px solid rgba(15, 17, 21, 0.09);
  border-radius: 16px;
  background: rgba(255, 255, 255, 0.76);
  box-shadow: 0 14px 34px rgba(15, 17, 21, 0.045);
}

.cover-board-note strong {
  display: block;
  color: #0f1115;
  font-size: 12.5px;
  line-height: 1.08;
}

.cover-board-note span {
  display: block;
  margin-top: 0.055in;
  color: #596571;
  font-size: 9.4px;
  line-height: 1.34;
}

.cover-frame {
  overflow: hidden;
  margin: 0;
  padding: 0.07in;
  border: 1px solid rgba(15, 17, 21, 0.12);
  border-radius: 19px;
  background:
    linear-gradient(180deg, rgba(255, 255, 255, 0.96), rgba(250, 252, 253, 0.82));
  box-shadow: 0 24px 68px rgba(15, 17, 21, 0.12);
}

.cover-frame img {
  display: block;
  width: 100%;
  height: 100%;
  border-radius: 13px;
  object-fit: cover;
}

.cover-frame.main img {
  object-position: 51% 42%;
}

.cover-frame.small img {
  object-fit: contain;
  object-position: 50% 26%;
  background: #ffffff;
}

.cover-support {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.16in;
}

.cover-support .cover-frame {
  box-shadow: 0 16px 42px rgba(15, 17, 21, 0.09);
}

.collage::before {
  content: "";
  position: absolute;
  inset: 0.18in 0.05in 0.18in 0.42in;
  border: 1px solid rgba(15, 17, 21, 0.09);
  border-radius: 22px;
  background:
    radial-gradient(circle at 22% 20%, rgba(122, 48, 48, 0.11), transparent 30%),
    radial-gradient(circle at 80% 72%, rgba(51, 75, 110, 0.14), transparent 34%),
    rgba(255, 255, 255, 0.42);
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.6);
}

.shot {
  position: absolute;
  overflow: hidden;
  border: 1px solid rgba(15, 17, 21, 0.13);
  border-radius: 16px;
  background: rgba(255, 255, 255, 0.88);
  box-shadow: 0 26px 70px rgba(15, 17, 21, 0.13);
}

.shot img {
  display: block;
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.shot.main {
  top: 0.24in;
  right: 0;
  width: 4.78in;
  height: 2.9in;
}

.shot.secondary {
  top: 3.22in;
  right: 1.34in;
  width: 3.34in;
  height: 1.88in;
}

.shot.tertiary {
  top: 4.74in;
  right: 0.05in;
  width: 2.8in;
  height: 1.6in;
}

.score-tile {
  position: absolute;
  left: 0.18in;
  bottom: 0.5in;
  z-index: 4;
  width: 1.2in;
  height: 1.2in;
  display: grid;
  place-items: center;
  border: 1px solid rgba(255, 255, 255, 0.12);
  border-radius: 18px;
  color: #ffffff;
  background:
    radial-gradient(circle at top right, rgba(255, 255, 255, 0.14), transparent 42%),
    linear-gradient(145deg, #0f1115, #263441);
  box-shadow: 0 26px 70px rgba(15, 17, 21, 0.18);
}

.score-tile strong {
  display: block;
  font-size: 34px;
  font-weight: 760;
  line-height: 0.9;
  text-align: center;
}

.score-tile span {
  display: block;
  margin-top: 0.06in;
  color: rgba(255, 255, 255, 0.7);
  font-size: 7px;
  font-weight: 820;
  letter-spacing: 0.18em;
  text-align: center;
  text-transform: uppercase;
}

.screen-label {
  position: absolute;
  left: 0.14in;
  top: 0.13in;
  z-index: 2;
  padding: 0.055in 0.08in;
  border-radius: 7px;
  color: #ffffff;
  background: rgba(15, 17, 21, 0.8);
  font-size: 8px;
  font-weight: 760;
  letter-spacing: 0.12em;
  text-transform: uppercase;
}

.split {
  display: grid;
  grid-template-columns: minmax(0, 4.35in) minmax(0, 1fr);
  gap: 0.34in;
  margin-top: 0.28in;
  min-height: 0;
}

.split.snapshot {
  height: 4.15in;
}

.split.reverse {
  grid-template-columns: minmax(0, 1fr) minmax(0, 4.35in);
}

.statement {
  padding: 0.02in 0 0;
}

.statement h2 {
  margin: 0;
  color: #0f1115;
  font-size: 34px;
  font-weight: 760;
  letter-spacing: 0;
  line-height: 1;
}

.statement p {
  margin: 0.2in 0 0;
  color: #36414e;
  font-size: 14.2px;
  line-height: 1.48;
}

.snapshot .statement h2 {
  font-size: 29px;
}

.snapshot .statement p {
  margin-top: 0.14in;
  font-size: 12.7px;
  line-height: 1.4;
}

.insight-list {
  display: grid;
  gap: 0.12in;
  margin-top: 0.33in;
}

.snapshot .insight-list {
  gap: 0.08in;
  margin-top: 0.18in;
}

.insight {
  display: grid;
  grid-template-columns: 0.34in minmax(0, 1fr);
  gap: 0.12in;
  padding: 0.15in;
  border: 1px solid rgba(15, 17, 21, 0.09);
  border-radius: 14px;
  background: rgba(255, 255, 255, 0.72);
}

.snapshot .insight {
  padding: 0.11in;
}

.index {
  display: grid;
  place-items: center;
  width: 0.34in;
  height: 0.34in;
  border-radius: 999px;
  color: #ffffff;
  background: #7a3030;
  font-size: 10px;
  font-weight: 800;
}

.insight:nth-child(2) .index {
  background: #334b6e;
}

.insight:nth-child(3) .index {
  background: #36554a;
}

.insight h3 {
  margin: 0;
  color: #0f1115;
  font-size: 13.2px;
  font-weight: 760;
  line-height: 1.1;
}

.snapshot .insight h3 {
  font-size: 12.2px;
}

.insight p {
  margin: 0.065in 0 0;
  color: #596571;
  font-size: 11px;
  line-height: 1.42;
}

.snapshot .insight p {
  font-size: 10px;
  line-height: 1.28;
}

.panel {
  position: relative;
  min-height: 0;
  padding: 0.24in;
  border: 1px solid rgba(15, 17, 21, 0.09);
  border-radius: 18px;
  background:
    linear-gradient(180deg, rgba(255, 255, 255, 0.92), rgba(250, 252, 253, 0.76)),
    radial-gradient(circle at top right, rgba(51, 75, 110, 0.065), transparent 34%);
  box-shadow: 0 18px 42px rgba(15, 17, 21, 0.055);
}

.snapshot .panel {
  padding: 0.2in;
}

.stack {
  display: grid;
  gap: 0.12in;
  height: 100%;
}

.snapshot .stack {
  gap: 0.09in;
}

.stack-row {
  display: grid;
  grid-template-columns: 0.66in minmax(0, 1fr);
  gap: 0.14in;
  align-items: center;
  min-height: 0.77in;
  padding: 0.14in;
  border: 1px solid rgba(15, 17, 21, 0.08);
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.68);
}

.snapshot .stack-row {
  min-height: 0.75in;
  padding: 0.12in;
}

.stack-row strong {
  color: #0f1115;
  font-size: 12.8px;
  line-height: 1.15;
}

.stack-row span {
  display: block;
  margin-top: 0.055in;
  color: #596571;
  font-size: 10.5px;
  line-height: 1.36;
}

.stack-num {
  color: #7a3030;
  font-size: 22px;
  font-weight: 760;
  line-height: 1;
}

.callout {
  margin-top: 0.2in;
  padding: 0.16in 0.18in;
  border-left: 0.06in solid #7a3030;
  border-radius: 12px;
  background: rgba(122, 48, 48, 0.075);
  color: #3e4852;
  font-size: 12px;
  line-height: 1.42;
}

.callout strong {
  display: block;
  margin-bottom: 0.04in;
  color: #7a3030;
  font-size: 8.5px;
  font-weight: 820;
  letter-spacing: 0.16em;
  text-transform: uppercase;
}

.thesis-grid {
  display: grid;
  grid-template-columns: 3.18in 2.8in 2.8in;
  gap: 0.18in;
  height: 4.76in;
  margin-top: 0.3in;
}

.thesis-layout {
  display: grid;
  grid-template-columns: 3.08in minmax(0, 1fr);
  gap: 0.25in;
  height: 4.62in;
  margin-top: 0.3in;
}

.thesis-anchor {
  display: grid;
  align-content: end;
  min-height: 0;
  padding: 0.25in;
  border-radius: 20px;
  color: #ffffff;
  background:
    radial-gradient(circle at top right, rgba(255, 255, 255, 0.14), transparent 42%),
    linear-gradient(145deg, #101820, #2b3a49);
  box-shadow: 0 24px 70px rgba(15, 17, 21, 0.16);
}

.thesis-anchor span {
  color: rgba(229, 179, 179, 0.92);
  font-size: 8.6px;
  font-weight: 820;
  letter-spacing: 0.18em;
  text-transform: uppercase;
}

.thesis-anchor h3 {
  margin: 0.14in 0 0;
  color: #ffffff;
  font-size: 31px;
  font-weight: 760;
  letter-spacing: 0;
  line-height: 0.96;
}

.thesis-anchor p {
  margin: 0.18in 0 0;
  color: rgba(255, 255, 255, 0.72);
  font-size: 12.2px;
  line-height: 1.42;
}

.asset-strip {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 0.07in;
  margin-top: 0.24in;
}

.asset-strip div {
  padding: 0.08in 0;
  border-top: 1px solid rgba(255, 255, 255, 0.14);
  color: rgba(255, 255, 255, 0.74);
  font-size: 9.3px;
  font-weight: 650;
  line-height: 1.18;
}

.thesis-ladder {
  display: grid;
  gap: 0.11in;
}

.thesis-step {
  display: grid;
  grid-template-columns: 0.7in minmax(0, 1fr);
  gap: 0.16in;
  align-items: start;
  padding: 0.16in 0.18in;
  border: 1px solid rgba(15, 17, 21, 0.09);
  border-radius: 15px;
  background:
    linear-gradient(180deg, rgba(255, 255, 255, 0.9), rgba(250, 252, 253, 0.75));
  box-shadow: 0 12px 30px rgba(15, 17, 21, 0.038);
}

.thesis-step b {
  color: #7a3030;
  font-size: 19px;
  font-weight: 760;
  line-height: 1;
}

.thesis-step h3 {
  margin: 0;
  color: #0f1115;
  font-size: 15px;
  font-weight: 760;
  line-height: 1.08;
}

.thesis-step p {
  margin: 0.07in 0 0;
  color: #596571;
  font-size: 10.8px;
  line-height: 1.42;
}

.thesis-card {
  padding: 0.22in;
  border: 1px solid rgba(15, 17, 21, 0.09);
  border-radius: 18px;
  background: rgba(255, 255, 255, 0.74);
  box-shadow: 0 14px 34px rgba(15, 17, 21, 0.045);
}

.thesis-card h3 {
  margin: 0;
  color: #0f1115;
  font-size: 19px;
  font-weight: 760;
  line-height: 1.03;
}

.thesis-card p {
  margin: 0.16in 0 0;
  color: #596571;
  font-size: 12px;
  line-height: 1.43;
}

.evidence-ledger {
  display: grid;
  gap: 0.1in;
  margin-top: 0.2in;
}

.ledger-row {
  padding: 0.12in 0;
  border-top: 1px solid rgba(15, 17, 21, 0.1);
}

.ledger-row strong {
  color: #0f1115;
  font-size: 12.2px;
}

.ledger-row span {
  display: block;
  margin-top: 0.04in;
  color: #596571;
  font-size: 10.5px;
  line-height: 1.3;
}

.product-grid {
  display: grid;
  grid-template-columns: minmax(0, 5.9in) minmax(0, 3.0in);
  gap: 0.2in;
  height: 3.08in;
  margin-top: 0.24in;
}

.product-main,
.product-side {
  overflow: hidden;
  padding: 0.07in;
  border: 1px solid rgba(15, 17, 21, 0.12);
  border-radius: 18px;
  background: rgba(255, 255, 255, 0.86);
  box-shadow: 0 22px 60px rgba(15, 17, 21, 0.11);
}

.product-main img,
.product-side img {
  display: block;
  width: 100%;
  height: 100%;
  border-radius: 12px;
  object-fit: cover;
  object-position: center;
}

.product-main img {
  object-position: 51% 42%;
}

.product-side img {
  object-position: 50% 24%;
}

.product-side-stack {
  display: grid;
  gap: 0.18in;
}

.product-side {
  height: 1.44in;
}

.proof-strip {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 0;
  margin-top: 0.22in;
  overflow: hidden;
  border: 1px solid rgba(15, 17, 21, 0.09);
  border-radius: 14px;
  background: rgba(255, 255, 255, 0.72);
}

.proof-item {
  padding: 0.12in;
  border-right: 1px solid rgba(15, 17, 21, 0.09);
}

.proof-item:last-child {
  border-right: 0;
}

.proof-item strong {
  color: #0f1115;
  font-size: 11.7px;
  line-height: 1.08;
}

.proof-item span {
  display: block;
  margin-top: 0.055in;
  color: #596571;
  font-size: 9.8px;
  line-height: 1.32;
}

.product-proof-layout {
  display: grid;
  grid-template-columns: minmax(0, 6.25in) minmax(0, 2.75in);
  gap: 0.24in;
  height: 3.72in;
  margin-top: 0.32in;
}

.product-showcase {
  overflow: hidden;
  margin: 0;
  padding: 0.08in;
  border: 1px solid rgba(15, 17, 21, 0.12);
  border-radius: 20px;
  background:
    linear-gradient(180deg, rgba(255, 255, 255, 0.96), rgba(250, 252, 253, 0.82)),
    radial-gradient(circle at top right, rgba(51, 75, 110, 0.08), transparent 34%);
  box-shadow: 0 24px 68px rgba(15, 17, 21, 0.12);
}

.product-showcase img {
  display: block;
  width: 100%;
  height: 100%;
  border-radius: 14px;
  object-fit: cover;
  object-position: 51% 42%;
}

.evidence-panel {
  display: grid;
  align-content: stretch;
  gap: 0.1in;
}

.evidence-heading {
  padding: 0.15in 0.16in;
  border-radius: 15px;
  color: #ffffff;
  background:
    radial-gradient(circle at top right, rgba(255, 255, 255, 0.13), transparent 42%),
    linear-gradient(145deg, #111820, #283846);
}

.evidence-heading span {
  display: block;
  color: rgba(255, 255, 255, 0.64);
  font-size: 8px;
  font-weight: 820;
  letter-spacing: 0.16em;
  text-transform: uppercase;
}

.evidence-heading strong {
  display: block;
  margin-top: 0.07in;
  color: #ffffff;
  font-size: 18px;
  font-weight: 760;
  line-height: 1.02;
}

.evidence-row {
  padding: 0.12in 0.14in;
  border: 1px solid rgba(15, 17, 21, 0.09);
  border-radius: 13px;
  background: rgba(255, 255, 255, 0.76);
}

.evidence-row strong {
  display: block;
  color: #0f1115;
  font-size: 11.7px;
  font-weight: 760;
  line-height: 1.08;
}

.evidence-row span {
  display: block;
  margin-top: 0.055in;
  color: #596571;
  font-size: 9.8px;
  line-height: 1.38;
}

.revenue-architecture {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 0.17in;
  margin-top: 0.3in;
}

.stage {
  position: relative;
  min-height: 2.35in;
  padding: 0.21in;
  border: 1px solid rgba(15, 17, 21, 0.09);
  border-radius: 18px;
  background: rgba(255, 255, 255, 0.74);
  box-shadow: 0 14px 34px rgba(15, 17, 21, 0.045);
}

.stage::before {
  content: "";
  position: absolute;
  left: 0.21in;
  right: 0.21in;
  top: 0.14in;
  height: 3px;
  border-radius: 999px;
  background: #7a3030;
}

.stage:nth-child(2)::before {
  background: #334b6e;
}

.stage:nth-child(3) {
  color: #ffffff;
  background:
    radial-gradient(circle at top right, rgba(255, 255, 255, 0.13), transparent 42%),
    linear-gradient(145deg, #101820, #2b3a49);
}

.stage:nth-child(3)::before {
  background: #9a7c39;
}

.stage:nth-child(3) .stage-label,
.stage:nth-child(3) h3 {
  color: #ffffff;
}

.stage:nth-child(3) p {
  color: rgba(255, 255, 255, 0.72);
}

.stage-label {
  color: #7a3030;
  font-size: 9px;
  font-weight: 820;
  letter-spacing: 0.16em;
  text-transform: uppercase;
}

.stage h3 {
  margin: 0.13in 0 0;
  color: #0f1115;
  font-size: 22px;
  font-weight: 760;
  line-height: 1.02;
}

.stage p {
  margin: 0.15in 0 0;
  color: #596571;
  font-size: 12px;
  line-height: 1.5;
}

.product-list {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 0.12in;
  margin-top: 0.22in;
}

.product-list div {
  padding: 0.13in 0.14in;
  border: 1px solid rgba(15, 17, 21, 0.08);
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.7);
  color: #36414e;
  font-size: 11px;
  line-height: 1.28;
}

.matrix {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  grid-template-rows: repeat(2, minmax(0, 1fr));
  gap: 0;
  height: 3.55in;
  overflow: hidden;
  border: 1px solid rgba(15, 17, 21, 0.1);
  border-radius: 18px;
  background: rgba(255, 255, 255, 0.76);
}

.matrix-cell {
  padding: 0.22in;
  border-right: 1px solid rgba(15, 17, 21, 0.1);
  border-bottom: 1px solid rgba(15, 17, 21, 0.1);
}

.matrix-cell:nth-child(2),
.matrix-cell:nth-child(4) {
  border-right: 0;
}

.matrix-cell:nth-child(3),
.matrix-cell:nth-child(4) {
  border-bottom: 0;
}

.matrix-cell span {
  color: #7a3030;
  font-size: 8.8px;
  font-weight: 820;
  letter-spacing: 0.16em;
  text-transform: uppercase;
}

.matrix-cell h3 {
  margin: 0.12in 0 0;
  color: #0f1115;
  font-size: 18px;
  font-weight: 760;
  line-height: 1.05;
}

.matrix-cell p {
  margin: 0.11in 0 0;
  color: #596571;
  font-size: 11.4px;
  line-height: 1.38;
}

.case-list {
  display: grid;
  gap: 0.1in;
  height: 3.55in;
}

.case-row {
  display: grid;
  grid-template-columns: 1.28in minmax(0, 1fr);
  gap: 0.13in;
  align-items: start;
  padding: 0.13in;
  border: 1px solid rgba(15, 17, 21, 0.085);
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.72);
}

.case-row strong {
  color: #0f1115;
  font-size: 12.2px;
  line-height: 1.12;
}

.case-row span {
  color: #596571;
  font-size: 10.8px;
  line-height: 1.38;
}

.plan-grid {
  display: grid;
  grid-template-columns: 3.4in minmax(0, 1fr);
  gap: 0.26in;
  height: 4.75in;
  margin-top: 0.3in;
}

.raise-number {
  display: grid;
  align-content: center;
  min-height: 2.2in;
  padding: 0.24in;
  border-radius: 18px;
  color: #ffffff;
  background:
    radial-gradient(circle at top right, rgba(255, 255, 255, 0.13), transparent 38%),
    linear-gradient(145deg, #111820, #283846);
  box-shadow: 0 22px 60px rgba(15, 17, 21, 0.16);
}

.raise-number span {
  color: rgba(255, 255, 255, 0.7);
  font-size: 9px;
  font-weight: 800;
  letter-spacing: 0.18em;
  text-transform: uppercase;
}

.raise-number strong {
  margin-top: 0.12in;
  font-size: 55px;
  font-weight: 760;
  letter-spacing: 0;
  line-height: 0.88;
}

.raise-number p {
  margin: 0.18in 0 0;
  color: rgba(255, 255, 255, 0.78);
  font-size: 12.5px;
  line-height: 1.42;
}

.timeline {
  display: grid;
  gap: 0.11in;
}

.timeline-row {
  display: grid;
  grid-template-columns: 0.64in minmax(0, 1fr);
  gap: 0.13in;
  align-items: start;
  padding: 0.13in 0.14in;
  border: 1px solid rgba(15, 17, 21, 0.085);
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.73);
}

.timeline-row strong {
  color: #7a3030;
  font-size: 13px;
  font-weight: 760;
}

.timeline-row h3 {
  margin: 0;
  color: #0f1115;
  font-size: 13.5px;
  font-weight: 760;
  line-height: 1.12;
}

.timeline-row p {
  margin: 0.065in 0 0;
  color: #596571;
  font-size: 11px;
  line-height: 1.42;
}

.funds-layout {
  display: grid;
  grid-template-columns: 2.54in minmax(0, 1fr);
  gap: 0.28in;
  height: 4.36in;
  margin-top: 0.28in;
}

.fund-summary {
  display: grid;
  align-content: center;
  padding: 0.22in;
  border-radius: 18px;
  color: #ffffff;
  background:
    radial-gradient(circle at top right, rgba(255, 255, 255, 0.13), transparent 40%),
    linear-gradient(145deg, #111820, #283846);
  border: 1px solid rgba(255, 255, 255, 0.08);
  box-shadow: 0 22px 60px rgba(15, 17, 21, 0.14);
}

.fund-summary .big {
  color: #ffffff;
  font-size: 48px;
  font-weight: 760;
  line-height: 0.92;
}

.fund-summary p {
  margin: 0.18in 0 0;
  color: rgba(255, 255, 255, 0.72);
  font-size: 12.2px;
  line-height: 1.42;
}

.fund-summary .eyebrow {
  color: rgba(229, 179, 179, 0.94);
}

.fund-badges {
  display: grid;
  gap: 0.08in;
  margin-top: 0.25in;
}

.fund-badges div {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  gap: 0.16in;
  padding-top: 0.08in;
  border-top: 1px solid rgba(255, 255, 255, 0.13);
  color: rgba(255, 255, 255, 0.7);
  font-size: 10.2px;
}

.fund-badges strong {
  color: #ffffff;
  font-size: 14px;
}

.fund-bars {
  display: grid;
  align-content: start;
  gap: 0.11in;
}

.fund-row {
  display: grid;
  grid-template-columns: 1.78in minmax(0, 1fr) 0.72in;
  gap: 0.13in;
  align-items: center;
}

.fund-row strong {
  color: #0f1115;
  font-size: 11.2px;
  font-weight: 730;
  line-height: 1.18;
}

.fund-track {
  height: 0.16in;
  overflow: hidden;
  border-radius: 999px;
  background: rgba(15, 17, 21, 0.08);
}

.fund-fill {
  width: var(--w);
  height: 100%;
  border-radius: inherit;
  background: var(--c);
}

.fund-row span {
  color: #596571;
  font-size: 10.8px;
  font-weight: 650;
  text-align: right;
}

.fund-row strong span.small {
  display: block;
  margin-top: 0.02in;
  font-size: 10.7px;
  line-height: 1.18;
  text-align: left;
}

.chart-layout {
  display: grid;
  grid-template-columns: minmax(0, 5.4in) minmax(0, 1fr);
  gap: 0.28in;
  height: 4.8in;
  margin-top: 0.28in;
}

.chart {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 0.23in;
  align-items: end;
  height: 3.2in;
  padding: 0.2in 0.25in 0.42in;
  border-bottom: 1px solid rgba(15, 17, 21, 0.16);
  background:
    repeating-linear-gradient(to top, transparent, transparent 0.61in, rgba(15, 17, 21, 0.065) 0.62in),
    rgba(255, 255, 255, 0.62);
  border-radius: 18px 18px 6px 6px;
}

.bar-group {
  position: relative;
  display: flex;
  align-items: end;
  justify-content: center;
  gap: 0.11in;
  height: 2.56in;
}

.bar {
  width: 0.32in;
  height: var(--h);
  min-height: 0.08in;
  border-radius: 7px 7px 0 0;
  background: var(--c);
}

.bar-label {
  position: absolute;
  left: 0;
  right: 0;
  bottom: -0.35in;
  color: #36414e;
  font-size: 11px;
  font-weight: 760;
  text-align: center;
}

.chart-note {
  margin-top: 0.16in;
  color: #596571;
  font-size: 11.3px;
  line-height: 1.4;
}

.metric-stack {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 0.13in;
}

.metric-stack .metric {
  min-height: 1.18in;
}

.legend {
  display: flex;
  gap: 0.17in;
  margin-top: 0.12in;
  color: #596571;
  font-size: 10.5px;
}

.swatch {
  display: inline-block;
  width: 0.1in;
  height: 0.1in;
  margin-right: 0.05in;
  border-radius: 2px;
  vertical-align: -1px;
}

.compute-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 0.17in;
  margin-top: 0.3in;
}

.compute-card {
  min-height: 3.95in;
  padding: 0.2in;
  border: 1px solid rgba(15, 17, 21, 0.09);
  border-radius: 18px;
  background: rgba(255, 255, 255, 0.74);
  box-shadow: 0 14px 34px rgba(15, 17, 21, 0.045);
}

.compute-card h3 {
  margin: 0;
  color: #0f1115;
  font-size: 18px;
  font-weight: 760;
  line-height: 1.02;
}

.compute-card .cost {
  margin-top: 0.13in;
  color: #7a3030;
  font-size: 12px;
  font-weight: 760;
}

.compute-card p {
  margin: 0.16in 0 0;
  color: #596571;
  font-size: 11.6px;
  line-height: 1.48;
}

.cap-list {
  display: grid;
  gap: 0.07in;
  margin-top: 0.18in;
}

.cap-list div {
  padding: 0.08in 0;
  border-top: 1px solid rgba(15, 17, 21, 0.09);
  color: #36414e;
  font-size: 10.8px;
  line-height: 1.25;
}

.closing-grid {
  display: grid;
  grid-template-columns: minmax(0, 5.35in) minmax(0, 3.45in);
  gap: 0.32in;
  height: 5.15in;
  margin-top: 0.3in;
}

.next-steps {
  display: grid;
  gap: 0.13in;
}

.next-step {
  display: grid;
  grid-template-columns: 0.52in minmax(0, 1fr);
  gap: 0.15in;
  align-items: start;
  padding: 0.17in;
  border: 1px solid rgba(15, 17, 21, 0.09);
  border-radius: 14px;
  background: rgba(255, 255, 255, 0.75);
}

.next-step .index {
  width: 0.42in;
  height: 0.42in;
  font-size: 12px;
}

.next-step h3 {
  margin: 0;
  color: #0f1115;
  font-size: 15.2px;
  font-weight: 760;
  line-height: 1.08;
}

.next-step p {
  margin: 0.08in 0 0;
  color: #596571;
  font-size: 11.4px;
  line-height: 1.44;
}

.contact-panel {
  display: grid;
  align-content: center;
  padding: 0.3in;
  border-radius: 18px;
  color: #ffffff;
  background:
    radial-gradient(circle at top right, rgba(255, 255, 255, 0.13), transparent 40%),
    linear-gradient(145deg, #121820, #293847);
  box-shadow: 0 24px 70px rgba(15, 17, 21, 0.16);
}

.contact-panel img {
  width: 1.8in;
  padding: 0;
  border-radius: 0;
  background: transparent;
  filter: brightness(0) invert(1);
}

.contact-panel h3 {
  margin: 0.42in 0 0;
  color: #ffffff;
  font-size: 24px;
  font-weight: 760;
  line-height: 1.08;
}

.contact-panel p {
  margin: 0.18in 0 0;
  color: rgba(255, 255, 255, 0.72);
  font-size: 12.5px;
  line-height: 1.55;
}

/* Page-specific print fitting. These compositions carry more copy than the
   standard template and must remain wholly inside the fixed letter canvas. */
.snapshot-page .body,
.thesis-page .body,
.business-page .body,
.plan-page .body,
.funds-page .body,
.architecture-page .body,
.diligence-page .body {
  padding-top: 0.24in;
}

.snapshot-page .title {
  font-size: 33px;
}

.snapshot-page .lede {
  margin-top: 0.16in;
  font-size: 14.2px;
  line-height: 1.38;
}

.snapshot-page .split.snapshot {
  height: 3.82in;
  margin-top: 0.2in;
}

.snapshot-page .snapshot .statement h2 {
  font-size: 26px;
}

.snapshot-page .snapshot .statement p {
  margin-top: 0.1in;
  font-size: 11.8px;
  line-height: 1.34;
}

.snapshot-page .snapshot .insight-list {
  gap: 0.065in;
  margin-top: 0.12in;
}

.snapshot-page .snapshot .insight {
  padding: 0.085in;
}

.snapshot-page .snapshot .insight p {
  font-size: 9.5px;
  line-height: 1.22;
}

.snapshot-page .snapshot .panel {
  padding: 0.16in;
}

.snapshot-page .snapshot .stack {
  gap: 0.065in;
}

.snapshot-page .snapshot .stack-row {
  min-height: 0.66in;
  padding: 0.095in;
}

.thesis-page .title.compact,
.plan-page .title.compact {
  max-width: 8.75in;
  font-size: 30px;
}

.thesis-page .lede,
.plan-page .lede {
  margin-top: 0.15in;
  font-size: 14px;
  line-height: 1.34;
}

.thesis-page .thesis-layout {
  height: 4.3in;
  margin-top: 0.2in;
}

.thesis-page .thesis-anchor {
  padding: 0.21in;
}

.thesis-page .thesis-anchor h3 {
  font-size: 28px;
}

.thesis-page .thesis-anchor p {
  margin-top: 0.14in;
  font-size: 11.5px;
  line-height: 1.36;
}

.thesis-page .asset-strip {
  margin-top: 0.18in;
}

.thesis-page .thesis-ladder {
  gap: 0.08in;
}

.thesis-page .thesis-step {
  padding: 0.13in 0.16in;
}

.plan-page .plan-grid {
  height: 4.15in;
  margin-top: 0.2in;
}

.plan-page .raise-number {
  min-height: 2.02in;
  padding: 0.2in;
}

.plan-page .raise-number strong {
  font-size: 49px;
}

.plan-page .raise-number p {
  margin-top: 0.13in;
  font-size: 11.5px;
  line-height: 1.35;
}

.plan-page .callout {
  margin-top: 0.12in;
  padding: 0.12in 0.16in;
  font-size: 11px;
  line-height: 1.3;
}

.plan-page .timeline {
  gap: 0.08in;
}

.plan-page .timeline-row {
  padding: 0.105in 0.13in;
}

.plan-page .timeline-row p {
  margin-top: 0.045in;
  font-size: 10.5px;
  line-height: 1.32;
}

.business-page .title.compact,
.funds-page .title.compact,
.diligence-page .title.compact {
  max-width: 8.75in;
  font-size: 30px;
}

.business-page .lede,
.funds-page .lede,
.diligence-page .lede {
  margin-top: 0.15in;
  font-size: 14px;
  line-height: 1.34;
}

.business-page .revenue-architecture {
  gap: 0.14in;
  margin-top: 0.21in;
}

.business-page .stage {
  min-height: 2.02in;
  padding: 0.18in;
}

.business-page .stage h3 {
  margin-top: 0.11in;
  font-size: 20px;
}

.business-page .stage p {
  margin-top: 0.12in;
  font-size: 11.2px;
  line-height: 1.38;
}

.business-page .product-list {
  gap: 0.08in;
  margin-top: 0.14in;
}

.business-page .product-list div {
  padding: 0.095in 0.12in;
}

.business-page .callout,
.architecture-page .callout {
  margin-top: 0.13in;
  padding: 0.115in 0.16in;
  font-size: 11.2px;
  line-height: 1.32;
}

.funds-page .funds-layout {
  height: 3.9in;
  margin-top: 0.2in;
}

.funds-page .fund-summary {
  padding: 0.19in;
}

.funds-page .fund-summary .big {
  font-size: 44px;
}

.funds-page .fund-summary p {
  margin-top: 0.13in;
  font-size: 11.4px;
  line-height: 1.34;
}

.funds-page .fund-badges {
  gap: 0.055in;
  margin-top: 0.16in;
}

.funds-page .fund-bars {
  gap: 0.075in;
}

.architecture-page .lede {
  margin-top: 0.16in;
  font-size: 14.2px;
  line-height: 1.36;
}

.architecture-page .title.compact {
  max-width: 8.4in;
  font-size: 30px;
}

.architecture-page .compute-grid {
  margin-top: 0.22in;
}

.architecture-page .compute-card {
  min-height: 3.18in;
  padding: 0.18in;
}

.architecture-page .compute-card p {
  margin-top: 0.12in;
  font-size: 11.1px;
  line-height: 1.4;
}

.architecture-page .cap-list {
  margin-top: 0.13in;
}

.diligence-page .closing-grid {
  height: 3.9in;
  margin-top: 0.14in;
}

.diligence-page .next-steps {
  gap: 0.055in;
}

.diligence-page .next-step {
  padding: 0.085in 0.12in;
}

.diligence-page .next-step .index {
  width: 0.32in;
  height: 0.32in;
  font-size: 9.5px;
}

.diligence-page .next-step h3 {
  font-size: 13px;
}

.diligence-page .next-step p {
  margin-top: 0.04in;
  font-size: 9.7px;
  line-height: 1.25;
}

.diligence-page .contact-panel {
  padding: 0.21in;
}

.diligence-page .contact-panel h3 {
  margin-top: 0.22in;
  font-size: 20px;
}

.diligence-page .contact-panel p {
  font-size: 10.8px;
  line-height: 1.34;
}

.diligence-page .body {
  padding-top: 0.16in;
}

.diligence-page .title.compact {
  max-width: 9in;
  font-size: 28px;
}

.diligence-page .lede {
  margin-top: 0.1in;
  font-size: 12.8px;
  line-height: 1.28;
}

.footer-note {
  position: absolute;
  left: 0.55in;
  right: 0.55in;
  bottom: 0.27in;
  display: flex;
  justify-content: space-between;
  color: #707a84;
  font-size: 8.7px;
  font-weight: 650;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  z-index: 2;
}
"""


def slide_start(
    number: str,
    eyebrow: str,
    title: str,
    lede: str,
    *,
    compact: bool = False,
    page_class: str = "",
) -> str:
    title_class = "title compact" if compact else "title"
    section_class = f"slide {page_class}".strip()
    return f"""
<section class="{section_class}">
  <div class="content">
    <header class="topbar">
      <div class="brand"><img src="{asset('Norynthe_master.png')}" alt="Norynthe"></div>
      <div class="meta">Selected investor review / August 2026</div>
    </header>
    <main class="body">
      <p class="eyebrow">{eyebrow}</p>
      <h1 class="{title_class}">{title}</h1>
      <p class="lede">{lede}</p>
"""


def slide_end(number: str) -> str:
    return f"""
    </main>
  </div>
  <div class="footer-note"><span>Norynthe Investor Packet</span><span>{number}</span></div>
</section>
"""


def metric(label: str, value: str, note: str) -> str:
    return f"""
<div class="metric">
  <div class="metric-label">{label}</div>
  <div class="metric-value">{value}</div>
  <div class="metric-note">{note}</div>
</div>
"""


def build_html(selected_slide: int | None = None) -> str:
    logo = asset("Norynthe_master.png")
    console = asset("previews/console-page-preview.jpg")
    customer = asset("previews/customer-report-page-preview.jpg")
    financial = asset("previews/financial-model-page-preview.jpg")

    slides: list[str] = []

    slides.append(f"""
<section class="slide cover">
  <div class="content">
    <header class="topbar">
      <div class="brand"><img src="{logo}" alt="Norynthe"></div>
      <div class="meta">Selected investor review / August 2026</div>
    </header>
    <main class="body">
      <div class="cover-grid">
        <div>
          <p class="eyebrow">Independent AI evaluation laboratory</p>
          <h1 class="title cover-title">Norynthe Investor Packet</h1>
          <p class="lede">Norynthe is building the controlled physical, computational, methodological, evidentiary, security, and governance environment required for independent AI evaluation.</p>
          <div class="metrics">
            {metric("Raise target", "$2.0M", "Establish the controlled evaluation laboratory.")}
            {metric("Operating model", "Founder-led", "Low headcount by design; infrastructure and governed workflows carry the load.")}
            {metric("Current state", "Foundation built", "Published research, Method v0.1, architecture, prototype surfaces, and early experimentation.")}
          </div>
        </div>
        <div class="cover-board">
          <div class="cover-score-row">
            <div class="cover-score"><div><strong>80</strong><span>sample score</span></div></div>
            <div class="cover-board-note"><strong>Build the institution that can earn the evidence.</strong><span>The prototype makes the workflow concrete. The funded phase must produce complete run packages, repeatability results, external challenge, and traceable reports.</span></div>
          </div>
          <figure class="cover-frame main"><img src="{console}" alt="Norynthe run console preview"></figure>
          <div class="cover-support">
            <figure class="cover-frame small"><img src="{customer}" alt="Norynthe customer report preview"></figure>
            <figure class="cover-frame small"><img src="{financial}" alt="Norynthe financial model preview"></figure>
          </div>
        </div>
      </div>
    </main>
  </div>
  <div class="footer-note"><span>Norynthe Investor Packet</span><span>01</span></div>
</section>
""")

    slides.append(slide_start(
        "02",
        "01 / Executive snapshot",
        "Norynthe is building the independent laboratory for AI trust.",
        "The laboratory joins controlled conditions, governed benchmarks and methods, hybrid compute, preserved evidence, external challenge, correction, and institutional reporting outside the model owner’s control.",
        page_class="snapshot-page",
    ) + f"""
      <div class="split snapshot">
        <div class="statement">
          <h2>Independent evidence requires an institution built to produce it.</h2>
          <p>Enterprises need a way to compare AI systems outside model-owner claims, vendor demos, and narrow benchmark headlines. Norynthe creates a governed evidence record that can travel through procurement, risk, and executive decision processes.</p>
          <div class="insight-list">
            <div class="insight"><div class="index">1</div><div><h3>Founder-built foundation</h3><p>Published research, Method v0.1, prototype workflow surfaces, illustrative reports, and early experimentation make the design concrete.</p></div></div>
            <div class="insight"><div class="index">2</div><div><h3>Independent score layer</h3><p>The score is built from governed benchmark assets, not model-owner marketing claims.</p></div></div>
            <div class="insight"><div class="index">3</div><div><h3>Laboratory capability unlock</h3><p>The $2M establishes the controlled base, hybrid compute, evidence systems, security, governance, external challenge, and founder-led runway.</p></div></div>
          </div>
        </div>
        <div class="panel">
          <div class="stack">
            <div class="stack-row"><div class="stack-num">01</div><div><strong>Benchmark assets</strong><span>Governed prompts, rubrics, test dimensions, and evaluation conditions.</span></div></div>
            <div class="stack-row"><div class="stack-num">02</div><div><strong>Norynthe Model</strong><span>Evaluator, scoring logic, confidence, blocker criteria, and judgment rules.</span></div></div>
            <div class="stack-row"><div class="stack-num">03</div><div><strong>Assessment records</strong><span>Versioned model standing, score detail, review state, findings, and flags.</span></div></div>
            <div class="stack-row"><div class="stack-num">04</div><div><strong>Enterprise reports</strong><span>Buyer-readable evidence for procurement, governance, risk, and operations.</span></div></div>
          </div>
        </div>
      </div>
""" + slide_end("02"))

    slides.append(slide_start(
        "03",
        "02 / Company thesis",
        "Independent scoring becomes infrastructure.",
        "Most AI evaluation collapses into demos, brand perception, leaderboard headlines, or provider-controlled tests. Norynthe starts from a different premise: trustworthy evaluation requires an independent evidence-producing institution.",
        compact=True,
        page_class="thesis-page",
    ) + """
      <div class="thesis-layout">
        <aside class="thesis-anchor">
          <span>Category thesis</span>
          <h3>Trust moves outside the model.</h3>
          <p>Norynthe is building the record system enterprises can use when model claims are not enough.</p>
          <div class="asset-strip">
            <div>Benchmark bank</div>
            <div>Scoring engine</div>
            <div>Assessment record</div>
            <div>Report surface</div>
          </div>
        </aside>
        <div class="thesis-ladder">
          <div class="thesis-step"><b>01</b><div><h3>AI choice is now an operating decision.</h3><p>Model selection is moving into workflows with procurement, policy, legal, risk, and operational consequences.</p></div></div>
          <div class="thesis-step"><b>02</b><div><h3>Existing evaluation is too vendor-shaped.</h3><p>Leaderboards and demos are useful, but they do not create an independently governed evidence record buyers can reuse across departments.</p></div></div>
          <div class="thesis-step"><b>03</b><div><h3>A governed evidence record becomes reusable infrastructure.</h3><p>The score creates comparison pressure; the record and report create the paid evidence layer behind it.</p></div></div>
          <div class="thesis-step"><b>04</b><div><h3>The moat compounds through evidence density.</h3><p>Benchmark governance, scoring logic, reviewer state, and buyer-facing reports harden together as more evaluations run.</p></div></div>
        </div>
      </div>
""" + slide_end("03"))

    slides.append(slide_start(
        "04",
        "03 / Current evidence state",
        "A founder-built foundation; laboratory validation ahead.",
        "The investor preview is a static prototype of the intended workflow. It is not a production backend or proof of completed scientific validation. The next proof is executable, preserved, repeatable run evidence.",
        compact=True,
    ) + f"""
      <div class="product-proof-layout">
        <figure class="product-showcase"><img src="{console}" alt="Norynthe console screen"></figure>
        <aside class="evidence-panel">
          <div class="evidence-heading"><span>Illustrative prototype</span><strong>Intended evaluation workflow before controlled laboratory validation.</strong></div>
          <div class="evidence-row"><strong>Launch</strong><span>Benchmark, target model, runtime posture, and evaluation conditions.</span></div>
          <div class="evidence-row"><strong>Score</strong><span>Evaluator logic, dimensions, evidence checks, flags, and confidence.</span></div>
          <div class="evidence-row"><strong>Record</strong><span>Intended assessment state, reviewer posture, illustrative findings, and caveats.</span></div>
          <div class="evidence-row"><strong>Report</strong><span>Buyer-facing output generated from the underlying evidence record.</span></div>
        </aside>
      </div>
""" + slide_end("04"))

    slides.append(slide_start(
        "05",
        "04 / Commercial model",
        "A bounded paid workflow comes before recurring products.",
        "The first commercial hypothesis is a scoped enterprise adoption-evidence engagement: one consequential decision, one controlled evaluation record, and one decision-ready report. Recurring products follow only after validation.",
        compact=True,
        page_class="business-page",
    ) + """
      <div class="revenue-architecture">
        <div class="stage">
          <div class="stage-label">Laboratory layer</div>
          <h3>Controlled evaluation</h3>
          <p>Governed conditions, run manifests, evidence preservation, review, limitations, and repeatability.</p>
        </div>
        <div class="stage">
          <div class="stage-label">First paid workflow</div>
          <h3>Adoption-evidence engagement</h3>
          <p>A bounded evaluation record and report tied to one real institutional decision.</p>
        </div>
        <div class="stage">
          <div class="stage-label">Later hypotheses</div>
          <h3>Recurring evidence access</h3>
          <p>Subscriptions, monitoring, comparisons, APIs, or licensing only where repeat demand and delivery economics support them.</p>
        </div>
      </div>
      <div class="product-list">
        <div>Full evaluation reports</div>
        <div>Score methodology</div>
        <div>Vendor comparisons</div>
        <div>Evidence trails</div>
        <div>Governance documentation</div>
        <div>Custom evaluations</div>
      </div>
      <div class="callout"><strong>Revenue discipline</strong>Commercial forecasts are withheld until design partners establish willingness to pay, cycle length, delivery effort, decision impact, and repeat usage.</div>
""" + slide_end("05"))

    slides.append(slide_start(
        "06",
        "05 / Enterprise use cases",
        "Norynthe is designed to turn model trust into a decision workflow.",
        "The funded laboratory will test whether controlled evidence improves judgment about which systems should be used, under what constraints, with what evidence, and with what level of review.",
        compact=True,
    ) + """
      <div class="split reverse">
        <div class="matrix">
          <div class="matrix-cell"><span>Compare</span><h3>Which model has standing?</h3><p>Test ranking under a shared benchmark surface instead of vendor-specific claims.</p></div>
          <div class="matrix-cell"><span>Explain</span><h3>Why did one system outrank another?</h3><p>Test whether dimensions, evidence, flags, and score context make a result inspectable.</p></div>
          <div class="matrix-cell"><span>Escalate</span><h3>Where should human review remain mandatory?</h3><p>Test blocker criteria, caveats, risk posture, and sensitive-use constraints.</p></div>
          <div class="matrix-cell"><span>Operationalize</span><h3>How should the selected system be used?</h3><p>Test whether evidence supports procurement, governance, and deployment decisions.</p></div>
        </div>
        <div class="case-list">
          <div class="case-row"><strong>Model selection</strong><span>Compare vendors under the same benchmark surface.</span></div>
          <div class="case-row"><strong>Procurement review</strong><span>Reduce dependence on vendor-defined evidence.</span></div>
          <div class="case-row"><strong>Internal governance</strong><span>Make trust judgments reviewable across teams.</span></div>
          <div class="case-row"><strong>Sensitive workflows</strong><span>Apply blocker criteria and escalation logic.</span></div>
          <div class="case-row"><strong>Operational deployment</strong><span>Decide where constraints and human oversight belong.</span></div>
        </div>
      </div>
      <div class="callout"><strong>Use-case hypothesis</strong>Norynthe should be strongest where decisions need reviewable evidence, shared language, and an evaluator outside the model vendor's control.</div>
""" + slide_end("06"))

    slides.append(slide_start(
        "07",
        "06 / Raise plan",
        "$2M to establish the controlled evaluation laboratory.",
        "The round creates the integrated physical, computational, methodological, evidentiary, security, governance, and operating capacity required for repeatable independent evaluation.",
        compact=True,
        page_class="plan-page",
    ) + """
      <div class="plan-grid">
        <div>
          <div class="raise-number"><span>Target raise</span><strong>$2.0M</strong><p>Laboratory-first capital for a controlled base, hybrid compute, evidence and security systems, method governance, external challenge, and founder-led runway.</p></div>
          <div class="callout"><strong>Operating read</strong>The plan remains intentionally low-headcount. Capital builds reusable capability and institutional evidence before payroll expansion.</div>
        </div>
        <div class="timeline">
          <div class="timeline-row"><strong>01</strong><div><h3>Specify and govern</h3><p>Facility alternatives, compute configuration, method register, benchmark register, security, conflicts, and correction.</p></div></div>
          <div class="timeline-row"><strong>02</strong><div><h3>Commission controlled execution</h3><p>Minimum viable environment, evidence ledger, version controls, chain of custody, and first complete run package.</p></div></div>
          <div class="timeline-row"><strong>03</strong><div><h3>Demonstrate repeatability</h3><p>Repeated-run variance, method reconciliation, external challenge, and traceable pilot reports.</p></div></div>
          <div class="timeline-row"><strong>04</strong><div><h3>Validate institutional demand</h3><p>Bounded design-partner engagements, willingness to pay, decision impact, and supported recurring paths.</p></div></div>
        </div>
      </div>
""" + slide_end("07"))

    funds = [
        ("Controlled laboratory base — diligence gated", "$1,126,571", "56.3%", "56.3%", "#7a3030"),
        ("Founder-led laboratory runway", "$477,429", "23.9%", "23.9%", "#334b6e"),
        ("Compute infrastructure", "$146,500", "7.3%", "7.3%", "#36554a"),
        ("Lab / workspace buildout", "$93,500", "4.7%", "4.7%", "#9a7c39"),
        ("Legal / entity / IP / property governance", "$72,000", "3.6%", "3.6%", "#466a72"),
        ("Institutional validation / design partners", "$50,000", "2.5%", "2.5%", "#8f6c50"),
        ("Ops / software / security", "$34,000", "1.7%", "1.7%", "#b7c7d2"),
    ]
    fund_rows = "\n".join(
        f"""<div class="fund-row"><strong>{label}<br><span class="small">{amount}</span></strong><div class="fund-track"><div class="fund-fill" style="--w:{width}; --c:{color};"></div></div><span>{pct}</span></div>"""
        for label, amount, pct, width, color in funds
    )
    slides.append(slide_start(
        "08",
        "07 / Use of funds",
        "Capital goes into governed laboratory capability before payroll scale.",
        "The allocation establishes a controlled base, hybrid compute, evidence and security systems, governance, institutional validation, and founder-led runway. The largest category remains subject to explicit facility and ownership diligence.",
        compact=True,
        page_class="funds-page",
    ) + f"""
      <div class="funds-layout">
        <div class="fund-summary">
          <div class="eyebrow">Total raise</div>
          <div class="big">$2.0M</div>
          <p>The use-of-funds view is intentionally literal. The controlled-base assumption is dominant and therefore must pass functional necessity, technical suitability, economic, governance, and capital-efficiency tests before commitment.</p>
          <div class="fund-badges">
            <div><span>Controlled base</span><strong>56.3%</strong></div>
            <div><span>Founder-led runway</span><strong>23.9%</strong></div>
            <div><span>Lab and compute</span><strong>12.0%</strong></div>
          </div>
        </div>
        <div class="fund-bars">
          {fund_rows}
        </div>
      </div>
""" + slide_end("08"))

    slides.append(slide_start(
        "09",
        "08 / 18-month proof program",
        "Capital deployment is staged against evidence, not calendar optimism.",
        "Prior internal revenue scenarios are not presented as investor guidance. The funded phase retires technical, methodological, institutional, and commercial risk in sequence.",
        compact=True,
    ) + """
      <div class="timeline">
        <div class="timeline-row"><strong>00–03</strong><div><h3>Govern the foundation</h3><p>One canonical method and benchmark relationship; facility, entity, IP, compute, evidence, security, conflict, appeal, and correction diligence.</p></div></div>
        <div class="timeline-row"><strong>03–06</strong><div><h3>Commission the minimum viable laboratory</h3><p>Controlled execution environment, evidence ledger, version controls, chain of custody, and first complete verified run package.</p></div></div>
        <div class="timeline-row"><strong>06–12</strong><div><h3>Earn repeatability</h3><p>Repeated-run variance results, reconciled method and benchmark versions, external methodological challenge, and traceable pilot reports.</p></div></div>
        <div class="timeline-row"><strong>12–18</strong><div><h3>Validate institutional demand</h3><p>Bounded design-partner engagements, willingness to pay, decision impact, delivery economics, and supported recurring products.</p></div></div>
      </div>
      <div class="callout"><strong>Forecast gate</strong>A board-usable commercial forecast follows evidence on cycle length, pricing, gross delivery effort, repeat usage, conversion, and the effect of Norynthe’s evidence on a real decision.</div>
""" + slide_end("09"))

    slides.append(slide_start(
        "10",
        "09 / Laboratory architecture",
        "Compute matters inside a governed evidence system.",
        "No workstation creates independence by itself. Norynthe requires integrated control across conditions, methods, benchmark custody, execution, evidence, security, review, correction, and reporting.",
        compact=True,
        page_class="architecture-page",
    ) + """
      <div class="compute-grid">
        <div class="compute-card">
          <h3>Method and evidence controls</h3>
          <div class="cost">Institutional core</div>
          <p>Canonical methods, governed benchmarks, run manifests, evidence ledger, chain of custody, review, correction, and institutional memory.</p>
          <div class="cap-list"><div>Traceability</div><div>Version control</div><div>Challenge and appeal</div><div>Preserved limitations</div></div>
        </div>
        <div class="compute-card">
          <h3>Hybrid compute</h3>
          <div class="cost">Configuration under diligence</div>
          <p>Selected local capacity, secure storage, APIs, and external capacity chosen by control, coverage, repeatability, security, and cost.</p>
          <div class="cap-list"><div>Local sensitive work</div><div>Frontier API coverage</div><div>Repeated execution</div><div>Cost discipline</div></div>
        </div>
        <div class="compute-card">
          <h3>Controlled physical base</h3>
          <div class="cost">Diligence gated</div>
          <p>A purpose-bound environment for evidence custody, security, infrastructure continuity, protected benchmark work, and founder-led operation.</p>
          <div class="cap-list"><div>Power and thermal control</div><div>Physical security</div><div>Operating continuity</div><div>Company governance</div></div>
        </div>
      </div>
      <div class="callout"><strong>Facility caveat</strong>The dominant base allocation must pass functional necessity, technical suitability, buy-versus-lease economics, company-control governance, and capital-efficiency tests before commitment.</div>
""" + slide_end("10"))

    slides.append(slide_start(
        "11",
        "10 / Founder and diligence path",
        "A low-headcount institution with explicit founder accountability.",
        "Alan Motley remains the principal operator, laboratory director, method steward, and institutional lead. His standpoint as a Black AI systems strategist informs which questions Norynthe asks; governed evidence must earn every finding.",
        compact=True,
        page_class="diligence-page",
    ) + f"""
      <div class="closing-grid">
        <div class="next-steps">
          <div class="next-step"><div class="index">1</div><div><h3>Inspect the evidence state</h3><p>Separate published method, prototype surfaces, synthetic samples, early experiments, and capital-enabled proof.</p></div></div>
          <div class="next-step"><div class="index">2</div><div><h3>Review laboratory necessity</h3><p>Test whether each physical, computational, evidentiary, security, and governance component produces a capability the institution needs.</p></div></div>
          <div class="next-step"><div class="index">3</div><div><h3>Challenge the capital map</h3><p>Pressure-test facility alternatives, hardware configuration, governance, runway, milestone gates, and the appropriate blend of capital.</p></div></div>
          <div class="next-step"><div class="index">4</div><div><h3>Define the next proof</h3><p>Agree on complete run packages, repeatability, external challenge, design partners, paid pilots, and decision impact.</p></div></div>
        </div>
        <aside class="contact-panel">
          <img src="{logo}" alt="Norynthe">
          <h3>Laboratory-first diligence.</h3>
          <p>The packet is organized to answer why the laboratory must exist, why it remains founder-led and low-headcount, what capital establishes, and what evidence the funded phase must earn.</p>
          <p><a href="https://investors.norynthe.com/">investors.norynthe.com</a><br><a href="mailto:hello@norynthe.com">hello@norynthe.com</a></p>
        </aside>
      </div>
""" + slide_end("11"))

    selected_markup = slides if selected_slide is None else [slides[selected_slide - 1]]
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Norynthe Investor Packet</title>
  <style>{CSS}</style>
</head>
<body>
{''.join(selected_markup)}
</body>
</html>
"""


def render_pdf(*, selected_slide: int | None = None, output: Path = OUTPUT) -> None:
    chrome = find_chrome()
    # Never treat a prior packet as evidence that a new Chrome render finished.
    # Removing it first also prevents the timeout path from preserving a stale
    # or only partially replaced file.
    output.unlink(missing_ok=True)
    with tempfile.TemporaryDirectory(prefix="norynthe-packet-") as tmp:
        html_path = Path(tmp) / "norynthe-investor-packet.html"
        profile_path = Path(tmp) / "chrome-profile"
        html_path.write_text(build_html(selected_slide), encoding="utf-8")
        command = [
            chrome,
            "--headless=new",
            "--disable-background-networking",
            "--disable-component-update",
            "--disable-default-apps",
            "--disable-extensions",
            "--disable-gpu",
            "--disable-dev-shm-usage",
            "--disable-sync",
            "--metrics-recording-only",
            "--no-first-run",
            "--no-sandbox",
            "--allow-file-access-from-files",
            "--print-to-pdf-no-header",
            "--no-pdf-header-footer",
            f"--user-data-dir={profile_path}",
            f"--print-to-pdf={output}",
            html_path.as_uri(),
        ]
        process = subprocess.Popen(
            command,
            stderr=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
        )
        try:
            process.wait(timeout=180)
        except subprocess.TimeoutExpired:
            if output.exists() and output.stat().st_size > 0:
                stop_renderer(process, profile_path)
            else:
                stop_renderer(process, profile_path)
                raise
        else:
            if process.returncode != 0 and not (output.exists() and output.stat().st_size > 0):
                raise RuntimeError("Chrome failed to render the investor PDF.")
    if not output.exists() or output.stat().st_size == 0:
        raise RuntimeError(f"PDF was not created: {output}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build the Norynthe investor packet.")
    parser.add_argument("--slide", type=int, choices=range(1, 12), help="Render one slide for print QA.")
    parser.add_argument("--output", type=Path, default=OUTPUT, help="PDF output path.")
    args = parser.parse_args()
    render_pdf(selected_slide=args.slide, output=args.output)
    print(args.output)
