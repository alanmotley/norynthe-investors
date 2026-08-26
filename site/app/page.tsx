"use client";

import { FormEvent, useState } from "react";

const groups = [
  {
    id: "start",
    number: "01",
    eyebrow: "Start here",
    title: "Begin with the laboratory.",
    description:
      "The institutional thesis, laboratory architecture, founder context, and capital-to-capability plan.",
    cards: [
      ["Laboratory architecture", "Why independent evaluation requires a controlled physical, computational, methodological, evidentiary, security, and governance environment.", "Core · 10 min", "https://investors.norynthe.com/norynthe-laboratory.html"],
      ["Investor PDF packet", "The laboratory thesis, current evidence state, capital plan, founder-led operation, and 18-month proof path.", "PDF · 11 pages", "/norynthe-investor-packet.pdf"],
      ["White Paper — evaluation architecture", "The technical rationale for independent scoring, verification, benchmark governance, and future agent-episode evaluation. Historical extension context; Method v0.1 remains canonical.", "Technical deep dive · 12 min", "https://investors.norynthe.com/norynthe-white-paper.html"],
      ["Company and category narrative", "Norynthe’s positioning as an independent AI assurance company and institution.", "Core · 7 min", "https://investors.norynthe.com/norynthe-investors.html"],
      ["Why this company exists", "Founder context on the trust problem and the rationale for an independent evaluation layer.", "Context · 6 min", "https://investors.norynthe.com/norynthe-founder-memo.html"],
      ["Capital-to-capability plan", "What the $2M establishes, why the controlled base matters, and which milestones govern deployment.", "Capital · 8 min", "https://investors.norynthe.com/norynthe-raise-plan.html"],
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
      ["Volume II — On Reality, Records, and the Calibration of Intelligence", "The published foundation for continuous epistemic calibration, revision memory, and reality-facing institutional inquiry.", "Published · Aug 25, 2026", "https://papers.norynthe.com/volume-ii/"],
      ["Norynthe AI Assurance Method v0.1", "The current public method defining assurance, independence, evidence, corrections, appeals, and non-certification limits.", "Method · M-001", "https://papers.norynthe.com/methods/ai-assurance-method-v0-1/"],
    ],
  },
  {
    id: "product",
    number: "03",
    eyebrow: "Evidence state",
    title: "Founder-built foundation; laboratory validation ahead.",
    description:
      "The investor surfaces demonstrate intended workflow and reporting architecture. They are not a production backend or proof of completed scientific validation.",
    cards: [
      ["Evaluation workflow preview", "A static investor walkthrough of the intended benchmark, scoring, review, evidence-record, and reporting workflow.", "Illustrative prototype · 10 min", "https://investors.norynthe.com/norynthe-run-console.html"],
      ["External report concept", "A synthetic example of how a future traceable assessment record could become a bounded institutional finding.", "Synthetic sample · 7 min", "https://investors.norynthe.com/norynthe-customer-report.html"],
      ["Comparative report concept", "A synthetic multi-model format showing intended comparison, evidence, reviewer notes, and score context.", "Synthetic sample · 12 min", "https://investors.norynthe.com/norynthe-customer-report-appendix.html"],
    ],
  },
  {
    id: "financials",
    number: "04",
    eyebrow: "Capital plan",
    title: "$2M to establish the controlled evaluation laboratory.",
    description:
      "The plan establishes the physical, computational, evidentiary, security, governance, and operating environment required for repeatable independent evaluation.",
    cards: [
      ["Capital-to-capability plan", "The controlled laboratory base, compute, evidence systems, governance, founder-led runway, and 18-month proof milestones.", "Financials · 8 min", "https://investors.norynthe.com/norynthe-raise-plan.html"],
      ["Capital assumptions and runway", "The deployment model, open property and compute diligence, low-headcount operating logic, and milestone gates.", "Financials · 10 min", "https://investors.norynthe.com/norynthe-financial-model-assumptions.html"],
    ],
  },
  {
    id: "strategy",
    number: "05",
    eyebrow: "Category and adoption",
    title: "Adoption paths and the infrastructure behind independent evaluation.",
    description:
      "Norynthe is designed to sit outside the model owner’s control and create evidence the market can compare, inspect, and rely upon.",
    cards: [
      ["Institutional adoption paths", "How independent model credibility records support buyers, regulated enterprises, and strategic reviewers.", "Strategy · 8 min", "https://investors.norynthe.com/norynthe-enterprise-use-cases.html"],
      ["Tokens are fuel. Compute is infrastructure.", "Why Norynthe needs hybrid compute inside a wider system of method, evidence custody, governance, and external challenge.", "Strategy · 7 min", "https://investors.norynthe.com/power-of-compute.html"],
    ],
  },
];

const answers = [
  ["What exists now?", "Published research, Method v0.1, a founder-built evaluation architecture, prototype workflow surfaces, illustrative reports, and early smaller-model experimentation requiring a verified evidence bundle."],
  ["Why a laboratory?", "Independent evaluation requires controlled conditions, benchmark custody, repeatability, evidence preservation, challenge, correction, and institutional continuity."],
  ["What does capital unlock?", "The controlled base, hybrid compute, evidence systems, security, methodology, external review, and founder-led runway required to establish the laboratory."],
  ["Why low headcount?", "Norynthe scales through infrastructure, automation, governed workflows, and accumulated evidence—not a large early payroll."],
  ["What is the near-term proof?", "Complete run packages, repeatability and variance results, externally challenged methodology, traceable reports, design partners, and bounded paid pilots."],
  ["What compounds?", "The benchmark bank, evidence ledger, revision history, methodology, corrections, and institutional memory."],
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
          <h1>Building the independent laboratory for AI trust.</h1>
          <p className="lede">
            Norynthe is building a controlled evaluation environment for intelligent systems:
            governed benchmarks, hybrid compute, preserved evidence, repeatable methods,
            and institutional reporting outside the model owner’s control.
          </p>
          <div className="thesis-line">
            <span>Research discipline</span><i>→</i><span>Controlled laboratory</span><i>→</i><span>Evidence institutions can inspect</span>
          </div>
        </div>

        <aside className="access-card" aria-label="Investor access gate">
          <p className="kicker">Selected diligence</p>
          <h2>Unlock the review.</h2>
          <p>The portal connects the institutional thesis, founder-built foundation, laboratory architecture, capital plan, and proof program.</p>
          {!unlocked ? (
            <form onSubmit={unlock}>
              <label htmlFor="password">Access password</label>
              <div className="input-row">
                <input id="password" type="password" value={password} onChange={(e) => setPassword(e.target.value)} placeholder="Enter password" />
                <button type="submit">Unlock</button>
              </div>
              <p className="form-note" role="status">{error || "Shared for selected investor and strategic conversations. This static review gate is not a confidential data room."}</p>
            </form>
          ) : <p className="unlocked">Access active · Review materials below</p>}
        </aside>
      </section>

      <section className="proof-strip" aria-label="Company proof points">
        <div><strong>Founder-built foundation</strong><span>Published method, prototype workflow, and reporting architecture.</span></div>
        <div><strong>Institutional research</strong><span>The Papers preserve the discipline and revision history behind the system.</span></div>
        <div><strong>$2M laboratory plan</strong><span>Controlled base, compute, evidence, security, governance, and runway.</span></div>
        <div><strong>Low-headcount by design</strong><span>Founder-led operation scaled through infrastructure and disciplined automation.</span></div>
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
          <p>Review the founder-built foundation, the intended workflow, the laboratory it requires, and the evidence the funded phase must produce.</p>
        </div>
        <div className="preview-grid">
          <figure className="preview-main">
            <img src="https://investors.norynthe.com/previews/console-page-preview.jpg" alt="Norynthe scoring console with benchmark context and evaluation workflow" />
            <figcaption><span>Illustrative prototype</span><strong>Intended governed evaluation workflow</strong></figcaption>
          </figure>
          <figure><img src="https://investors.norynthe.com/previews/customer-report-page-preview.jpg" alt="Illustrative Norynthe report concept" /><figcaption><span>Synthetic sample</span><strong>Intended decision-report format</strong></figcaption></figure>
          <figure><img src="https://investors.norynthe.com/previews/financial-model-page-preview.jpg" alt="Norynthe laboratory capital plan preview" /><figcaption><span>Capital plan</span><strong>Infrastructure tied to proof</strong></figcaption></figure>
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
        <p>Norynthe is building the controlled laboratory, governed method, and durable evidence record required to evaluate, compare, and understand intelligent systems over time.</p>
        <a className="button-primary" href="https://tally.so/r/ZjezPA">Request a walkthrough ↗</a>
      </section>

      <footer>
        <a className="wordmark footer-wordmark" href="https://norynthe.com/">Norynthe.</a>
          <p>Selected investor review · Independent evaluation · Governed methodology · Traceable evidence</p>
        <div><a href="https://papers.norynthe.com/">Papers</a><a href="https://norynthe.com/privacy.html">Privacy</a><span>© 2026 Norynthe.</span></div>
      </footer>
    </main>
  );
}
