"use client";

import { FormEvent, useState } from "react";

const groups = [
  {
    id: "start",
    number: "01",
    eyebrow: "Start here",
    title: "A short path through the diligence packet.",
    description:
      "The company narrative, founder context, revenue logic, and a concise boardroom view.",
    cards: [
      ["Investor PDF packet", "The complete thesis, product proof, business model, raise plan, and diligence path.", "PDF · 11 pages", "https://norynthe-pulse-tracker.alanmotley.workers.dev/download/investor-packet?site=investor&access=61b63b8f581904d31752068285cbbb5b18e9d81bf45daf02"],
      ["Company and category narrative", "Norynthe’s positioning, market argument, and standard-forming opportunity.", "Core · 7 min", "https://investors.norynthe.com/norynthe-investors.html"],
      ["Revenue logic and paid evidence layer", "Public trust scores, enterprise evidence access, and recurring decision-infrastructure revenue.", "Core · 6 min", "https://investors.norynthe.com/norynthe-business-model.html"],
      ["Why this company exists", "Founder context on the trust problem and the rationale for an independent evaluation layer.", "Context · 6 min", "https://investors.norynthe.com/norynthe-founder-memo.html"],
      ["Boardroom-readable summary", "A compact review of the score, evidence layer, benchmark system, and long-term strategy.", "Summary · 5 min", "https://investors.norynthe.com/executive-overview.html"],
    ],
  },
  {
    id: "research",
    number: "02",
    eyebrow: "Institutional foundation",
    title: "The discipline before the institution.",
    description:
      "The Norynthe Papers establish the intellectual and methodological foundation the product is designed to operationalize.",
    cards: [
      ["The Norynthe Papers", "A continuing institutional publication series documenting the science of trustworthy inference.", "Research archive", "https://papers.norynthe.com/"],
      ["Volume I — On Trust, Inference, and Intelligence", "The founding treatise: intelligence and trust are different, inference should become an object of science, and evaluation requires institutional memory.", "Foundational publication", "https://papers.norynthe.com/volume-i/"],
      ["Durable research record", "Methodology notes, benchmark releases, research reports, and state-of-trust reports preserve how the standard evolves.", "Forthcoming series", "https://papers.norynthe.com/#publications"],
    ],
  },
  {
    id: "product",
    number: "03",
    eyebrow: "Product evidence",
    title: "The working system behind the thesis.",
    description:
      "The evaluation OS turns the research discipline into governed workflows, evidence records, and decision-ready reporting.",
    cards: [
      ["Norynthe OS walkthrough", "The working console for benchmark selection, scoring dimensions, reviewer state, model outputs, and records.", "Product · 10 min", "https://investors.norynthe.com/norynthe-run-console.html"],
      ["External report surface", "The customer-facing format translating assessment records into executive findings and score detail.", "Product · 7 min", "https://investors.norynthe.com/norynthe-customer-report.html"],
      ["Comparative evidence and scoring detail", "A deeper multi-model report with evidence excerpts, reviewer notes, and traceable score context.", "Product · 12 min", "https://investors.norynthe.com/norynthe-customer-report-appendix.html"],
    ],
  },
  {
    id: "financials",
    number: "04",
    eyebrow: "Capital plan",
    title: "Compute capacity is the present constraint.",
    description:
      "The raise moves Norynthe from founder-built proof and smaller-model reviews to a repeatable independent evaluation lab.",
    cards: [
      ["$2M to build the AI trust lab", "The funding target, use of funds, compute unlock, and milestones for larger-model trust scoring.", "Financials · 8 min", "https://investors.norynthe.com/norynthe-raise-plan.html"],
      ["Assumptions, forecast, and reserve logic", "The deployment model, lab budget, commercial ramp, revenue forecast, and investor-ready charts.", "Financials · 10 min", "https://investors.norynthe.com/norynthe-financial-model-assumptions.html"],
    ],
  },
  {
    id: "strategy",
    number: "05",
    eyebrow: "Category and adoption",
    title: "An independent trust layer for models and agents.",
    description:
      "Norynthe is designed to sit outside the model owner’s control and create evidence the market can compare, inspect, and rely upon.",
    cards: [
      ["External trust layer for models and agents", "The deeper thesis for Norynthe.Score, benchmark governance, and external trust infrastructure.", "Strategy · 12 min", "https://investors.norynthe.com/norynthe-white-paper.html"],
      ["Institutional adoption paths", "How independent model credibility records support buyers, regulated enterprises, and strategic reviewers.", "Strategy · 8 min", "https://investors.norynthe.com/norynthe-enterprise-use-cases.html"],
      ["Tokens are fuel. Compute is infrastructure.", "Why capacity is the current bottleneck—and why the evaluation infrastructure should be independent.", "Strategy · 7 min", "https://investors.norynthe.com/power-of-compute.html"],
    ],
  },
];

const answers = [
  ["What exists now?", "A working evaluation OS, scoring workflow, evidence records, and customer-facing reporting surfaces."],
  ["What does capital unlock?", "Dedicated lab and compute capacity for larger-model evaluation, repeatability, and commercial delivery."],
  ["Who buys first?", "Enterprise CTO, procurement, governance, and risk teams that need external evidence before consequential AI decisions."],
  ["What is the near-term proof?", "Paid pilots, repeatable evaluations, comparative records, and evidence-linked reports."],
  ["What compounds?", "The benchmark bank, scoring history, methodology, institutional memory, and public meaning of Norynthe.Score."],
  ["Why is this different?", "Norynthe is an outside-in trust signal—not another inside-out governance or observability dashboard."],
];

export default function Home() {
  const [unlocked, setUnlocked] = useState(false);
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  function unlock(event: FormEvent) {
    event.preventDefault();
    if (password === "INVEST_2026") {
      setUnlocked(true);
      setError("");
      requestAnimationFrame(() => document.querySelector("#materials")?.scrollIntoView({ behavior: "smooth" }));
    } else {
      setError("That password wasn’t recognized. Please check the invitation and try again.");
    }
  }

  return (
    <main>
      <header className="site-header">
        <a className="wordmark" href="https://norynthe.com/" aria-label="Norynthe home"><img src="/Norynthe_master.png" alt="Norynthe." /></a>
        <span className="portal-label">Investor access</span>
        <a className="text-link" href="https://tally.so/r/ZjezPA">Contact ↗</a>
      </header>

      <section className="hero">
        <div className="hero-copy">
          <p className="kicker">Selected investor and strategic review conversations</p>
          <h1>Independent infrastructure for AI trust.</h1>
          <p className="lede">
            Norynthe is building the external evaluation layer for intelligent systems:
            governed methods, durable evidence, and a standard the market can trust
            outside the model owner’s control.
          </p>
          <div className="thesis-line">
            <span>Research discipline</span><i>→</i><span>Evaluation OS</span><i>→</i><span>Independent trust signal</span>
          </div>
        </div>

        <aside className="access-card" aria-label="Investor access gate">
          <p className="kicker">Controlled diligence</p>
          <h2>Unlock the review.</h2>
          <p>The portal connects the institutional thesis, working product, capital plan, and category opportunity.</p>
          {!unlocked ? (
            <form onSubmit={unlock}>
              <label htmlFor="password">Access password</label>
              <div className="input-row">
                <input id="password" type="password" value={password} onChange={(e) => setPassword(e.target.value)} placeholder="Enter password" />
                <button type="submit">Unlock</button>
              </div>
              <p className="form-note" role="status">{error || "Shared for selected investor and strategic conversations."}</p>
            </form>
          ) : <p className="unlocked">Access active · Review materials below</p>}
        </aside>
      </section>

      <section className="proof-strip" aria-label="Company proof points">
        <div><strong>Working OS</strong><span>Evaluation and reporting surfaces exist today.</span></div>
        <div><strong>Institutional research</strong><span>The Papers preserve the discipline behind the system.</span></div>
        <div><strong>$2M plan</strong><span>Dedicated lab and compute capacity.</span></div>
        <div><strong>Compounding asset</strong><span>Benchmarks, evidence, history, and trust.</span></div>
      </section>

      <section className="research-bridge">
        <div className="section-index">The research layer / 01</div>
        <div>
          <p className="kicker">The Norynthe Papers</p>
          <h2>The discipline before the institution.</h2>
        </div>
        <div>
          <p>
            Norynthe was not founded to build another artificial intelligence system.
            It was founded to understand trustworthy inference. The Papers preserve
            the philosophical, scientific, and institutional foundations of that work.
          </p>
          <a className="button-secondary" href="https://papers.norynthe.com/">Read the Papers ↗</a>
        </div>
      </section>

      <section className="artifact-preview">
        <div className="section-heading">
          <p className="kicker">From thesis to evidence</p>
          <h2>A guided packet, not a file dump.</h2>
          <p>Review the working product, the report it produces, and the capital plan that expands its reach.</p>
        </div>
        <div className="preview-grid">
          <figure className="preview-main">
            <img src="https://investors.norynthe.com/previews/console-page-preview.jpg" alt="Norynthe scoring console with benchmark context and evaluation workflow" />
            <figcaption><span>Working MVP</span><strong>Governed evaluation workflow</strong></figcaption>
          </figure>
          <figure><img src="https://investors.norynthe.com/previews/customer-report-page-preview.jpg" alt="Norynthe customer report score summary" /><figcaption><span>Customer report</span><strong>Decision-ready evidence</strong></figcaption></figure>
          <figure><img src="https://investors.norynthe.com/previews/financial-model-page-preview.jpg" alt="Norynthe financial model and use-of-funds chart" /><figcaption><span>Use of funds</span><strong>Capital tied to proof</strong></figcaption></figure>
        </div>
      </section>

      {!unlocked ? (
        <section className="locked-map">
          <p className="kicker">What access unlocks</p>
          <div className="locked-grid">
            {groups.map((group) => <div key={group.id}><span>{group.number}</span><strong>{group.eyebrow}</strong><p>{group.title}</p></div>)}
          </div>
        </section>
      ) : (
        <section id="materials" className="materials">
          {groups.map((group) => (
            <section className="material-group" key={group.id} id={group.id}>
              <div className="group-intro">
                <span className="group-number">{group.number}</span>
                <p className="kicker">{group.eyebrow}</p>
                <h2>{group.title}</h2>
                <p>{group.description}</p>
              </div>
              <div className="card-grid">
                {group.cards.map(([title, description, meta, href], index) => (
                  <a className={index === 0 ? "material-card featured" : "material-card"} href={href} key={title}>
                    <span className="card-meta">{meta}</span>
                    <h3>{title}</h3>
                    <p>{description}</p>
                    <span className="card-link">Open material ↗</span>
                  </a>
                ))}
              </div>
            </section>
          ))}

          <section className="questions">
            <div className="section-heading"><p className="kicker">Diligence snapshot</p><h2>The six investor questions, answered.</h2></div>
            <div className="answer-grid">
              {answers.map(([question, answer], index) => <article key={question}><span>0{index + 1}</span><h3>{question}</h3><p>{answer}</p></article>)}
            </div>
          </section>
        </section>
      )}

      <section className="closing">
        <p className="kicker">The category thesis</p>
        <h2>If AI becomes infrastructure, trust becomes infrastructure too.</h2>
        <p>Norynthe is building the durable, independent evidence layer required to evaluate, compare, and understand intelligent systems over time.</p>
        <a className="button-primary" href="https://tally.so/r/ZjezPA">Request a walkthrough ↗</a>
      </section>

      <footer>
        <a className="wordmark footer-wordmark" href="https://norynthe.com/">Norynthe.</a>
        <p>Confidential investor review · Independent evaluation · Governed methodology · Traceable evidence</p>
        <div><a href="https://papers.norynthe.com/">Papers</a><a href="https://norynthe.com/privacy.html">Privacy</a><span>© 2026 Norynthe.</span></div>
      </footer>
    </main>
  );
}
