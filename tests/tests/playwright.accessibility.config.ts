import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
    testDir: '.',

    use: {
        baseURL: 'http://localhost:5173',
        trace: 'on'
    },

    projects: [
        {
            name: 'chromium',
            use: { ...devices['Desktop Chrome'] }
        }
    ]
});