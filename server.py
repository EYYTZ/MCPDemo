from mcp.server.fastmcp import FastMCP
import urllib.request
import json

# 1. 建立 FastMCP 伺服器實例
# FastMCP 會幫我們處理掉所有底層的 JSON-RPC 和傳輸層細節
mcp = FastMCP("advanced-mcp-server")

# 2. 註冊工具 (Tool)
# 只要加上 @mcp.tool() 裝飾器，FastMCP 就會自動把這個函式轉換成 AI 可以呼叫的工具
@mcp.tool()
def add_numbers(a: int, b: int) -> str:
    """
    將兩個數字相加
    """
    result = a + b
    return f"{a} 與 {b} 的總和是 {result}"

@mcp.tool()
def multiply_numbers(a: int, b: int) -> str:
    """
    將兩個數字相乘
    """
    result = a * b
    return f"{a} 與 {b} 的相乘結果是 {result}"

# 3. 整合外部服務工具 (Tool)
@mcp.tool()
def get_github_user(username: str) -> str:
    """
    呼叫外部 GitHub API 取得指定使用者的基本公開資訊。
    當你需要查詢開發者資訊時可以使用此工具。
    """
    url = f"https://api.github.com/users/{username}"
    try:
        # 加入 User-Agent 是 GitHub API 的要求
        req = urllib.request.Request(url, headers={'User-Agent': 'MCP-Demo'})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            name = data.get('name') or username
            return f"開發者 {name} 有 {data.get('public_repos')} 個公開專案，粉絲數: {data.get('followers')}。"
    except Exception as e:
        return f"無法取得 {username} 的資料: {str(e)}"

# 4. 註冊資源 (Resource)
# 資源是被動的資料，AI 可以在需要時讀取這些上下文 (例如讀取本地資料庫狀態或日誌檔)
@mcp.resource("system://status")
def get_system_status() -> str:
    """獲取當前系統狀態"""
    return "System OK. Database connection: Active. External API: Online."

# 5. 註冊提示詞模板 (Prompt)
# 讓 Server 提供預設的指令模板，指導 AI 該如何使用上述的工具
@mcp.prompt()
def analyze_developer(username: str) -> str:
    """建立一個分析特定 GitHub 開發者的提示詞模板"""
    return (f"請幫我分析 GitHub 開發者 {username}。"
            f"請先呼叫 get_github_user 工具取得他的基本資料，然後根據資料評估他在開源社群的活躍程度。")

# 6. 啟動伺服器
if __name__ == "__main__":
    # 預設會使用 stdio (標準輸入輸出) 作為傳輸層，完美適配 Claude Desktop
    mcp.run()
