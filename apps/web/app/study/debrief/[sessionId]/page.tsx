import { DebriefContent } from "@/components/study/debrief-content";

export default async function DebriefPage({ params }: { params: Promise<{ sessionId: string }> }) {
  const { sessionId } = await params;
  return <DebriefContent sessionId={sessionId} />;
}
