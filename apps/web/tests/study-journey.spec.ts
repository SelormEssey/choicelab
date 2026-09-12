import { expect, test } from "@playwright/test";

test("participant can complete the study and reach the debrief", async ({ page }) => {
  await page.goto("/");
  await page.getByRole("link", { name: "Try the study" }).click();
  await page.getByRole("link", { name: "Read study information" }).click();
  await page.getByRole("checkbox").check();
  await page.getByRole("button", { name: "I agree to participate" }).click();

  for (let decision = 1; decision <= 10; decision += 1) {
    await expect(page.getByText(`Decision ${decision} of 10`)).toBeVisible();
    await page.locator('.decision-form input[type="radio"]').first().check();
    await page.getByLabel("How confident are you in your choice?").fill("50");
    await page.getByRole("button", { name: "Continue" }).click();
  }

  await expect(
    page.getByRole("heading", { name: "Reflect on the study experience." }),
  ).toBeVisible();
  for (const fieldset of await page.locator("fieldset.likert").all()) {
    await fieldset.locator('input[value="3"]').check();
  }
  await page.getByRole("button", { name: "Complete study" }).click();

  await expect(page.getByRole("heading", { name: "Thank you for taking part" })).toBeVisible();
  await expect(page.getByText("Some were intentionally incorrect")).toBeVisible();
});

test("a session URL cannot be resumed without its browser token", async ({ page, request }) => {
  const created = await request.post("http://127.0.0.1:8000/v1/study/sessions", {
    data: { consent: true },
  });
  const { session_id: sessionId } = await created.json();

  await page.goto(`/study/session/${sessionId}`);
  await expect(page.getByRole("alert")).toContainText("session token is required");
});
