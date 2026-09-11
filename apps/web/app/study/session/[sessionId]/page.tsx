import { SessionExperience } from "@/components/study/session-experience";

export default async function SessionPage({ params }: { params: Promise<{ sessionId: string }> }) {
  const { sessionId } = await params;
  return <SessionExperience sessionId={sessionId} />;
}
