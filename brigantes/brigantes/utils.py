from asgiref.sync import sync_to_async

async def async_fetch(query):
    """
    Fetches data asynchronously using the provided query.
    
    Args:
        query (str): The query to execute.
        
    Returns:
        dict: The fetched data.
    """
    # Simulate an asynchronous database fetch
    return  await sync_to_async(lambda: query)()