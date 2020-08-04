# Loading Data from Electronic Data Files

```{contents} Table of Contents
:depth: 4
```

## Introduction: Please don’t bend, fold, spindle or mutilate me
"['Do Not Fold, Spindle or Mutilate': A Cultural  History of the Punch Card](http://www.cs.mun.ca/~harold/Courses/Old/CS1400.W15/Diary/Lubar1992.pdf)" by Steven Lubar details the earliest method of data storage and transference. Punch cards were first used by the U.S. government to tabulate the 1890 census. Before World War 1, punch cards started being used by the military, the railroads, and insurance companies to store data. In the 1930s, punch cards were used by the New Deal agencies, and by the 1940s punch cards were widespread throughout American society.
<img src="https://github.com/jkropko/DS-6001/raw/master/localimages/punchcard1.png" width=600>

Punchcards predated computers, which is to say that data storage and transference predates computers. These early uses of punchcards employed [data tabulation machines](https://en.wikipedia.org/wiki/Tabulating_machine) capable of counting the number of times particular holes have been punched in a series of cards, fed into the machine one at a time. The tabulation machine used for counting the 1890 census was developed by a company that later became IBM. 
<img src="https://github.com/jkropko/DS-6001/raw/master/localimages/punchcard2.jpg" width=600>

When punchcards became widely used, they were printed with a universal warning: "don’t bend, fold, spindle or mutilate", which became a cultural meme that long outlived the use of punchcards. In the 1960s, punchcards and the slogan "don’t bend, fold, spindle or mutilate" became symbols of alienation and technocratic oppression used by campus protests and many countercultural movements:

> The depersonalization of the punch-card era found its catch phrase in the words on the cards; its ubiquity gave it instant familiarity. One observer of the period wrote that  marijuana, the 60s escape from the rigors of the real world, let you see "the strangeness of real unfolded-unspindled-unmutilated life" (Gitlan 202). "Do not fold, spindle, or mutilate" became shorthand for a whole realm of  countercultural experience. The ecological movement of the early 1970s, a child of the 1960s counterculture, picked up on it too: a popular poster for Earth Day 1970 showed a picture of the Earth taken from space with the legend  "Do not fold, spindle, or mutilate" (Lubar 1992, p. 48). 

Starting in the 1950s it became possible to run more advanced statistical analyses, such as linear regression, using [mainframe computers](https://en.wikipedia.org/wiki/Mainframe_computer) with punchcard inputs. Many of my professors in grad school had stories about trekking across campus at 3am, the only time they could get access to the computer, to the building with the giant, noisy computer in the basement. They would carry a stack of punchcards, trying hard not to trip or slip on ice because dropping the punchcards would mean hours of work to get them back into a specific order. Finally, while inputting the cards, inevitably one would get jammed, which meant alerting the surly technician on call.

Two technological advances together made punchcards obsolete. First, in the late 1970s and through the 1980s, it became possible to store data directly on a computer hard drive or a floppy disk, which led to the creation of electronic data files such as CSV. Second, the internet made it possible to transfer data electronically, which led to APIs, HTML, and remote databases. 

Today there are several common ways to access electronic data.

1. People can share individual data files through websites, email, or hard storage. These files are often in ASCII format, but can be stored in other (sometimes proprietary) formats.

2. Through an application programming interface (API): a specific system that connects clients to web servers and allows the transfer of data, often formatted in JavaScript Object Notation (JSON).

3. Through raw HTML that can be converted into tabular data through web-scraping.

4. Through a local or remote relational database - a collection of many individual datasets - managed using SQL. 

For modern data science, it's important to be very comfortable working with all of these methods of sharing data. We will go over individual data files in this module, and the other methods in the following modules. 

In this notebook, I demonstrate how to load CSV files with various messy properties that have to be addressed when loading the data into Python. I also demonstrate how to look at a dataframe once it's loaded to search for problems, and how to load fixed width, Excel, SAS, Stata, and SPSS data files. All of the data for these examples are available on this [GitHub page](https://github.com/jkropko/DS-6001/tree/master/localdata).

Before we begin, we load the following libraries:

import numpy as np
import pandas as pd
import os
import sys
sys.tracebacklimit = 0 # turn off the error tracebacks

## Changing the Working Directory
Before we go over the functions to load and save data files, it is useful to set the working directory at the start of your script or notebook. This **sets the default folder where Python opens and saves files**. If all of your files are in the same folder, setting the working directory means you don't have to write out the paths each time you load or save a file.

To set the working directory:

* Load the `os` package.
* Type the folder's address into `os.chdir("`*folder*`")`

To check on the path Python is currently using as a default, type `os.getcwd()` into the console. If you want to change the working directory back after you've run the relevant code, save your old path as an object to begin your notebook, and change the path back to the old path to end your notebook, like this:
```python
import os
oldpath = os.getcwd()
os.chdir("folder")

#(Your code goes here)

os.chdir(oldpath)
```

Because I want this notebook to work on anyone's environment, I will only work with files that are accessable through the web. But make sure to change the working directory in your own notebooks for working with local data files.

<embed src="https://github.com/jkropko/DS-6001/raw/master/localimages/ascii.pdf" width=500>

## Text-Based Data Files
When data could first be stored on harddrives and disks, space was very limited. In order to store data as efficiently as possible, universal standards for which symbols would be considered valid data were adopted. These standards, which are still in use today, are called [ASCII](https://en.wikipedia.org/wiki/ASCII):

**ASCII** - (pronounced "As-Key") American Standard Code for Information Interchange:
* 128 characters are considered to be "legal" in data files.
* ASCII files are plain text files. They may be messy, and not immediately ready for use in analyses, but we have methods to load and clean ASCII data.
* ASCII files are designed to be as small and as universally portable as possible.
* Data points are usually delimited by commas, spaces, or tabs, or might require a data dictionary to read.

The most common ASCII format is comma-separated values (CSV), in which individual data points are separated by commas. A CSV file is a plain text file that can be opened with Notepad on Windows or with TextEdit on Mac. Each row in the data appears on a new row in the text file, but the columns do not necessarily align - instead the commas represent new columns, so that the fourth and fifth commas on a line surround the fifth column in the data, for example. If the column names are included in the data, they will be listed on the first line. If you open a CSV file in a plain text editor, it will look like this:

<img src="https://github.com/jkropko/DS-6001/raw/master/localimages/ascii1.png" width=600>

On many computers with Microsoft Office installed, CSV files are opened by default in Microsoft Excel. Excel might be a convenient tool for aligning the columns and visualizing the data in a spreadsheet, but please note that the `.csv` filetype is a universal and lightweight format that can be opened in any programming environment. It is not specific to Microsoft:

<img src="https://github.com/jkropko/DS-6001/raw/master/localimages/butterfly.jpg" width=400>

In a CSV, the comma is called the delimiter: the character that separates datapoints. Another frequently used delimiter is the tab. Here's the same data in tab-separated format:

<img src="https://github.com/jkropko/DS-6001/raw/master/localimages/tsv.png" width=600>

In some situations the data are stored in a way that minimizes the memory needed to contain the data. In that case, we can do away with the delimiter altogether and instead fixing particular spaces on each line to represent specific columns. We can save further space by also removing the column names from the file. This format is called a fixed-width data file, and in a plain text editor it looks like this:

<img src="https://github.com/jkropko/DS-6001/raw/master/localimages/fixedwidth.png" width=600>

Notice that this file contains no information to help us understand what the columns are or where they begin or end. Fixed-width files always come with a data dictionary that contains this information.

I will show examples of how to work with tab-separated, fixed-width, and other files below. But first, to load a standard CSV file with no issues that need to be fixed, use the `pd.read_csv()` function. The first argument of `pd.read_csv()` is `filepath_or_buffer`, and can be one of three things:

1. The full file address and file name of the data file.

2. Just the file name of the data file if you've already set the working directory to the folder where the file exist.

3. The URL of a data file that's accessible online.

Once a data file is loaded into Python with `pd.read_csv()`, it is called a `DataFrame`.

Here I load public opinion data from the [American National Election Study](https://electionstudies.org):

url = "https://raw.githubusercontent.com/jkropko/DS-6001/master/localdata/anes_example.csv"
anes = pd.read_csv(url)

This dataset is *messy*! As we proceed you will see confusing column names, misleading codes for missing values, strange encodings for categorical features, and other flaws. It is important for us to work with messy data because data is in general always messy in the real-world. 

## Looking at the DataFrame to See if it Loaded Correctly
One of the biggest mistakes someone can make when loading data into Python (or any programming environment) is to assume that the data loaded correctly when the code does not give an error. There are lots of things that can still go wrong. The data might not have properly read the column names, the dimensions might be wrong, the data might have been read in a way that led to valid data getting replaced with missing values, and so on.

There are several functions that are useful for seeing the data to understand whether the data loaded properly. The best strategy is to load data, look at the loaded data to understand any problems, and if necessary, reload the data to fix these problems from the outset.

### Viewing the Data as a Spreadsheet
The best way to visualize the data frame is to type the name of the data frame into a cell in a Jupyter notebook. The output of the cell will be rendered as a spreadsheet, and in that format it will be clear what problems, if any, exist with the data frame. One issue: for large data frames (many rows, many columns, or both), displaying the entire spreadsheet unnecessarily takes up a lot of space. Prior to displaying a spreadsheet, we can set the defaults for the number of rows and columns to be displayed as follows:

pd.set_option('display.max_columns', 10) #display a maximumn of 10 columns
pd.set_option('display.max_rows', 10) #display a maximumn of 10 rows

Now I can see a manageable slice of the data frame. Here's what the ANES data look like:

anes

Note the `...` cells: they are unobtrusive, but in this case they represent 1190 rows and 158 columns. To see more of the data than are contained in this 10 x 10 table, change the defaults in the code listed above.

To see the first several rows, use the `.head()` method. A method is different from a regular function in that it is applied specifically to an existing object in Python's memory, and it is typed as a suffix to a call to that object. For example, to see the first 10 rows of the `anes` data frame, type:

anes.head(10)

To see the last several rows, use the `.tail()` method in exactly the same way:

anes.tail(10)

### Displaying the Data Type of Each Column
All data that is stored in Python's memory is assigned a type that controls how various functions operate by default on that data. For example, the `.describe()` method (that I discuss in the next section) provides means and other summary statistics for numeric data, and frequencies for text data. If you intend to perform mathematical operations on a column in a data frame, such as by including the column in a regression model, it is important to first confirm that the column is read with an appropriate data type. The most common data types are:

* `int64`: integer numbers with up to 64 digits
* `float64`: numbers with decimals with up to 64 total digits
* `object`: text, or numeric data coded as text
* `bool`: only `True` or `False`

We can use the `.dtypes` attribute to display the data types of every column. Because this information is stored in a table, we need to turn off the default limit on the number of rows displayed to see all of the columns' data types:

pd.set_option('display.max_rows', None) #to see all the variables
anes.dtypes

Before moving on, we set the default number of rows displayed back to 10:

pd.set_option('display.max_rows', 10)

### Displaying Column Names
It can be very useful to display the column names in one readable list so that we can work with the variables/features contained in these columns. But as with data frames, we again need to contend with Python's default display settings. To turn off the display limit for items in a list, type:

pd.set_option('display.max_seq_items', None)

To display the column names, use the `.columns` attribute. An attribute is like a method in that it is attached to an existing object in Python's memory, but while a method is a type of function, an attribute is another object. In this case, the column names are contained in a list-type object:

anes.columns

It can be difficult to read a list of column names formatted as a list. To see the column names in a more cleanly formatted table, use the `.dtypes` attribute described above or the `.info()` method with `verbose=True`. The `info()` method also displays the dimensions of the data, a count of the data types across columns, and the memory used by the data frame:

anes.info(verbose=True)

### Descriptive Statistics
One way to catch some big errors is to display statistics derived from the columns of the data frame, such as the mean and minimum and maximum values. For example, in the ANES data, `ftobama` records people's responses to the question: "On a scale from 0 to 100, with 0 being the coldest and 100 being the warmest, how warmly to you feel towards Barack Obama?" I can display various summary statistics for this feature with the following code:

anes[['ftobama']].describe()

The `.describe()` method displays these summary statistics, and typing `anes[['ftobama']]` limits the results to just this one feature (we will discuss subsetting data by columns later in this course). Notice anything strange in the results? The mean value of about 50 seems reasonable, as do the standard deviation and percentiles. But the maximum value is 998 for a feature which by design should be no larger than 100. It turns out that throughout the data 998 is one of a few numeric codes that indicates a nonresponse. We can replace these values with missing values from the outset, and we will do so below in the [Data with Numeric Missing Codes](#miss) section.

To change the percentiles that are displayed, use the `percentiles` parameter and provide a list of the desired percentiles. To show percentiles in increments of 20%, type:

anes[['ftobama']].describe(percentiles = [.2, .4, .6, .8])

Note that the median (50%) is always displayed.

By default the `.describe()` method displays summary statistics for all columns with `int` and `float` data types. To see the summary statistics for the `object` type columns, use the `include` parameter:

anes.describe(include="object")

`object` type columns are treated as text, which means that statistics like the mean and median are impossible to calculate. Instead the `.describe()` method gives us the count of non-missing observations, the number of unique observations, the most frequent value of the feature, and the number of times the most frequent value appears.

## Identifying and Solving Problems with Text-Based Data Files
There are many ways that text-based data files can be arranged that cause problems for loading the data into Python and for using the data for analyses. Please note that not every problem needs to be solved in the loading step: the entire `pandas` library exists for cleaning data once it is loaded into Python's memory. But some problems are more efficiently solved as we load the file. Here we will discuss some common problems and strategies for solving them while loading the data. 

I've uploaded to the [Github page](https://github.com/jkropko/DS-6001/tree/master/localdata) several additional versions of the ANES data that I messed up on purpose.

### Comments Prior to the Header
I created a version of the ANES data with four rows of comments prior to the column names. The following lines of code display the raw text of this file without trying to load the data frame:

url = "https://raw.githubusercontent.com/jkropko/DS-6001/master/localdata/anes_example_toplines.csv"
import requests
file = requests.get(url)
print(file.text[0:1000])

If I try to load the data file as it currently exists by typing
```python
anes = pd.read_csv(url)
```
I get the following error:
```
ParserError: Error tokenizing data. C error: Expected 1 fields in line 5, saw 168
```

This error occurs because the first line tells the `pd.read_csv()` function that there is one column in the data, as there are no commas on this line. So by the time the column names appear there are more commas than the parser knows how to handle.

To solve this problem, use the `header` parameter to tell `pd.read_csv()` how many rows of the data file are taken up by the unwanted header. This function always supposes that the column names are the first row of the data after the header.

anes = pd.read_csv(url, header = 4)
anes

### Data with Numeric Missing Codes
I created a version of the data that uses -999 throughout to represent various missing values, such as when a survey respondent refuses to answer a question:

url = "https://raw.githubusercontent.com/jkropko/DS-6001/master/localdata/anes_example_missing.csv"
anes = pd.read_csv(url)
anes

We can always proceed with the data frame as it is, and use various functions in `pandas` to replace these -999 values. But in this case, it is easier to read these values as missing as we load the data. We can do that with the `na_values` parameter. Then all of the -999 values are replaced with the `NaN` character, which Python recognizes as a missing datapoint.

anes = pd.read_csv(url, na_values = -999)
anes

### Comments Inside the Data
Suppose that you work with a data file in which the data provider left comments throughout the data. That's heresy. But it can definitely happen. Hopefully the commenter had enough forethought to place a uniform character in front of these comments. If so, we can remove the comments while loading the data. Consider the following data file:

url = "https://raw.githubusercontent.com/jkropko/DS-6001/master/localdata/anes_example_comments.txt"
anes = pd.read_csv(url, header = 4)
anes

To ignore these comments, use the `comment` parameter:

anes = pd.read_csv(url, header = 4, comment = '@')
anes

### Data Without Column Names
The `pd.read_csv()` function assumes that the column names are listed on the first line of the data file, unless the `header` parameter is used, in which it assumes the column names are on the first line after the header. But if the data do not contain a row of column names then Python will use the first line of valid data as the column names. I created a version of the ANES data with the column names deleted. Consider what happens when I load this data file normally:

url = "https://raw.githubusercontent.com/jkropko/DS-6001/master/localdata/anes_example_nocolnames.csv"
anes = pd.read_csv(url)
anes

The column names are not descriptive of what the columns represent. But worse than that, these names are the datapoints from the first row of the data. That means we've lost an observation. To deal with this problem, use the `header=None` parameter.

anes = pd.read_csv(url, header=None)
anes

While we still have the issue that the column names are non-descriptive, at they are logically labeled in numeric order from left to right, and we haven't lost the first observation. If we want to add the prefix "X" to each of these numbers, we can add the `prefix="X"` parameter:

anes = pd.read_csv(url, header=None, prefix="X")
anes

If the data do not contain a header row for variable names, and we want the variables to have the right names, we have to define the names separately and pass this list using the `names` parameter:

col_names = ['caseid', 'turnout12', 'turnout12b', 'vote12', 'percent16', 'meet',
       'givefut', 'info', 'march', 'sign', 'give12mo', 'compromise', 'ftobama',
       'ftblack', 'ftwhite', 'fthisp', 'ftgay', 'ftjeb', 'fttrump', 'ftcarson',
       'fthrc', 'ftrubio', 'ftcruz', 'ftsanders', 'ftfiorina', 'ftpolice',
       'ftfem', 'fttrans', 'ftmuslim', 'ftsci', 'reg', 'demcand', 'repcand',
       'vote16jb', 'vote16bc', 'vote16tc', 'vote16mr', 'vote16dt', 'presjob',
       'lazyb', 'lazyw', 'lazyh', 'lazym', 'violentb', 'violentw', 'violenth',
       'violentm', 'econnow', 'econ12mo', 'pid1d', 'pid2d', 'pid1r', 'pid2r',
       'pidstr', 'pidlean', 'lcself', 'lcd', 'lcr', 'lchc', 'lcbo', 'lcdt',
       'lcmr', 'lctc', 'srv_spend', 'campfin', 'immig_legal', 'immig_numb',
       'equalpay', 'parleave', 'crimespend', 'death', 'terror_worry',
       'terror_12mo', 'terror_local', 'relig_bc', 'relig_bcstr', 'relig_srv',
       'relig_srvstr', 'incgap20', 'isis_troops', 'syrians_a', 'syrians_b',
       'pc_a', 'pc_b', 'minwage', 'healthspend', 'childcare', 'getahead',
       'ladder', 'finwell', 'warm', 'warmbad', 'warmcause', 'warmdo',
       'freetrade', 'stopwhite', 'stopblack', 'forcewhite', 'forceblack',
       'stop_12mo', 'arrested_12mo', 'charged_12mo', 'jailed_12mo',
       'convict_12mo', 'famstop_12mo', 'stop_ever', 'arrested_ever',
       'charged_ever', 'jailed_ever', 'convict_ever', 'famstop_ever',
       'pk_deficit', 'pk_sen', 'pk_spend', 'birthright_a', 'birthright_b',
       'femoff_jobs', 'femoff_ed', 'femoff_spend', 'femoff_issues',
       'lpres_pleased', 'lpres_immig', 'lpres_la', 'vaccine', 'autism',
       'bo_muslim', 'bo_confid', 'amer_ident', 'race_ident', 'whitework',
       'whitejob', 'wguilt1', 'wguilt2', 'wguilt3', 'buycott', 'boycott',
       'skintone_mob', 'skintone', 'skin_discrim', 'africanam10_1',
       'white10_1', 'hispanic10_1', 'asianam10_1', 'nativeam10_1', 'other10_1',
       'other10_open', 'birthyr', 'gender', 'race', 'race_other', 'educ',
       'marstat', 'speakspanish', 'employ', 'employ_t', 'faminc', 'faminc2',
       'state', 'votereg', 'pid3', 'pid7', 'ideo5', 'newsint', 'pew_bornagain',
       'pew_churatd', 'religpew', 'religpew_t', 'ever_vs_12mo_rand']
anes = pd.read_csv(url, header=None, names=col_names)
anes

### Delimiters Other Than Commas
Here's a version of the ANES data that is delimited by tabs:

url = "https://raw.githubusercontent.com/jkropko/DS-6001/master/localdata/anes_example_tab.txt"
file = requests.get(url)
print(file.text[0:2000])

The `pd.read_csv()` file also loads text-based data files with delimiters other than commas. To load tab-delimited data, use the `sep="\t"` parameter:

anes = pd.read_csv(url, sep="\t")
anes

For delimiters other than a tab, simply type that character in quotes with the `sep` parameter. Here's another version of the ANES data, delimited by semi-colons:

url = "https://raw.githubusercontent.com/jkropko/DS-6001/master/localdata/anes_example_semicolon.txt"
file = requests.get(url)
print(file.text[0:2000])

To load the data:

anes = pd.read_csv(url, sep=";")
anes

### Fixed-width Files
A fixed-width file contains no delimiters. Instead, it aligns all of the data for one variable in the same position on each row. These files generally do not store variable names, and might use less memory than CSV. But that makes the data impossible to parse without an external list of where each variable is stored. The first and most important step is to get this list. 

For this example, I pulled data from a public opinion survey conducted by the National Journal a few years ago. The data are available from the [Roper Center for Public Opinion Research](https://ropercenter.cornell.edu/), and the raw data are in fixed-width format. The codebook is stored on [GitHub](https://github.com/jkropko/DS-6001/raw/master/localdata/njcc_codebook.pdf), take a look. The features are listed on page 3, along with their column positions.

Loading a fixed-width file is a two step process. First, we use the codebook to create lists of the variable names, and either the width of each variable (how many columns each variable takes up), or the starting and ending position. Here we save both lists, although you will only need one of these two lists. 

For the starting and ending position of each variable, we create a list of length 2 for each variable, where the first element is the column the previous variable ends on (or 0 for the first variable) and the second element is the column the current variable ends on. For example, if a variable occupies columns 34, 35, and 36, its list of length 2 is [33,36]. Then we store the lists-of-2 in a list-of-lists.

url = "https://raw.githubusercontent.com/NovaVolunteer/Practice_Application_DS/master/Week%205/njcc33850.dat"

datanames = ['psraid', 'sample', 'int_date', 'area',
'state', 'cregion', 'density', 'usr', 'cc1', 'cc1a',
'cc2', 'cc3', 'cc4', 'cc5', 'cc6', 'cc7', 'ql1', 'ql1a',
'qc1', 'hh1', 'employ', 'par', 'sex', 'age', 'educ2',
'hisp', 'race', 'inc', 'income', 'reg', 'party',
'partyln', 'iphoneus', 'hphoneus', 'recage', 'receduc',
'racethn', 'standwt', 'raceos']

datawidths = [6, 1, 6, 3, 2, 1, 1, 3, 1, 1, 
            1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 
            1, 1, 1, 2, 1, 1, 1, 2, 1, 1, 
            1, 1, 1, 1, 1, 1, 1, 4, 30]

datapos = [[0,6], [6,7], [7,13], [13,16], [16,18],
    [18,19], [19,20], [20,23], [23,24], [24,25],
    [25,26], [26,27], [27,28], [28,29], [29,30],
    [30,31], [31,32], [32,33], [33,34], [34,35],
    [35,36], [36,37], [37,38], [38,40], [40,41],
    [41,42], [42,43], [43,45], [45,46], [46,47],
    [47,48], [48,49], [49,50], [50,51], [51,52],
    [52,53], [53,54], [54,58], [58,88]]

To load the fixed-width data into Python, we use the `pd.read_fwf()` function. We specify the location (or URL) of the data file and the names of the columns. And we can either specify the widths of each column, or the starting and ending positions (but not both). Using the widths: 

njcc = pd.read_fwf(url, widths=datawidths, header=None, names=datanames)
njcc

And using the starting and ending positions:

njcc = pd.read_fwf(url, colspecs=datapos, header=None, names=datanames)
njcc

## Loading Other Kinds of Electronic Data Files
CSV, ASCII, and other kinds of plain text files are very common in fields that primarily use open-source programming environments like Python and R, as these file types are lightweight and universal. But there are many more people out there who work in fields that use specific, proprietary data analysis software. It can be a real challenge to load a specific file format in a context outside of its native software environment. There are specialized software that only exist to transfer proprietary data from one environment to another. One package is Stat/Transfer, which can easily convert data from Stata to SAS to SPSS to Excel for [$129 a year for academic users](https://stattransfer.com/ordering/academic/).

If you are using Stata, SAS, SPSS, Excel, or another program, or if you are working with someone who uses that software, and you want to transfer data to Python, the easiest approach is to save the working data as a CSV file and then load it into Python with `pd.read_csv()`. All of those software packages have the functionality to save data as CSV.

That doesn't help you if you are dealing with an SPSS file and you do not have access to SPSS. Fortunately, Python has functions to load data from pretty much every software environment. Here's a rundown of these functions.

### Loading Excel Files
There are a few methods for loading Excel files in Python but a great function is the `pd.read_excel()` function in `pandas`. One big way that Excel files differ from other data formats is the use of sheets in the same document. The main challenge in loading an Excel file in Python is dealing with the sheets. 

I've saved an Excel file on [GitHub](https://github.com/jkropko/DS-6001/raw/master/localdata/NBA-Team-Sample-BoxScore-Dataset.xlsx) that contains information about NBA teams during the 2018-2019 season. This Excel document contains four sheets, named "NBA-TEAM-SAMPLE", "METADATA", "TEAMS", and "CONVERT DATE FORMAT". All four sheets have visual formatting. I want to load the "TEAMS" sheet without carrying forward any code that refers to the visual appearance of this sheet.

The first argument of `pd.read_excel()` is the path, as with pd.read_csv(), and it can take a URL. The second argument is sheet_name. If the Excel file has sheets with names, you can type the name of the sheet here. Or type a number: 0 refers to the first sheet, 1 to the second, etc. This function loads the data directly to a data frame, and ignores other graphical elements of Excel sheets, such as shading particular cells or using fonts.

url = "https://github.com/NovaVolunteer/Practice_Application_DS/blob/master/Week%205/NBA-Team-Sample-BoxScore-Dataset.xlsx?raw=true"
nba = pd.read_excel(url, sheet_name="TEAMS")
nba

If you specify more than one sheet within the `sheet_name` parameter using a list, `pd.read_excel()` will produce a list of dataframes, one for each sheet you specify. Typing `sheet_name = None` produces a list with all of the sheets. For example, to load the "NBA-TEAM-SAMPLE" and "TEAMS" sheets, and save them as two separate data frames embedded in a list, type:

nba = pd.read_excel(url, sheet_name=[0,2])
nba[0]

In this case, because we explicity did not include the sheets indexed as 1 and 3, Python leaves these indices empty. To access the "TEAMS" sheet, specify the index-2 item of the `nba` list:

nba[2]

### Loading SAS, Stata, and SPSS Files
For SAS files with extensions`.sas7bdat` or `.xport`, or Stata files with extension `.dta`. the `pd.read_sas()` and `pd.read_stata()` functions work just like other data parsing functions in `pandas`. We can pass the file path, the file name alone (if we've set the working directory), or a URL to these functions and they loads the data directly to a data frame.

On GitHub, I've saved a SAS file containing the monthly inflation rate in the United States since 1983, and a Stata file containing a CBS public opinion poll. To load the SAS file, I type:

url = "https://github.com/jkropko/DS-6001/raw/master/localdata/inflation.sas7bdat"
inflation = pd.read_sas(url)
inflation

And to load the Stata file:

url = "https://github.com/jkropko/DS-6001/raw/master/localdata/cbspoll.dta"
cbspoll = pd.read_stata(url)
cbspoll

SPSS files have the file extension `.sav`, and can be loaded with `pd.read_spss()` in the same way. One issue (at the time this notebook was written) is that the `pd.read_spss()` function only accepts local files, and not files from URLs. I saved data from a public opinion survey on [GitHub](https://github.com/jkropko/DS-6001/raw/master/localdata/survey.sav). If you want to try loading it into Python, download the file and move it to the folder where you've set your working directory (or type out the whole file path in the following code), and type:
```python
survey = pd.read_spss("survey.sav")
survey
```
Eventually I expect this `pd.read_spss()` function to be able to accept URLs as well. At that point, the following code should also work:
```python
url = "https://github.com/jkropko/DS-6001/raw/master/localdata/survey.sav"
survey = pd.read_spss(url)
survey
```

## Saving CSV and ASCII Files to Disk
Suppose we've done all the steps needed to clean and manage the data. We might want to save a clean version of the data in a CSV or other ASCII file on our local disk space. We can do so by applying the `.to_csv()` method to the `anes` data frame. The first argument is the filename with whatever extension we want for the saved file. As with `pd.read_csv()`, we can also specify the `sep` parameter to choose a delimiter for the text-based data file we are creating. Let's save the ANES dataframe as "anes_cleaned.csv" in our working directory:

anes.to_csv("anes_cleaned.csv", sep=",")

For a tab-separated file we can employ the more general ".txt" extension:

anes.to_csv("anes_cleaned.txt", sep="\t")