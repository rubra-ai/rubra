# Standard Library
import asyncio
import os
import re
from tempfile import TemporaryDirectory
from urllib.parse import urljoin

# Third Party
from bs4 import BeautifulSoup
from langchain.docstore.document import Document
from langchain.text_splitter import TokenTextSplitter
from markdownify import markdownify as md
from playwright.async_api import async_playwright


class WebPageBrowser:
    def __init__(self):
        self.browser = WebBrowser()
        self.tmpdir = TemporaryDirectory()
        self.text_splitter = TokenTextSplitter()
        self.url_map = {}

    async def initialize(self):
        await self.browser.initialize()

    async def abrowse(self, url: str) -> str:
        page_source = await self.browser.goto(url)

        # Filter and Parse HTML
        soup = BeautifulSoup(page_source, "html.parser")
        # Update relative URLs to absolute URLs
        for a_tag in soup.find_all("a", href=True):
            a_tag["href"] = urljoin(url, a_tag["href"])
        # Remove unwanted tags like 'script', 'style', etc.
        for script in soup(["script", "style", "noscript"]):
            script.extract()
        filtered_html = str(soup)

        # Convert HTML to Markdown
        results = md(filtered_html)

        # Remove consecutive newlines
        results = re.sub(r"\n+", "\n", results).strip()

        return results

    async def close(self):
        await self.browser.close()

    def browse(self, url: str) -> str:
        return asyncio.get_event_loop().run_until_complete(self.abrowse(url))

    async def async_browse_and_save(self, url: str) -> str:
        content = await self.async_browse(url)
        filepath = self.save(url)
        return filepath

    def browse_and_save(self, url: str) -> str:
        return asyncio.get_event_loop().run_until_complete(
            self.async_browse_and_save(url)
        )

    def save(self, url: str) -> str:
        content = self.browse(url)

        # Generate filename based on the URL
        filename = f"{url.replace('https://', '').replace('/', '_')}.md"
        filepath = os.path.join(self.tmpdir.name, filename)

        # Save the content to a file in the temporary directory
        with open(filepath, "w") as f:
            f.write(content)

        self.url_map[filename] = url

        self.filename = filename

        return filepath

    def read(self, filename: str) -> str:
        filepath = os.path.join(self.tmpdir.name, filename)
        with open(filepath, "r") as f:
            content = f.read()
        return content

    def explore_website(self, query: str) -> str:
        """Assumes you have already fetched the contents of a webpage that is saved to `filename`. Using the query, it will try to respond to the query using the contents of the webpage. If a response cannot be generated, but you think there is a link that may lead you to the answer respond with the links"""

        if self.filename is None:
            raise ValueError("Filename is not set. Cannot explore website.")

        file_contents = self.read(self.filename)
        filename_only = os.path.basename(self.filename)
        # Extract the URL from filename for metadata
        url = self.url_map.get(filename_only, filename_only)
        # Prepare documents
        docs = [Document(page_content=file_contents, metadata={"source": url})]
        web_docs = self.text_splitter.split_documents(docs)
        results = []
        for i in range(0, len(web_docs), 4):
            input_docs = web_docs[i : i + 4]
            window_result = self.qa_chain(
                {"input_documents": input_docs, "question": query},
                return_only_outputs=True,
            )
            results.append(f"Response from window {i} - {window_result}")
        results_docs = [
            Document(page_content="\n".join(results), metadata={"source": url})
        ]
        res = self.qa_chain(
            {"input_documents": results_docs, "question": query},
            return_only_outputs=True,
        )
        return res


class WebBrowser:
    def __init__(self):
        self.browser = None
        self.playwright = None

    async def initialize(self):
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=True)

    async def goto(self, url: str):
        # Create a new browser context
        if self.browser is None:
            await self.initialize()
        context = await self.browser.new_context(
            java_script_enabled=False
        )  # Turn off JavaScript
        page = await context.new_page()
        try:
            await page.goto(url, wait_until="domcontentloaded")
        except Exception:
            pass  # Ignore timeout or other exceptions
        content = await page.content()
        await page.close()
        await context.close()
        return content

    async def close(self):
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
