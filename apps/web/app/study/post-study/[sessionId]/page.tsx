import { QuestionnaireForm } from "@/components/study/questionnaire-form";

export default async function PostStudyPage({
  params,
}: {
  params: Promise<{ sessionId: string }>;
}) {
  const { sessionId } = await params;
  return <QuestionnaireForm sessionId={sessionId} />;
}
