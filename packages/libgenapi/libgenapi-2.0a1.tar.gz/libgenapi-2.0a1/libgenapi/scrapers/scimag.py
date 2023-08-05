from datetime import time
import math
from random import random
import re
from typing import List

import urllib3
from libgenapi.scrapers.base import BaseParser
import requests
from bs4 import BeautifulSoup


class Issue:
    """Issue Details of an Article."""

    year: int
    month: int
    day: int
    volume: str
    issue: str
    first_page: int
    last_page: int


class Article:
    """Article Details."""

    doi: str
    author: str
    article: str
    doi_owner: str
    journal: str
    issue: Issue = Issue()
    issn: str
    size: str
    mirrors: List[str] = []
    
class ArticleSearchRequest:
    search_term: str,
    journal_id: str,
    volume_year: str,
    issue: str, 
    request = {
        "s": search_term,
        "journalid": journal_title_issn,
        "v": volume_year,
        "i": issue,
        "p": pages,
        "redirect": "0",
    }


class ScimagParser(BaseParser):
    """Parser for the Scientific Magazines section.

    It allows to search the scientific magazines section and it provides with all the
    metadata found and the mirror links to the articles.
    """

    __columns = [
        "doi_and_mirrors",
        "author",
        "article",
        "doi_owner",
        "journal",
        "issue",
        "issn",
        "size",
    ]

    def __init__(self, url: str) -> None:
        """Initializates the ScimagParser.

        Args:
            url (str): Full url to the Scientific Magazine Section
        """
        self.url = url

    def __parseColumn(self, article: Article, column: str, columnData) -> int:
        if column == "doi_and_mirrors":  # Getting doi and mirrors links
            article.doi = columnData.select("table/tr[1]/td[2]").text()
            mirrors = columnData.select("table/tr//a/@href")
            for mirror in mirrors:
                article.mirrors += [
                    g.make_url_absolute(mirror.text())
                ]  # TODO: Fix this somehow.
        elif column == "issn":
            article.issn = columnData.select("*/text()").node_list()
        elif column == "issue":
            splitIssueData = [
                x.split(":")[1] for x in columnData.select("text()").node_list()
            ]
            article.issue.year = splitIssueData[0]
            article.issue.month = splitIssueData[1]
            article.issue.day = splitIssueData[2]
            article.issue.volume = splitIssueData[3]
            article.issue.issue = splitIssueData[4]
            article.issue.first_page = splitIssueData[5]
            article.issue.last_page = splitIssueData[6]
        else:
            setattr(article, column, columnData.text())

    def __parse(self, body: BeautifulSoup):
        article = Article()
        parse_result = []
        for row in body.select("//body/table[2]/tr"):
            article = Article()
            for i, col in enumerate(row.select("td")):
                if i > len(self.__columns) - 1:
                    break
                self.__parseColumn(article, self.__columns[i], col)
            parse_result += [article]
        return parse_result

    def search(
        self,
        search_term: str = "",
        journal_title_issn: str = "",
        volume_year: str = "",
        issue: str = "",
        pages: str = "",
        number_results: int = 25,
    ):
        request = {
            "s": search_term,
            "journalid": journal_title_issn,
            "v": volume_year,
            "i": issue,
            "p": pages,
            "redirect": "0",
        }
        url = self.url + "?" + urllib3.parse.urlencode(request)
        response = requests.get(url)
        body = BeautifulSoup(response.text)
        search_result = []
        nresults = re.search(
            r"([0-9]*) results", body.select("/html/body/font[1]").one().text()
        )
        nresults = int(nresults.group(1))
        pages_to_load = int(
            math.ceil(number_results / 25.0)
        )  # Pages needed to be loaded
        # Check if the pages needed to be loaded are more than the pages available
        if pages_to_load > int(math.ceil(nresults / 25.0)):
            pages_to_load = int(math.ceil(nresults / 25.0))
        for page in range(1, pages_to_load + 1):
            if len(search_result) > number_results:  # Check if we got all the results
                break
            url = ""
            request.update({"page": page})
            url = self.url + "?" + urllib3.parse.urlencode(request)
            response = requests.get(url)
            body = BeautifulSoup(response.text)
            search_result += self.__parse(body)
            if page != pages_to_load:
                # Random delay because if you ask a lot of pages,your ip might get blocked.
                time.sleep(random.randint(250, 1000) / 1000.0)
        return search_result[:number_results]
