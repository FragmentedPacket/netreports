"""Base CRUD operations."""
from typing import Any, Dict, List, Optional, Tuple, Union
from datetime import datetime
import pymongo
from pymongo import results

from netreports.schemas.commands import ReturnCommand
from netreports.schemas.devices import ReturnDevice
from netreports.core import config


async def get_documents(
    conn: pymongo.MongoClient,
    collection_name: str,
    return_model: Any,
    query: Optional[dict[str, Any]] = None,
    limit: int = config.PROJECT_QUERY_LIMIT,
    skip: int = 0,
    **kwargs,
) -> Tuple[int, List[Union[ReturnCommand, ReturnDevice]]]:
    """Get all documents with query.

    Args:
        conn (MongoClient): Connection to DB.
        collection (str): The collection to get from.
        query (dict, optional): Query to filter the DB fetch. Defaults to {}.

    Returns:
        List[Union[ReturnCommand, ReturnDevice]]: Return the fetched objects.
    """
    documents = []
    count = 0

    if not query:
        query = {}

    cursor = conn["reports"][collection_name].find(query, limit=limit, skip=skip, **kwargs)

    for doc in cursor:
        count += 1
        documents.append(return_model(**doc))
    cursor.close()

    return count, documents


async def insert_many_documents(
    conn: pymongo.MongoClient,
    collection_name: str,
    documents: List[Dict[Any, Any]],
    **kwargs,
) -> results.InsertManyResult:
    """Get all documents with query.

    Args:
        conn (MongoClient): Connection to DB.
        collection (str): The collection to get from.
        query (dict, optional): Query to filter the DB fetch. Defaults to {}.

    Returns:
        List[Union[ReturnCommand, ReturnDevice]]: Return the fetched objects.
    """
    with conn.start_session() as session:
        with session.start_transaction():
            result = conn["reports"][collection_name].insert_many(documents=(d.dict() for d in documents), **kwargs)

    return result
