"""Demonstrate real MCP stdio discovery, resource reads and tool invocation."""
import asyncio
import sys
from pathlib import Path
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    server = str(Path(__file__).resolve().parent / "mcp_server.py")
    params = StdioServerParameters(command=sys.executable, args=[server])
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            resources = await session.list_resources()
            tools = await session.list_tools()
            print("Resources:", [str(r.uri) for r in resources.resources])
            print("Tools:", [t.name for t in tools.tools])
            for resource in resources.resources:
                result = await session.read_resource(resource.uri)
                print("Read", resource.uri, "items:", len(result.contents))
            result = await session.call_tool("search_corpus", {"query": "solar", "limit": 3})
            assert not result.isError, result
            print("Search result:", result.content)

if __name__ == "__main__":
    asyncio.run(main())
