# Requires BeautifulSoup4 and lxml 

import bs4
import flask
import urllib3
import random

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

app = flask.Flask(  # Create a flask app
  __name__,
  template_folder='templates',  # Name of html file folder
  static_folder='static'  # Name of directory for static files
)

@app.route('/')
def home():
  # Concatenate passed arguments
  args = flask.request.args.keys()
  query_string = "?hl=en&as_sdt=0%2C5&q=alex+atkins+bristol&btnG="
  if len(args) > 0:
    query_string = ""
    for arg in args:
      query_string += f"{arg}={flask.request.args.get(arg)}&"
    query_string.replace(" ", "+")

  pool_manager = urllib3.PoolManager()
  r = pool_manager.request(
    'GET',
    'scholar.google.co.uk/scholar?' + query_string,
    headers={
      'user-agent':
      'Mozilla/3.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
    })

  # Create empty XML for RSS feed
  rss_empty = bs4.BeautifulSoup(features='xml')
  rss_frame = rss_empty.new_tag("rss", version="2.0")
  rss_empty.append(rss_frame)
  rss_channel = rss_empty.new_tag("channel")
  rss_frame.append(rss_channel)

  rss_channel.append(rss_empty.new_tag("title", text="Scholar"))
  rss_channel.append(rss_empty.new_tag("link", text="http://www.url.com"))
  rss_channel.append(rss_empty.new_tag("description", text="Google Scholar API scraper."))


  html = bs4.BeautifulSoup(r.data, 'html.parser')

  print(r.data)
  
  # Iterate over gs_ri elements
  for research_item_html in html.findAll(attrs={"class" : "gs_ri"}):

      research_item = ResearchItem.from_html_element(research_item_html)

      rss_channel.append(research_item.to_xml(rss_empty))

  print(rss_empty.prettify())

  return rss_empty.prettify()


if __name__ == "__main__":  # Makes sure this is the main process
  app.run(  # Starts the site
    host='0.0.0.0',  # EStablishes the host, required for repl to detect the site
    port=8080  # Randomly select the port the machine hosts on.
  )