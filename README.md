# CurrysReviews
Scraping Reviews from Currys(UK)

You Only need url of product page for scraping customer reviews.

Example:
LG PK5 Currys Product Page:


from CurrysBot import currys_dong_scraper
url='https://www.currys.co.uk/gbuk/audio-and-headphones/audio/hifi-systems-and-speakers/lg-pk5-xboom-go-portable-bluetooth-speaker-black-10180615-pdt.html'

curry=currys_dong_scraper(url)
curry.dong_scraper()

Result you'll get Dataframe consisting of
Rating/Date/Pros/Cons/Month/Year



