import pywikibot    # type: ignore

site = pywikibot.Site("en", "wikipedia")
simple_site = pywikibot.Site("simple", "wikipedia")


def fetch_summaries(article: str, lang: str = "en") -> str | None:
    try:
        site = pywikibot.Site(lang, "wikipedia")
        page = pywikibot.Page(site, article)

        if not page.exists():
            print(f"Page {article} does not exist.")
            return None

        if page.isDisambig():
            print(f"Page {article} is a disambiguation page.")
            return None

        if page.isRedirectPage():
            page = page.getRedirectTarget()

        return page.extract()
    except pywikibot.exceptions.Error as e:
        print(f"Error fetching {article}: {e}")
        return None
