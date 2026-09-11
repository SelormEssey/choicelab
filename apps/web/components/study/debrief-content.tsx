"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { studyApi } from "@/lib/api/client";
import type { Debrief } from "@/lib/api/types";
import { LoadingState, StudyError } from "./study-shell";

export function DebriefContent({ sessionId }: { sessionId: string }) {
  const [debrief, setDebrief] = useState<Debrief>();
  const [error, setError] = useState("");
  useEffect(() => {
    studyApi
      .getDebrief(sessionId)
      .then(setDebrief)
      .catch((caught) =>
        setError(caught instanceof Error ? caught.message : "Unable to load the debrief."),
      );
  }, [sessionId]);
  if (error)
    return (
      <section className="study-card">
        <StudyError message={error} />
      </section>
    );
  if (!debrief) return <LoadingState />;
  return (
    <section className="debrief">
      <p className="eyebrow">Study debrief</p>
      <h1>{debrief.title}</h1>
      {debrief.paragraphs.map((paragraph) => (
        <p key={paragraph}>{paragraph}</p>
      ))}
      <Link className="button-link" href="/">
        Return to ChoiceLab
      </Link>
    </section>
  );
}
