from mcp.server.fastmcp import FastMCP
import requests

mcp = FastMCP("健身房助手")

JAVA_API_URL = "http://localhost:8080"

@mcp.tool()
def get_member_classes(member_account: str) -> str:
    """查询会员已报名的课程"""
    resp = requests.get(
        f"{JAVA_API_URL}/api/class/getClassByMember",
        params={"memberAccount": member_account}
    )
    data = resp.json()
    orders = data.get("orders", [])
    if not orders:
        return "该会员暂无报名课程"
    return "\n".join([
        f"课程：{o['className']}，教练：{o['coach']}，时间：{o['classBegin']}"
        for o in orders
    ])

@mcp.tool()
def get_all_classes(query: str = "") -> str:
    """查询健身房所有课程"""
    resp = requests.get(f"{JAVA_API_URL}/api/class/getAllClass")
    data = resp.json()
    classList = data.get("classList", [])
    return "\n".join([
        f"课程：{c['className']}，教练：{c['coach']}，时间：{c['classBegin']}"
        for c in classList
    ])

@mcp.tool()
def get_gym_info(query: str = "") -> str:
    """查询健身房基本信息"""
    return "营业时间：06:00-22:00\n地址：xx市xx路xx号"

if __name__ == "__main__":
    mcp.run()