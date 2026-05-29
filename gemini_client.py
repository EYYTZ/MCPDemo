import asyncio
import os
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# 1. 定義要如何啟動 MCP Server (這就是 Client "讀取" Server 的方式)
# 它相當於在背景執行指令: python c:\...\server.py
server_script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "server.py")
server_params = StdioServerParameters(
    command="python",
    args=[server_script_path]
)

async def run_gemini_client():
    # 2. 透過 stdio (標準輸入輸出) 啟動背景程序，並建立傳輸通道
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # 3. 初始化連線 (Client 與 Server 握手確認身分)
            await session.initialize()
            print("✅ 成功在背景啟動並連線到 MCP Server!")
            
            # 4. 向 Server 索取它擁有的所有工具
            tools = await session.list_tools()
            print("\n🛠️ 取得的工具列表:")
            for tool in tools.tools:
                print(f" - {tool.name}: {tool.description}")
                
            # 💡 接下來在真實的 Gemini 應用中，我們會把這裡取得的 tools 列表
            # 轉換成 Google Gemini API 支援的 "Function Calling" 格式交給 Gemini 模型。

if __name__ == "__main__":
    asyncio.run(run_gemini_client())
