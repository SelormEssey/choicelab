import Link from "next/link";
import type { ReactNode } from "react";

export function StudyShell({ children }: { children: ReactNode }) {
  const demoMode = process.env.NEXT_PUBLIC_CHOICELAB_DEMO_MODE === "true";
  return (
    <main className="study-shell">
      <header className="study-header">
        <Link className="wordmark" href="/" aria-label="ChoiceLab home">
          <span className="wordmark-mark" aria-hidden="true">
            C
          </span>
          <span>ChoiceLab</span>
        </Link>
        <span className="study-label">Human-AI decision study</span>
      </header>
      {demoMode && (
        <p className="demo-notice" role="note">
          Public demonstration only. Submissions are disposable product-test records and are not
          research data.
        </p>
      )}
      {children}
    </main>
  );
}

export function LoadingState() {
  return (
    <p className="study-status" role="status">
      Preparing your study session…
    </p>
  );
}

export function StudyError({ message }: { message: string }) {
  return (
    <p className="study-error" role="alert">
      {message}
    </p>
  );
}
