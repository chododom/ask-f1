import fastf1

from fastmcp import FastMCP

mcp = FastMCP("F1 MCP Server")


@mcp.tool
def get_circuit_info(circuit_name: str) -> dict:
    """
    Returns information about a given F1 circuit using the fastf1 API.
    To be used for any questions related to F1 circuits on the 2025 calendar and their characteristics.

    Returns:
        A dictionary containing circuit information such as location, country, date, and round.
    """

    schedule = fastf1.get_event_schedule(2025)
    event = schedule[schedule["Location"].str.contains(circuit_name, case=False, na=False)]

    if event.empty:
        return {"error": f"Circuit '{circuit_name}' not found in 2025 F1 season."}

    circuit = event.iloc[0]
    return {
        "Circuit": circuit["Location"],
        "Country": circuit["Country"],
        "Date": circuit["EventDate"].strftime("%Y-%m-%d"),
        "RoundNumber": int(circuit["RoundNumber"]),
    }


if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=8000)
