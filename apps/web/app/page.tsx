const process = ["Research", "Design", "Build", "Evaluate", "Iterate"];

export default function Home() {
  return (
    <main>
      <header className="site-header">
        <a className="wordmark" href="#top" aria-label="ChoiceLab home">
          <span className="wordmark-mark" aria-hidden="true">C</span>
          <span>ChoiceLab</span>
        </a>
        <span className="status"><span aria-hidden="true" /> Research &amp; Development</span>
      </header>

      <section className="hero" id="top" aria-labelledby="hero-title">
        <p className="eyebrow">Human-centered financial decision support</p>
        <h1 id="hero-title">Keep the judgment<br />with the person.</h1>
        <p className="hero-copy">
          ChoiceLab explores how intelligent financial interfaces can help people understand tradeoffs
          without replacing their judgment.
        </p>
        <a className="scroll-cue" href="#problem">Explore the research <span aria-hidden="true">↓</span></a>
      </section>

      <section className="problem section-rule" id="problem" aria-labelledby="problem-title">
        <div className="section-label">
          <span>01</span>
          <p>Problem space</p>
        </div>
        <div className="section-content">
          <h2 id="problem-title">A recommendation can be useful. It can also hide the decision.</h2>
          <p>
            Financial decision-support systems often prioritize a single recommendation. ChoiceLab begins
            from a different possibility: people may need support examining assumptions, consequences,
            and tradeoffs before deciding what is right for them.
          </p>
          <p className="note">This is a framing for investigation, not a claim established by this project.</p>
        </div>
      </section>

      <section className="question section-rule" aria-labelledby="question-title">
        <div className="section-label">
          <span>02</span>
          <p>Provisional question</p>
        </div>
        <div className="section-content">
          <p className="question-kicker">The research question will be refined after formative research.</p>
          <blockquote id="question-title">
            How does reflection-first intelligent assistance affect users&apos; understanding, perceived agency,
            and trust compared with recommendation-first assistance during financial decision-making?
          </blockquote>
        </div>
      </section>

      <section className="process section-rule" aria-labelledby="process-title">
        <div className="section-label">
          <span>03</span>
          <p id="process-title">Project process</p>
        </div>
        <ol className="process-list">
          {process.map((step, index) => (
            <li key={step}>
              <span>{String(index + 1).padStart(2, "0")}</span>
              <strong>{step}</strong>
              {index < process.length - 1 && <i aria-hidden="true">→</i>}
            </li>
          ))}
        </ol>
      </section>

      <section className="reflection section-rule" aria-labelledby="reflection-title">
        <div className="section-label">
          <span>04</span>
          <p>Interaction concept</p>
        </div>
        <div className="reflection-grid">
          <div>
            <h2 id="reflection-title">Reflection first</h2>
            <p>
              Rather than starting with an answer, a reflection-first interaction could make the reasoning
              visible: what matters, what changes across options, and which uncertainties remain.
            </p>
          </div>
          <div className="concept-card" aria-label="Illustrative reflection sequence">
            <p className="concept-label">An early interaction direction</p>
            <ol>
              <li><span>01</span> Name what matters in this decision</li>
              <li><span>02</span> Examine a tradeoff</li>
              <li><span>03</span> Compare possible consequences</li>
              <li><span>04</span> Decide with context</li>
            </ol>
            <p className="concept-footnote">A design hypothesis to examine through research.</p>
          </div>
        </div>
      </section>

      <section className="future section-rule" aria-labelledby="future-title">
        <div>
          <p className="eyebrow">Project status</p>
          <h2 id="future-title">The Decision Lab is<br />coming later.</h2>
        </div>
        <button type="button" disabled aria-describedby="future-note">In development</button>
        <p id="future-note" className="sr-only">The Decision Lab is not available yet.</p>
      </section>

      <footer>
        <span>ChoiceLab</span>
        <span>HCI research project</span>
      </footer>
    </main>
  );
}
