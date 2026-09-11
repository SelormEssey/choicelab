const process = ["Research", "Design", "Build", "Evaluate", "Iterate"];

export default function Home() {
  return (
    <main>
      <header className="site-header">
        <a className="wordmark" href="#top" aria-label="ChoiceLab home">
          <span className="wordmark-mark" aria-hidden="true">
            C
          </span>
          <span>ChoiceLab</span>
        </a>
        <span className="status">
          <span aria-hidden="true" /> Research &amp; Development
        </span>
      </header>

      <section className="hero" id="top" aria-labelledby="hero-title">
        <p className="eyebrow">Human-AI decision research</p>
        <h1 id="hero-title">
          Keep the judgment
          <br />
          with the person.
        </h1>
        <p className="hero-copy">
          ChoiceLab explores how recommendations, explanations, and confidence cues shape human
          judgment and reliance.
        </p>
        <a className="scroll-cue" href="/study">
          Try the study <span aria-hidden="true">→</span>
        </a>
      </section>

      <section className="problem section-rule" id="problem" aria-labelledby="problem-title">
        <div className="section-label">
          <span>01</span>
          <p>Problem space</p>
        </div>
        <div className="section-content">
          <h2 id="problem-title">A recommendation can be useful. It can also hide the decision.</h2>
          <p>
            Decision aids can change how people evaluate options. ChoiceLab studies how
            recommendation, explanation, and confidence cues influence choices, trust, and reliance.
          </p>
          <p className="note">
            This is a framing for investigation, not a claim established by this project.
          </p>
        </div>
      </section>

      <section className="question section-rule" aria-labelledby="question-title">
        <div className="section-label">
          <span>02</span>
          <p>Provisional question</p>
        </div>
        <div className="section-content">
          <p className="question-kicker">
            The research question will be refined after formative research.
          </p>
          <blockquote id="question-title">
            How do AI recommendations, explanations, and confidence cues affect human
            decision-making and reliance?
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
            <h2 id="reflection-title">Controlled decision aids</h2>
            <p>
              The study uses reproducible decision-aid fixtures so each participant experiences an
              intentional combination of recommendation, explanation, or confidence information.
            </p>
          </div>
          <div className="concept-card" aria-label="Illustrative reflection sequence">
            <p className="concept-label">Study interaction</p>
            <ol>
              <li>
                <span>01</span> Review a fictional scenario
              </li>
              <li>
                <span>02</span> Compare available options
              </li>
              <li>
                <span>03</span> Make an active choice
              </li>
              <li>
                <span>04</span> Reflect on confidence
              </li>
            </ol>
            <p className="concept-footnote">
              A research prototype with controlled experimental stimuli.
            </p>
          </div>
        </div>
      </section>

      <section className="future section-rule" aria-labelledby="future-title">
        <div>
          <p className="eyebrow">Project status</p>
          <h2 id="future-title">
            The Decision Lab is
            <br />
            ready to explore.
          </h2>
        </div>
        <a className="button-link" href="/study">
          Start the study
        </a>
      </section>

      <footer>
        <span>ChoiceLab</span>
        <span>HCI research project</span>
      </footer>
    </main>
  );
}
