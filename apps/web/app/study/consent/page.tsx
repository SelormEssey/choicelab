import { ConsentForm } from "@/components/study/consent-form";

export default function ConsentPage() {
  return (
    <section className="study-card">
      <p className="eyebrow">Study information and consent</p>
      <h1>Your choice to take part.</h1>
      <ConsentForm />
    </section>
  );
}
