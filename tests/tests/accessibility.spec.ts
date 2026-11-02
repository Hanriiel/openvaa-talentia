import { expect, test } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

test.describe('Accessibility', () => {
    test.setTimeout(120000);

    test('voter app has no automatically detectable accessibility violations', async ({ page }) => {
        const checkAccessibility = async (view: string) => {
            const results = await new AxeBuilder({ page })
                .disableRules(['tabindex'])
                .exclude('.vaa-basicPage-actions [disabled]')
                .analyze();

            console.log(`Accessibility check: ${view}`);

            if (results.violations.length > 0) {
                console.log(
                    results.violations.map((violation) => ({
                        id: violation.id,
                        impact: violation.impact,
                        elements: violation.nodes.map((node) => node.html)
                    }))
                );
            }

            expect(
                results.violations,
                `Accessibility violations: ${view}`
            ).toEqual([]);
        };

        // Etusivu
        await page.goto('/fi');

        await expect(
            page.getByRole('heading', {
                name: '10 kysymystä sosiaalialasta ja varhaiskasvatuksesta'
            })
        ).toBeVisible({ timeout: 15000 });

        await checkAccessibility('front page');

        // Aloita vaalikone
        await page.getByRole('button', {
            name: 'Löydä sopivimmat ehdokkaat!'
        }).click();

        await page.getByRole('button', { name: 'Jatka' }).click();

        // Valitse vaalipiiri
        await page.getByPlaceholder('Valitse Vaalipiirit').click();
        await page.getByText('Helsingin vaalipiiri').click();
        await page.getByRole('button', { name: 'Jatka' }).click();

        // Siirry kysymyksiin
        await page.getByRole('button', {
            name: 'Vastaa 10 kysymykseen'
        }).click();

        await page.getByRole('button', { name: 'Jatka' }).click();

        // Odota ensimmäisen kysymyksen latautumista
        await expect(
            page.getByLabel('Täysin eri mieltä')
        ).toBeVisible({ timeout: 15000 });

        await checkAccessibility('first question');

        // Vastaa kaikkiin 10 kysymykseen
        const answers = [
            'Täysin eri mieltä',
            'Osittain eri mieltä',
            'Ei samaa eikä eri mieltä',
            'Osittain samaa mieltä',
            'Täysin samaa mieltä',
            'Täysin eri mieltä',
            'Osittain eri mieltä',
            'Ei samaa eikä eri mieltä',
            'Osittain samaa mieltä',
            'Täysin samaa mieltä'
        ];

        for (const [index, answer] of answers.entries()) {
            await page.getByLabel(answer).check();

            // Odota automaattinen siirtyminen vastauksen jälkeen
            await page.waitForTimeout(1000);

            const continueButton = page.getByRole('button', {
                name: 'Jatka'
            });

            // Kysymysten 3, 6 ja 8 jälkeen tulee kategorian välisivu
            if (index === 2 || index === 5 || index === 7) {
                await expect(continueButton).toBeVisible({
                    timeout: 15000
                });

                await checkAccessibility(
                    `after question ${index + 1} - category page`
                );

                await continueButton.click();

                await expect(
                    page.getByLabel(answers[index + 1])
                ).toBeVisible({
                    timeout: 15000
                });
            }

            await checkAccessibility(`after question ${index + 1}`);
        }

        // Varmista, että päästiin tulossivulle
        await expect(page).toHaveURL(/\/fi\/results/, {
            timeout: 15000
        });

        await checkAccessibility('results page');

        console.log('Accessibility test completed');
    });
});