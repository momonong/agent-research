from scrapegraphai.graphs import SmartScraperGraph
from scrapegraphai.utils import prettify_exec_info


def run_scraper(prompt: str, source: str, scraper_config: dict) -> str:
    """
    使用 SmartScraperGraph 執行單頁爬取，返回爬取結果。

    參數：
        - prompt: 爬蟲提示，例如 "List me all the FAQ with their answers"
        - source: 目標 URL，例如成功大學國際處的某個網頁
        - scraper_config: 用於初始化爬蟲工具的配置字典（通常來自你的 config 模組）
    """
    # (可根據需要加入 warnings 設定)
    scraper = SmartScraperGraph(
        prompt=prompt,
        source=source,
        config=scraper_config,
    )
    result = scraper.run()
    print("\n[SmartScraperGraph] Scraping 結果：")
    print(result)
    if hasattr(scraper, "execution_info"):
        print("\n[SmartScraperGraph] 執行狀態資訊：")
        print(prettify_exec_info(scraper.execution_info))
    else:
        print("\n[SmartScraperGraph] 無法取得執行狀態資訊。")
    return result


def extract_next_page(current_url: str, page_content: str) -> str:
    """
    根據目前頁面的內容提取下一頁的 URL。
    此函數需要你根據目標網站的結構來實作。
    如果找不到下一頁，則返回空字串或 None。
    """
    # 這裡僅作示例，實際需要解析 page_content (可能使用 BeautifulSoup)
    # 假設我們能從 page_content 中提取一個 <a id="next" href="...">Next</a>
    next_url = None  # 實作解析邏輯
    return next_url


def crawl_all_pages(start_url: str, prompt: str, scraper_config: dict) -> list:
    """
    從起始 URL 開始，循環爬取所有頁面並合併結果。
    """
    results = []
    current_url = start_url
    while current_url:
        # 呼叫單頁爬蟲
        result = run_scraper(prompt, current_url, scraper_config)
        results.append(result)
        # 根據結果解析下一頁 URL
        next_url = extract_next_page(current_url, result)
        if next_url and next_url != current_url:
            current_url = next_url
        else:
            break
    return results


# 測試用（直接運行此模組測試）
if __name__ == "__main__":
    # 假設你有一個初始化 scraper_config 的方法，例如在 scraper_client.py 中
    from src.clients.scraper_client import init_scraper_config
    scraper_config = init_scraper_config()
    start_url = "https://oia.ncku.edu.tw/"
    prompt = "請從成功大學國際處網站（僅限此網站及其內部連結）中，搜尋與「獎學金申請截止日期」相關的 FAQ 內容。請深入查找所有相關頁面，並彙整出完整資訊，最終請以清晰的列表格式返回答案。"
    all_results = crawl_all_pages(start_url, prompt, scraper_config)
    print("所有頁面的爬蟲結果：")
    for res in all_results:
        print(res)
