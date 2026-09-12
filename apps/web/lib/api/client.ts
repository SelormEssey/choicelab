import type { Debrief, Questionnaire, Session, Trial } from "./types";

type ApiError = Error & { status?: number };

const tokenKey = (sessionId: string) => `choicelab:session:${sessionId}`;

async function request<T>(path: string, init?: RequestInit, sessionId?: string): Promise<T> {
  const sessionToken = sessionId ? window.sessionStorage.getItem(tokenKey(sessionId)) : null;
  const response = await fetch(`/api/study${path}`, {
    ...init,
    headers: {
      "Content-Type": "application/json",
      ...(sessionToken ? { "X-Session-Token": sessionToken } : {}),
      ...init?.headers,
    },
    cache: "no-store",
  });
  if (!response.ok) {
    const body = await response.json().catch(() => null);
    const error: ApiError = new Error(body?.detail || "Something went wrong. Please try again.");
    error.status = response.status;
    throw error;
  }
  if (response.status === 204) return undefined as T;
  return response.json() as Promise<T>;
}

export const studyApi = {
  createSession: async () => {
    const session = await request<{ session_id: string; session_token: string }>("/sessions", {
      method: "POST",
      body: JSON.stringify({ consent: true }),
    });
    window.sessionStorage.setItem(tokenKey(session.session_id), session.session_token);
    return { session_id: session.session_id };
  },
  getSession: (id: string) => request<Session>(`/sessions/${id}`, undefined, id),
  getCurrentTrial: (id: string) => request<Trial>(`/sessions/${id}/current-trial`, undefined, id),
  createAttempt: (id: string, trialId: string) =>
    request<{ attempt_id: string }>(
      `/sessions/${id}/trial-attempts`,
      {
        method: "POST",
        body: JSON.stringify({ trial_id: trialId }),
      },
      id,
    ),
  submitResponse: (id: string, payload: Record<string, unknown>) =>
    request<{ next_status: string }>(
      `/sessions/${id}/responses`,
      {
        method: "POST",
        body: JSON.stringify(payload),
      },
      id,
    ),
  getQuestionnaire: (id: string) =>
    request<Questionnaire>(`/sessions/${id}/questionnaire`, undefined, id),
  submitQuestionnaire: (id: string, payload: Record<string, unknown>) =>
    request<void>(
      `/sessions/${id}/post-study`,
      { method: "POST", body: JSON.stringify(payload) },
      id,
    ),
  stop: (id: string) => request<void>(`/sessions/${id}/stop`, { method: "POST" }, id),
  getDebrief: (id: string) => request<Debrief>(`/sessions/${id}/debrief`, undefined, id),
};
