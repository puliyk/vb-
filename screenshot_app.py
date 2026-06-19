#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Playwright 自动截图：启动服务器 → 导航 → 操作 → 截图"""
import subprocess, time, os, signal, sys
from playwright.sync_api import sync_playwright

OUT = r'c:\Users\16137\Desktop\vb期末\screenshots'
os.makedirs(OUT, exist_ok=True)

# ── 启动 HTTP 服务器 ──
server = subprocess.Popen(
    [sys.executable, '-m', 'http.server', '8080', '--bind', '127.0.0.1'],
    cwd=r'c:\Users\16137\Desktop\vb期末',
    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
)
time.sleep(1.5)
print('[OK] Server started on http://127.0.0.1:8080')

BASE = 'http://127.0.0.1:8080/index.html'

JAVA_CODE = '''public static int factorial(int n) {
    if (n <= 1) {
        return 1;
    }
    return n * factorial(n - 1);
}'''

try:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={'width': 1440, 'height': 900})

        # ── 图5: 仪表盘全貌 ──
        print('[1/6] Dashboard screenshot...')
        page.goto(BASE, wait_until='networkidle', timeout=15000)
        time.sleep(1)

        # Dismiss onboarding if present
        try:
            skip = page.locator('text=跳过')
            if skip.is_visible(timeout=2000):
                skip.click()
                time.sleep(0.5)
        except:
            pass
        # Also try clicking anywhere to dismiss overlay
        try:
            overlay = page.locator('#onboardOverlay')
            if overlay.is_visible(timeout=1000):
                page.locator('#onboardSkipBtn').click(timeout=2000)
                time.sleep(0.5)
        except:
            pass

        page.screenshot(path=os.path.join(OUT, 'fig5_dashboard.png'), full_page=True)
        print('  [OK] fig5_dashboard.png')

        # ── 图6: 技术版说明书 ──
        print('[2/6] Tech doc after Java parse...')
        # Navigate to 说明书 panel
        page.locator('.nav-item[data-panel="doc"]').click()
        time.sleep(0.5)

        # Set language to Java
        page.locator('#langSelect').select_option('java')
        time.sleep(0.2)

        # Clear and paste code
        page.locator('#codeInput').fill(JAVA_CODE)
        time.sleep(0.2)

        # Click generate
        page.locator('#parseBtn').click()
        time.sleep(1.5)  # wait for parsing + render

        # Ensure tech tab is active
        page.locator('.tab:has-text("技术版")').click()
        time.sleep(0.3)

        page.screenshot(path=os.path.join(OUT, 'fig6_techdoc.png'), full_page=True)
        print('  [OK] fig6_techdoc.png')

        # ── 图7: 小白版说明书 (same code) ──
        print('[3/6] Beginner doc...')
        page.locator('.tab:has-text("小白版")').click()
        time.sleep(0.3)
        page.screenshot(path=os.path.join(OUT, 'fig7_beginnerdoc.png'), full_page=True)
        print('  [OK] fig7_beginnerdoc.png')

        # ── 图8: 响应式窄屏 ──
        print('[4/6] Responsive narrow screen...')
        page.set_viewport_size({'width': 375, 'height': 812})
        time.sleep(0.5)
        page.screenshot(path=os.path.join(OUT, 'fig8_responsive.png'), full_page=True)
        print('  [OK] fig8_responsive.png')

        # Reset viewport
        page.set_viewport_size({'width': 1440, 'height': 900})
        time.sleep(0.3)

        # ── 图9: 成就徽章墙 ──
        print('[5/6] Badge wall...')
        page.locator('.nav-item[data-panel="badges"]').click()
        time.sleep(0.8)
        page.screenshot(path=os.path.join(OUT, 'fig9_badges.png'), full_page=True)
        print('  [OK] fig9_badges.png')

        # ── 图10: AI 文档面板 ──
        print('[6/6] AI Doc panel...')
        page.locator('.nav-item[data-panel="aiDoc"]').click()
        time.sleep(0.8)
        page.screenshot(path=os.path.join(OUT, 'fig10_aidoc.png'), full_page=True)
        print('  [OK] fig10_aidoc.png')

        browser.close()
        print('\n[DONE] All 6 screenshots saved!')

finally:
    server.terminate()
    server.wait()
    print('[OK] Server stopped')

# List results
for f in sorted(os.listdir(OUT)):
    size_kb = os.path.getsize(os.path.join(OUT, f)) / 1024
    print(f'  {f} ({size_kb:.0f} KB)')
