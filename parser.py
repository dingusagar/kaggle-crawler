import os
import glob
import logging
from natsort import natsorted
from bs4 import BeautifulSoup

from seqlbtoolkit.io import set_logging, save_json

logger = logging.getLogger(__name__)


def main():
    html_files = natsorted(glob.glob("pages/*.html"))

    titles, hrefs = list(), list()

    for html_file in html_files:
        with open(html_file, "r") as f:
            html_content = f.read()

        try:
            tts, refs = parse(html_content)

            if not tts or not refs:
                logger.warning(f"No competition found in {html_file}")
                continue

            titles.extend(tts)
            hrefs.extend(refs)

        except Exception as e:
            logger.error(f"Failed to parse {html_file}: {e}")

    save_json({"titles": titles, "hrefs": hrefs}, "competitions.json")
    logger.info("Competition information saved to competitions.json")

    return None


def parse(html_content: str) -> None:
    """
    Parse HTML content and extract article information

    Parameters
    ----------
    html_content: HTML string

    Returns
    -------
    list of dict
    """
    soup = BeautifulSoup(html_content, "html.parser")
    body = soup.body
    uls = body.find_all("ul")
    for ul in uls:
        if "jpEqsK" in ul.attrs.get("class", []):
            break

    titles = list()
    hrefs = list()
    for li in ul.children:
        titles.append(li.attrs["aria-label"].strip())
        a = li.find("a")
        hrefs.append(a.attrs["href"].strip())

    return titles, hrefs


if __name__ == "__main__":
    set_logging()
    main()
