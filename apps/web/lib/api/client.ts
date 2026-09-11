import type { Debrief, Questionnaire, Session, Trial } from "./types";

type ApiError = Error & { status?: number };

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`/api/study${path}`, {
    ...init,
    headers: { "Content-Type": "application/json", ...init?.headers },
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
  createSession: () =>
    request<{ session_id: string }>("/sessions", {
      method: "POST",
      body: JSON.stringify({ consent: true }),
    }),
  getSession: (id: string) => request<Session>(`/sessions/${id}`),
  getCurrentTrial: (id: string) => request<Trial>(`/sessions/${id}/current-trial`),
  createAttempt: (id: string, trialId: string) =>
    request<{ attempt_id: string }>(`/sessions/${id}/trial-attempts`, {
      method: "POST",
      body: JSON.stringify({ trial_id: trialId }),
    }),
  submitResponse: (id: string, payload: Record<string, unknown>) =>
    request<{ next_status: string }>(`/sessions/${id}/responses`, {
      method: "POST",
      body: JSON.stringify(payload),
    }),
  getQuestionnaire: (id: string) => request<Questionnaire>(`/sessions/${id}/questionnaire`),
  submitQuestionnaire: (id: string, payload: Record<string, unknown>) =>
    request<void>(`/sessions/${id}/post-study`, { method: "POST", body: JSON.stringify(payload) }),
  stop: (id: string) => request<void>(`/sessions/${id}/stop`, { method: "POST" }),
  getDebrief: (id: string) => request<Debrief>(`/sessions/${id}/debrief`),
};
