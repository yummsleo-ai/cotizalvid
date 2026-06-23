import { test, expect } from '@playwright/test';

test('CN05 - Precio negativo', async ({ page }) => {

  // Login
  await page.goto('http://localhost:5173/login');

  await page.locator('input').nth(0).fill('admin@alvid.com');
  await page.locator('input[type="password"]').fill('alvid2024');

  await page.locator('button').click();

  await page.waitForURL(url => !url.pathname.includes('/login'));

  // Materiales
  await page.goto('http://localhost:5173/materiales');

  // Nombre
  await page.getByLabel(/nombre/i).fill('Material Negativo');

  // Precio
  await page.getByLabel(/precio/i).fill('-10');

  // Guardar
  await page.getByRole('button', { name: /guardar/i }).click();

  // Evidencia
  await page.screenshot({
    path: 'evidencias/cn05-precio-negativo.png',
    fullPage: true
  });
});