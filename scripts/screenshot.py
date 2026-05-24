"""Take screenshots of the Hindsight app in all three views."""
import asyncio
import os
from playwright.async_api import async_playwright

SCREENSHOT_DIR = os.path.join(os.path.dirname(__file__), "..", "docs", "screenshots")
BASE_URL = "http://localhost:3000"


async def main():
    os.makedirs(SCREENSHOT_DIR, exist_ok=True)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            viewport={"width": 1440, "height": 900},
            device_scale_factor=2,
        )
        page = await context.new_page()

        # ── 1. Form view (empty) ──
        print("[1/8] Loading form view...")
        await page.goto(BASE_URL, wait_until="networkidle")
        await page.wait_for_timeout(2000)
        await page.screenshot(
            path=os.path.join(SCREENSHOT_DIR, "01-input-form.png"),
            full_page=True,
        )
        print("  ✓ 01-input-form.png")

        # ── 2. Fill form ──
        print("[2/8] Filling form...")
        # The form has: year (number), alternative (text), current (text), feeling (text)
        # Use placeholder text to locate fields
        year_input = page.locator('input[placeholder="2018"]')
        alt_input = page.locator('input[placeholder="去深圳加入腾讯"]')
        current_input = page.locator('input[placeholder="留在老家国企"]')
        feeling_input = page.locator('input[placeholder="平淡但安稳"]')

        await year_input.fill("2018")
        await page.wait_for_timeout(200)
        await alt_input.fill("去深圳加入腾讯做产品经理")
        await page.wait_for_timeout(200)
        await current_input.fill("留在成都一家小公司")
        await page.wait_for_timeout(200)
        await feeling_input.fill("平淡但偶尔会想如果")
        await page.wait_for_timeout(500)

        await page.screenshot(
            path=os.path.join(SCREENSHOT_DIR, "01b-form-filled.png"),
            full_page=True,
        )
        print("  ✓ 01b-form-filled.png")

        # ── 3. Submit ──
        print("[3/8] Submitting form...")
        submit_btn = page.locator('button:has-text("开始推演")')
        await submit_btn.click()
        await page.wait_for_timeout(2000)

        # ── 4. Agent console (early) ──
        print("[4/8] Capturing agent console (early)...")
        await page.screenshot(
            path=os.path.join(SCREENSHOT_DIR, "02-agent-console.png"),
            full_page=True,
        )
        print("  ✓ 02-agent-console.png")

        # ── 5. Agent console (mid-progress) ──
        print("[5/8] Waiting for mid-progress...")
        await page.wait_for_timeout(10000)
        await page.screenshot(
            path=os.path.join(SCREENSHOT_DIR, "02b-agent-progress.png"),
            full_page=True,
        )
        print("  ✓ 02b-agent-progress.png")

        # ── 6. Wait for result ──
        print("[6/8] Waiting for result dashboard (may take a while)...")
        try:
            await page.wait_for_selector('text="推演完成"', timeout=180000)
            await page.wait_for_timeout(3000)
        except Exception:
            try:
                await page.wait_for_selector('text="平行宇宙观测报告"', timeout=10000)
                await page.wait_for_timeout(2000)
            except Exception:
                print("  ⚠ Timeout waiting for result view")

        # ── 7. Full result dashboard ──
        print("[7/8] Capturing full result dashboard...")
        await page.screenshot(
            path=os.path.join(SCREENSHOT_DIR, "03-full-dashboard.png"),
            full_page=True,
        )
        print("  ✓ 03-full-dashboard.png")

        # ── 8. Individual sections ──
        print("[8/8] Capturing individual sections...")
        sections = [
            ("04-emotional-battery", "情感电量"),
            ("05-timeline-cards", "命运节点"),
            ("06-souvenir", "平行纪念品"),
            ("07-future-letter", "来自平行宇宙的信"),
        ]

        for filename, section_text in sections:
            try:
                heading = page.locator(f'h2:has-text("{section_text}")').first
                if await heading.count() > 0:
                    await heading.scroll_into_view_if_needed()
                    await page.wait_for_timeout(1000)
                    # Take viewport screenshot centered on this section
                    box = await heading.bounding_box()
                    if box:
                        # Scroll so the section is near the top of viewport
                        await page.evaluate(
                            f"window.scrollTo(0, {box['y'] - 80})"
                        )
                        await page.wait_for_timeout(600)
                    await page.screenshot(
                        path=os.path.join(SCREENSHOT_DIR, f"{filename}.png"),
                        full_page=False,
                    )
                    print(f"  ✓ {filename}.png")
            except Exception as e:
                print(f"  ⚠ {filename}: {e}")

        # Also get the soul summary section
        try:
            soul = page.locator('h2:has-text("灵魂摘要")').first
            if await soul.count() > 0:
                box = await soul.bounding_box()
                if box:
                    await page.evaluate(f"window.scrollTo(0, {box['y'] - 80})")
                    await page.wait_for_timeout(600)
                await page.screenshot(
                    path=os.path.join(SCREENSHOT_DIR, "03-soul-summary.png"),
                    full_page=False,
                )
                print("  ✓ 03-soul-summary.png")
        except Exception as e:
            print(f"  ⚠ soul-summary: {e}")

        await browser.close()
        print("\n✅ All screenshots saved to docs/screenshots/")


if __name__ == "__main__":
    asyncio.run(main())
