"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { studyApi } from "@/lib/api/client";
import { StudyError } from "./study-shell";

export function ConsentForm() {
  const [agreed, setAgreed] = useState(false);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const router = useRouter();

  async function begin() {
    if (!agreed) return;
    setBusy(true);
    setError("");
    try {
      const session = await studyApi.createSession();
      router.push(`/study/session/${session.session_id}`);
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "Unable to start the study.");
      setBusy(false);
    }
  }

  return (
    <form
      className="consent-form"
      onSubmit={(event) => {
        event.preventDefault();
        void begin();
      }}
    >
      <fieldset>
        <legend>Before you decide</legend>
        <p>
          This is a research prototype about how people interact with decision support.
          Participation is voluntary.
        </p>
        <ul>
          <li>You will complete fictional software and resource-selection scenarios.</li>
          <li>An AI-like decision aid may appear in some scenarios.</li>
          <li>
            Your choices, confidence, optional reasoning, and response time may be recorded for
            research and evaluation.
          </li>
          <li>
            No name, email, account, demographic identity, or sensitive personal information is
            required.
          </li>
          <li>You may stop at any time. Stopping ends the session and opens a debrief.</li>
        </ul>
        <label className="check-row">
          <input
            type="checkbox"
            checked={agreed}
            onChange={(event) => setAgreed(event.target.checked)}
          />
          <span>I have read this information and agree to take part.</span>
        </label>
      </fieldset>
      {error && <StudyError message={error} />}
      <div className="study-actions">
        <Link className="text-action" href="/">
          Leave study
        </Link>
        <button type="submit" disabled={!agreed || busy}>
          {busy ? "Starting…" : "I agree to participate"}
        </button>
      </div>
    </form>
  );
}
