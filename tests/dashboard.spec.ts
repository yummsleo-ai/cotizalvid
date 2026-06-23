import { test } from '@playwright/test';

test('Generar evidencia del Dashboard', async ({ page }) => {

  await page.goto('http://localhost:5173');

  await page.screenshot({
    path: 'evidencias/dashboard.png',
    fullPage: true
  });

});