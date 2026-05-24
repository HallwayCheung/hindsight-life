"""Take screenshots of the result dashboard using mock data.
Creates a temporary page that directly renders ResultDashboard with mock data."""
import asyncio
import os
from playwright.async_api import async_playwright

SCREENSHOT_DIR = os.path.join(os.path.dirname(__file__), "..", "docs", "screenshots")
BASE_URL = "http://localhost:3000"

# Mock data matching page.tsx MOCK_DATA
MOCK_DATA_JSON = """
{
  soul_summary: "你为了留住晚霞，错过了清晨的列车。平行宇宙里的你拥有了属于自己的车队，但副驾驶上，再也没有当年那个陪你躲雨的人。",
  emotional_metrics: {
    happiness_battery: { reality: 80, parallel: 30, label: "快乐电量" },
    regret_index: { reality: 20, parallel: 65, label: "遗憾指数" },
    peace_of_mind: { reality: 90, parallel: 15, label: "内心平静度" },
  },
  parallel_souvenir: {
    item_name: "一张褪色的头等舱机票",
    description: "这是你在平行宇宙中频繁出差的证明。航程很远，但降落时没人接机。",
    icon_type: "ticket",
  },
  future_letter: {
    greetings: "展信佳：",
    content: "我是做出了那个选择的你。不要羡慕我，我现在的体检报告一塌糊涂，昨晚又失眠到了凌晨三点。其实，我时常会偷偷溜到你的世界看你，看你下班后在街角买的那束花，看你安稳的睡眠。照顾好现在的自己，那就是我们最好的结局。",
    signature: "—— 另一个时空的你",
  },
  timeline_nodes: [
    {
      year: 2021,
      reality_snapshot: "在老家按揭了一套小房子，周末和朋友去江边露营。",
      parallel_snapshot: "拿到了人生第一个百万年薪，但确诊了中度抑郁状态。",
      divergence_point: "得失守恒",
    },
    {
      year: 2023,
      reality_snapshot: "升了职，虽然工资涨得慢，但每天下班还能赶上夕阳。",
      parallel_snapshot: "跳槽到更大的平台，开始频繁出差，护照盖满了章。",
      divergence_point: "有些风景，只有慢下来才看得到",
    },
    {
      year: 2025,
      reality_snapshot: "孩子上幼儿园了，周末带他去公园喂鸽子。",
      parallel_snapshot: "拿到了梦寐以求的期权，但体检报告上多了三个箭头。",
      divergence_point: "时间会告诉你，什么才是真正的财富",
    },
  ],
}
"""

# HTML page that renders the result dashboard with mock data
RESULT_PAGE_HTML = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>后悔药 — 结果预览</title>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@300;400;600;700&display=swap');

    :root {
      --background: #F9F8F6;
      --foreground: #292524;
    }

    * { margin: 0; padding: 0; box-sizing: border-box; }

    body {
      background: var(--background);
      color: #44403c;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      line-height: 1.6;
      -webkit-font-smoothing: antialiased;
    }

    .font-serif { font-family: 'Noto Serif SC', serif; }

    .paper-card {
      background: white;
      box-shadow: 0 1px 3px rgba(0,0,0,0.06);
      border: 1px solid #e7e5e4;
      border-radius: 12px;
    }

    .max-w-2xl { max-width: 42rem; }
    .mx-auto { margin-left: auto; margin-right: auto; }
    .px-4 { padding-left: 1rem; padding-right: 1rem; }
    .py-8 { padding-top: 2rem; padding-bottom: 2rem; }
    .space-y-12 > * + * { margin-top: 3rem; }
    .space-y-16 > * + * { margin-top: 4rem; }
    .text-center { text-align: center; }
    .space-y-3 > * + * { margin-top: 0.75rem; }
    .tracking-\\[0\\.3em\\] { letter-spacing: 0.3em; }
    .tracking-\\[0\\.2em\\] { letter-spacing: 0.2em; }
    .uppercase { text-transform: uppercase; }
    .text-\\[11px\\] { font-size: 11px; }
    .text-xs { font-size: 12px; }
    .text-sm { font-size: 14px; }
    .text-lg { font-size: 18px; }
    .text-xl { font-size: 20px; }
    .text-2xl { font-size: 24px; }
    .text-3xl { font-size: 30px; }
    .text-4xl { font-size: 36px; }
    .text-stone-200 { color: #e7e5e4; }
    .text-stone-300 { color: #d6d3d1; }
    .text-stone-400 { color: #a8a29e; }
    .text-stone-500 { color: #78716c; }
    .text-stone-600 { color: #57534e; }
    .text-stone-700 { color: #44403c; }
    .text-stone-800 { color: #292524; }
    .text-emerald-700 { color: #047857; }
    .text-orange-700 { color: #c2410c; }
    .bg-stone-200 { background-color: #e7e5e4; }
    .bg-stone-300 { background-color: #d6d3d1; }
    .bg-stone-400 { background-color: #a8a29e; }
    .bg-emerald-200 { background-color: #a7f3d0; }
    .bg-emerald-400 { background-color: #34d399; }
    .bg-orange-200 { background-color: #fed7aa; }
    .bg-orange-400 { background-color: #fb923c; }
    .bg-white { background-color: white; }
    .font-light { font-weight: 300; }
    .font-medium { font-weight: 500; }
    .leading-loose { line-height: 2; }
    .rounded-full { border-radius: 9999px; }
    .rounded-xl { border-radius: 0.75rem; }
    .w-1 { width: 0.25rem; }
    .h-1 { height: 0.25rem; }
    .w-1\\.5 { width: 0.375rem; }
    .h-4 { height: 1rem; }
    .h-px { height: 1px; }
    .w-16 { width: 4rem; }
    .flex { display: flex; }
    .grid { display: grid; }
    .inline-block { display: inline-block; }
    .items-center { align-items: center; }
    .justify-center { justify-content: center; }
    .gap-3 { gap: 0.75rem; }
    .gap-4 { gap: 1rem; }
    .gap-6 { gap: 1.5rem; }
    .mb-2 { margin-bottom: 0.5rem; }
    .mb-3 { margin-bottom: 0.75rem; }
    .mb-4 { margin-bottom: 1rem; }
    .mb-6 { margin-bottom: 1.5rem; }
    .mt-4 { margin-top: 1rem; }
    .p-6 { padding: 1.5rem; }
    .p-8 { padding: 2rem; }
    .pt-4 { padding-top: 1rem; }
    .pb-8 { padding-bottom: 2rem; }
    .flex-1 { flex: 1; }
    .flex-col { flex-direction: column; }
    .flex-wrap { flex-wrap: wrap; }
    .max-w-lg { max-width: 32rem; }
    .grid-cols-2 { grid-template-columns: repeat(2, 1fr); }

    .section-label {
      display: flex;
      align-items: center;
      gap: 0.75rem;
      margin-bottom: 1.5rem;
    }
    .section-label .accent {
      width: 0.25rem;
      height: 1rem;
      border-radius: 9999px;
      background: #a8a29e;
    }
    .section-label h2 {
      font-size: 12px;
      color: #a8a29e;
      letter-spacing: 0.2em;
      text-transform: uppercase;
    }
    .section-label .line {
      height: 1px;
      flex: 1;
      background: #e7e5e4;
    }

    /* Letter paper */
    .letter-paper {
      background: linear-gradient(135deg, #faf9f6 0%, #f5f3ef 50%, #f0ede8 100%);
      border: 1px solid #e7e5e4;
      border-radius: 12px;
      box-shadow: inset 0 2px 8px rgba(0,0,0,0.03), 0 1px 3px rgba(0,0,0,0.06);
    }

    /* Animations */
    @keyframes fadeUp {
      from { opacity: 0; transform: translateY(12px); }
      to { opacity: 1; transform: translateY(0); }
    }
    .fade-up {
      animation: fadeUp 0.5s ease-out forwards;
      opacity: 0;
    }
    .delay-1 { animation-delay: 0.1s; }
    .delay-2 { animation-delay: 0.2s; }
    .delay-3 { animation-delay: 0.3s; }
    .delay-4 { animation-delay: 0.4s; }
    .delay-5 { animation-delay: 0.5s; }
    .delay-6 { animation-delay: 0.6s; }
    .delay-7 { animation-delay: 0.7s; }

    /* Bar animation */
    @keyframes growBar {
      from { transform: scaleX(0); }
      to { transform: scaleX(1); }
    }
    .bar-animated {
      transform-origin: left;
      animation: growBar 1s ease-out forwards;
    }
  </style>
</head>
<body>
  <div style="min-height:100vh; width:100%;">
    <div class="max-w-2xl mx-auto px-4 py-8" style="padding-top:2rem; padding-bottom:2rem;">

      <!-- Header -->
      <header class="text-center space-y-3 fade-up" style="margin-bottom:3rem;">
        <p class="text-[11px] text-stone-400 tracking-[0.3em] uppercase">推演完成</p>
        <h1 class="font-serif text-2xl sm:text-3xl font-light text-stone-700" style="letter-spacing:0.05em;">平行宇宙观测报告</h1>
        <div class="w-16 h-px bg-stone-200 mx-auto"></div>
      </header>

      <!-- Soul Summary -->
      <section class="fade-up delay-1" style="margin-bottom:3rem;">
        <div class="section-label">
          <div class="accent"></div>
          <h2>灵魂摘要</h2>
          <div class="line"></div>
        </div>
        <div class="paper-card p-6 sm:p-8">
          <p class="font-serif text-stone-600 text-lg leading-loose">
            你为了留住晚霞，错过了清晨的列车。平行宇宙里的你拥有了属于自己的车队，但副驾驶上，再也没有当年那个陪你躲雨的人。
          </p>
        </div>
      </section>

      <!-- Emotional Metrics -->
      <section class="fade-up delay-2" style="margin-bottom:3rem;">
        <div class="section-label">
          <div class="accent"></div>
          <h2>情感电量</h2>
          <div class="line"></div>
        </div>
        <div class="paper-card p-6 sm:p-8">
          <!-- Battery bars -->
          <div style="display:flex; flex-direction:column; gap:1.5rem;">
            <!-- Happiness Battery -->
            <div>
              <div style="display:flex; justify-content:space-between; margin-bottom:0.5rem;">
                <span class="text-sm text-stone-600 font-medium">快乐电量</span>
                <div style="display:flex; gap:0.75rem; font-size:12px;">
                  <span class="text-emerald-700">现实 80%</span>
                  <span class="text-orange-700">平行 30%</span>
                </div>
              </div>
              <div style="display:flex; flex-direction:column; gap:0.375rem;">
                <div style="height:8px; background:#f5f5f4; border-radius:9999px; overflow:hidden;">
                  <div class="bar-animated" style="width:80%; height:100%; background:linear-gradient(to right, #a7f3d0, #34d399); border-radius:9999px;"></div>
                </div>
                <div style="height:8px; background:#f5f5f4; border-radius:9999px; overflow:hidden;">
                  <div class="bar-animated" style="width:30%; height:100%; background:linear-gradient(to right, #fed7aa, #fb923c); border-radius:9999px; animation-delay:0.2s;"></div>
                </div>
              </div>
            </div>
            <!-- Regret Index -->
            <div>
              <div style="display:flex; justify-content:space-between; margin-bottom:0.5rem;">
                <span class="text-sm text-stone-600 font-medium">遗憾指数</span>
                <div style="display:flex; gap:0.75rem; font-size:12px;">
                  <span class="text-emerald-700">现实 20%</span>
                  <span class="text-orange-700">平行 65%</span>
                </div>
              </div>
              <div style="display:flex; flex-direction:column; gap:0.375rem;">
                <div style="height:8px; background:#f5f5f4; border-radius:9999px; overflow:hidden;">
                  <div class="bar-animated" style="width:20%; height:100%; background:linear-gradient(to right, #a7f3d0, #34d399); border-radius:9999px;"></div>
                </div>
                <div style="height:8px; background:#f5f5f4; border-radius:9999px; overflow:hidden;">
                  <div class="bar-animated" style="width:65%; height:100%; background:linear-gradient(to right, #fed7aa, #fb923c); border-radius:9999px; animation-delay:0.2s;"></div>
                </div>
              </div>
            </div>
            <!-- Peace of Mind -->
            <div>
              <div style="display:flex; justify-content:space-between; margin-bottom:0.5rem;">
                <span class="text-sm text-stone-600 font-medium">内心平静度</span>
                <div style="display:flex; gap:0.75rem; font-size:12px;">
                  <span class="text-emerald-700">现实 90%</span>
                  <span class="text-orange-700">平行 15%</span>
                </div>
              </div>
              <div style="display:flex; flex-direction:column; gap:0.375rem;">
                <div style="height:8px; background:#f5f5f4; border-radius:9999px; overflow:hidden;">
                  <div class="bar-animated" style="width:90%; height:100%; background:linear-gradient(to right, #a7f3d0, #34d399); border-radius:9999px;"></div>
                </div>
                <div style="height:8px; background:#f5f5f4; border-radius:9999px; overflow:hidden;">
                  <div class="bar-animated" style="width:15%; height:100%; background:linear-gradient(to right, #fed7aa, #fb923c); border-radius:9999px; animation-delay:0.2s;"></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Timeline Cards -->
      <section class="fade-up delay-3" style="margin-bottom:3rem;">
        <div class="section-label">
          <div class="accent"></div>
          <h2>命运节点</h2>
          <div class="line"></div>
        </div>
        <div style="display:flex; flex-direction:column; gap:1rem;">
          <!-- Node 1 -->
          <div class="paper-card p-6">
            <div style="display:flex; align-items:center; gap:0.5rem; margin-bottom:1rem;">
              <span class="font-serif text-stone-700" style="font-size:20px; font-weight:300;">2021</span>
            </div>
            <div class="grid-cols-2" style="display:grid; gap:1.5rem;">
              <div>
                <div style="display:flex; align-items:center; gap:0.375rem; margin-bottom:0.5rem;">
                  <div style="width:6px; height:6px; border-radius:9999px; background:#047857;"></div>
                  <span class="text-xs text-stone-400">现实</span>
                </div>
                <p class="text-sm text-stone-600 leading-loose">在老家按揭了一套小房子，周末和朋友去江边露营。</p>
              </div>
              <div>
                <div style="display:flex; align-items:center; gap:0.375rem; margin-bottom:0.5rem;">
                  <div style="width:6px; height:6px; border-radius:9999px; background:#c2410c;"></div>
                  <span class="text-xs text-stone-400">平行宇宙</span>
                </div>
                <p class="text-sm text-stone-600 leading-loose">拿到了人生第一个百万年薪，但确诊了中度抑郁状态。</p>
              </div>
            </div>
            <div style="text-align:center; margin-top:1rem; padding-top:0.75rem; border-top:1px solid #f5f5f4;">
              <span class="text-xs text-stone-400" style="letter-spacing:0.15em;">得失守恒</span>
            </div>
          </div>
          <!-- Node 2 -->
          <div class="paper-card p-6 fade-up delay-4">
            <div style="display:flex; align-items:center; gap:0.5rem; margin-bottom:1rem;">
              <span class="font-serif text-stone-700" style="font-size:20px; font-weight:300;">2023</span>
            </div>
            <div class="grid-cols-2" style="display:grid; gap:1.5rem;">
              <div>
                <div style="display:flex; align-items:center; gap:0.375rem; margin-bottom:0.5rem;">
                  <div style="width:6px; height:6px; border-radius:9999px; background:#047857;"></div>
                  <span class="text-xs text-stone-400">现实</span>
                </div>
                <p class="text-sm text-stone-600 leading-loose">升了职，虽然工资涨得慢，但每天下班还能赶上夕阳。</p>
              </div>
              <div>
                <div style="display:flex; align-items:center; gap:0.375rem; margin-bottom:0.5rem;">
                  <div style="width:6px; height:6px; border-radius:9999px; background:#c2410c;"></div>
                  <span class="text-xs text-stone-400">平行宇宙</span>
                </div>
                <p class="text-sm text-stone-600 leading-loose">跳槽到更大的平台，开始频繁出差，护照盖满了章。</p>
              </div>
            </div>
            <div style="text-align:center; margin-top:1rem; padding-top:0.75rem; border-top:1px solid #f5f5f4;">
              <span class="text-xs text-stone-400" style="letter-spacing:0.15em;">有些风景，只有慢下来才看得到</span>
            </div>
          </div>
          <!-- Node 3 -->
          <div class="paper-card p-6 fade-up delay-5">
            <div style="display:flex; align-items:center; gap:0.5rem; margin-bottom:1rem;">
              <span class="font-serif text-stone-700" style="font-size:20px; font-weight:300;">2025</span>
            </div>
            <div class="grid-cols-2" style="display:grid; gap:1.5rem;">
              <div>
                <div style="display:flex; align-items:center; gap:0.375rem; margin-bottom:0.5rem;">
                  <div style="width:6px; height:6px; border-radius:9999px; background:#047857;"></div>
                  <span class="text-xs text-stone-400">现实</span>
                </div>
                <p class="text-sm text-stone-600 leading-loose">孩子上幼儿园了，周末带他去公园喂鸽子。</p>
              </div>
              <div>
                <div style="display:flex; align-items:center; gap:0.375rem; margin-bottom:0.5rem;">
                  <div style="width:6px; height:6px; border-radius:9999px; background:#c2410c;"></div>
                  <span class="text-xs text-stone-400">平行宇宙</span>
                </div>
                <p class="text-sm text-stone-600 leading-loose">拿到了梦寐以求的期权，但体检报告上多了三个箭头。</p>
              </div>
            </div>
            <div style="text-align:center; margin-top:1rem; padding-top:0.75rem; border-top:1px solid #f5f5f4;">
              <span class="text-xs text-stone-400" style="letter-spacing:0.15em;">时间会告诉你，什么才是真正的财富</span>
            </div>
          </div>
        </div>
      </section>

      <!-- Parallel Souvenir -->
      <section class="fade-up delay-5" style="margin-bottom:3rem;">
        <div class="section-label">
          <div class="accent"></div>
          <h2>平行纪念品</h2>
          <div class="line"></div>
        </div>
        <div class="paper-card p-6 sm:p-8" style="max-width:32rem; margin:0 auto; text-align:center;">
          <div style="font-size:36px; margin-bottom:1rem;">🎫</div>
          <p style="font-size:10px; color:#a8a29e; letter-spacing:0.1em; text-transform:uppercase; margin-bottom:0.5rem;">来自平行宇宙的纪念品</p>
          <h3 class="font-serif text-lg text-stone-700" style="margin-bottom:0.75rem;">一张褪色的头等舱机票</h3>
          <p class="text-sm text-stone-500 leading-loose">这是你在平行宇宙中频繁出差的证明。航程很远，但降落时没人接机。</p>
        </div>
      </section>

      <!-- Future Letter -->
      <section class="fade-up delay-6" style="margin-bottom:3rem;">
        <div class="section-label">
          <div class="accent"></div>
          <h2>来自平行宇宙的信</h2>
          <div class="line"></div>
        </div>
        <div class="letter-paper p-6 sm:p-8" style="max-width:32rem; margin:0 auto;">
          <p class="font-serif text-stone-600 text-lg" style="margin-bottom:1.5rem;">展信佳：</p>
          <p class="font-serif text-stone-600 leading-loose" style="margin-bottom:1rem;">我是做出了那个选择的你。不要羡慕我，我现在的体检报告一塌糊涂，昨晚又失眠到了凌晨三点。</p>
          <p class="font-serif text-stone-600 leading-loose" style="margin-bottom:1rem;">其实，我时常会偷偷溜到你的世界看你，看你下班后在街角买的那束花，看你安稳的睡眠。</p>
          <p class="font-serif text-stone-600 leading-loose" style="margin-bottom:2rem;">照顾好现在的自己，那就是我们最好的结局。</p>
          <p class="font-serif text-stone-500 text-sm" style="text-align:right;">—— 另一个时空的你</p>
        </div>
      </section>

      <!-- Restart -->
      <div class="text-center fade-up delay-7" style="padding-top:1rem; padding-bottom:2rem;">
        <button style="font-size:14px; color:#a8a29e; letter-spacing:0.05em; text-decoration:underline; text-underline-offset:4px; background:none; border:none; cursor:pointer;">
          重新开始推演
        </button>
      </div>

    </div>
  </div>
</body>
</html>"""


async def main():
    os.makedirs(SCREENSHOT_DIR, exist_ok=True)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)

        # Desktop viewport
        context = await browser.new_context(
            viewport={"width": 1440, "height": 900},
            device_scale_factor=2,
        )
        page = await context.new_page()

        # Load the static result page
        print("[1/7] Loading result dashboard...")
        await page.set_content(RESULT_PAGE_HTML, wait_until="networkidle")
        await page.wait_for_timeout(2000)

        # Full page screenshot
        await page.screenshot(
            path=os.path.join(SCREENSHOT_DIR, "03-full-dashboard.png"),
            full_page=True,
        )
        print("  ✓ 03-full-dashboard.png")

        # Soul summary
        print("[2/7] Soul summary...")
        await page.evaluate('window.scrollTo(0, 200)')
        await page.wait_for_timeout(500)
        await page.screenshot(
            path=os.path.join(SCREENSHOT_DIR, "03-soul-summary.png"),
            full_page=False,
        )
        print("  ✓ 03-soul-summary.png")

        # Emotional battery
        print("[3/7] Emotional battery...")
        heading = page.locator('h2:has-text("情感电量")')
        box = await heading.bounding_box()
        if box:
            await page.evaluate(f'window.scrollTo(0, {box["y"] - 80})')
        await page.wait_for_timeout(600)
        await page.screenshot(
            path=os.path.join(SCREENSHOT_DIR, "04-emotional-battery.png"),
            full_page=False,
        )
        print("  ✓ 04-emotional-battery.png")

        # Timeline cards
        print("[4/7] Timeline cards...")
        heading = page.locator('h2:has-text("命运节点")')
        box = await heading.bounding_box()
        if box:
            await page.evaluate(f'window.scrollTo(0, {box["y"] - 80})')
        await page.wait_for_timeout(600)
        await page.screenshot(
            path=os.path.join(SCREENSHOT_DIR, "05-timeline-cards.png"),
            full_page=False,
        )
        print("  ✓ 05-timeline-cards.png")

        # Souvenir
        print("[5/7] Souvenir...")
        heading = page.locator('h2:has-text("平行纪念品")')
        box = await heading.bounding_box()
        if box:
            await page.evaluate(f'window.scrollTo(0, {box["y"] - 80})')
        await page.wait_for_timeout(600)
        await page.screenshot(
            path=os.path.join(SCREENSHOT_DIR, "06-souvenir.png"),
            full_page=False,
        )
        print("  ✓ 06-souvenir.png")

        # Future letter
        print("[6/7] Future letter...")
        heading = page.locator('h2:has-text("来自平行宇宙的信")')
        box = await heading.bounding_box()
        if box:
            await page.evaluate(f'window.scrollTo(0, {box["y"] - 80})')
        await page.wait_for_timeout(600)
        await page.screenshot(
            path=os.path.join(SCREENSHOT_DIR, "07-future-letter.png"),
            full_page=False,
        )
        print("  ✓ 07-future-letter.png")

        # Mobile view
        print("[7/7] Mobile view...")
        await context.close()
        mobile_ctx = await browser.new_context(
            viewport={"width": 390, "height": 844},
            device_scale_factor=3,
        )
        mobile_page = await mobile_ctx.new_page()
        await mobile_page.set_content(RESULT_PAGE_HTML, wait_until="networkidle")
        await mobile_page.wait_for_timeout(2000)
        await mobile_page.screenshot(
            path=os.path.join(SCREENSHOT_DIR, "08-mobile-view.png"),
            full_page=True,
        )
        print("  ✓ 08-mobile-view.png")

        await mobile_ctx.close()
        await browser.close()
        print("\n✅ All result screenshots saved to docs/screenshots/")


if __name__ == "__main__":
    asyncio.run(main())
