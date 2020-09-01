# Getting Yourself Unstuck

```{contents} Table of Contents
:depth: 4
```

## Introduction
Welcome to DS 6001: Practice and Application of Data Science! In this course, we will focus on the **data pipeline**.

<figure>
  <img src="https://cdn.pixabay.com/photo/2016/03/09/15/16/wave-1246560_1280.jpg" width="600" alt="Image of a surfer">
 <figcaption>
Source <a href="https://pixabay.com/photos/wave-surfer-sport-sea-surf-water-1246560">pixabay.com</a>
 </figcaption>
</figure>

The pipeline refers to all of the steps needed to go from **raw, messy, original data** to data that is ready for any kind of analysis. In the real world, data is almost never ready to be analyzed without a great deal of work to prepare the data first. [This article in Forbes](https://www.forbes.com/sites/gilpress/2016/03/23/data-preparation-most-time-consuming-least-enjoyable-data-science-task-survey-says/#3ebb8cd06f63) describes a survey of data scientists in which the respondents claim to spend nearly 80% of their time collecting and cleaning data.
<img src="https://thumbor.forbes.com/thumbor/960x0/https%3A%2F%2Fblogs-images.forbes.com%2Fgilpress%2Ffiles%2F2016%2F03%2FTime-1200x511.jpg" alt="Apologies for the pie chart, it will be the last one we see in this course" width="600"/>

The goal of this course is to make this huge part of the job easier, faster, less frustrating, and more enjoyable for you. The techniques we will discuss are not the only ways to accomplish a task, but they represent fast and straightforward ways to do the work.

This course is divided into three parts:

<ol start="1">
    <li> <b>How do we acquire data?</b></li>
</ol>

  * From external files with flat, tabular structure (Module 2)
  * From JSONs, often from APIs (Modules 3 and 4)
  * From web-scraping using `beautifulsoup` (Module 5)
  * From remote access to an SQL database (Modules 6-7)

<ol start="2">
    <li> <b>How do we clean data?</b></li>
</ol>

  * With SQL queries (Modules 6-7)
  * With `pandas` (Module 8)
  * Including merging and reshaping dataframes (Module 9)

<ol start="3">
    <li> <b>How do we perform simple analyses to understand our data?</b></li>
</ol>

  * With summary and descriptive statistics tables (Module 10)
  * With static visualizations using `matplotlib` and `seaborn` (Module 11)
  * With interactive visualizations using `plotly` (Module 12)

However, prior to launching into the data pipeline, we have to talk about the single most important skill for a data scientist: **how to get yourself unstuck**. That is, how to find the help you need to solve the inevitable problems, errors, and anomalies that will occur as you code. Remember, being a great data scientist does NOT mean doing everything perfectly. Great data scientists make mistakes just as often as anyone else. What sets them apart is their skill in using help resources to get to the **right answer, as quickly as possible**. In this notebook, we will discuss the various methods and resources at your disposal for finding help, and the *order* in which you should employ each resource. If you practice these skills for getting yourself unstuck, you won't have any trouble squashing all the bugs in your code.

<img src="http://phdcomics.com/comics/archive/phd011406s.gif" width="600">

## The Places to Go For Help, In Order
There are many resources available to you. I suggest using the following resources in a particular order:

1.  Reading and understanding Python errors
2.  Python documentation
3.  Google
4.  Stack Overflow
5.  PySlackers
6.  Internet relay chat (IRC) rooms with other Python users
7.  Various Python mailing lists

See https://www.python.org/community/ for more information about these resources.

Please notice, many programmers use Google and Stack Overflow as their first options for getting help. I strongly suggest that you do **not** look to Google and Stack Overflow before trying to use the official Python built-in documentation. The documentation isn't as intuitive and easy to access as Google, but the answers that the official documentation will provide are guaranteed to be correct and specific to the functions you are trying to use, if you know what those functions are. In contrast, for all of the strengths of Google and Stack Overflow, there is a lot of information out there that isn't especially helpful and will slow you down a great deal.

## Method 1: Reading and Understanding Python Errors
Usually, when you are stuck, it's because you ran some code that resulted in an error. Reading and understanding the error is the single most important and useful way to get yourself unstuck. These errors are not aesthetically pleasing, and they are written in technical language, but the *intention* of these error messages is to tell you exactly what went wrong. Many Python users skip reading the errors entirely, which is a shame because the error might indicate exactly the fastest way to solve the problem.

There are two reasons why people skip over reading the errors:

1. The error appears in a big pink box with pea green and cyan text inside of it. It's pretty ugly.

2. The first several lines of code are reserved for a function's **traceback**. The traceback is an attempt to isolate the particular line of code within a larger function that causes the error. However, the traceback is often very technical and not especially useful. After reading the first few lines of the traceback, most people give up on the entire error message. 

But the useful part of the error message occurs **at the bottom of the message**. The traceback is useful when developing new functions and debugging original software. But for the vast majority of the time, whenever you are using pre-programmed functions, only the bottom of the error message matters.

For example, in the next module we will discuss loading electonic data files. Many things can go wrong. One error we will contend with comes from the following code:
```python
from pandas import read_csv
url = "https://raw.githubusercontent.com/jkropko/DS-6001/master/localdata/anes_example_toplines.csv"
anes = read_csv(url)
```
What this code is supposed to do is not important at the moment. It produces the following error output:
```python
---------------------------------------------------------------------------
ParserError                               Traceback (most recent call last)
<ipython-input-15-f4f15a0ffe03> in <module>
      1 from pandas import read_csv
      2 url = "https://raw.githubusercontent.com/jkropko/DS-6001/master/localdata/anes_example_toplines.csv"
----> 3 anes = read_csv(url)

~/anaconda3/lib/python3.7/site-packages/pandas/io/parsers.py in parser_f(filepath_or_buffer, sep, delimiter, header, names, index_col, usecols, squeeze, prefix, mangle_dupe_cols, dtype, engine, converters, true_values, false_values, skipinitialspace, skiprows, skipfooter, nrows, na_values, keep_default_na, na_filter, verbose, skip_blank_lines, parse_dates, infer_datetime_format, keep_date_col, date_parser, dayfirst, cache_dates, iterator, chunksize, compression, thousands, decimal, lineterminator, quotechar, quoting, doublequote, escapechar, comment, encoding, dialect, error_bad_lines, warn_bad_lines, delim_whitespace, low_memory, memory_map, float_precision)
    674         )
    675 
--> 676         return _read(filepath_or_buffer, kwds)
    677 
    678     parser_f.__name__ = name

~/anaconda3/lib/python3.7/site-packages/pandas/io/parsers.py in _read(filepath_or_buffer, kwds)
    452 
    453     try:
--> 454         data = parser.read(nrows)
    455     finally:
    456         parser.close()

~/anaconda3/lib/python3.7/site-packages/pandas/io/parsers.py in read(self, nrows)
   1131     def read(self, nrows=None):
   1132         nrows = _validate_integer("nrows", nrows)
-> 1133         ret = self._engine.read(nrows)
   1134 
   1135         # May alter columns / col_dict

~/anaconda3/lib/python3.7/site-packages/pandas/io/parsers.py in read(self, nrows)
   2035     def read(self, nrows=None):
   2036         try:
-> 2037             data = self._reader.read(nrows)
   2038         except StopIteration:
   2039             if self._first_chunk:

pandas/_libs/parsers.pyx in pandas._libs.parsers.TextReader.read()

pandas/_libs/parsers.pyx in pandas._libs.parsers.TextReader._read_low_memory()

pandas/_libs/parsers.pyx in pandas._libs.parsers.TextReader._read_rows()

pandas/_libs/parsers.pyx in pandas._libs.parsers.TextReader._tokenize_rows()

pandas/_libs/parsers.pyx in pandas._libs.parsers.raise_parser_error()

ParserError: Error tokenizing data. C error: Expected 1 fields in line 5, saw 168
```

None of this output helps me understand my mistake until I reach the final line that begins `ParserError`. With a little bit of experience, I can understand this error: it says that it expected the fifth row of the data file to have one column, but instead it found 168 columns. That's useful, but I had to wade through dozens of lines of technicality to arrive at the useful error message. 

I recommend turning off the traceback to make reading error messages easier. To do this, load the `sys` library and issue the following command:

import sys
sys.tracebacklimit = 0

Now, when I use the same code, I get a different error output:
```
ERROR:root:Internal Python error in the inspect module.
Below is the traceback from this internal error.

Traceback (most recent call last):
pandas.errors.ParserError: Error tokenizing data. C error: Expected 1 fields in line 5, saw 168


During handling of the above exception, another exception occurred:

Traceback (most recent call last):
AttributeError: 'ParserError' object has no attribute '_render_traceback_'

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
AssertionError

---------------------------------------------------------------------------
```

I can't say that this error output is pretty or intuitive in and of itself, but relative to the previous error message this output has some nice properties. First, it is shorter (and there's less pink). Second, and most importantly, the useful part of the error message appears near the top of the output.

To turn the traceback back on, simply type:

sys.tracebacklimit = None

## Method 2: Using the Built-in Python Documentation 
Packages, modules, classes and functions in Python have built-in documentation that you can display directly in the console or in the output of a notebook. These built-in documentations are called **docstrings**.

### Using a Console Window in JupyterLab
The docstring should be the first place to look for help with specific, pre-built Python code. The problem is, calling up a docstring is very annoying in a Jupyter notebook. Ideally, you should be working with two windows side by side: one for the notebook or script that contains your code, and one for calling docstrings and running commands to view saved objects.

I strongly suggest using JupyterLab (not just Jupyter), which is available from  Anaconda Navigator: https://docs.anaconda.com/anaconda/navigator/. Please take a moment to download and install Anaconda Navigator, launch JupyterLab, and open this notebook in JupyterLab (by clicking on the file folder icon in the upper left corner of the screen, navigating to this file, and clicking on it) if you haven't already done so.

Next, click **File**, then **New**, then **Console**. This will open a console window, in which you type commands one at a time into the bar at the bottom of the window, pressing SHIFT + ENTER/RETURN to execute the command. Find the tab at the top of the screen for the console, and click and drag it to the side of the screen. The notebook and console windows should now be side-by-side.

Finally, click on the console window, then click on **Kernel** at the top of the screen, and **Change Kernel...**. That brings up a "Select Kernel" menu. In the drop-down menu, choose the name of this notebook. That loads all the packages and objects that have been stored in the notebook's memory in the console. 

Now the console is very easy to use to call up docstrings or to run commands on the notebook's objects.

### How to Call Up and Read a Docstring
There are a few ways to display the help documentation for a function or an object (replace `function` below with the function you want help with):

* `help(function)` -- displays the docstring for the function in question.
* `function?` or `?function` -- displays an abbreviated docstring, as well as the
signature (the complete function syntax, including all arguments and their default values)
* `function??` or `??function` -- the same as `?` but shows the internal code so long as the function is not written in C

For example, consider the docstring for the `print()` function, which displays results to the notebook or console output. We can call:


help(print)

Or alternatively:

?print

And finally:

??print

In this case, `?print` and `??print` yield the same output because the internal code of `print` is C code.

Docstrings often have **sections** that convey particular information.

1. The header (only appears with `help(print)`): tells us that the `print` function exists in the `builtins` module (the module that loads automatically when we launch Python)

2. The signature: lists all of the parameters of a function. Each parameter in the signature is set equal to its default value. If the user doesn’t specify the parameter in the function all, it’s set to the default.

3. The short description: A one-or-two sentence summary of what the function does. For the `print` function, this summary is "Prints the values to a stream, or to sys.stdout by default" which is technical-speak for prints to whatever the output medium happens to be.

4. The parameters: **this section is the most useful for learning how to use a function**. The parameters section lists the parameters, in the order in which they appear in the signature of the function, along with information about each parameter. 
Each parameter is described in a sentence or two to explain what the parameter does.
Sometimes the parameters may be noted as either required or optional in a call to the function, and the docstring might also list the type of each parameter: in this case, the `sep` and `end` parameters are denoted as strings.

Other docstrings might include sections that describe:

1. Returns: describes the output from a call to the function.

2. Attributes: lists objects that can be pulled out of the object that contains the output. We'll see a bunch of examples of attributes in the next few weeks. For example, a dataframe object has an attribute`.dtypes` that shows the data type of each column in the dataframe.

3. Related methods: lists methods that can be applied to the output of the function. Methods are like attributes, only they work as functions rather than as objects, and these methods may have their own docstrings embedded inside the orginal docstring. We'll see examples of these quite a lot too. 

4. See also: a list of related functions.

5. Examples: Examples are meant to be run, not just looked at.  Copy-and-paste
the examples into your notebook or script, run the code.  Then see if you
can do more things with the given objects than the examples do.


## Method 3: Using Google and Other Search Engines
Many of us have a habit of going to Google first whenever we have a coding problem. Please make a concerted effort starting right now to break this habit. If you know the functions you need more information about, using the built-in docstrings the best habit.

The reason why we shouldn't rely on Google as the first option is that Google is slow as a method of getting help. With open-source environments such as Python, there are many ways to do the same thing, and there are way too many presentations on the internet of any one topic to sift through efficiently. Many of the resources you find this way come from a field or a point of view that differs from your own, leading you to have to work hard to translate the language that explains the method. And some of the information is out of date or simply wrong.

Use Google or another search engine if 

* you don't know the functions you need to do a task,
* you don't have a textbook or set of notes that you trust for guidance,
* or if the built-in docsting doesn't give you the information you need (not everyone who write Python modules writes comprehensive docstrings).

The best Google search is
```
Python (the function you want help with) (additional details)
```

Google will often take you to Stack Overflow (https://stackoverflow.com/), but other useful and credible websites that can help are

* More detailed documentation for specific Python modules, such as:
  * https://scikit-learn.org/
  * https://pandas.pydata.org/
  * https://matplotlib.org/


* High-quality blogs:
  * https://towardsdatascience.com/
  * https://medium.com/


* Free content from tutorial websites with a lot more paid content:
  * https://realpython.com/
  * https://www.geeksforgeeks.org
  * https://www.w3schools.com
  * https://www.datacamp.com
  * https://www.dataquest.io/
  
There are also many, many more resources and new ones are created all the time. Find the resources you like best: going directly to the most credible links will save you a great deal of time in this effort to get yourself unstuck.

## How to Avoid Toxicity in Online Communities
The next options involve becoming a **responsible, respectful** member of the worldwide community of Python users. Open-source platforms like Python and R depend on a community of volunteers who develop and maintain the tools that we use. All of these people are doing volunteer work for the common good, and that's a beautiful thing.

In addition to Python itself, Stack Overflow, Slack, the Freenode IRC, and mailing lists are online communities for Python users. But, like any online community, there's the potential for a toxic culture to destroy everything.

What is a toxic culture? How do you know one when you see one?

Toxic cultures are more likely when

* members are allowed to be anonymous (see [Lapidot-Lefler and Barak 2011](https://www.dhi.ac.uk/san/waysofbeing/data/health-jones-lapidotlefler-2012.pdf))
* and members up-vote and down-vote and comment on each other's contributions (see [Massanari 2015](https://journals.sagepub.com/doi/full/10.1177/1461444815608807)).

A culture can be either actively or passively toxic. Actively toxic communities are easy to identify. They encourage and are characterized by overt sexism, racism, bigotry, and calls for violence or other aggression against individuals. Most of the toxicity you will encounter in online programming and data science communities is not actively, but passively toxic. Passive toxicity is characterized by **gate-keeping**: Subtle behaviors that discourage people with less experience, or with some social anxiety, from participating.

Stack overflow, IRCs, and mailing lists are notorious for passive toxic behavior. Passive toxicity is a bigger problem for us than active toxicity because actively toxic behavior is usually explicitly banned by codes of conduct, and individuals are often unaware of when they are acting in a passively toxic way.

Examples of passive toxic behavior:

* **Condescending language**: often people who are trying to earnestly answer a question unthinkingly use language that makes someone feel dumb for asking the question. Avoid using words such as "obviously", "clearly", "actually", "just", "that should be easy", "google it", "read the manual" (or "RTFM"). Here's an [example](https://twitter.com/aprilwensel/status/974859164747931650).

* **Shaming**: attacking someone for asking a question by implying that the solution is easy and that someone is an idiot for not knowing it. Some examples: "Learn to debug your own code" and "If you don't get this, you have no business being a data scientist."

* **Downvotes without explanation**: this can be both confusing and very upsetting to anyone, especially to people with less experience.

* **Virtue signaling**: implying that people are superior/inferior because of the language, software, or methods they use. For example: "Real programmers don't use for loops", "You still use SAS?", and so many memes:
<img src="https://external-preview.redd.it/fU0szLnA4FwuYk3sMNqdf6f21vM_lvC9O-VgjyT11ek.jpg?width=1024&auto=webp&s=7634d370c0a5a46b794e8426850137538eadb615" alt="" width="400"/>

* **Authoritarianism**: Abusing people for failing to follow all of a community's rules for asking questions. For example, a comment that entirely ignores the content of the question but comments "all questions must provide an example," or editing a user's post to remove where they wrote "Hi everyone" and "thanks."

* **Overzealous curation**: Being very quick to tag a question as a "duplicate" without checking to see nuanced ways in which the question comes from a new situation.

The result of passive toxicity is that **many potential community members choose not to participate in the community** because their initial experiences made them feel ashamed, confused, or belittled. In addition, other potential new members observe these negative interactions involving other members, and choose to disengage.

**Passive toxicity shrinks the community and makes it more homogeneous.** Across society, small, homogeneous communities are much more likely to exclude or discriminate against people based on sex, race, class, language} and other factors. And that leads to many ethical problems.

*Under no circumstances are you to contribute to an active or passive toxic culture in any community, online or otherwise.*

Please keep the behaviors described here in mind when you engage in online communities, and avoid them. Don't be afraid to call out other people who behave in these ways.

## Method 4: Stack Overflow
[Stack Overflow](https://stackoverflow.com) is the most popular and most useful website for help with programming of all kinds. Google searching a Python problem will usually lead to a Stack Overflow post on the same issue. Python is now the most frequent tag for posts on Stack Overflow, and shown in this video:

from IPython.display import IFrame
IFrame(src="https://www.youtube.com/embed/cKzP61Gjf00", width="560", height="315")

Finding a Stack Overflow post that's relevant to your problem can give you both the code and underlying intuition to solve your problem. Or maybe not! Small differences in the situation can make the solution irrelevant to you. Be cautious and don't treat a Stack Overflow post as automatically a definitive answer.

### How Stack Overflow Works

1. Someone asks a question
2. Other people comment on and provide answers to the question
3. The person who asked the question replies to the comments, and can choose an answer to mark as "accepted".
4. People with reputation scores higher than 15 can upvote or downvote questions and answers.
5. Reputation points are awarded for asking questions or giving answers that other people upvote, or for having an answer accepted. Points are taken away for downvotes or spam or offensive posts.

Going for reputation is an entirely optional activity. If you don't want to worry about it, don't.

### Asking a Question on Stack Overflow

Okay, so you're stuck. You've combed through the Python documentation, Google, and old Stack Overflow posts, but you haven't found a solution. It's time to consider writing a new question on Stack Overflow.

<img src="https://github.com/jkropko/DS-6001/raw/master/localimages/leia.png" alt="" width="400"/>

This can be frightening. A lot of the time, people answering questions on Stack Overflow can be, well ... huge assholes that cause [real suffering](https://medium.com/@Aprilw/suffering-on-stack-overflow-c46414a34a52). You might choose to avoid posting to Stack Overflow, so as not to support a website that has harbored abuse. That's completely fair. If you do post to Stack Overflow, you are likely to get some very useful responses if you follow some guidelines. There's [a strategy for getting good responses](https://stackoverflow.com/help/how-to-ask). You are more likely to get a good response if you follow these steps:

1. **Search Stack Overflow and Google to see if the question has already been answered.** Commenters dislike if the same question is asked repeatedly. This [poor guy](https://stackoverflow.com/questions/27885020/find-all-possible-combinations-of-letters-in-a-string-in-python) got roasted for posing a "duplicate" question. (An aside: *Why?* It's not like Stack Overflow is running out of space on their website.  There's an idea that Stack Overflow should be a central repository of knowledge. That means there should be one canonical answer to one question. But people often take this much too far. There are kinder ways to point to an existing answer.) So spend a significant amount of time digging through the internet. If there's something similar, but not quite what you need, you can say so in your post.

2. **Write a good title for your post.** A good title is specific about the problem, and also succinct:
  * Bad: Problem with matplotlib (not specific)
  * Also Bad: How do I place the labels of cars in a scatterplot of the weight and miles per gallon of cars onto the points in the scatterplot using matplotlob 3.3.1 on Python 3.7.4 on Mac OSX 10.14.5? (not succinct)
  * Good: How to place labels on top of points in a matplotlib scatterplot?


3. **Start the post with a paragraph describing the problem in more detail.** Some good things to include in this paragraph:
  * The context of the problem -- how did you come across the problem? Describe the overall goal, not the just the buggy step.
  * What you've already tried to solve the problem, and what happened.
  * What is the expected output? What do you see instead?
  * You can write the version of Python you are using, the version of the modules, and the operating system on your computer, in case the problem turns out to be specific to one of those


4. If possible, **include code that reproduces the problem.** The code SHOULD NOT simply be the code in your script that isn't working. It needs to be able to work on someone else's computer. That means the code should not depend on any specific data files, and should not contain file addresses that refer to a location on your computer. Only use modules that are easy to get. If the code needs to run on data, can you use something pre-loaded in Python that everyone can access? (There are example datasets included with `scikit-learn`, for example.) Make the code as short as possible, and use comments to help people understand the code more quickly.

A few additional things to keep in mind:

* Be courteous and respectful. Respond to and thank everyone who comments.

* Post a follow-up once the problem is solved so that people who come across this page in the future with the same problem know the solution.

* Don't ask people to write code for you. It's better to request help with code your provide.

* Don't claim you found a bug in Python or in a module. It's a bit rude to the people who programmed the code (who don't get paid).

* Don't ask about homework problems. ([Here's an example](https://stackoverflow.com/questions/23098699/calculate-the-mean-of-one-column-from-several-csv-files-in-r) of someone getting called out on this.)

## Method 5: Python Slack
The main slack page for the global community of Python users is **Pyslackers**: https://pyslackers.com/web. To join, just go to the URL and click "join the community". The main discussion happens on #python_, but there are many other useful channels including #data_science and #job_advice. This method is especially worthwhile if you already are used to using slack for work or for personal networking. 

If you aren't used to slack, we will practice slack together in this course. One thing that helped me use slack much more consistently is downloading the desktop app (https://slack.com/downloads), and always leaving the app open on my local computer.

## Method 6: Live Chats With Python Users on Freenode
The Python user community is world-wide, and for the most part, very supportive. There are active internet relay chat (IRC) networks where you can post a question to members who are also logged in, to possibly get an answer right away. The most active Python IRC is the #python channel on Freenode: https://webchat.freenode.net. When I logged in while writing this notebook, there were 1,778 people logged on.

Internet chatrooms can be rough places, but the #python channel claims to enforce this [Code of Conduct](https://www.python.org/psf/codeofconduct/). Getting started on Freenode can be tricky, but it's easier if you follow these steps:

1. Go to https://webchat.freenode.net/. Choose a nickname, and make it professional (you're a UVA student after all!) and unique. 

2. Don't write anything under channel. Prove you are not a robot by selecting pictures of motorcycles or something. Then, once your humanity has been established, click "Start".

3. To use the #python channel, you need to register your nickname. To check if your nickname is unique, click on the "freenode" tab on the left-hand sidebar. A text box will appear on the bottom of the screen. Type:
```
/msg NickServ info
```

4. Step 3 will open a new tab. Switch to that tab. If no one else already has your nickname, you will see
```
NickServ: (notice) <nickname> is not registered.
```
If you see something else, it means someone already has your nickname. You can change your nickname right here by typing `/nick` followed by another nickname. Then type `/msg NickServ info` again. Repeat until you see the message listed above.

**Important note**: DON'T use a password here that you use for important things like email, bank accounts, etc. We shouldn't have the same faith in the security of Freenode's servers as we can have in Google's. Also, this is the kind of platform that tends to attract hackers. And for people used to a graphical user interface, it might be easy to mistype in a way that accidentally displays your password in the chat. Use a unique, throwaway password!

5. To register this nickname, type
```
/msg NickServ register <password> <email-address>
```
where `<password>` is a password you will use in the future, and `<email address>` is the email you want associated with this account.

6. Check your email for a confirmation code. Be patient, it can take up to 20 minutes for the email to go through.

7. Once you have the code, paste it and your nickname into this code, and submit it:
```
/msg NickServ VERIFY REGISTER <nickname> <secret-code>
```

8. You are now registered! Return to https://webchat.freenode.net/ and log-in with your nickname and password. Type #python under channel. You are free to chat away. Pay attention to the guidelines that appear as links on the top of the screen.

## Method 7: Python Mailing Lists and Newsgroups
[Usenet](https://en.wikipedia.org/wiki/Usenet) is a distributed discussion system (which means it has no central server). It was invented in 1979, and is still in use today. The Python Usenet message boards are at https://mail.python.org/archives/?sort=popular. The `comp.lang.python` board is for general discussions and questions about Python.

The tutor mailing list (https://mail.python.org/mailman/listinfo/tutor) is for users who want to ask questions about learning computer programming with Python.

If you have a question for the Python core development team, send an email to [help@python.org](mailto:help@python.org). The team is pretty busy, so be sure to check other resources and lists for an answer first.