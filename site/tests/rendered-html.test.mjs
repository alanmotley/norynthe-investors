import assert from "node:assert/strict";
import { access, readFile } from "node:fs/promises";
import test from "node:test";

async function render() {
  const workerUrl = new URL("../dist/server/index.js", import.meta.url);
  workerUrl.searchParams.set("test", `${process.pid}-${Date.now()}`);
  const { default: worker } = await import(workerUrl.href);
  return worker.fetch(
    new Request("http://localhost/", { headers: { accept: "text/html" } }),
    { ASSETS: { fetch: async () => new Response("Not found", { status: 404 }) } },
    { waitUntil() {}, passThroughOnException() {} },
  );
}

test("server-renders the laboratory-first investor landing page", async () => {
  const response = await render();
  assert.equal(response.status, 200);
  assert.match(response.headers.get("content-type") ?? "", /^text\/html\b/i);
  const html = await response.text();
  assert.match(html, /Independent AI Evaluation Laboratory/i);
  assert.match(html, /Building the independent laboratory for AI trust/i);
  assert.match(html, /Founder-built foundation/i);
  assert.match(html, /Low-headcount by design/i);
  assert.match(html, /noindex, nofollow, noarchive/i);
  assert.doesNotMatch(html, /working evaluation OS|compute capacity is the present constraint/i);
});

test("packages the complete local diligence set", async () => {
  const root = new URL("../dist/client/", import.meta.url);
  const required = [
    "norynthe-laboratory.html",
    "norynthe-raise-plan.html",
    "norynthe-financial-model-assumptions.html",
    "norynthe-founder-memo.html",
    "norynthe-run-console.html",
    "norynthe-customer-report.html",
    "norynthe-customer-report-appendix.html",
    "norynthe-white-paper.html",
    "norynthe-investor-packet.pdf",
  ];
  await Promise.all(required.map((name) => access(new URL(name, root))));
  const [lab, report, appendix, compute, raise, financial, business, consolePage, whitePaper, privacy, robots, headers] = await Promise.all([
    readFile(new URL("norynthe-laboratory.html", root), "utf8"),
    readFile(new URL("norynthe-customer-report.html", root), "utf8"),
    readFile(new URL("norynthe-customer-report-appendix.html", root), "utf8"),
    readFile(new URL("power-of-compute.html", root), "utf8"),
    readFile(new URL("norynthe-raise-plan.html", root), "utf8"),
    readFile(new URL("norynthe-financial-model-assumptions.html", root), "utf8"),
    readFile(new URL("norynthe-business-model.html", root), "utf8"),
    readFile(new URL("norynthe-run-console.html", root), "utf8"),
    readFile(new URL("norynthe-white-paper.html", root), "utf8"),
    readFile(new URL("privacy.html", root), "utf8"),
    readFile(new URL("robots.txt", root), "utf8"),
    readFile(new URL("_headers", root), "utf8"),
  ]);
  assert.match(lab, /Founder identity/i);
  assert.match(lab, /Low headcount\. Explicit accountability/i);
  assert.match(report, /SYNTHETIC SAMPLE DATA/i);
  assert.match(appendix, /SYNTHETIC SAMPLE DATA/i);
  assert.match(report, /position:sticky/i);
  assert.match(appendix, /position:sticky/i);
  assert.doesNotMatch(compute, /Two GB300-class|Why Two Workstations|Approx\. \$100K per top-tier system/i);
  assert.match(compute, /\$146,500 fully owned compute-infrastructure budget/i);
  assert.match(raise, /Capital Architecture Under Consideration/i);
  assert.match(raise, /Founder-Led Laboratory Runway/i);
  assert.match(raise, /Founder-led, one-employee first phase/i);
  assert.match(raise, /href="norynthe-white-paper\.html">White Paper/i);
  assert.doesNotMatch(raise, /Why This Round|Funding And Burn|What This Round Proves|What the \$2M lab build should unlock/i);
  assert.doesNotMatch(raise, /Travel \/ Business Development|Remaining Liquidity \/ Operating Reserve|International \/ Legal \/ Entity Setup/i);
  assert.doesNotMatch(financial, /revenue:\s*\[|grossProfit:\s*\[|operatingProfit:\s*\[/i);
  assert.match(business, /sole initial paid model/i);
  assert.match(consolePage, /sample_core_v2/i);
  assert.doesNotMatch(consolePage, /backend online|runtime online|validation-ready score production|completed a governed evaluation/i);
  assert.match(whitePaper, /canonical public baseline/i);
  assert.match(whitePaper, /Independent AI Evaluation Architecture/i);
  assert.doesNotMatch(whitePaper, /founder-built evaluation OS|current system can review smaller models and validate the scoring logic/i);
  assert.match(privacy, /noindex, nofollow, noarchive/i);
  assert.doesNotMatch(privacy, /access unlock events|remember access status/i);
  assert.match(robots, /Disallow:\s*\//i);
  assert.match(headers, /X-Robots-Tag:\s*noindex/i);
});
