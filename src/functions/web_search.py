import urllib.parse
from datetime import datetime
import asyncio
from playwright.async_api import async_playwright

# 非同步函式：使用 Firefox 進行網路搜尋
async def search_web_with_firefox(query: str, source_url: str = None) -> list:
    results = []  # 用來存放搜尋結果的列表
    # 使用 async with 管理 async_playwright 的上下文，確保資源釋放
    async with async_playwright() as p:
        # 啟動 Firefox 瀏覽器，headless 模式下不顯示瀏覽器介面
        browser = await p.firefox.launch(headless=True)
        # 設定 Firefox 的 User-Agent
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:115.0) Gecko/20100101 Firefox/115.0"
        # 建立一個新的分頁，並設定使用自訂的 User-Agent
        page = await browser.new_page(user_agent=user_agent)
        
        # 若未提供來源 URL，則根據 query 生成 Bing 搜尋 URL
        if source_url is None:
            # 確保 query 為字串，並做 URL 編碼
            if not isinstance(query, str):
                query = str(query)
            encoded_query = urllib.parse.quote_plus(query)
            source_url = f"https://www.bing.com/search?q={encoded_query}"
        
        # 導航至指定的搜尋頁面，timeout 設定為 15000 毫秒
        await page.goto(source_url, timeout=15000)
        # 等待頁面加載完成，直到網路處於空閒狀態
        await page.wait_for_load_state("networkidle")
        
        # 根據 Bing 搜尋結果的結構，選取結果元素（這裡假設結果位於 <li class="b_algo"> 中的 h2 a 元素）
        result_elements = page.locator("li.b_algo h2 a")
        # 取得搜尋結果元素的數量（非同步方法）
        count = await result_elements.count()
        print("找到搜尋結果元素數量：", count)
        
        # 逐一處理每個搜尋結果元素
        for i in range(count):
            try:
                element = result_elements.nth(i)
                # 取得元素內的文字內容作為標題，並去除首尾空白
                title = (await element.inner_text()).strip()
                # 取得元素的 href 屬性作為連結
                link = await element.get_attribute("href")
                if link and title:
                    # 取得目前時間作為 timestamp
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    results.append({"title": title, "link": link, "timestamp": timestamp})
            except Exception as e:
                print("錯誤：", e)
                continue

        # 關閉瀏覽器
        await browser.close()
    return results

# 測試部分：如果直接執行此模組，則進行搜尋測試
if __name__ == "__main__":
    query = "2025 機器學習 李宏毅"
    # 使用 asyncio.run 執行非同步函式，取得搜尋結果
    search_results = asyncio.run(search_web_with_firefox(query))
    print("搜尋結果：")
    if search_results:
        for res in search_results:
            print(f"標題: {res['title']}")
            print(f"連結: {res['link']}")
            print("-" * 40)
    else:
        print("沒有搜尋結果。")
