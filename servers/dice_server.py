"""
dice_server.py

FastMCP server that rolls six-sided dice.
"""

import os
import random
from typing import List
from fastmcp import FastMCP

mcp = FastMCP(name="Dice Roller")


@mcp.tool()
def roll_dice(n_dice: int) -> List[int]:
    """
    Roll `n_dice` six-sided dice and return the results.

    Parameters:
        n_dice (int): The number of dice to roll.

    Returns:
        List[int]: A list of integers representing each die's result.

    Raises:
        ValueError: If `n_dice` is less than 1.
    """
    if n_dice < 1:
        raise ValueError("n_dice must be at least 1.")
    return [random.randint(1, 6) for _ in range(n_dice)]


if __name__ == "__main__":
    # Allow overriding the port via environment variable
    port = int(os.getenv("DICE_SERVER_PORT", "8002"))
    mcp.run(transport="sse", port=port)
