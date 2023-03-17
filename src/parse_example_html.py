import bs4

class ResearchItem:

    def __init__(self, title, href, author):
        self.title = title
        self.href = href
        self.author = author

    def __str__(self):
        string_truncate = lambda str_in : str_in if len(str_in) < 32 else str_in[0:29]+"..."
        return f"ResearchItem:\n" + \
               f"| Title  : {string_truncate(self.title)}\n" + \
               f"| Author : {string_truncate(self.author)}\n" + \
               f"| URL    : {string_truncate(self.href)}\n"
    
    def to_xml(self, xml_root):
        xml_element = xml_root.new_tag("item")
        xml_element.append(xml_root.new_tag("title", text=self.title))
        xml_element.append(xml_root.new_tag("author", text=self.author))
        xml_element.append(xml_root.new_tag("url", text=self.href))
        return xml_element

    @staticmethod
    def from_html_element(element):

        # Get title object
        title_obj = element.find(attrs={"class" : "gs_rt"})
        # and anchor
        title_anchor = element.find("a")

        # Get author text
        author_obj = element.find(attrs={"class" : "gs_a"})

        return ResearchItem(title_anchor.text, title_anchor.get("href"), author_obj.text)

if __name__ == "__main__":

    # Create empty XML for RSS feed
    rss_empty = bs4.BeautifulSoup(features='xml')
    rss_frame = rss_empty.new_tag("rss", version="2.0")
    rss_empty.append(rss_frame)
    rss_channel = rss_empty.new_tag("channel")
    rss_frame.append(rss_channel)

    rss_channel.append(rss_empty.new_tag("title", text="Scholar"))
    rss_channel.append(rss_empty.new_tag("link", text="http://www.url.com"))
    rss_channel.append(rss_empty.new_tag("description", text="Google Scholar API scraper."))

    with open("data/example_data.xml", "r") as fh:

        html = bs4.BeautifulSoup(fh.read(), 'html.parser')
        
        # Iterate over gs_ri elements
        for research_item_html in html.findAll(attrs={"class" : "gs_ri"}):

            research_item = ResearchItem.from_html_element(research_item_html)

            rss_channel.append(research_item.to_xml(rss_empty))

    print(rss_empty)



