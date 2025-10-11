from ddgs import DDGS 


def search_internet(query: str, num_results: int = 5) -> str:
    """Search the internet using DuckDuckGo

    Args:
        query: A consise and specific query to search the internet
        num_results: The number of results to return (recommended: 1-5)
    """
    print("Calling tool 'search_internet' with parameters query = " + query + " | num_results = " + str(num_results))
    ddgs = DDGS()
    results = ddgs.text(query, max_results = num_results)
    
    print("results: ", results)

    results_text = "\n--\n".join([f"# {page['title']} [{page['href']}]\n{page['body']}" for page in results])
    print(results_text)
    return results_text

print(search_internet('Middle East'))
