# Acquiring Data from APIs 

```{contents} Table of Contents
:depth: 4
```

## Introduction: What is an API?
### Transfering Data Over the Internet
Where do we get our data? That depends on who is providing the data. In the simplest of cases, the data provider gives us a single file in CSV or JSON format. But some of the most important data providers are extremely big operations: social media companies, search engines, governments, finance firms, etc. Getting data from these organizations is more complicated than asking for a data file, but it is very possible to do using the application programming interfaces (APIs) that these organizations have set-up and made available online.

It's not feasible for these organizations to interact personally with every individual who requests data because every request may be unique, asking for different records, features, timeframes, locations, and formatting. In addition, to fulfill a request, the data provider might need information from the data requester first: for example, if I want Google Maps to give me the latitudinal and longitudinal coordinates of my house, I first need to tell Google Maps my address. In short, there are too many requests for humans to handle given that each request requires a conversation between the person providing the data and the person requesting the data.

Organizations instead store and share their data electronically through automated **web applications**. A web application has three parts: the user interface (the frontend), the data storage and organization system (the backend), and an API that connects the frontend and backend. Many authors, including [Huang, Chung, and Chan](https://www.oreilly.com/library/view/python-api-development/9781838983994/), use the analogy of a restaurant to describe an API. Customers place orders for the chefs to prepare, and waiters take the orders to the chefs, and return the food to the customers. In this analogy, customers are the frontend, issuing data requests; chefs are the backend, organizing and disseminating data; and waiters are the API, conducting the communication between the frontend and backend. Another analogy is the way our brains receive and react to sensory information. In this case, our senses comprise the API that connects the outside world to the internal workings of our brains.

APIs usually send and receive data in JSON (and sometimes XML) format. So being very comfortable with JSON formatted data is essential for working with APIs.

There are many reasons why big organizations would want to share their data. Governments might be required by law to provide general access to public data. For profit companies like Google and Twitter share data to enable the development of third-party web applications that do useful things with the data. Twitter recently bought out [aiden.ai](https://www.aiden.ai/), a company that uses Twitter data to train AI models for marketing. (It's a brilliant strategy. By making their data available, Twitter encourages the creation of start-ups that are entirely dependent on Twitter data with no additional investment from Twitter. Then Twitter can use its data as leverage to buy-out the most successful start-ups for below market price.) Financial firms and other companies charge subscription fees for access to their data.

A carefully-constructed API also gives data providers certain powers over the data users. First, data providers might first require that users register for access to the API, surrendering their own personal information in exchange for access keys. Second, data providers can tightly control what and how much data they share. This power is called **encapsulation**. [Taina Bucher (2013)](http://computationalculture.net/objects-of-intense-feeling-the-case-of-the-twitter-api/) writes that encapulation also gives data providers the power to shape the narrative that a selection of shared data will tell:

> While there is nothing wrong with using APIs to collect data, of course, researchers should be wary about letting any current obsessions with big data overshadow the fact that APIs are far from neutral tools. . . . APIs have ‘politics’, meaning that they can be seen as having ‘powerful consequences for the social activities that happen with them, and in the worlds imagined by them’.

So when using an API, it's a good idea to think about what data are being shared, and what data are not being shared, why, and what that means for the analysis you are working on.

### Dealing with API Jargon
Getting started with APIs can be confusing because of all the technical jargon that API documentation uses. But once you are familiar with this language, it gets a lot easier to use APIs.

Regardless of the analogy that helps us understand what an API does, an essential characteristic of systems that APIs serve is "client-server separation". That is, the system that interacts with the users and the system that interacts with the data must be separate and independent of each other. That way problems in one system do not cause problems in the other system, and either system can be replaced. Twitter's data server can interact with many different third-party user clients through its API. 

Client-server separation is one property an API needs to satisfy in order to meet the **Representational State Transfer (REST)** standards. An API that meets these standards is called a REST API (or "RESTful"). In addition to client-server separation, a REST API is stateless, which means that every request is independent of all other requests. That is, a request should produce the same output from the API regardless of whatever other requests have already been made. A REST API is also cacheable, which means that responses can be stored and retrieved when needed. If a new request exactly duplicates an old request, the API can use its stored cache from the old request to provide an instant response to the new request. A REST API should include a uniform user interface, so that all users see the same interface and interact with the API in the same way, and a REST API should include layers, so that distinct tasks are handled by many distinct sub-systems. 

APIs are designed to handle all transfers of data from the backend to the frontend, and vice versa. For that, there are basic functions (also called "verbs") that an API can execute. The two most common functions are GET, which pulls data from the backend, and POST, which stores new data in the backend. We can use the `requests` library in Python to issue both GET and POST commands. In addition, we can use PUT to replace a record in the backend with a new version, PATCH to make changes to an existing record, or DELETE to remove a record. These five verbs are part of the standard method for transfering information from servers to browsers over the internet, called the **hypertext transfer protocol (HTTP)**, and responses from a REST API include [HTTP numeric status codes](https://en.wikipedia.org/wiki/List_of_HTTP_status_codes): 200 indicates a successful request, for example, and 404 means that the resource could not be found (maybe because there's a typo in the web address we entered). More generally, these functions are also called CRUD (create, read, update, and delete) operations.

### Reading API Documentation (Example: the NASA Image and Video Library)
Most web-applications with an API include documentation to guide people who want to use the API. Knowing *how* to read the documentation, that is, knowing the jargon, is the most important skill for using an API. First, please note that like other kinds of documentation, some software authors take more care to produce good documentation than others. Still, all API documentation should share some universal characteristics:

* The most important piece of information to find in the documentation is the **root** and **endpoint**. The API root is a web-address for all resources that exist and are accessable through the API. The endpoint is a subdirectory where records of a specific type are stored. 

* Each endpoint will usually have a separate section in the API documentation that contains a description of the kinds of data stored in this endpoint, a list of **parameters** to narrow down the data being requested, and (hopefully lots of) examples. 

* Finally, if an API requires authentication, there should be instructions on how to register for an **access key**.

The goal is to generate a complete URL that points to the desired data by putting the root, endpoint, parameters, and access key together in the following way:

*root* **/** *endpoint* **?** *parameters=value* **&** *key=value*

Let's use as an example the API to access [NASA's Image and Video Library](https://images.nasa.gov/). The documentation for this API is available at https://images.nasa.gov/docs/images.nasa.gov_api_docs.pdf. This API does not require authentication, so we only need to find the root, endpoint, and parameters. Let's say that I want to find a photo of the moon. According to the documentation, the root is https://images-api.nasa.gov, and there are several endpoints including one dedicated to searches (`/search`). 

I scroll down to the section devoted to this endpoint and look at the parameters to see which ones will allow me to search for a photo of the moon. I can use the `q` parameter to enter free text as a search term, and the `media_type` parameter set equal to `image` to find a photo.

Therefore the complete URL for this API GET request is: https://images-api.nasa.gov/search?q=moon&media_type=image. Go ahead and click on this link. You will see a JSON file in which the metadata tells me there are 8626 hits in this search. Under the `data` header, the first result is an image entitled "Nearside of the Moon", which has a NASA ID code PIA12235.

Next I want to GET the URL for the JSON data related to this specific image. The endpoint to find a specific image is `/asset`. There's only one parameter, the NASA ID. Notice that the documentation lists this path as `asset/{nasa_id}` and NOT as `asset ? nasa_id = {nasa_id}`. That means that for this particular endpoint we simply enter a slash and the ID after the endpoint. So to see the JSON data stored for this image, the URL is https://images-api.nasa.gov/asset/PIA12235. This JSON contains the links to various image files. I can link to one of them to display it in this document:

<img src="https://images-assets.nasa.gov/image/PIA12235/PIA12235~small.jpg">

Some documentation also contain API schematics that visualize the endpoints and the interaction between the frontend and backend via the API. As an example, here's a schematic of an API for a project we are working on with [Code for Charlottesville](https://codeforcharlottesville.org), a local chapter of [Code for America](https://codeforamerica.org) that I help to run. Our project involves building software for the agenices in town that help people with housing insecurity find a place to live. Our web application will allow people at different agencies share their data about available rental properties and landlords who are willing to rent to people with vouchers and who might have other complicated situations. Here's our API's schematic:
<img src="https://github.com/code-for-charlottesville/housinghub/raw/master/backend/docs/JWT%20Auth%20Workflow.png" width=800>

Different API schematics vary in their presentation, but here the blue box represents the frontend interface that people at the housing agency will be using, the green boxes represent parts of the backend where different parts of the database will be stored, and the yellow blocks are notes that help our volunteers keep track of what each part of the schematic means. The arrows point either from the frontend to the backend, or from the backend to the frontend, and illustrate the data that is being sent from the origin to the destination. There are five endpoints. `/auth/register` stores the information about the users of the web-application and allows new users to input their information into the backend with a POST function. `/auth/login` allows registered users to POST their username and password. `/auth/status` allows users to GET their current login status, and `/auth/logout` allows users to GET confirmation that they've logged out. `/property` allows the housing agency users to GET information about available properties and landlords. Throughout the schematic, JWT stands for [Javascript web token](https://jwt.io/introduction/), a JSON file with extra security built in for secure web transfers. So get a list of properties, a user enters information to filter the search into the frontend, and this information is converted into a JSON file and passed to the `/property` endpoint of the backend, which sends back a JSON file containing a list of the relevant properties.

## Using the `requests` Library (Example: Wikipedia)
The `requests` library in Python is one of the most widely used and one of the most important extensions to Python. If you need to install or update the `requests` library, type `pip install requests` in a console window. Then load the library. As we will be working with JSON data, it will be necessary to load the `json` library as well. It's also a good habit to always load `numpy` and `pandas`:

import requests
import json
import numpy as np
import pandas as pd

In the example of the NASA Video and Image library, we read the API documentation to build URLs that led us to JSON data we could display in a web browser. But if we want to use that JSON data in Python, `requests` connects to APIs and brings the output into Python's memory. We can access the data we requested and apply the methods we learned about in module 3 to convert the JSON structure to a data frame.

Here we will discuss the use of `requests` by working with the examples of Wikipedia.

Wikipedia's API is entirely open and allows users to access anything that exists on any Wikipedia page. But Wikipedia's API is also huge, and that necessitates a system for passing options to the Wikipedia API to let the server know what data you are asking for and how that data should be prepared. We will have to use the **documentation** for the Wikipedia API to navigate it.

**Our goal in this example:** to pull the text of the [Wikipedia page for UVA](https://en.wikipedia.org/wiki/University_of_Virginia) into Python. Wikipedia's title for this page is `University_of_Virginia`.

The Wikipedia API documentation is here: https://www.mediawiki.org/wiki/API:Main_page. First, we have to choose the correct version of Wikipedia in the endpoint table. We will be using the English langauge API: https://en.wikipedia.org/w/api.php. 

To connect to this enpoint to make a GET request, use the `requests.get()` function:

r = requests.get("https://en.wikipedia.org/w/api.php")
r

The output of `requests.get()`, stored in `r`, displays the HTTP response by default. 200 means that `requests` was able to successfully connect to the endpoint we provided. 

To extract the text of the UVA page, we need to specify the correct parameters. We return to the Wikipedia API documentation page and look along the side. There's a link for [Get the contents of a page](https://www.mediawiki.org/wiki/API:Get_the_contents_of_a_page). Here the documentation lists several sets of instructions for retrieving the content of a page. Method 1 requires the following parameters: 

* `action=query`
* `prop=revisions`
* `titles=University_of_Virginia`
* `rvslots=*`
* `rvprop=content`
* `formatversion=2`

We also add `format=json` to get JSON formatted output. We could either use these parameters to construct the following URL:
https://en.wikipedia.org/w/api.php?action=query&prop=revisions&titles=University_of_Virginia&rvslots=*&rvprop=content&formatversion=2&format=json

Or we can organize these parameters in a dictionary and pass them to the `params` argument of `requests.get()`:

p_dict = {'action': 'query',
         'prop': 'revisions',
          'titles': 'University_of_Virginia',
          'rvslots': '*',
          'rvprop': 'content',
          'formatversion': '2',
          'format': 'json'}
r = requests.get("https://en.wikipedia.org/w/api.php", params = p_dict)
r

To extract the JSON data, use the `.text` attribute and the `json.loads()` function:

uva_wiki = json.loads(r.text)

The text we need is buried in this JSON data. It turns out that the text we need exists in the following path:

uva_text = uva_wiki['query']['pages'][0]['revisions'][0]['slots']['main']['content']
print(str(uva_text)[6000:7000])

## Obtaining and Handling API Keys (Example: the U.S. Census Bureau)
APIs like the NASA Image and Video Library and Wikipedia are entirely open. Anyone can access these APIs without registration and without having to supply credentials. But many APIs do make users first go through an authentication process to access the data. There are many reasons why a data provider might want to control access in this way. The data provider might just want information about who is using the API and for what purposes. Additionally, many APIs place restructions to limit how much one account can use the API. **Rate limits** set maximum numbers of total calls one account can make to the API in a specified period of time, possibly to protect the backend from crashing. Some APIs charge for access, or set tiers of accessibility at different price points. For whatever reason, if the data provider has a reason to keep track of who is using the API and how much they use it, the API will require an **access key**. 

To obtain an access key, find the documentation for the API online. There should be clear instructions in the documentation about how to register and get an access key. Every data provider is different in terms of what information they ask for in exchange for the access key, so there's no general methodology beyond carefully following the instructions in the API documentation.

**Important:** Once you have an access key, keep it SECRET. Treat it like a password. Do not share it, and if you are writing a script or notebook that involves calling an API with an access key, take steps ([described below](#secret)) to hide your access key.

Let's take the U.S. Census Bureau's API as an example. To access this API we start with the [Developers](https://www.census.gov/developers/) page on the Census Bureau's website. In the bottom-left corner of the screen there's a large button labeled "Request a Key" that links to this URL: https://api.census.gov/data/key_signup.html. In order to obtain a key, you will have to tell the Census your organization and email address, and you will have to agree to the Census's terms of service. After supplying that information, click on "Submit Key Request". You will receive an email after a few minutes containing your access key.

According to the Census's (huge) [API documentation](https://www.census.gov/content/dam/Census/data/developers/api-user-guide/api-guide.pdf), the purpose of making users register for access keys is to limit the amount of use:

> You can include up to 50 variables in a single API query and can make up to 500 queries per IP address per day. More than 500 queries per IP address per day requires that you register for a Census key. That key will be part of your data request URL string (9).

### How to Keep Your Access Key Secret
People who are new to Python and APIs often make the mistake of explicitly writing a line of code that displays an access key, like this:

CensusKey = "abcdefghijklmnopqrstuvwxyz"

Putting the access key explicitly into a notebook or script will work for the purposes of getting the data from the API. But it will be a problem if you intend to share your code in any way. Declaring the key in this way is like announcing your password.

Instead, we will follow the protocol laid out by Jonathan Soma on his [excellent blog](http://jonathansoma.com/lede/foundations-2019/classes/apis/keeping-api-keys-secret/) for writing scripts and notebooks that access APIs while keeping your keys secret. 

#### Step 1: Creating a Environmental Variables File
The first step is to create a plain text file named `.env` in the same folder as your notebook or script. This file contains "environmental variables", which are variables that exist in your server environment without being part of your code - they are loaded into Python's memory in the background. Using environmental variables will allow you to share your code without having to share the sensitive information contained in the `.env` file. To create a `.env` file using Jupyter Labs:

1. Right click on your notebook and select "New Console for Notebook". That launches a new console with the complete environment of your notebook loaded into it.

2. Type `import os` and `os.getcwd()` into the console to confirm that the current working directory is the same folder where you have saved your notebook.

3. Type `!touch .env` into the console. This command creates a blank text file in this folder named `.env`.

#### Step 2: Putting Access Keys Into the `.env` File
Navigate to the folder where you created the `.env` file and open it. If you do not see the file, it might be considered a hidden file by your operating system. On a Mac, open the folder using Finder and press the **Shift, Command, and Period** keys together. Then the hidden files will display. On Windows, follow these [instructions](https://support.microsoft.com/en-us/help/14201/windows-show-hidden-files) to show the hidden files.

Once you've opened the `.env` file, you will see a text editor with no text. Type your access keys into the text editor in the following format:
```
CensusKey=abcdefghijklmnopqrstuvwxyz
```
Don't put spaces or quotes in what you type. If you want to save more than one key, that's fine, just put each key on a new line. Finally, save the `.env` file.

#### Step 3: Loading the Environmental Variables into Python
The easiest way to bring your keys into Python is to use the `dotenv` and `os` libraries Type `pip install dotenv` in the console if you haven't yet installed this library (or `sudo pip install python-dotenv` into a terminal session if you run into an error with the standard pip install). Then type the following code:

import os
import dotenv
dotenv.load_dotenv()

CensusKey = os.getenv('CensusKey')

Now `CensusKey` is a Python variable that contains your secret access key. You will be able to pass this variable to `requests.get()` to make calls to the Census API, and the key itself is never displayed on in the notebook. (You can type `CensusKey` in a cell to confirm that this worked, but be sure to delete that cell before sharing the notebook.) Better still, if you share the notebook or script with others who have also set up `.env` files on their own, then they can run the same calls using their own keys with no alterations to the code.

#### Step 4: Using the Access Key
Now that we have the access key stored in a Python variable we can pass it directly to the `params` parameter of `requests.get()` in a dictionary along with all of the other API parameters we specify. 

For example, suppose I want to download the population of every U.S. state by accessing the Census API through Python and then organize these data in a data frame. First I find and read the Census [API documentation](https://www.census.gov/content/dam/Census/data/developers/api-user-guide/api-guide.pdf). The endpoint for population data is https://api.census.gov/data/2019/pep/charagegroups. I look at the documentation for this specific endpoint and find the list of parameters. There are three parameters I need to specify:

* `get`: allows us to choose the features we wish to obtain from the API. Here let's get `GEO_ID` (the Census geocode for each state), and `POP` (the population).

* `for`: allows us to specify the geographic entities we want included in the data. Typing `state:*` tells the API to provide data on all of the states.

* `key`: this is where I enter my API access key.

In general, while values of API parameters should be entered in quotes, `CensusKey` should be entered without quotes to ensure that the value of `CensusKey` and not the string "CensusKey" is entered in the dictionary. The dictionary is:

mydict = {'get':'GEO_ID,POP',
         'for':'state:*',
         'key':CensusKey}

To download the data from the API, I pass the endpoint and the parameter dictionary to `requests.get()`

r = requests.get("https://api.census.gov/data/2019/pep/charagegroups", params=mydict)
r

Response 200 means that the connection to the API and the request were both successful. To see the output of the request, I look at the `.text` attribute:

r.text

The data are organized as a list of lists, where each element is a list of the data for each individual state. The first list contains the column names. To convert the data to a `pandas` data frame I use `json.loads()` to register the data as JSON, then `pd.DataFrame()` to convert the JSON to a data frame. I remove the first element and set it as the column names.

statepop = json.loads(r.text)
statepopDF = pd.DataFrame(statepop[1:], columns=statepop[0])
statepopDF

## Using Python Libraries that Directly Interface With a Particular API
Many APIs now have their own specialized libraries for Python that wrap around the `requests` library so that you don't need any calls to `requests`. These libraries (mostly) try to make the process of working with a complicated API much easier and more user friendly. We'll discuss two examples here. The main library for working with the Twitter API in Python is `tweepy`, and the library for working with the Google Maps API is `googlemaps`. If you haven't yet done so, please install these two libraries.

### Using an API with Credentialling and Limits (Example: Twitter)
Twitter limits the use of its API to people who apply for and are granted a special "Twitter developer" account. To apply for a developer account, follow these steps:

1. Go to https://dev.twitter.com/apps/new and log in to with your Twitter username and password (get a regular Twitter account first if you don't yet have one).

2. Click on "Create an app". 

3. You will be prompted to apply for a developer account if you haven't yet done so (if you already have an account, sign in and skip to step 4). Click "apply", then:

  a. Request access for personal use. Give your account a name and select your country.

  b. On the next page, select academic research or another topic if any are relevant. 

  c. Under "Describe in your own words what you are building" I typed the following: "(1) I'm using Twitter's APIs to teach myself how to download and analyze Twitter data (2) I plan to analyze Tweets to understand how APIs and natural language processing work (3) No, I will not be Tweeting content (4) Tweets will not be displayed to any users" You should probably adapt the language to suit your own purposes and because we shouldn't send dozens of identical applications to Twitter.

  d. Agree to the terms-of-service, click through, and check your email for a confirmation link to click

  e. Once you've confirmed your email address, proceed to https://developer.twitter.com/en/account/get-started and click on "Create an app". Then click on the blue "Create an app" button in the upper-right corner.

4. Enter your Application Name (something like "Jon's twitter app" is fine), Description ("An app for Jon to use as he learns how to download data from Twitter" worked for me), and your website URL (I used www.virginia.edu). Under "Tell us how this app will be used" I wrote "I'm using this app to learn how to download data from Twitter into Python for the purpose of studying how to use APIs." You can leave the other parts of the form empty.

5. Submit the form by clicking the Create your Twitter Application. This takes you to a page for your app. Click on "Keys and tokens" along the top.

6. Click on "Generate" under "Access token & access token secret." 

7. You should now see **four strings of random letters and numbers**. The first the consumer API key. The second the the API secret key. The third is the access token, and the fourth is the access token secret.  **Keep these numbers secret!**  Keep this page open so you can copy and paste into your `.env` file.

Once you have your consumer key, consumer secret, access token, and access token secret, paste the four strings into a `.env` for your project, as [described above](#secret). I bring these keys from the envirnomental variables to working variables in the Python environment by typing:

ConsumerKey = os.getenv('ConsumerKey')
ConsumerSecret = os.getenv('ConsumerSecret')
AccessToken = os.getenv('AccessToken')
AccessTokenSecret = os.getenv('AccessTokenSecret')

In this example, our goal is to collect recent **tweets that contain the hashtag #uva**. 

Many large organizations with APIs have built specialized modules in Python to facilitate using the API directly in Python. For Twitter, the module that works best with the Twitter API is `tweepy`:

import tweepy

We pass our keys to the Twitter API with the following code:

auth = tweepy.OAuthHandler(ConsumerKey, ConsumerSecret)
auth.set_access_token(AccessToken, AccessTokenSecret)
api = tweepy.API(auth)

Now that we've set up our credentials, we can access the Twitter API without having to build a URL or use `requests`. The `.cursor()` method allows us to pass parameters from the Twiiter API documentation directly to the call to the API. The list of parameters for searching through tweets is here: https://developer.twitter.com/en/docs/tweets/search/api-reference/get-search-tweets. Notice the parameter `q` = "A UTF-8, URL-encoded search query of 500 characters maximum, including operators. Queries may additionally be limited by complexity." We can use this parameter to enter opur search term "#uva".

In the code below, we use the `.search` method applied to `api`, and we pass the search term we need. We also use the method `items(30)` to limit the number of returned tweets to 30.

uva_tweets = tweepy.Cursor(api.search, q='#uva').items(30)

According to the `tweepy` documentation on the `.cursor()` method (http://docs.tweepy.org/en/v3.5.0/cursor_tutorial.html) the best way to explore the output is with a loop.  In the following code, I first create empty lists named `msgs` and `msg` -- `msg` will contain a tuple of the data I want to extract from a single tweet, and `msgs` will append this information together across tweets. I then save the `msgs` array as a dataframe:

msgs = []
msg =[]

for tweet in tweepy.Cursor(api.search, q='#uva').items(30):
    msg = [tweet.text, tweet.created_at, tweet.user.screen_name] 
    msg = tuple(msg)                    
    msgs.append(msg)

df = pd.DataFrame(msgs, columns = ['text', 'created_at', 'user'])
df.head(30)

### Using an API that Requires a User to Send Data to the API First (Example: Google Maps)
APIs are a two-way system of data transfer. Not only can we pull data from APIs (a GET request), we can send data to remote servers using APIs (a POST request). For some applicaitons of APIs, we need to provide data to the server so that the server knows what data to send back to us. One example of this interchange is using the Google Maps API to get the latitude-longitude coordinates for an address, so that we can plot addresses on a map. The goal in this example is to get the coordinates for the address for "60 Bonnycastle Dr Charlottesville, VA 22904", otherwise known as the Dell, where the offices for the UVA School of Data Science are located.

address = "60 Bonnycastle Dr Charlottesville, VA 22904"

As with Twitter, the Google Maps API is a credentialed system. To obtain the proper keys, go to https://console.cloud.google.com/projectselector2/apis/credentials?pli=1&supportedpurview=project and sign in to your Google account. Choose your country and agree to the terms of service. Click on "create", and choose a project name, organization name, and location (a website) for your organization. It doesn't really matter what these are. That will bring you back to the main page, where after a minute a page for your project will appear. If you click on the project main page, along the left-hand side there's a link for "APIs and Services": click on "Credentials", then click on the "Create credentials" button, and "API Key". The API key will appear. Copy and paste it into your `.env` file.

I load the key into Python's environment:

GoogleKey = os.getenv('GoogleKey')

You will also need to enable your API to be able to use place location. Navigate to the main dashboard for your app. At the top click the button marked "APIs & Services". Find "Geocoding API": click it, then push "Enable". (Note: it can take about 5 minutes for changes to take effect). You might also have to sign up for a Google Cloud billing acount. If you never use Google Cloud, they won't charge you, so feel free to sign up.

The easiest way to interface with the Google Maps API in Python is to use the `googlemaps` library:

import googlemaps

To issue your credentials to the Google Maps API, use the following code:

gmaps = googlemaps.Client(key=GoogleKey)

Now that we've created a session with the Google Maps API, we can use the `.geocode()` method to search for a particular address, and to return all information about that address in JSON format:

geocode_result = gmaps.geocode('60 Bonnycastle Dr Charlottesville, VA 22904')
geocode_result

Because the output is formatted as a list in which the only element is a dictionary, we start by calling the 0 item of the list. We can then find the latitude and longitude coordinates with the following path:

geocode_result[0]['geometry']['location']