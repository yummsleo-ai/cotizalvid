import { test, expect } from '@playwright/test';

test('Login con contraseña incorrecta', async ({ page }) => {

  await page.goto('http://localhost:5173/login');

  // Usuario válido
  await page.locator('input[type="email"]')
    .fill('admin@alvid.com');

  // Contraseña incorrecta
  await page.locator('input[type="password"]')
    .fill('123456');

  await page.getByRole('button', { name: /ingresar/i })
    .click();

  // Debe permanecer en login
  await expect(page).toHaveURL(/login/i);

});
