"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import { useRouter } from "next/navigation";
import { studyApi } from "@/lib/api/client";
import type { Session, Trial } from "@/lib/api/types";
import { LoadingState, StudyError } from "./study-shell";

export function SessionExperience({ sessionId }: { sessionId: string }) {
  const [session, setSession] = useState<Session>();
  const [trial, setTrial] = useState<Trial>();
  const [attemptId, setAttemptId] = useState("");
  const [selection, setSelection] = useState("");
  const [confidence, setConfidence] = useState("");
  const [reasoning, setReasoning] = useState("");
  const [startedAt, setStartedAt] = useState(0);
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);
  const router = useRouter();
  const requestKey = useRef("");

  const load = useCallback(async () => {
    setError("");
    try {
      const nextSession = await studyApi.getSession(sessionId);
      if (nextSession.status === "QUESTIONNAIRE_PENDING")
        return router.replace(`/study/post-study/${sessionId}`);
      if (nextSession.status === "COMPLETED" || nextSession.status === "STOPPED")
        return router.replace(`/study/debrief/${sessionId}`);
      const nextTrial = await studyApi.getCurrentTrial(sessionId);
      const attempt = await studyApi.createAttempt(sessionId, nextTrial.id);
      setSession(nextSession);
      setTrial(nextTrial);
      setAttemptId(attempt.attempt_id);
      setStartedAt(performance.now());
      setSelection("");
      setConfidence("");
      setReasoning("");
      requestKey.current = crypto.randomUUID();
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "Unable to load this session.");
    }
  }, [router, sessionId]);

  useEffect(() => {
    const timer = window.setTimeout(() => void load(), 0);
    return () => window.clearTimeout(timer);
  }, [load]);

  async function submit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!trial || !attemptId || !selection || confidence === "") return;
    setBusy(true);
    setError("");
    try {
      const responseTime = Math.round(performance.now() - startedAt);
      const receipt = await studyApi.submitResponse(sessionId, {
        trial_id: trial.id,
        attempt_id: attemptId,
        selected_option_id: selection,
        participant_confidence: Number(confidence),
        reasoning: reasoning || null,
        response_time_ms: responseTime,
        idempotency_key: requestKey.current,
      });
      if (receipt.next_status === "QUESTIONNAIRE_PENDING")
        router.replace(`/study/post-study/${sessionId}`);
      else await load();
    } catch (caught) {
      setError(
        caught instanceof Error
          ? caught.message
          : "Your response was not saved. You can try again.",
      );
    } finally {
      setBusy(false);
    }
  }

  async function stop() {
    if (
      !window.confirm(
        "Stop this study? You will not be able to resume trials after viewing the debrief.",
      )
    )
      return;
    setBusy(true);
    try {
      await studyApi.stop(sessionId);
      router.replace(`/study/debrief/${sessionId}`);
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "Unable to stop the session.");
      setBusy(false);
    }
  }

  if (error && !trial)
    return (
      <section className="study-card">
        <StudyError message={error} />
        <button onClick={() => void load()}>Try again</button>
      </section>
    );
  if (!trial || !session) return <LoadingState />;
  return (
    <section className="trial-layout" aria-labelledby="trial-title">
      <div className="progress-row">
        <p>
          Decision {trial.trial_number} of {trial.total_trials}
        </p>
        <progress value={trial.trial_number} max={trial.total_trials}>
          Decision {trial.trial_number} of {trial.total_trials}
        </progress>
      </div>
      <div className="trial-heading">
        <p className="eyebrow">Fictional scenario</p>
        <h1 id="trial-title">{trial.title}</h1>
        <p>{trial.context}</p>
        <div className="criteria">
          <strong>Decision criteria</strong>
          <span>{trial.criteria}</span>
        </div>
      </div>
      {trial.assistance && (
        <aside className="assistance" aria-label="Decision aid information">
          <p className="eyebrow">Decision aid</p>
          <p>
            <strong>Suggested option: {trial.assistance.recommendation_name}</strong>
          </p>
          {trial.assistance.explanation && <p>{trial.assistance.explanation}</p>}
          {trial.assistance.confidence_percent !== null && (
            <p>
              Reported confidence: <strong>{trial.assistance.confidence_percent}%</strong>
            </p>
          )}
        </aside>
      )}
      <form onSubmit={submit} className="decision-form">
        <fieldset>
          <legend>{trial.decision_question}</legend>
          <div className="option-grid">
            {trial.options.map((option) => (
              <label className="option-card" key={option.id}>
                <input
                  type="radio"
                  name="option"
                  value={option.id}
                  checked={selection === option.id}
                  onChange={() => setSelection(option.id)}
                  required
                />
                <span>
                  <strong>{option.name}</strong>
                  <dl>
                    {trial.attribute_labels.map((label) => (
                      <div key={label}>
                        <dt>{label}</dt>
                        <dd>{option.attributes[label]}</dd>
                      </div>
                    ))}
                  </dl>
                </span>
              </label>
            ))}
          </div>
        </fieldset>
        <label className="confidence-field">
          How confident are you in your choice?
          <input
            type="number"
            required
            min="0"
            max="100"
            inputMode="numeric"
            value={confidence}
            onChange={(event) => setConfidence(event.target.value)}
            aria-describedby="confidence-help"
          />
          <span id="confidence-help">
            0 = not confident · 50 = moderately confident · 100 = completely confident
          </span>
        </label>
        <label className="reasoning-field">
          What influenced your choice? <span>(optional)</span>
          <textarea
            maxLength={800}
            value={reasoning}
            onChange={(event) => setReasoning(event.target.value)}
          />
        </label>
        {error && <StudyError message={error} />}
        <div className="study-actions">
          <button type="button" className="text-action" disabled={busy} onClick={() => void stop()}>
            Stop study
          </button>
          <button disabled={busy || !selection || confidence === ""}>
            {busy ? "Saving…" : "Continue"}
          </button>
        </div>
      </form>
    </section>
  );
}
