import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def test():
    server_params = StdioServerParameters(
        command="python",
        args=["mcp_server.py"]
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # 列出所有工具
            tools = await session.list_tools()
            print("可用工具：")
            for tool in tools.tools:
                print(f"  - {tool.name}: {tool.description}")
            
            # 测试查询所有课程
            result = await session.call_tool("get_all_classes", {"query": ""})
            print("\n查询所有课程：")
            print(result.content[0].text)
            
            # 测试查询会员课程
            result = await session.call_tool("get_member_classes", {"member_account": "202122269"})
            print("\n查询会员课程：")
            print(result.content[0].text)

asyncio.run(test())