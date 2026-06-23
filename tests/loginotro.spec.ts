import { test, expect } from '@playwright/test';

test('Login inválido muestra error', async ({ page }) => {

  await page.goto('http://localhost:5173/login');

  await page.locator('input[type="email"]')
    .fill('admin@alvid.com');

  await page.locator('input[type="password"]')
    .fill('clave_incorrecta');

  await page.getByRole('button', { name: /ingresar/i })
    .click();

  // Sigue en login
  await expect(page).toHaveURL(/login/i);

  // Busca mensaje de error
  await expect(page.locator('body'))
    .toContainText(/error|incorrecta|inválida|credenciales/i);

});