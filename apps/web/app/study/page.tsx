import Link from "next/link";

export default function StudyIntroduction() {
  return (
    <section className="study-intro">
      <p className="eyebrow">ChoiceLab study</p>
      <h1>How do people respond to decision aids?</h1>
      <p>
        This short study uses fictional software and resource-selection scenarios. You will compare
        options, make choices, and report how confident you feel.
      </p>
      <div className="intro-details">
        <div>
          <strong>About 10 decisions</strong>
          <span>Fictional scenarios with no real-world consequences.</span>
        </div>
        <div>
          <strong>Voluntary participation</strong>
          <span>You can stop at any point and view a debrief.</span>
        </div>
        <div>
          <strong>Anonymous session</strong>
          <span>No account or identifying information is requested.</span>
        </div>
      </div>
      <Link className="button-link" href="/study/consent">
        Read study information
      </Link>
    </section>
  );
}
