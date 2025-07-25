"""
MCP (Model Context Protocol) Demo Client
Demonstrates integration between AI agents and external tools via MCP servers.
"""

from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import asyncio
import os

# Load environment variables
load_dotenv()

async def create_mcp_client():
    """Initialize MCP client with math and weather servers."""
    return MultiServerMCPClient({
        "math": {
            "command": "python",
            "args": ["mathserver.py"],
            "transport": "stdio",
        },
        "weather": {
            "url": "http://localhost:8000/mcp",
            "transport": "streamable_http",
        }
    })

def create_ai_model():
    """Create and configure the AI model."""
    os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
    return ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0
    )

async def test_agent(agent, query, description):
    """Test the agent with a specific query."""
    print(f"\n=== {description} ===")
    try:
        response = await agent.ainvoke(
            {"messages": [{"role": "user", "content": query}]}
        )
        print(f"Response: {response['messages'][-1].content}")
    except Exception as e:
        print(f"Error: {e}")

async def main():
    """Main execution function."""
    # Initialize components
    client = await create_mcp_client()
    model = create_ai_model()
    
    # Get available tools
    tools = await client.get_tools()
    print(f"Available tools: {[tool.name for tool in tools]}")
    
    # Create agent
    agent = create_react_agent(model, tools)
    
    # Test scenarios
    await test_agent(
        agent, 
        "Calculate 3 + 5", 
        "Simple Math"
    )
    
    await test_agent(
        agent, 
        "First use the add tool to calculate 3 + 5, then use the multiple tool to multiply that result by 12", 
        "Complex Math"
    )
    
    await test_agent(
        agent, 
        "What's the weather in California?", 
        "Weather Query"
    )
    
    print("\n✅ Demo completed successfully!")

if __name__ == "__main__":
    print("🚀 Starting MCP Demo...")
    asyncio.run(main())