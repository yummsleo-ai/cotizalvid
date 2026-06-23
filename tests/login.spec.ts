import { test, expect } from '@playwright/test';

test.describe('Pruebas de Caja Negra - Login', () => {

  test('Carga correctamente la página de login', async ({ page }) => {
    await page.goto('http://localhost:5173/login');

    await expect(page.locator('input[type="email"]')).toBeVisible();
    await expect(page.locator('input[type="password"]')).toBeVisible();
  });

  test('Los campos usuario y contraseña existen', async ({ page }) => {
    await page.goto('http://localhost:5173/login');

    await expect(page.locator('input')).toHaveCount(2);
  });

  test('Intento de login con campos vacíos', async ({ page }) => {
    await page.goto('http://localhost:5173/login');

    await page.locator('button').click();

    await page.screenshot({
      path: 'evidencias/login-campos-vacios.png',
      fullPage: true
    });
  });

  test('Intento de login con contraseña incorrecta', async ({ page }) => {
    await page.goto('http://localhost:5173/login');

    await page.locator('input').nth(0).fill('admin@alvid.com');
    await page.locator('input[type="password"]').fill('incorrecta');

    await page.locator('button').click();

    await page.screenshot({
      path: 'evidencias/login-password-incorrecta.png',
      fullPage: true
    });
  });

  test('Intento de login con usuario inexistente', async ({ page }) => {
    await page.goto('http://localhost:5173/login');

    await page.locator('input').nth(0).fill('usuario@falso.com');
    await page.locator('input[type="password"]').fill('123456');

    await page.locator('button').click();

    await page.screenshot({
      path: 'evidencias/login-usuario-inexistente.png',
      fullPage: true
    });
  });

  test('Login válido', async ({ page }) => {
    await page.goto('http://localhost:5173/login');

    await page.locator('input[type="email"]').fill('admin@alvid.com');
    await page.locator('input[type="password"]').fill('alvid2024');

    await page.locator('button').click();

    await page.waitForTimeout(5000);

    console.log('URL actual:', page.url());

    await page.screenshot({
      path: 'evidencias/login-debug.png',
      fullPage: true
    });
  });

});