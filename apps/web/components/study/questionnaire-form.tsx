"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { studyApi } from "@/lib/api/client";
import type { Questionnaire } from "@/lib/api/types";
import { LoadingState, StudyError } from "./study-shell";

export function QuestionnaireForm({ sessionId }: { sessionId: string }) {
  const [questionnaire, setQuestionnaire] = useState<Questionnaire>();
  const [answers, setAnswers] = useState<Record<string, number>>({});
  const [freeText, setFreeText] = useState("");
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);
  const router = useRouter();

  useEffect(() => {
    studyApi
      .getQuestionnaire(sessionId)
      .then(setQuestionnaire)
      .catch((caught) =>
        setError(caught instanceof Error ? caught.message : "Unable to load the questionnaire."),
      );
  }, [sessionId]);
  if (error && !questionnaire)
    return (
      <section className="study-card">
        <StudyError message={error} />
      </section>
    );
  if (!questionnaire) return <LoadingState />;
  const complete = questionnaire.items.every((item) => answers[item.id]);
  async function submit(event: React.FormEvent) {
    event.preventDefault();
    if (!complete) return;
    setBusy(true);
    setError("");
    try {
      await studyApi.submitQuestionnaire(sessionId, {
        responses: answers,
        free_text: freeText || null,
      });
      router.replace(`/study/debrief/${sessionId}`);
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "Unable to save the questionnaire.");
      setBusy(false);
    }
  }
  return (
    <form className="questionnaire" onSubmit={submit}>
      <p className="eyebrow">Post-study questionnaire</p>
      <h1>Reflect on the study experience.</h1>
      <p className="form-intro">Please select one response for each statement.</p>
      {questionnaire.items.map((item) => (
        <fieldset key={item.id} className="likert">
          <legend>{item.statement}</legend>
          <div>
            {Object.entries(questionnaire.scale).map(([value, label]) => (
              <label key={value}>
                <input
                  type="radio"
                  name={item.id}
                  value={value}
                  checked={answers[item.id] === Number(value)}
                  onChange={() => setAnswers({ ...answers, [item.id]: Number(value) })}
                  required
                />
                <span>
                  {value}
                  <small>{label}</small>
                </span>
              </label>
            ))}
          </div>
        </fieldset>
      ))}
      <label className="reasoning-field">
        {questionnaire.free_text_prompt} <span>(optional)</span>
        <textarea
          maxLength={1000}
          value={freeText}
          onChange={(event) => setFreeText(event.target.value)}
        />
      </label>
      {error && <StudyError message={error} />}
      <div className="study-actions">
        <button disabled={!complete || busy}>{busy ? "Saving…" : "Complete study"}</button>
      </div>
    </form>
  );
}
