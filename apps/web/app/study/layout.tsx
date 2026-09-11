import type { ReactNode } from "react";
import { StudyShell } from "@/components/study/study-shell";

export default function StudyLayout({ children }: { children: ReactNode }) {
  return <StudyShell>{children}</StudyShell>;
}
