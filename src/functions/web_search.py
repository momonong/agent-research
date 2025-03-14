import urllib.parse
from datetime import datetime
from playwright.sync_api import sync_playwright

def search_web_with_firefox(query: str, source_url: str = None) -> list:
    results = []
    with sync_playwright() as p:
        # 使用 Firefox 引擎，headless 模式可以根據需求設定
        browser = p.firefox.launch(headless=True)
        # 使用 Firefox 的 User-Agent
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:115.0) Gecko/20100101 Firefox/115.0"
        page = browser.new_page(user_agent=user_agent)

        if source_url is None:
            encoded_query = urllib.parse.quote_plus(query)
            # 使用 Bing 搜尋 URL
            source_url = f"https://www.bing.com/search?q={encoded_query}"

        page.goto(source_url, timeout=15000)
        page.wait_for_load_state("networkidle")

        # 調整選擇器以符合 Bing 搜尋結果的結構，通常每個結果在 <li class="b_algo"> 內
        result_elements = page.locator("li.b_algo h2 a")
        count = result_elements.count()
        print("找到搜尋結果元素數量：", count)
        for i in range(count):
            try:
                element = result_elements.nth(i)
                title = element.inner_text().strip()
                # 直接取得 <a> 元素的 href 屬性
                link = element.get_attribute("href")
                if link and title:
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    results.append({"title": title, "link": link, "timestamp": timestamp})
            except Exception as e:
                print("錯誤：", e)
                continue

        browser.close()
    return results

if __name__ == "__main__":
    query = "2025 機器學習 李宏毅"
    search_results = search_web_with_firefox(query)
    print("搜尋結果：")
    if search_results:
        for res in search_results:
            print(f"標題: {res['title']}")
            print(f"連結: {res['link']}")
            print("-" * 40)
    else:
        print("沒有搜尋結果。")
