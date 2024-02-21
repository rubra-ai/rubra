# Standard Library
import logging
import urllib.parse

# Third Party
from googlesearch import search as search_api

from .browser import WebPageBrowser


def web_scraper(url: str):
    wb = WebPageBrowser()
    result = wb.browse(url)
    return result


class WebBrowseTool:
    name = "GoogleSearchTool"
    description = "Useful for search information on internet."
    parameters = {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "the completed question to search",
            },
        },
        "required": ["query"],
    }

    async def _arun(self, query: str):
        return await google_search_api(query)

    def _run(self, query: str, web_browse: bool = False, concat_text: bool = True):
        res = google_search_api(query)
        summaries = []
        if web_browse:
            for i, r in enumerate(res):
                context = parse_url(r["url"], query)
                res[i]["text"] += "\n" + context

        if concat_text:
            for i, r in enumerate(res):
                formatted_summary = f"{i+1}.\nTITLE:{r['title']}\nTEXT:{r['text']}\nSOURCE_URL:{r['url']}"
                summaries.append(formatted_summary)

            joint_res = "\n\n".join(summaries)
            return joint_res
        else:
            return res


def google_search_api(query: str) -> str:
    max_results = 5
    res = [
        {"title": r.title, "url": r.url, "text": r.description}
        for i, r in enumerate(search_api(query, advanced=True))
        if i < max_results
    ]
    return res


def create_google_search_url(query: str) -> str:
    encoded_query = urllib.parse.quote_plus(query)
    url = f"https://www.google.com/search?q={encoded_query}"
    return url


def num_tokens_from_string(string: str, encoding_name: str = "cl100k_base") -> int:
    """Returns the number of tokens in a text string."""
    # Third Party
    import tiktoken

    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens


def parse_url(url: str, query: str, stream: bool = False) -> str:
    """
    Args:
        query (str): _description_
        stream (bool, optional): _description_. Defaults to False.
        summarize (bool, optional): _description_. Defaults to False.

    Returns:
        _type_: _description_
    """
    try:
        context = web_scraper(url)
    except Exception as e:
        logging.error(f"Error in web_scraper: {e}")
        context = ""
    return context
