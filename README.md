# Google Scholar to RSS API
Takes a Google Scholar query string and outputs an RSS stream of the first page
of paper titles, authors and corresponding URLs.

Example query string:

    ?hl=en&as_sdt=0%2C5&q=magnetic+resonance+imaging&btnG=

And RSS formatted result:

    <?xml version="1.0" encoding="utf-8"?>
    <rss version="2.0">
        <channel>
            <title text="Scholar"/>
            <link text="http://www.url.com"/>
            <description text="Google Scholar API scraper."/>
            <item>
                <title text="Contraindications to magnetic resonance imaging"/>
                <author text="T Dill - Heart, 2008 - heart.bmj.com"/>
                <url text="https://heart.bmj.com/content/94/7/943.short?casa_token=QUHPNx83IggAAAAA:kz8kP70Rle0gXyPi8XUWRFYov3vEYRsYSHbb1CzLhqRmzteCugAfZphS0Tm8oPaYexP0b0vm"/>
            </item>
            ...
        </channel>
    </rss>
