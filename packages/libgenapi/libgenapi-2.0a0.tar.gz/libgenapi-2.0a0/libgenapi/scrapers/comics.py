
    class __Comics(object):
        def __init__(self, url):
            self.url = url

        def __parse(self, g):
            doc = g.doc
            comic = {
                "cover": None,
                "mirrors": [],
                "title": None,
                "size": None,
                "filetype": None,
                "dateAdded": None,
                "scanDpi": None,
                "scanPixels": None,
                "pages_nfiles": None,
                "pages_npictures": None,
                "comicsDOTorg": None,
            }
            i = 0
            d_keys = [
                "cover",
                "mirrors",
                "http_mirror_and_title",
                "size_filetype",
                "dateAdded",
                "scanDpi_and_scanPixels",
                "pages",
                "comicsDOTorg",
            ]
            parse_result = []
            for resultRow in doc.select("/html/body/table[2]/tr"):
                i = 0
                comic = {
                    "cover": None,
                    "mirrors": [],
                    "title": None,
                    "size": None,
                    "filetype": None,
                    "dateAdded": None,
                    "scanDpi": None,
                    "scanPixels": None,
                    "pages_nfiles": None,
                    "pages_npictures": None,
                    "comicsDOTorg": None,
                }
                for resultColumn in resultRow.select("td"):
                    if i > len(d_keys) - 1:
                        break
                    if d_keys[i] == "mirrors":  # Getting mirrors.
                        mirrors = resultColumn.select("font/a/@href")
                        for mirror in mirrors:
                            comic["mirrors"] += [g.make_url_absolute(mirror.text())]
                    elif (
                        d_keys[i] == "http_mirror_and_title"
                    ):  # Getting http mirror link and title.
                        # http_mirror = resultColumn.select("font/a/@href")[0].text()
                        # comic["mirrors"] += [http_mirror]
                        comic["title"] = resultColumn.select(
                            "descendant-or-self::text()"
                        ).node_list()[0]
                    elif d_keys[i] == "size_filetype":  # Getting size and filetype.
                        comic["size"] = resultColumn.select("text()[1]").text()
                        comic["filetype"] = resultColumn.select("text()[2]").text()
                    elif (
                        d_keys[i] == "scanDpi_and_scanPixels"
                    ):  # Getting scan size in pixels and scan dpi.
                        comic["scanPixels"] = resultColumn.select("font/a")[0].text()
                        comic["scanDpi"] = resultColumn.select("font/a")[2].text()
                    elif d_keys[i] == "cover":  # Gettin
                        comic["cover"] = g.make_url_absolute(
                            resultColumn.select("a/img/@src").text()
                        )
                    elif d_keys[i] == "pages":  # Getting pages info.
                        comic["pages_nfiles"] = resultColumn.select("font/a")[0].text()
                        comic["pages_npictures"] = resultColumn.select("font/a")[
                            2
                        ].text()
                    else:
                        comic[d_keys[i]] = resultColumn.text()
                    i += 1
                parse_result += [comic]
            return parse_result

        def search(self, search_term="", pages="", number_results=25):
            # TODO: Add Batch search for comics.
            g = grab.Grab()
            request = {"s": search_term, "p": pages}
            if sys.version_info[0] < 3:
                url = self.url + "?" + urllib.urlencode(request)
            else:
                url = self.url + "?" + urllib.parse.urlencode(request)
            g.go(url)
            search_result = []
            nresults = re.search(
                r"([0-9]*) results", g.doc.select("/html/body/font[1]").one().text()
            )

            nresults = int(nresults.group(1))
            pages_to_load = int(
                math.ceil(number_results / 25.0)
            )  # Pages needed to be loaded
            # Check if the pages needed to be loaded are more than the pages available
            if pages_to_load > int(math.ceil(nresults / 25.0)):
                pages_to_load = int(math.ceil(nresults / 25.0))
            for page in range(1, pages_to_load + 1):
                if (
                    len(search_result) > number_results
                ):  # Check if we got all the results
                    break
                url = ""
                request.update({"page": page})
                if sys.version_info[0] < 3:
                    url = self.url + "?" + urllib.urlencode(request)
                else:
                    url = self.url + "?" + urllib.parse.urlencode(request)
                g.go(url)
                search_result += self.__parse(g)
                if page != pages_to_load:
                    # Random delay because if you ask a lot of pages,your ip might get blocked.
                    time.sleep(random.randint(250, 1000) / 1000.0)
            return search_result[:number_results]
