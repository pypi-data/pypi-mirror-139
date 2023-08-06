"""Cache URLs and their contents."""

import skutterbug
import web

app = web.application(
    __name__, prefix="cache", args={"domain": r"[\w:.-]+", "page": r".+"}
)


def index(url, depth=0, confine=True):
    """
    Fetch and index given `url` if not already indexed.

    Set `depth` to -1 to continue forever.

    """
    current_url, resource = web.tx.cache[url]
    if depth == 0:
        return
    elif depth > 0:
        depth -= 1
    for link in resource.dom.select("a"):
        try:
            link = link.href.strip()
        except AttributeError:  # no href=".."; eg. onClick js only
            continue
        if link == "" or link.startswith(("#", "mailto:")):
            continue
        if link.startswith("/"):
            new_url = current_url
            new_url.path = link
            web.enqueue(index, str(new_url), depth, confine)
            continue
        new_url = skutterbug.uri(link)
        if new_url.origin != current_url.origin and confine:
            continue
        web.enqueue(index, str(new_url), depth, confine)


@app.control("")
class Cache:
    """"""

    def get(self):
        """"""
        return app.view.index(web.tx.cache.domains)

    def post(self):
        """"""
        web.enqueue(index, web.form("url").url)
        raise web.Accepted("added URL to cache")


@app.control("{domain}")
class Site:
    """"""

    def get(self):
        """"""
        resources = web.tx.cache.get_pages(self.domain)
        return app.view.domain(self.domain, resources)

    def post(self):
        action = web.form("action").action
        if action == "forget":
            web.tx.cache.forget_domain(self.domain)
            raise web.Accepted("Site forgotten.")


@app.control("{domain}/{page}")
class Page:
    """"""

    def get(self):
        """"""
        resource = web.tx.db.select(
            "cache",
            where="url = ? OR url = ?",
            vals=[f"https://{self.resource}", f"http://{self.resource}"],
        )[0]
        return app.view.resource(resource)
