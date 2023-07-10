"""API Utilities."""
from typing import Dict
from netreports.core import config


async def find_parameters(skip: int = 0, limit: int = config.PROJECT_QUERY_LIMIT) -> Dict:
    """Mongodb find parameters.

    Args:
        skip (int, optional): Skip results. Defaults to 0.
        limit (int, optional): Limit results. Defaults to 100.

    Returns:
        Dict: results
    """
    return {"skip": skip, "limit": limit}
