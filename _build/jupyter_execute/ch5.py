# Web Scraping Using `BeautifulSoup`

```{contents} Table of Contents
:depth: 4
```

## Introduction: Is Web Scraping Legal?
Web scraping is the practice of downloading the raw HTML code that generates a website, and instead of parsing the code to display it like we do with a web browser whenever we navigate to a page, we dig through the code for data. 

There are **significant legal and ethical questions** regarding web scraping. Right now, there is a court case - [HiQ Labs vs. LinkedIn](https://en.wikipedia.org/wiki/HiQ_Labs_v._LinkedIn) - that will establish whether and under what conditions web scraping is legal. 

<img src="https://crowdjustice.imgix.net/pictures/courtroom5-gray_uI7BCRV.png?auto=enhance%2Cformat&crop=faces&fit=crop&q=80&w=1200" width="600" height="600">

HiQ is a company that scraps data from individuals' LinkedIn profiles to compile data to use to build models that predict whether employees will leave their positions for new jobs. They use the insights from these models to consult with businesses to reduce employee turnover. In 2017 LinkedIn issued a Cease and Desist order to HiQ and took steps to prevent anyone including HiQ from deploying scrapers on profiles. Because HiQ's business model is entirely dependent on collecting data from LinkedIn profiles, this action by LinkedIn would have caused HiQ to go out of business. Instead, HiQ filed a lawsuit against LinkedIn in federal court. HiQ argued that user profiles contain data that are owned by the LinkedIn users themselves who intend to make that information public using the LinkedIn platform -- and so, because the data owners are sharing their own data, HiQ should be able to access that data. LinkedIn argued that the HiQ's scraping of user data amounts to theft, is a violation of the [Consumer Fraud and Abuse Act](https://en.wikipedia.org/wiki/Computer_Fraud_and_Abuse_Act), and violates LinkedIn users' privacy. 

In 2017 a federal district court issued an injunction that prevented LinkedIn from blocking HiQ's scraping scripts. The case was appealed to the Circuit Court, where [this injuction was upheld in 2019](https://www.reuters.com/article/us-microsoft-linkedin-profiles/microsofts-linkedin-loses-appeal-over-access-to-user-profiles-idUSKCN1VU21W). In March 2020 LinkedIn filed for the case to be appealed to the U.S. Supreme Court. It is likely that this case will be decided at the highest level in the United States sometime in the next year. What the Supreme Court decides will have [massive ramifications](https://www.natlawreview.com/print/article/linkedin-files-petition-to-supreme-court-hiq-web-scraping-case) on the use of web scraping, data science, and on the tech industry at large. It will establish whether web scraping is legal, legal with restrictions, or illegal, and it will have implications for data ownership and the extent to which large tech companies control and own the data that exist on their platforms.

If this debate is interesting to you, here's a longer, philosophically-oriented article about the virtues of web scraping for academic research: https://research.gold.ac.uk/6768/1/Marres_Weltrevede_Scraping_the_Social_draft.pdf

Even if scraping is legal, it might not be ethical. Scraping calls a server that is not designed for the transference of data the way an API is. As such, many repeated calls (from bots) to a website for the purpose of scraping data might overwhelm the server, keeping the website's owners from being able to achieve their purpose for having the website. This [article by James Densmore](https://towardsdatascience.com/ethics-in-web-scraping-b96b18136f01) outlines some ethical considerations for scrapers and for website owners, and lays out the following code of conduct: 

"I, the web scraper will live by the following principles:

* If you have a public API that provides the data I’m looking for, I’ll use it and avoid scraping all together.

* I will always provide a User Agent string that makes my intentions clear and provides a way for you to contact me with questions or concerns.

* I will request data at a reasonable rate. I will strive to never be confused for a DDoS attack.

* I will only save the data I absolutely need from your page. If all I need it OpenGraph meta-data, that’s all I’ll keep.

* I will respect any content I do keep. I’ll never pass it off as my own.

* I will look for ways to return value to you. Maybe I can drive some (real) traffic to your site or credit you in an article or post.

* I will respond in a timely fashion to your outreach and work with you towards a resolution.

* I will scrape for the purpose of creating new value from the data, not to duplicate it.

 . . . . I, the site owner will live by the following principles:

* I will allow ethical scrapers to access my site as long as they are not a burden on my site’s performance.

* I will respect transparent User Agent strings rather than blocking them and encouraging use of scrapers masked as human visitors.

* I will reach out to the owner of the scraper (thanks to their ethical User Agent string) before blocking permanently. A temporary block is acceptable in the case of site performance or ethical concerns.

* I understand that scrapers are a reality of the open web.

* I will consider public APIs to provide data as an alternative to scrapers."

In general, while scraping appears to exist in a legal and ethical grey area, there is a lot of litigation and many arguments that suggest that once information is posted publically on a website, that there is no longer an expectation of privacy, and the data is open for anyone to use. But be careful when you use web scraping! If there IS an expectation of privacy, such as for any website with a password or other restrictions on access, then the legality and ethics of web scraping are much more dubious. If an API is available, it's available for a reason, and it's the correct ethical decision to use the API instead of scraping. Use care and judgment.

## How Websites Prevent You From Scraping
This discussion follows the excellent overview by a Stack Overflow and GitHub contributor with the username JonasCz (I wish I knew this user's real name!) on [how to prevent web scraping](https://github.com/JonasCz/How-To-Prevent-Scraping/blob/master/README.md).

To understand the restrictions and challenges you will encounter when scraping data, put yourself in the position of a website's owner:

If you own and maintain a website, there are many reasons why you might want to prevent web scraping bots from accessing the data on your website. Maybe the bots will overload the traffic to your site and make it impossible for your website to work as you intend. You might be running a business through this website and sharing the data in mass transfers would undercut your business. For whatever reason, you are now faced with a challenge: how to you prevent automated scraping of the data on your webpage while still allowing individual customers to view your website?

Web scraping will require issuing HTTP requests to a particular web address with a tool like `requests`, sometimes many times in a short period. Every HTTP request is logged by the server that receives the request, and these logs contain the IP address of the entity making the request. If too many requests are made by the same IP address, the server can block that IP address. The coding logic to automatically identify and block overactive IP addresses is simple, so many websites include these security measures. Some blocks are temporary, placing a rate limit on these requests to slow down the scrapers, and some blocks reroute scrapers through a CAPTCHA (which stands for "Completely Automated Test to Tell Computers and Humans Apart") to prevent robots like a scraper from accessing the website. JonasCz recommends that these security measures look at other factors as well: the speed of actions on the website, the amount of data requested, and other factors that can identify a user when the IP address is masked.

Stronger gates, such as making users register for a username and password with email confirmation to use your website, are effective against scraping bots. But they also turn away individuals who wouldn't want to jump through those hoops. Saving all text as images on your server will prevent bots from accessing the text very easily, but it makes the website harder to use and violates regulations that protect people with disabilities.

Instead, JonasCz recommends building your website in a way that never reveals the entirety of the data you own, and never reveals the private API endpoints you use to display the data. Also, web scrapers are fragile: they are built to pull data from the specific HTML structure of a particular website. Changing the HTML code frequently or using different versions of the code based on geographic location will break the scrapers that are built for that code. JonasCz also suggests adding "honeypot" links to the HTML code that will not be displayed to legitimate users but will be followed by scrapers that recursively follow links, and taking action against the agents that follow these links: block their IP addresses, require a CAPTCHA, or deliver fake data.

One important piece of information in a request is the user agent header (which we discuss in more detail [below](#useragent)). JonasCz recommends looking at this information and blocking requests when the user agent is blank or matches information from agents that have previously been identified as malicious bots.

Understanding the steps you would take to protect your data from bots if you owned a website, you should have greater insight into why a web scraping endeavor may fail. Your web scraper might not be malicious, but might still violate the rules that the website owner setup to guard against bots. These rules are usually listed explicitly in a file on the server, usually called `robots.txt`. Some tips for reading and understanding a `robots.txt` file are here: https://www.promptcloud.com/blog/how-to-read-and-respect-robots-file/

For example, in this document we will be scraping data on the playlist of a radio station from https://spinitron.com/. This website has a `robots.txt` file here: https://spinitron.com/robots.txt, which reads:
```
User-agent: *
Crawl-delay: 10
Request-rate: 1/10
```
The `User-agent: *` line tells us that the next two lines apply to all user agent strings. `Crawl-delay: 10` places a limit on the frequency with which our scraper can make a request from this website. In this case, individual requests must be made 10 second apart. `Request-rate: 1/10` tells us that our scraper is only allowed to access one page every 10 seconds, and that we are not allowed to make requests from more than one page at the same time.

## Using `requests` with a User Agent Header
As the articles by James Densmore and JonasCz described, requests are much more likely to get blocked by websites if the request does not specify a header that contains a user agent. An HTTP header is a parameter that gets sent along with the HTTP request that contains metadata about the request. A user agent header contains contact and identification information about the person making the request. If there is any issue with your web scraper, you want to give the website owner a chance to contact you directly about that problem. If you do not feel comfortable being contacted by the website's owner, you should reconsider whether you should be scraping that website.

Fortunately, it is straightforward to include headers in a GET request using `requests`: just use the `headers` argument. First, we import the relevant libraries:

import numpy as np
import pandas as pd
import requests

In module 4 we issued GET requests from the Wikipedia API as an example.

r = requests.get("https://en.wikipedia.org/w/api.php")
r

To add a user agent string, I use the following code:

headers = {'user-agent': 'Kropko class example (jkropko@virginia.edu)'}
r = requests.get("https://en.wikipedia.org/w/api.php", headers = headers)
r

What information needs to go into a user agent header? Different resources have different information about that. According to [Amazon Web Services](https://docs.developer.amazonservices.com/en_US/dev_guide/DG_UserAgentHeader.html), a user agent should identify your application, its version number, and programming language. So a user agent should look like this:

headers = {'user-agent': 'Kropko class example version 1.0 (jkropko@virginia.edu) (Language=Python 3.8.2; Platform=Mac OSX 10.15.5)'}
r = requests.get("https://en.wikipedia.org/w/api.php", headers = headers)
r

Including a user agent is not hard, and it goes a long way towards alleviating the anxieties that website owners have about dealing with your web scraping code. It is a good practice to cultivate into a habit. 

## Using `BeautifulSoup()` (Example: WNRN, Charlottesville's Legendary Radio Station)
WNRN is a legendary radio station, and it's based right here in Charlottesville at 91.9 FM (and streaming online at www.wnrn.org). It's commercial-free, with only a few interruptions for local nonprofits to tell you about cool things happening in town. They play a mix of new and classic alternative rock and R&B. They emphasize music for bands coming to play at local venues. And they play the Grateful Dead on Saturday mornings. You should be listening to WNRN!

<center><img src="https://upload.wikimedia.org/wikipedia/en/thumb/0/0e/WNRN-FM_2014.PNG/200px-WNRN-FM_2014.PNG" width="300" height="300" class="center"></img></center>

The playlist of the songs that WNRN has played in the last few hours is here: https://spinitron.com/WNRN/. I want to scrape the data off this website. I also want to scrape the data off of the additional playlists that this website links to, to collect as much data as possible. Our goal in this example is to create a dataframe of each song WNRN has played, the artist, the album, and the time each song was played.

The process involves four steps:

1. Download the raw text of the HTML code for the website we want to scrape using the `requests` library.

2. Use the `BeautifulSoup()` function from the `bs4` library to parse the raw text so that Python can understand, search through, and operate on the HTML tags from string.

3. Use methods associated with `BeautifulSoup()` to extract the data we need from the HTML code.

4. Place the data into a `pandas` data frame.

### Downloading and Understanding Raw HTML
For this example, I first download the HTML that exists on https://spinitron.com/WNRN using the `requests.get()` function. To be ethical and to help this website's owners know that I am not a malicious actor, I also specify a user agent string. 

url = "https://spinitron.com/WNRN"
headers = {'user-agent': 'Kropko class example (jkropko@virginia.edu)'}
r = requests.get(url, headers=headers)
r

The raw HTML code contains a series of text fragments that look like this,
```
<tag attribute="value"> Navigable string </tag>
```
where `tag`, `attribute`, `"value"`, and `Navigable string` are replaced by specific parameters and data that control the content and presentation of the webpage that gets displayed in a web browser. For example, here are the first 1000 characters of the raw text from WNRN's playlist:

print(r.text[0:1000])

**Tags** specify how the data contained within the page are organized and how the visual elements on this page should look. Tags are designated by opening and closing angle braces, < and >. In the HTML code displayed above, there are tags named 

* `<html>`, which tells browsers that the following code is written in HTML, 
* `<meta>`, which defines metadata in the document that help govern how the output shold be displayed in the browser, 
* `<title>`, which sets the title of the document, and 
* `<link>`, which pulls data or images from external resources for later use. 

To see what other HTML tags do, look at the list on https://www.w3schools.com/TAGs/. 

In some cases the tag operates on the text that immediately follows, and a closing tag `</tag>` frames the text that gets operated on by the tag. The text in between the opening and closing tag is called the **navigable string**. For example, the tag `<title>WNRN – Independent Music Radio</title>` specifies that "WNRN – Independent Music Radio", and only this string, is the title.

Some tags have **attributes**, which are arguments listed inside an opening tag to modify the behavior of that tag or to attach relevant data to the tag. The first `<html>` tag listed above contains an attribute `lang` with a value `"en"` that specifies that this document contains HTML code in English.



### Parsing Raw HTML Using `BeautifulSoup()`
The `requests.get()` function only downloads the raw text of the HTML code, but it does not yet understand the logic and organization of the HTML code. Getting Python to register text as a particular coding standard is called **parsing** the code. We've parsed code into Python before with JSON data. We used `requests.get()` to download the JSON formatted data, but we needed `json.loads()` to parse the data in order to be able to navigate the branches of the JSON tree. 

There are two widely used Python libraries for parsing HTML data: `bs4` which contains the `BeautifulSoup()` function, and `selenium`. `BeautifulSoup()` works with raw text, but cannot access websites themselves (we use `requests.get()` for that). In order to access the data on a website, the data needs to be visible in the raw HTML that `requests.get()` returns. If there are measures taken by a website to hide that data, possibly by calling server-side Javascript to populate data fields, or by saving data as image files, then we won't be able to access the data with an HTML parser. `selenium` has more features to extract more complicated data and circumvent anti-scraping measures, such as taking a screenshot of the webpage in a browser and using optical character recognition (OCR) to pull data directly from the image. However, `selenium` requires each request to be loaded in a web browser, so it can be quite a bit slower than `BeautifulSoup()`. If you are interested in learning how to use `selenium`, see this guide: https://selenium-python.readthedocs.io/. Here we will be using `BeautifulSoup()`.

First I import the `BeautifulSoup()` function:

from bs4 import BeautifulSoup

To use it, we pass the `.text` attribute of the `requests.get()` output from https://spinitron.com/WNRN to `BeautifulSoup()` (which I saved as `r.text` above). This function can parse either HTML or XML code, so the second argument should specify HTML:

wnrn = BeautifulSoup(r.text, 'html')

Now that the https://spinitron.com/WNRN source code is registered as HTML code in Python, we can begin executing commands to navigate the organizational structure of the code and extract data. 

### Searching for HTML Tags and Extracting Data
While HTML is a coding language, it does not force coders to follow very strict templates. There's a lot of flexibility and creativity possible for HTML programmers, and as such, there is no one universal method for extracting data from HTML. The best approach is to open a browser window, navigate to the webpage you want to scrape, and "view page source". (Different web browsers have different ways to do that. On Mozilla Firefox, right click somewhere on the page other than an active link, and "view page source" should be an option.) The source will display the raw HTML code that generates the page. You will need to search through this code to find examples of the data points you intend to collect, possibly using control+F to search for specific values. Once you find the data you need, make note of the tags that surround the data and use the tools we will describe next to extract the data.

The parsable HTML `BeautifulSoup()` output, `wnrn`, has important methods and attributes that we will use to extract the data we want. First, we can use the name of a tag as an attribute to extract the first occurrence of that tag. Here we extract the first `<meta>` tag:

metatag = wnrn.meta
metatag

This tag stores its attributes as a list, so we can extract the value of an attribute by calling the name of that attribute as follows:

metatag['charset']

If a tag has a navigable string, we can extract that with the `.string` attribute of a particular tag. For example, to extract the title, we start with the `<title>` tag:

titletag = wnrn.title
titletag

Then we extract the title as follows:

titletag.string

Our goal in this example is to extract the artist, song, album, and time played for every song played on WNRN. I look in the raw HTML source code for the first instance of an artist. These data are contained in the `<span>` tags:

spantag = wnrn.span
spantag

Calling one tag is not especially useful, because we generally want to extract all of the relevant data on a page. For that, we can use the `.find_next()` and `.find_all()` methods, both of which are very literal. The next `<span>` tag in the HTML code contains the song associated with the artist:

spantag.find_next()

And the next occurrence of `<span>` contains the album name (under `"release"`):

spantag.find_next().find_next()

To find all occurrences of the `<span>` tag, organized in a list, use `.find_all()` and provide the tag as the argument:

spanlist = wnrn.find_all("span")
spanlist

Notice that the HTML source code distinguishes between the three types of datapoint with different `class` values. To limit this list to just the artists, we can specify the `"artist"` class as a second argument of `.find_all()`:

artistlist = wnrn.find_all("span", "artist")
artistlist

Likewise we can create lists of the songs:

songlist = wnrn.find_all("span", "song")
songlist

And a list for the albums:

albumlist = wnrn.find_all("span", "release")
albumlist

Finally, we want to also extract the times each song was played. I look at the HTML code and find an example of the play time. These times are stored in the `<td>` tag with `class="spin-time"`. I create a list of these times:

timelist = wnrn.find_all("td", "spin-time")
timelist

Sometimes the information we need exists in a particular tag, but only when a specific attribute is present. For example, in the WNRN playlist HTML there are many `<a>` tags, but only some of those tags include a `title` attribute. To extract all of the `<a>` tags with a `title` attribute, specify `title=True` in the call to `.find_all()`:

atags_title = wnrn.find_all("a", title=True)
print(atags_title[0:5]) # just show the first 6 elements

### Constructing a Data Frame from HTML Data
Next we need to place these data into a clean data frame. For that, we will need to keep the valid data while dropping the HTML tags. We stored the tags with the artists, songs, albums, and times in separate lists. Every name is stored as a navigable string in the HTML tags, so to extract these names we need to loop across the elements of the list. The simplest loop for this task is called a **list comprehension**, which has the following syntax:

*newlist* `= [` *expression* `for` *item* `in` *oldlist* `if` *condition* `]`

In this syntax, we are creating a new list by iteratively performing operations on the elements of an existing list (*oldlist*). *item* is a token that we will use to represent one item of the existing list. *expression* is the same Python code we would use on a single element of the existing list, except we replace the name of the element with the token defined with *item*. Finally *condition* is an optional part of this code which sets a filter by which only certain elements of the old list are transformed and placed into the new list (there's an example of conditioning in a comprehension loop in the section on [spiders](#spider)).

For example, to extract the navigable string from every element of `artistlist`, we can set *item* to `a`, *expression* to `a.string`, and *list* to `artistlist`:

artists = [a.string for a in artistlist]
artists

Likewise, we extract the navigable strings for the songs, albums, and times:

songs = [a.string for a in songlist]
albums = [a.string for a in albumlist]
times = [a.string for a in timelist]

Finally, to construct a clean data frame, we create a dictionary that combines these lists and passes this dictionary to the `pd.DataFrame()` function:

mydict = {'time':times,
          'artist':artists,
         'song':songs,
         'album':albums}
wnrn_df = pd.DataFrame(mydict)
wnrn_df

## Building a Spider
At the bottom of the WNRN playlist on https://spinitron.com/WNRN/ there are links to older song playlists. Let's extend our example by building a **spider** to capture the data that exists on these links as well. A spider is a web scraper that follows links on a page automatically and scrapes from those links as well. 

I look at the page source for these links, and find that they are contained in a `<div class="recent-playlists">` tag. I start by finding this tag. As there's only one occurrence, I can use `.find()` instead of `.find_all()`:

recent = wnrn.find("div", "recent-playlists")
recent

Notice that all of the addresses we need are contained in `<a>` tags. We can extract these `<a>` tags with `.find_all()`:

recent_atags = recent.find_all("a")
recent_atags

The resulting list contains the web endpoints we need, and also some web endpoints we don't need: we want the URLs that contain the string `/pl/` as these are playlists, and we want to exclude the URLs that contain the string `/dj/` as these pages refer to a particular DJ. We need a comprehension loop that loops across these elements, extracts the `href` attribute of the entries that include `/pl/`, and ignore the entries that include `/dj/`. We again use this syntax:

*newlist* `= [` *expression* `for` *item* `in` *oldlist* `if` *condition* `]`

In this case:

* *newlist* is a list containing the URLs we want to direct our spider to. I call it `urls`.
* *item* is one element of `recent_atags`, which I will call `pl`.
* *expression* is code that extracts the web address from the `href` attribute of the `<a>` tag, so here the code would be `pl['href']`.
* Finally, *condition* is a logical statement that should be `True` if the web address contains `/pl/` and `False` if the web address contains `/dj/`. Here, the conditional statement should be `if "/pl/" in pl['href']`. This code will look for the string `"/pl/"` inside the string called by `pl['href']` and return `True` or `False` depending on whether this string is found.

Putting all this syntax together gives us our list of playlist URLs:

wnrn_url = [pl['href'] for pl in recent_atags if "/pl/" in pl['href']]
wnrn_url

First, we need to collect all of the code we created above to extract the artist, song, album, and play times from the HTML code. We define a function that does all of this work. We specify one argument for this function, the URL, so that all the function needs is the URL and it can output a clean dataframe. I name the function `wnrn_spider()`:

def wnrn_spider(url):
    """Perform web scraping for any WNRN playlist given the available link"""
    
    headers = {'user-agent': 'Kropko class example (jkropko@virginia.edu)'}
    r = requests.get(url, headers=headers)
    wnrn = BeautifulSoup(r.text, 'html')
    
    artistlist = wnrn.find_all("span", "artist")
    songlist = wnrn.find_all("span", "song")
    albumlist = wnrn.find_all("span", "release")
    timelist = wnrn.find_all("td", "spin-time")
    
    artists = [a.string for a in artistlist]
    songs = [a.string for a in songlist]
    albums = [a.string for a in albumlist]
    times = [a.string for a in timelist]
    
    mydict = {'time':times, 'artist':artists, 'song':songs, 'album':albums}
    wnrn_df = pd.DataFrame(mydict)
    
    return wnrn_df


We can pass any of the URLs we collected to our function and get the other playlists. We will have to add the domain "https://spinitron.com" to the beginning of each of the URLs we collected:

wnrn2 = wnrn_spider('https://spinitron.com/' + wnrn_url[0])
wnrn2

Our goal here is to loop across all the URLs we collected, extract the data in a clean data frame, and append these data frames together to construct a longer playlist. To do that, we will use a `for` loop, which has the following syntax:
```
for index in list:
    expressions
```
This syntax is similar to the syntax we used to build a comprehension loop. `list` is an existing list, and `index` stands in for one element of this list. For each element of the list, we execute the code contained in `expressions`, which can use the `index`.

For our spider, we will use the following steps:

1. We take the data we already scraped from https://spinitron.com/WNRN (saved as `wnrn_df`) and clone it as a new variable named `wnrn_total_playlist`. It is important that we make a copy, and that we do not overwrite `wnrn_df`. We will be repeatedly saving over `wnrn_total_playlist` within the loop, and if we do not overwrite `wnrn_df`, it gives us a stable data frame to return to as a starting point if we need to rerun this loop. 

2. We use a `for` loop to loop across all the web addresses inside `wnrn_url`.

3. In the `for` loop, we use the `wnrn_spider()` function to extract the playlist data from each of the URLs inside `wnrn_url`.

4. In the `for` loop, we use the `.append()` method to attach the new data to the bottom of the existing data, matching corresponding columns.

The code is as follows:

wnrn_total_playlist = wnrn_df 
for w in wnrn_url:
    moredata = wnrn_spider('https://spinitron.com/' + w) 
    wnrn_total_playlist = wnrn_total_playlist.append(moredata)

We now have a data frame that combines all of the playlists on https://spinitron.com/WNRN and on the playlists linked to under "Recent":

wnrn_total_playlist