from contextlib import contextmanager

import requests
import uuid as uuid
from furl import furl
from bs4 import BeautifulSoup as bs
import os


class WebParser:
    def create_task_dir(self, dirname: str):
        if os.path.exists(dirname):
            os.rmdir(dirname)
        os.mkdir(dirname)
        return os.path.join(os.getcwd(), dirname)

    def save_link_contents(self, url: furl , dir: os.path, filename: str):
        resp = requests.get(url.url)
        with open(os.path.join(dir, filename.replace("/", "")), "w") as f:
            f.write(resp.text)

    def parse(self, url: furl, uuid: uuid.uuid4):
        base_link = url.origin

        resp = requests.get(url.url)
        soup = bs(resp.text, "html.parser")
        task_path = self.create_task_dir(str(uuid))
        # create a html dir and put all the html code there
        os.mkdir(os.path.join(task_path, "html"))
        html_dir = os.path.join(task_path, "html")
        with open(os.path.join(html_dir, "html_body.html"), "w") as file:
            file.write(soup.body.prettify())
        # create a css dir - " -
        os.mkdir(os.path.join(task_path, "css"))
        css_dir = os.path.join(task_path, "css")
        for css in soup.findAll("link"):
            if css.get("rel")[0] in ("stylesheet", "shortcut", "icon"):
                href = css.get("href")
                furl_href = furl(href)
                if getattr(furl_href, "scheme", None) and getattr(furl_href, "netloc", None):
                    self.save_link_contents(furl_href.remove(args=True), css_dir, str(furl_href.path) + str(getattr(furl_href, "query", "")))
                else:
                    self.save_link_contents(furl(base_link).add(path=href), css_dir, href)
        # create a js dir - " -
        os.mkdir(os.path.join(task_path, "js"))
        js_dir = os.path.join(task_path, "js")
        for script in soup.findAll("script"):
            src = script.get("src")
            furl_src = furl(src)
            if src:
                if getattr(furl_src, "scheme", None) and getattr(furl_src, "netloc", None):
                    self.save_link_contents(furl_src.remove(args=True), js_dir, str(furl_src.path))
                else:
                    self.save_link_contents(furl(base_link).add(path=furl_src.remove(args=True).url), js_dir, str(furl_src.remove(args=True)))

# if __name__ == "__main__":
#     WebParser().parse(furl("https://www.thepythoncode.com/article/extract-web-page-script-and-css-files-in-python"),
#                       uuid.uuid4())
