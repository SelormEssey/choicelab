import Link from "next/link";
import type { ReactNode } from "react";

export function StudyShell({ children }: { children: ReactNode }) {
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
