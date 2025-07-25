from mcp.server.fastmcp import FastMCP
import uvicorn

mcp = FastMCP("Weather")

@mcp.tool()
async def get_weather(location: str) -> str:
    """Get the weather for a specific location"""
    # Simple mock weather responses
    weather_data = {
        "california": "It's sunny and 75°F in California",
        "new york": "It's cloudy and 68°F in New York", 
        "london": "It's rainy and 62°F in London",
        "tokyo": "It's partly cloudy and 72°F in Tokyo"
    }
    
    location_lower = location.lower()
    for key in weather_data:
        if key in location_lower:
            return weather_data[key]
    
    return f"Weather data not available for {location}. Try California, New York, London, or Tokyo."

if __name__ == "__main__":
    print("Starting weather server on http://localhost:8000/mcp")
    mcp.run(transport="streamable-http")