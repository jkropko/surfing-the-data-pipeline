#!/usr/bin/env python
# coding: utf-8

# # Data Wrangling with `pandas`

# ```{contents} Table of Contents
# :depth: 4
# ```

# ## Introduction: Why It's So Important to Get Data Management Right
# ### The Case of "Genomic Signatures to Guide the Use of Chemotherapeutics"
# In 2006, a study "[Genomic Signatures to Guide the Use of Chemotherapeutics](https://www.nature.com/articles/nm1491)" was published in *Nature Medicine*. This study tackles the question of why chemotherapy works well for some cancer patients and less well for others. The authors claimed that they could predict whether and how treatments would work for a patient based on the sequence of chemicals in the DNA in the patient's cancer cells. This study got a lot of attention as a major breakthrough in cancer treatments. The hope was to use genomic data to tailor a treatment regime for individual patients that maximizes the likelihod that the treatment would be effective. 
# 
# Unfortunately, as you can see on the journal's website for this article, the study has been retracted. The story of how this study came into question, and the damage it did before it was retracted, is described by Keith Baggerly in his talk "[The Importance of Reproducibility in High-Throughput Biology: Case Studies in Forensic Bioinformatics](https://www.youtube.com/watch?v=7gYIs7uYbMo)":

# In[1]:


from IPython.display import IFrame
IFrame(src="https://www.youtube.com/embed/7gYIs7uYbMo", width="560", height="315")


# The slides for this talk are available [here](http://www.bioconductor.org/help/course-materials/2009/BioC2009/talks/wrap_bioc_shareb.pdf). In short, Baggerly and his coauthor Kevin R. Coombes attempted to reproduce the findings in the Potti et al study, and they were unable to do so. There is a difference between reproduction and replication: reproducing a study involves using the same data used in the original study and writing code that yields the exact same results; replication involves repeating the study using new data. While replication is an essential practice for establishing the validity of a study, replication is also a higher standard than reproduction. If a study cannot be reproduced, then there must have been errors in the process collecting and cleaning the raw data that led to the publication of incorrect results.
# 
# After deciding to replicate the Potti et al article, Baggerly and Coombes were able to get a copy of the raw data that were used in the study, but they did not find scripts or documentation that described the steps the original study took to clean the raw data. That's because there were no scripts and no documentation: the data were cleaned on the fly, probably with a point-and-click interface like Microsoft Excel, with no records of what was done to the data.
# 
# Without having good documentation available that explains how research was done, Baggerly and Coombes had to resort to "forensics". They started with the results and the raw data, and they inferred what the researchers must have done to obtain the reported results from the raw data. They were alerted to potential problems with the study when they tried to replicate the finding that there is a clear difference between two types of drugs, as shown in the graphic on slide 13 of Baggerly's slide deck. It should have been an easy finding to replicate. Instead they found significant overlap between the two drugs, as shown in the graphic on slide 14. They responded by trying to reproduce exactly what was done to the raw data in the original study to produce the first finding. After exhausting all possible *valid* data management steps, they started **making mistakes on purpose** to see if one of those mistakes would replicate the published results. 
# 
# Baggerly and Coombes found that the authors of the original paper made an error in which the codes for each reported gene were off by one. That is, the data for each gene is matched to the label for the gene whose data exists one row above. This error happened, according to Baggerly's best guess, because the software that the authors used requires the inputted data file to NOT have a header row for column names. But they seemed to just copy and paste the data, along with the header row. A second result that Baggerly says should "bother you" is that, on the heat map on slide 29, Baggery and Coombs matched 6 of the 7 heat maps despite the fact that they only matched the reported gene names for 3 of the 7 drugs. Therefore they would expect to reproduce the heat map for only these 3 drugs. Baggerly doesn't know why they matched the heat maps for the other 3 drugs despite the fact that they are using the wrong data.
# 
# A second discrepancy that raises a red flag for Baggerly is the plot showing the sensitive and resistant patients, as compared to the analogous plot from the paper that introduced the test dataset. The plot shows 13 sensitive and 11 resistant samples, whereas the paper that introduced the data shows 11 sensitive and 13 resistant samples. Baggery believes that the authors mixed up the 0 and 1, indicating sensitive and resistant, in the spreadsheet.
# 
# In short, Baggerly and Coombes were only able to reproduce the findings in the Potti et al study by making "small" mistakes on purpose. When I say small, I mean that these sorts of errors can occur frequently when using a point-and-click interface for data management and a copy-and-paste method for transfering data. These errors also occur without informing the user of any errors. But in practice these small errors have profound impacts on the results of the study. If those results are taken seriously and applied outside of the specific study, these mistakes can do a lot of harm in the world.
# 
# In the case of the Potti et al study, while Baggerly and Coombes were investigating the paper,
# drug trials began at Duke University based on the results of the study. The treatment was administered to the patients with childhood leukemia. Because of the mistake that swaped the 0s and 1s, the treatment was administered to patients who are resistant to it, will not benefit from it, and may in fact be harmed by it.
# 
# Baggerly and Coombes wrote a report detailing these inconsistencies and a few others - there's evidence that some samples were reused 2, 3, or 4 times, and 4 genes appear in the results despite the fact that they are not included in the test data - and sent the report to *Nature Medicine*. Their report caused Duke to stop the clinical trials of these drugs pending an investigation. But a short while later the trials were restarted, with the statement that the investigation had "strengthened confidence in this approach." The investigators refused to share their findings. Baggery and Coombs has to issue a freedom of informatiom act (FOIA) request to see the results of the investigation, only to find that no mention was made of the problematic drugs. Writing directly to Duke yielded no response. They had to get many prominent biostatisticians to sign a joint letter of concern. The letter got some attention in the media, but mostly because it was revealed that the principal investigator of the flawed studies lied on his CV about being a Rhodes scholar! Only after the letter generated a serious amount of negative media attention for Duke did the trials get suspended.

# ### The Reproducible Research Movement
# There are four lessons we can learn from that Baggerly and Coombes's work to reassess the Potti et al. First, mistakes at the data management stage happen all the time, and when the environment uses a point-and-click interface the errors are easier to miss because of a lack of a sufficient error system. Second, small errors can have big effects. It's easy to confuse categories when they are labeled with arbitrary numbers instead of words, but if that confusion results in mixing up the treatment and control groups then every effect reported in the study will have the incorrect sign, and all of the conclusions we draw will be the exact opposite of the truth. Third, it is common for people who do work with data to fail to keep records of their code and the steps they used to manipulate the raw data prior to an analysis, and without documentation, it can be extremely difficult to impossible to catch errors in the data management process. Fourth, while most scientists are hopefully open to seeing and admitting their mistakes, there aren't a lot of incentives in academia and other fields to make the research stream more transparent.
# 
# In "[The Reproducible Research Movement in Statistics](http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.667.6492)", Victoria Stodden describes the problem:
# 
# > The research system must offer rewards for reproducible research at every level from departmental decisions to grant funding and journal publication, incorporating notions of code and data sharing into institutional 
# promotion and hiring and grant proposal review. The current academic research system places the primary emphasis on publication and little on reproducibility. This has the effect of penalizing those researchers that produce reproducible computational research. Software development has been characterized as support of science rather than doing real science. The result is that scientists are discouraged from spending time writing, testing, or releasing code. With the ever-increasing pervasiveness of computation and software across the research landscape, such attitudes and practices must change (p.1069-1070).
# 
# As a result of these issues, the last decade has seen a remarkable cultural shift in fields that use data towards making data management easier and more transparent. These efforts are often called part of the "reproducible research movement". The movement involves two efforts: first, a greater push to develop software that makes it easier to clean data and to share and communicate code; second, a drive to change standards of best practice in fields that use data. Since Victoria Stodden's article in 2013, data science has incorporated both parts of the reproducible research movement. In Python, the `pandas` package makes it much easier to clean data using code that is intuitive and relatively easy to follow, and Jupyter notebooks combine code, results, and text that explains the code in one document. Modern data science requires practioners to share or be ready to share their code, often in a notebook.

# ### The Origin of `pandas`
# The `pandas` package in Python is written and maintained by Wes McKinney, who also wrote [Python for Data Analysis](https://learning.oreilly.com/library/view/python-for-data/9781491957653/). On the `pandas` [team page](https://pandas.pydata.org/about/team.html), under governance, McKinney is listed as the `pandas` "[Benevolent Dictator for Life](https://en.wikipedia.org/wiki/Benevolent_dictator_for_life)". The phrase "Benevolent Dictator for Life" is given to leaders of important open-source projects, and originated with Guido van Rossum, the creator of Python.
# 
# McKinney developed `pandas` in 2008 and first released the project publicly in 2009. Though not explicitly presented as a contribution to the reproducible research movement, the goal of `pandas` was to replace existing tools for data manipulation that had led to major mistakes in research, as was the case for the Potti et al article. According to this [profile of Wes McKinney](https://qz.com/1126615/the-story-of-the-most-important-tool-in-data-science/) in Quartz Magazine, `pandas` "makes it so that data analysis tasks that would have taken 50 complex lines of code in the past now only take 5 simple lines, because McKinney already did the heavy lifting." Specifically:
# 
# > Python was missing some key features that would make it a good language for data analysis. For example, it was challenging to import CSV files (one of the most common formats for storing datasets). It also didn’t have an intuitive way of dealing with spreadsheet-like datasets with rows and columns, or a simple way to create a new column based on existing columns.
# 
# > Pandas addressed these problems. David Robinson, a data scientist at Stack Overflow, explained the importance of it in technical terms. “The idea of treating in memory data like you would a SQL table is incredibly powerful,” he says. “By introducing the ‘DataFrame,’ Pandas made it possible to do intuitive analysis and exploration in Python that wasn’t possible in other languages like Java. And is still not possible.”
# 
# That is, `pandas`, like SQL, is a declarative language, not a procedural one. Simple functions and methods in `pandas` call underlying imperative code that performs the requested action by operating on vectors, matrices, and arrays. `pandas` as much as possible uses `numpy` functions to perform actions as quickly as possible (by using `numpy`'s [vectorized](https://en.wikipedia.org/wiki/Vectorization_(mathematics)) code). In short, the motivation for the development of `pandas` is to make data manipulation as straightforward as possible and for those functions to run as quickly as possible.
# 
# `pandas` is an extremely popular package for data science, and the Quartz article asserts that much of the growth in popularity that Python has experienced on Stack Overflow can be attibuted to `pandas`. While `pandas` is currently the [34th most frequently downloaded Python package](https://hugovk.github.io/top-pypi-packages/), it is certainly one of the most frequently downloaded for data science applications in Python.

# ### Tidy Data
# In Module 7, we discussed the concept of Tidy Data as described by Hadley Wickham, founder of RStudio and creator of the `tidyverse` packages in R, in the article "[Tidy Data](https://www.jstatsoft.org/article/view/v059i10)". Tidy Data is an organizational schema for data that makes most kinds of data analysis possible. To qualify as tidy, data must follow these rules:
# 
# > 1. Each [feature] forms a column.
# > 2. Each observation forms a row.
# > 3. Each type of observational unit forms a table (p. 2).
# 
# In addition, even when data are arranged in a single table in which records are rows, features are columns, and all records are of like units, there are many steps a researcher should take to manipulate the data to make a dataframe easier to work with. Hadley Wickham defines four essential "verbs" of data manipulation:
# 
# > * Filter: subsetting or removing observations based on some condition.
# > * Transform: adding or modifying variables. These modifications can involve either a single variable (e.g., log-transformation), or multiple variables (e.g., computing density from weight and volume).
# > * Aggregate: collapsing multiple values into a single value (e.g., by summing or taking means).
# > * Sort: changing the order of observations (p. 13).
# 
# This philosophy of data management is built into the `tidyverse` packages for R, but it also forms a guiding principle for data manipulation with `pandas` because `pandas` includes tools to accomplish all of these tasks. In fact, Hadley Wickham and Wes McKinney are currently working together on a project called [https://ursalabs.org/](https://ursalabs.org/), which aims to bridge the R-Python divide and to develop platform-independent data science tools.

# ## Example: The American National Election Study
# The [American National Election Study](https://electionstudies.org) (ANES) is a massive public opinion survey conducted after every national election. It is one of the greatest sources of data available about the voting population of the United States. It contains far more information than a typical public opinion poll. Iterations of the survey contain thousands of features from thousands of respondents, and examines people's attitudes on the election, the candidates, the parties, it collects massive amounts of demographic information and other characteristics from voters, and it records people's opinions on a myriad of political and social issues.
# 
# Prior to each election the ANES conducts a "pilot study" that asks many of the questions that will be asked on the post-election survey. The idea is to capture a snapshot of the American electorate prior to the election and to get a sense of how the survey instrument is working so that adjustments can be made in time. Here we will work with the [2019 ANES pilot data](https://electionstudies.org/data-center/2019-pilot-study/). To understand the features and the values used to code responses, the data have an associated [questionnaire](https://electionstudies.org/wp-content/uploads/2020/02/anes_pilot_2019_questionnaire.pdf) and [codebook](https://electionstudies.org/wp-content/uploads/2020/02/anes_pilot_2019_userguidecodebook.pdf). The pilot data were collected in December 2019 and contain 900 features collected from 3,165 respondents. 
# 
# Despite a great dfeal of pre-processing on the part of the data authors, the data is not currently in form we can analyze. We will use the tools available in `pandas` to manipulate the data and prepare it for analysis. The data are available in CSV, SAS, and Stata formats. I put the CSV version on my Github repository so that we can have easier access to it, but I encourage you to access the data yourself by registering for a free account on electionstudies.org. 
# 
# We start by loading the `numpy` and `pandas` packages, along with some additional packages and modules to perform some specialized tasks. Please use `pip install` or `conda install` to install these packages if you have not yet done so:

# In[2]:


import numpy as np
import pandas as pd
import sidetable
import warnings
warnings.filterwarnings('ignore')


# Then we load the data with `pd.read_csv()`:

# In[3]:


anes = pd.read_csv("https://github.com/jkropko/DS-6001/raw/master/localdata/anes_pilot_2019.csv")


# These data are technically in tidy format because the records are stored in the rows, the features are stored in the columns, and the rows all represent individual people. But there are still problems that will keep us from being able to use the data in analyses. There are more features here than we can manage in a feasible amount of time. Many of the features have names that we might want to change to be more descriptive, and use arbitrary numeric codes to stand in for categories. If we look at the codebook, we will also see that negative numbers in the cells represent missing datapoints, and unless we take steps to replace these datapoints they will be read as valid numeric data. We will use the tools in `pandas` to manipulate the data so that we keep only the features of interest, labels throughout the data are intuitive and readable, columns have the correct data type, and missing datapoints are coded as missing.

# ## Tools for Understanding the Data and Diagnosing Problems
# Before we can start manipulating the data, we need to be able to effectively look at the data to catch the problems that we need to address. All of these tools exist as methods or attributes of a `pandas` dataframe or of a specific column of a dataframe. This discussion reviews some of the material covered in Module 2, because these methods are useful for assessing both whether a data file loaded properly and for seeing the problems that still exist after the data have been loaded.
# 
# First, to see the dimensions of a dataframe and the dataframe's memory usage, we can use the `.info()` method:

# In[4]:


anes.info()


# In this case, the `anes` data has 3,165 rows and 900 columns, and takes up a little bit more than 21.7 MB of memory. The `.info()` output also tells us that of the 900 columns, 223 have float (numeric with decimals) valued data, 600 have integer valued data, and 77 have object values, which refers to strings or categories.
# 
# Viewing the data table itself can be extremely useful. As we discussed in module 2, however, the default behavior limits the number of rows and columns that can be displayed in a dataframe. I find it useful to turn off the limit on the number of columns that can be displayed:

# In[5]:


pd.set_option('display.max_columns', None) 


# Now we can see all of the columns in any dataframe we call. With 900 columns, there will be quite a lot of sidescrolling, and it will be difficult to find any one column in particular. Viewing the data will become more useful once we limit the columns we will include in the data. To see the first few rows, use the `.head(n)` method, where `n` is the number of rows from the top to display. The first three rows, for example, are

# In[6]:


anes.head(3)


# To see the last several rows, use the `.tail(m)` method where `m` is the number of rows from the bottom. The last three rows are:

# In[7]:


anes.tail(3)


# To see a random selection of rows, use the `.sample(p, replace=False)` method, where `p` is the sample size and `replace=False` indicates sampling without replacement. To take a sample with replacement (for bootstrapping, for example), write `replace=True`. Here are five randomly drawn rows from `anes`:

# In[8]:


anes.sample(5, replace=False)


# To see the count of non-missing observations and summary statistics such as the mean, standard deviation, minimum, maximum, and quantiles for the numeric columns, use the `.describe()` method:

# In[9]:


anes.describe()


# To change the quantiles that are displayed, use the `percentiles` argument, set equal to a list of the desired quantiles. To see the 33rd and 67th quantiles, type

# In[10]:


anes.describe(percentiles = [.33, .67])


# To see the count of non-missing observations, number of unique values, and the most frequent value and its frequency for string or categorical features, use the `include='object'` argument:

# In[11]:


anes.describe(include='object')


# To see the name and data type of each column, use the `.dtypes` attribute. To avoid truncation, type `pd.set_option('display.max_rows', None)`. Because there are 900 columns to report in this case, to save space I won't turn off the truncation:

# In[12]:


anes.dtypes


# To find rows in the data that are duplicated, use the `.duplicated()` method. This method outputs a list of values that are `True` or `False` indicating whether or not each row is a duplicate of another row in the dataframe. To view the duplicated rows, use the `.duplicated()` output to filter the rows when using `.loc` to subset the data (more on `.loc` below). By default, `.duplicated()` marks all duplicate rows as `True` except for the first occurrence in the dataframe. In the case of the ANES data, there are no duplicated rows:

# In[13]:


anes.loc[anes.duplicated(),]


# To generate a dataframe without these duplicted rows, use the `~` operator to negate the logical values. That tells Python to keep the rows that are not duplicated:

# In[14]:


anes.loc[~anes.duplicated(),]


# To examine the values of a specific column, call the column name either as an attribute of the dataframe (for example, to see people's "feeling thermometer" ratings of Joe Biden, type `anes.ftbiden`) or as a string within a list (`anes['ftbiden']`). Then it is possible to employ methods like `.describe()` on this single column:

# In[15]:


anes['ftbiden'].describe() # or anes.ftbiden.describe()


# For categorical columns, to list of the unique categories and their frequencies, use the `.value_counts()` method:

# In[16]:


anes.vote20cand.value_counts()


# There's a nicer-looking and more informative version of this frequency table available in the `sidetable` package, which adds the `.stb.freq()` method to a `pandas` dataframe. Pass a list with the column name to this function:

# In[17]:


anes.stb.freq(['vote20cand'])


# ## Indexing a Data Frame
# Indexing a dataframe is the act of extracting a selection of rows or columns from a dataframe based on either the numeric position of the row or column, or based on the name of the row or column. There are four ways to index a dataframe:
# 
# * Using the `.iloc` attribute of the dataframe. This attribute allows us to extract certain rows and columns from a dataframe by directly entering in the row and column numbers of the selection.
# 
# * Using the `.loc` attribute of the dataframe. This attribute allows us to extract rows and columns based on the row and column names.
# 
# * Calling a specific column by name as an attribute of a dataframe.
# 
# * Using square brackets `[]` after writing the dataframe's name to extract one or more columns by referring to those columns' names. 
# 
# To extract based on numeric position, use the `.iloc` attribute of a dataframe as follows:
# ```
# df.iloc[rownumbers, columnnumbers]
# ```
# `.iloc` provides a version of the dataframe that can take row and column coordinates as the first and second elements within an associated list, like an array. To specify more than one row or more than one column, these elements can be lists or can use `:` to express a range. For example, to extract rows 1 through 4 (remembering that the first row is row 0 and tha the second number in the range is excluded) and columns 12 through 14, we can type:

# In[18]:


anes.iloc[1:5, 12:15]


# To extract rows 2, 4, 6, and 8 for columns 20, 25, and 30, we type:

# In[19]:


anes.iloc[[2,4,6,8], [20, 25, 30]]


# The advantage of the `.loc` approach to extract rows and columns by name is the ability to use **slicing** - that is, specifying a range of columns from the leftmost to the rightmost column, and all columns in between. Writing `:` alone in the rows slot returns all of the rows. For example, the first of the feeling therometer features from left-to-right in the `anes` data is `fttrump` and the last column is `ftpales`. To extract all of these columns, we type:

# In[20]:


anes.loc[:,'fttrump':'ftpales']


# We can return one column by calling its name just like any other attribute by typing the dataframe, a period, and a column name. This approach is appropriate when we want to extract just one column for the datadrame. To extract the `ftbiden` column from `anes`, we type:

# In[21]:


anes.ftbiden


# Equivalently, we can call this column within brackets as follows:

# In[22]:


anes['ftbiden']


# This approach allows us to extract more than one column by including a list of column names in the index:

# In[23]:


anes[['ftbiden', 'fttrump']]


# ## Selecting, Renaming, and Rearranging Columns
# The `anes` data has 900 columns, which is too many for us to feasibly work with in this notebook. Even if the intention is to run a machine learning model that processes a large number of columns, it is probably the case that some columns should not be included in the feature space. The first task in data manipulation is to restrict the data to only those columns we actually need.
# 
# For the ANES, let's keep the following columns:
# 
# * `caseid` - the primary key that identifies individual survey respondents
# * `liveurban` - Do you currently live in a rural area, small town, suburb, or a city?
# * `vote16` - In the 2016 presidential election, who did you vote for?
# * `particip_3` - In the last 12 months, have you joined in a protest march, rally, or demonstration?
# * `vote20jb` - If the election is between Donald Trump and Joe Biden, who will you vote for?
# * `mip` - What do you think is the most important problem facing this country? (free response)
# * `confecon` - Overall, how worried are you about the national economy?
# * `ideo5` - How would you describe your personal political ideology?
# * `pid7` - Which party to you identify with?
# * `guarinc` - Do you favor or oppose a universal basic income?
# * `famsep` - Do you favor or oppose the policy of family separation at the border?
# * `freecol` - Do you favor or oppose a policy of free tuition at public universities?
# * `loans` - Do you favor or oppose a policy of student loan debt forgiveness?
# * `race` - Race
# * `birthyr` - Birth year
# * `gender` - Gender
# * `educ` - Educational attainment
# * `inputstate` - State of residence
# * `weight` - The survey probability weights that need to be applied to rows to make results more representative of the U.S. adult population
# 
# The easiest way to reduce the dataframe to include only these columns is to define a list of these column names, then pass the list to the dataframe index as follows:

# In[24]:


mycols = ['caseid','liveurban','vote16','particip_3','vote20jb',
          'mip','confecon','ideo5','pid7','guarinc','famsep',
          'freecol','loans','race','birthyr','gender','educ','inputstate', 'weight']
anes[mycols]


# Note that while we displayed the reduced dataframe, we have not yet saved this reduced dataframe as a Python variable. 
# 
# In addition to the features listed above, let's also include the columns that contain the "feeling thermometers". The respondents are asked to rate many things from 0 (strongly dislike) to 100 (strongly like) including politicians like Joe Biden and Donald Trump, countries like Turkey and Canada, groups of people like Asians, immigrants, and journalists, and organizations like NATO and the NRA. These columns all begin with "ft": the ratings for Donald Trump and Joe Biden are contained in `fttrump` and `ftbiden`, for example. Other columns contain metadata regarding these responses: `ftbiden_skp` indicates whether the respondent skipped this question, `ord_ftbiden` reports where this question appeared in each respondent's randomized question ordering, and `ftbiden_page_timing` records how long the respondent took to answer this question. For this example, we only want to keep the feeling thermometers.
# 
# In this case, we want to use code that automatically identifies all of the columns that begin with a specific string like "ft" or end with a specific string like "timing". There are two approaches to identifying and selecting columns that start or end a certain way. First, we can use the `.str.startswith()`, `.str.endswith()`, and `str.contains()` methods of the `.columns` attribute of a dataframe, and pass the result to the `.loc` attribute to extract the matching columns. To extract the columns that begin "ft", we write

# In[25]:


anes.loc[:, anes.columns.str.startswith('ft')]


# The issue here is that this call included the page timing columns, which we did not want, because these columns also begin with "ft". In addition, this approach does not enable us to include the features listed above. 
# 
# A second approach to selecting columns is technically more complicated, but offers a great deal more control over which columns are included in the edited data and which columns are not. This approach involves using a comprehension loop on the `.columns` attribute to extract the elements of this list that match given patterns. The individual elements of `.columns` are strings on which `.startswith()`, `.endswith()`, and `.contains()` apply. The comprehension loop allows us to use these methods in logical statements that determine whether each element is included or excluded in the new list.
# 
# For example, 
# ```
# [x for x in anes.colummns]
# ```
# generates a list of all 900 column names in the `anes` dataframe. But we can use `if` to place conditions on which names are included in the list. If we type
# ```
# [x for x in anes.colummns if x.startswith("ft")]
# ```
# then names in `anes.columns` are included only if it is true that they start with "ft". However, that condition also captures the metadata columns we don't want that begin with "ft" and end with "timing" or "skp". We can exclude these columns by using `not` clauses in the logical condition as follows:

# In[26]:


ftcols = [x for x in anes.columns if x.startswith("ft") and not x.endswith("timing") and not x.endswith("skp")]
ftcols


# To append two lists together, we simply add them together. Here we can append the `mycols` list defined above to the `ftcols` list to create a comprehensive list of all the columns we want to extract from `anes`, and we can create a new variable named `anes_clean` that contains only these columns:

# In[27]:


anes_clean = anes[mycols + ftcols]
anes_clean


# A related method is choosing which columns in a dataframe to drop, instead of which columns to keep. This technique is useful when we want to keep most of the columns, and it is easier to specify the few columns we want to drop. The method to drop columns is `.drop()`, applied to a dataframe. There are two ways to use this method. First,
# ```
# df = df.drop(colstodrop, axis=1)
# ```
# where `colstodrop` is a vector of column names for the columns we want to drop. Alternatively, we can write
# ```
# df.drop(colstodrop, axis=1, inplace=True)
# ```
# These two versions of the command have the same effect of dropping the columns defined in `colstodrop` and overwriting the Python variable for the dataframe with the new version. `axis=1` specifies that the names refer to columns to be dropped, in contrast to `axis=0` which would refer to rows. `inplace=True` provides an equivalent to `df = `. Either approach is fine, although I tend to avoid using `inplace=True` so that the code is more consistent. To delete the `inputstate` column from `anes_clean`, we type

# In[28]:


anes_clean = anes_clean.drop('inputstate', axis=1)


# If we wanted to drop multiple columns, we would write a list of the column names we want to drop in the first argument.
# 
# There are many ways to rename the columns in a dataframe, including assigning a list of new column names to the `.columns` attribute of a dataframe. I do not recommend that approach, however, because it requires an entry for every column and it requires these names to be written in exactly the same order as the existing columns, or else the data will be corrupted. Instead, use the `.rename()` method. This method does not require us to think about the left-to-right order of the columns, and it allows us to rename only a few columns without worrying about the ones we do not want to rename. To use this method, specify two parameters: first a dictionary that contains elements in the form of `'oldname':'newname'`, and second `axis='columns'` or `axis=1` to work with columns. 
# 
# To rename some of the columns in `anes_clean`, I use the following code:

# In[29]:


anes_clean = anes_clean.rename({'particip_3':'protest',
                                'vote20jb':'vote',
                                'mip':'most_important_issue',
                                'ideo5':'ideology',
                                'pid7':'partyID',
                                'guarinc':'universal_income',
                                'famsep':'family_separation',
                                'freecol':'free_college',
                                'loans':'forgive_loans',
                                'gender':'sex',
                                'educ':'education'}, axis=1)
anes_clean


# ## Working with Categorical Features
# ### Recoding a Single Categorical Column
# The ANES uses numeric codes to represent both ordinal and nominal (unordered) categorical features. That cuts down on the memory size of the data file (storing `2` is smaller than storing `Trump`), but it also makes it so we can't really understand what the individual datapoints represent. For example, here's a frequency table of the values of `vote`:

# In[30]:


anes_clean.vote.value_counts()


# According to the codebook, these values mean
# * 1 - Donald Trump
# * 2 - Joe Biden
# * 3 - Someone else
# * 4 - Probably will not vote
# 
# It would be much better to replace the numeric datapoints with these labels so that we can better understand the data we see. Carefully replacing the numbers with text will keep us from potentially confusing which number stands for which category. Also, if we want to construct any tables or graphs, it's much better to display the text labels than the numeric codes. Replacing the numeric codes with text for the categorical labels is a two step process:
# 
# 1. Create a dictionary in which the keys are existing values we want to recode, and the values are the new labels we want to replace these categories with.
# 
# 2. Use the `.map()` method on the column of interest to apply the mapping defined by the dictionary to the data.
# 
# An alternative method is `.replace()` as applied to the entire dataframe, but `.map()` tends to be [much faster](https://stackoverflow.com/questions/41985566/pandas-replace-dictionary-slowness) than `.replace()`. For example, to put the text labels onto the `vote` column, we can first define the following dictionary, then we can apply it to the data:

# In[31]:


replace_map = {1:'Donald Trump', 
               2:'Joe Biden', 
               3:'Someone else', 
               4:'Probably will not vote'}
anes_clean.vote = anes_clean.vote.map(replace_map)
anes_clean.vote


# One drawback of `.map()` compared to `.replace()` is that *all* of the categories must be replaced. If only some categories need to be recoded and a dictionary only lists the categories to replace, then `.map()` replaces all of the unlisted categories with missing values, while `.replace()` leaves these categories as they are.
# 
# This method can also be used to collapse categories into a smaller number of categories and can be used to replace numeric codes that represent missing values with codes recognized as missing by Python. To combine categories, we set existing values to the same label. To turn some categories to missing values, we set those categories equal to `np.nan`. 
# 
# Take `ideology`, for example. According to the codebook, the values of this feature mean
# * -7 - No answer
# * 1 - Very liberal
# * 2 - Liberal
# * 3 - Moderate
# * 4 - Conservative
# * 5 - Very conservative
# * 6 - Not sure
# Suppose that we want to label these categories in a way that combines categories 1 and 2 to be "Liberal", sets category 3 as "Moderate", combines categories 4 and 5 to be "Conservative", and replaces categories -7 and 6 with missing values.  We can do so with the following dictionary:

# In[32]:


replace_map = {-7:np.nan, 1:'Liberal', 2:'Liberal', 3:'Moderate', 
               4:'Conservative', 5:'Conservative', 6:np.nan}
anes_clean.ideology = anes_clean.ideology.map(replace_map)
anes_clean.ideology


# ### Recoding Many Categorical Columns At Once
# To label the categories of many features, the simplest code defines a dictionary in which each feature to be recoded is a key and the mapping dictionary for that feature is the value. Then we can pass this entire dictionary to the whole dataframe with `.replace()`. This approach might take longer than defining a loop that uses `.map()` on each of these columns (`.map()` is only defined for series and not for dataframes), but using `.replace()` here is more intuitive and elegant. 
# 
# We can recode all the remaining categorical features in the ANES data as follows:

# In[33]:


replace_map = {'liveurban':{1:'Rural', 2:'Town', 3:'Suburb', 4:'City'},
              'vote16':{-1:'Did not vote', 1:'Donald Trump', 2:'Hillary Clinton', 3:'Someone else'},
              'protest':{1:True, 2:False},
              'confecon':{1:'Not at all worried', 2:'A little worried', 3:'Moderately worried', 4:'Very worried', 5:'Extremely worried'},
              'partyID':{-7:np.nan, 8: np.nan, 1:'Democrat', 2:'Democrat', 3:'Democrat', 4:'Independent', 5:'Republican', 
                         6:'Republican', 7:'Republican'},
              'universal_income':{1:'Favor a great deal', 2:'Favor a moderate amount', 3:'Favor a little', 4:'Neither favor nor oppose', 
                                  5:'Oppose a little', 6:'Oppose a moderate amount', 7:'Oppose a great deal'},
              'family_separation':{-7:np.nan, 1:'Favor strongly', 2:'Favor somewhat', 3:'Neither favor nor disagree',
                                   4:'Oppose somewhat', 5:'Oppose strongly'},
               'free_college':{-7:np.nan, 1:'Favor a great deal', 2:'Favor a moderate amount', 3:'Favor a little', 
                               4:'Neither favor nor oppose', 5:'Oppose a little', 6:'Oppose a moderate amount', 7:'Oppose a great deal'},
               'forgive_loans':{-7:np.nan, 1:'Favor a great deal', 2:'Favor a moderate amount', 3:'Favor a little', 
                               4:'Neither favor nor oppose', 5:'Oppose a little', 6:'Oppose a moderate amount', 7:'Oppose a great deal'},
               'race':{1:'White', 2:'Black', 3:'Hispanic', 4:'Other', 5:'Other', 6:'Other', 7:'Other', 8:'Other'},
               'sex':{1:'Male',2:'Female'},
               'education':{1:'No HS diploma', 2:'High school graduate', 3:'Some college', 4:'2-year degree', 
                            5:'4-year degree', 6:'Post-graduate'}}
anes_clean = anes_clean.replace(replace_map)


# To apply the same recoding dictionary to many columns in the dataframe, first generate a list of the column names that share the dictionary. Then pass that list to the dataframe index to select those columns. Finally, apply the `.replace()` to this dataframe, inputting the dictionary for the shared recoding instructions. For example, for all of the feeling thermometer features in the data, various types of non-response are coded as -1, -7, and 997. I want to apply the dictionary
# ```
# {-1:np.nan, -7:np.nan, 997:np.nan}
# ```
# to every feeling thermometer feature in the data. If all of the values are to be recoded to the same single (missing) value, a shortcut is to pass to `.replace()` a list of the values to be recoded and `np.nan`. So we can equivalently write
# ```
# .replace([-1, -7, 997], np.nan)
# ```
# First we can generate a list of these columns, then we pass it to the dataframe. Then we apply `.replace()` to this selection: 

# In[34]:


ftcols = [x for x in anes_clean.columns if x.startswith("ft")]
anes_clean[ftcols] = anes_clean[ftcols].replace([-1, -7, 997], np.nan)


# All of the features in the data have now been recoded:

# In[35]:


anes_clean


# ### Dealing With Missing Data
# 
# After recoding, we are left with quite a few missing values in the data. To generate a logical matrix that indicates for every cell whether the datapoint is missing or not, we can use `anes_clean.isnull()`. To delete every row that has even one missing value, we can use `anes_clean.dropna()`. That's a heavy-handed treatment of missing data, however, that can severely reduce sample size and can lead to biases in analytical results of datapoints are missing not at random. There are much better treatments for missing data, called **imputation** methods. Many methods for missing data imputation are implemented in the [scikit-learn package](https://scikit-learn.org/stable/modules/impute.html).
# 
# One application of the `isnull()` method is to replace missing values with known values if those values are available elsewhere. For example, the ANES asked two versions of the feeling thermometer for immigrants. A respondent is only asked one of the two questions, so one of `ftimmig1` and `ftimmig2` is missing:

# In[36]:


anes_clean[['ftimmig1','ftimmig2']]


# We can create a new column called `ftimmig` and set it equal to `ftimmig1`. Then we can subset this column to just the rows for which `ftimmig1` is missing by typing
# ```
# anes_clean.ftimmig[anes_clean.ftimmig1.isnull()]
# ```
# We can then set these values equal to `ftimmig2` for the same subset where `ftimmig1` is missing:

# In[37]:


anes_clean['ftimmig'] = anes_clean.ftimmig1
anes_clean.ftimmig[anes_clean.ftimmig1.isnull()] = anes_clean.ftimmig2[anes_clean.ftimmig1.isnull()]
anes_clean[['ftimmig','ftimmig1','ftimmig2']]


# Now that we have created `ftimmig`, we can drop `ftimmig1` and `ftimmig2`:

# In[38]:


anes_clean = anes_clean.drop(['ftimmig1','ftimmig2'], axis=1)


# ### Why Recoding Categorical Data is Dangerous
# Before we move on to another topic, there are three reasons why **recoding categorical data is one of the most dangerous tasks in data manipulation**.  
# 
# First, it is very easy here to mistakenly place the wrong labels on categories. If we make an error here, Python will not inform us of the error. It is important to read the codebook carefully and make certain that the categories are labeled correctly. For example, suppose I want to study the effect of attending a political protest on voters' preferences and beliefs. The ANES data contains a feature that reports whether or not each individual has attended a political protest in the last year. The value 1 means that the person attended a protest, and the value 2 means that the person did not attend a protest. If we mix up these labels, then any analysis that uses the protest feature will not only be wrong - it will generate results that are exactly the opposite of the truth. Suppose that people who attend a protest are 20% more likely to vote in the upcoming election than people who have not attended a protest. If we mislabel the protest categories, the result would suggest that people who attend a protest are 20% *less* likely to vote, and this result will have the same level of uncertainty as the truth. Imagine if these data came from a drug trial: if we mislabel the treatment and control groups, we would conclude that a drug that benefits patients harms those patients, or vice versa. 
# 
# Second, we have an opportunity to change the data in significant ways while recoding categories. These changes might be the correct ones to make, but it is important to be extremely transparent with all of the changes as they can impact the results of any subsequent analysis. For example, the party identification feature in the ANES data is coded as
# * 1 - Strong Democrat
# * 2 - Not very strong Democrat
# * 3 - Independent, closer to Democrats
# * 4 - Independent
# * 5 - Independent, closer to Republicans
# * 6 - Not very strong Republican
# * 7 - Strong Republican
# 
# For my purposes I choose to recode this feature as having three categories, Democrat, Republican, and independent. But to do so, I have to choose how exactly to collapse categories. I choose to combine "Strong Democrat", "Not very strong Democrat", and "Independent, closer to Democrats" into a category named "Democrat", and "Strong Republican", "Not very strong Republican", and "Independent, closer to Republicans" into a category named "Republican". I leave "Independent" as it is. There is not an unambiguously correct way to perform this recoding: maybe the two leaning-independent categories should be grouped within "Independent" instead. I recode the feature in this way because I theorize that many people in the survey will declare themselves to be independent, but really behave more like Democrats or Republicans. Even though I have a reason for choosing my coding scheme, it is a decision that can change any analysis that uses party identification. Maybe the results would be very different if we expanded the independent category. 
# 
# Third, if the categories for a feature can be aligned in a meaningful order, we have a choice about whether to treat this feature as categorical or as numeric. If we treat the feature as categorical, then we label each number. That's useful especially for generating visualizations in which this feature comprises an axis. If we treat the feature as numeric, we leave the numbers as they are (while ensuring that the categories are in the right order). That's useful if we want to report statistics like the mean and variance, and we believe that these statistics have meaning for the ordered scale. For features like `universal_income` in the ANES data, the categories represent degrees of support for a policy. If we label the categories, we see clearly how many people adopt each nuanced position on the spectrum between support and non-support. If we leave the categories as numbers, we can report the average level of support on the 7-point scale. Whether to label the categories of an ordered categorical feature or leave them as numeric should therefore depend on the problems the feature will be applied to.

# ## Sorting Rows
# Sorting is a largely cosmetic thing to do because most analyses don't use the ordering of the rows to generate results. That said, especially in the early data cleaning stages of an analysis, it can be very useful to sort the rows of a dataframe according to the values in one or more columns, especially if the data contain an ID with a clear alphabetic or numeric order, like country names or time.
# 
# To sort, use the `.sort_values()` method. Within the method, use the `by` argument to specify the column you want to sort by. By default, sorting is done in ascending order for numeric features and in alphabetical order for string features, To save the sorting, either write `inplace=True` or re-assign the sorted dataframe to the same variable. `.sort_values()` will always put rows that have missing values for the sorting column at the bottom of the dataframe. 
# 
# For example, to sort by lowest to highest ratings of Donald Trump, we can type:

# In[39]:


anes_clean.sort_values(by = 'fttrump')


# To sort in descending order from the highest to lowest values of `fttrump`, we can use the `ascending=False` parameter:

# In[40]:


anes_clean.sort_values(by = 'fttrump', ascending=False)


# We can also sort the rows by the values of more than one column. When we do that, the second (and third, and so on) column is only used to break the ties of the first (and second, etc.) column. All we have to do is write more than one column name in a list, and pass that list to the `by` argument of `.sort_values()`. The `ascending` argument also takes a list of `True` or `False` values to denote whether each of the columns should be sorted in ascending or descending order. To sort the rows in ascending order by values of the Donald Trump thermometer, while breaking ties by descending order of the Joe Biden thermometer, we can type:

# In[41]:


anes_clean.sort_values(by=['fttrump', 'ftbiden'], ascending = [True, False])


# ## Filtering Rows
# Filtering is the task of keeping or deleting rows based on a logical condition. Prior to discussing the code for filtering, let's review logical operators. Every logical statement returns a value of `True` or `False` in Python, and these statements are useful for keeping rows for which a condition is `True` and deleting rows for which a condition is `False`. 
# 
# Python has the following logical operators:
# 
# * `==` "is equal to"
# 
# * `!=` "is not equal to"
# 
# * `>` "is greater than"
# 
# * `>=` "is greater than or equal to"
# 
# * `<` "is less than"
# 
# * `<=` "is less than or equal to"
# 
# * `in` "is in the list"
# 
# * `not in` "is not in the list"
# 
# It also has the following symbols to *connect* logical statements to build more complicated statements:
# 
# * `&` "and" (both conditions must be true for the whole statement to be true)
# 
# * `|` "or" (at least one of the conditiona must be true for the whole statement to be true)
# 
# * `not` turns `True` results to `False`, and vice versa
# 
# * `(` and `)` (parentheses work with logic the way they do with algebra -- consider this part of the statement first)
# 
# There are many ways to filter the rows in a dataframe based on a logical condition, but the best method is `.query()` because of its notational ease and because it allows **chaining**: that is, specifying many logical conditions with repeated calls to `.query()`. Chaining is another way to express "and" in a combined logical statement. To use `.query()`, type it as a method applied to the dataframe in question, and put the logical condition in double quotes - that allows us to use single quotes within the query. For example, to see just the Joe Biden voters, type:

# In[42]:


anes_clean.query("vote=='Joe Biden'")


# To keep the rows for people that will vote for Joe Biden, but rate him less than 40:

# In[43]:


anes_clean.query("vote=='Joe Biden' & ftbiden < 40")


# Or alternatively,

# In[44]:


anes_clean.query("vote=='Joe Biden'").query('ftbiden < 40')


# Who in their right mind would rate Joe Biden 100 and Trump 100? These 6 people!

# In[45]:


anes_clean.query("ftbiden == 100 & fttrump == 100")


# I want to see all of the voters that are extremely worried about the economy and either live in rural areas or were born prior to 1950:

# In[46]:


anes_clean.query("confecon == 'Extremely worried' & (liveurban == 'Rural' | birthyr < 1950)")


# ## Creating New Columns and Replacing Existing Columns
# ### Using Arithmetic Operations
# There are many situations in which it makes sense to create new columns based on calculations with existing columns. There are two methods for  creating a new column or replace an existing one. The first approach is to define a new column name in a dataframe's index, and assign it to new values constructed from existing values in the dataframe.
# 
# For example, we can create a column that represents the difference between the Biden thermometer and the Trump thermometer, so that negative values (up to -100) represent partisanship for Trump, and positive values (up to 100) represent partisanship for Biden. We can either create a new column that contains these differences, or we can replace an existing column with this new column. To create a new column called `partisanship`, we can type:

# In[47]:


anes_clean['partisanship'] = anes_clean.ftbiden - anes_clean.fttrump
anes_clean[['ftbiden', 'fttrump', 'partisanship']]


# The second approach is to use the dataframe's `.assign()` method. Within `assign()`, we write the name of the column we are creating, and we set it equal to an arithmetic or logical expression involving existing columns. The equivalent code that creates a `partisanship` column using the `.assign()` method is:

# In[48]:


anes_clean = anes_clean.assign(partisanship = anes_clean.ftbiden - anes_clean.fttrump)
anes_clean[['ftbiden', 'fttrump', 'partisanship']]


# To replace an existing column with a new version of that column, we use the same syntax, but we write an existing column name to set equal to an expression. For example, to replace the Barack Obama feeling thermometer with a Z-score standardized version of this column (subtracting the mean and dividing by the standard deviation) so that the values of `ftobama` change to represent the number of standard deviations away from the mean of `ftobama`. We can type

# In[49]:


obama_mean = anes_clean.ftobama.mean()
obama_sd = anes_clean.ftobama.std()
anes_clean['ftobama'] = (anes_clean.ftobama - obama_mean)/obama_sd
anes_clean[['ftbiden', 'fttrump', 'ftobama']]


# Then we can reconstruct the original `ftobama` feature:

# In[50]:


anes_clean['ftobama'] = anes_clean.ftobama*obama_sd + obama_mean
anes_clean[['ftbiden', 'fttrump', 'ftobama']]


# We can also perform both tasks using `.assign()`. We can replace `ftobama` with a standardized version of the feature:

# In[51]:


anes_clean = anes_clean.assign(ftobama = (anes_clean.ftobama - obama_mean)/obama_sd)
anes_clean[['ftbiden', 'fttrump', 'ftobama']]


# Then we can reconstruct the original values of `ftobama`:

# In[52]:


anes_clean = anes_clean.assign(ftobama = anes_clean.ftobama*obama_sd + obama_mean)
anes_clean[['ftbiden', 'fttrump', 'ftobama']]


# ### Breaking Continuous Features into Categories
# A useful function in `pandas` is `pd.cut()` which creates categories from break points in a continuous-valued column. There are three arguments for `pd.cut()`: first, the continuous column whose values we want to categorize, second `bins` takes either an integer to express the number of uniformly spaced categories, or a list of the breakpoints (inclusive for the upper bound but not the lower bound), and `labels` is a tuple of the labels to assign to each category. To cut the `ftbiden` column into three categories, we can write

# In[53]:


anes_clean['ftbiden_level'] = pd.cut(anes_clean.ftbiden, bins=[-0.1,40,70,100], labels=("dislike", "neutral", "like"))
anes_clean[['ftbiden', 'ftbiden_level']]


# Or equivalently,

# In[54]:


anes_clean = anes_clean.assign(ftbiden_level = 
                               pd.cut(anes_clean.ftbiden, 
                                      bins=[-0.1,40,70,100], 
                                      labels=("dislike", "neutral", "like")))
anes_clean[['ftbiden', 'ftbiden_level']]


# ### Indexing Versus `.assign()`
# The advantage of using `.assign()` as opposed to writing new columns into the dataframe's index is that we can create or replace multiple columns within one call to `.assign()` by separating each expression with commas. We can calculate `age` from `birthyr` and we can also generate a column containing the square of age (which is useful to place a curvilinear effect into a linear regression model): 

# In[55]:


anes_clean = anes_clean.assign(age = 2020 - anes_clean.birthyr,
                              age2 = (2020 - anes_clean.birthyr)**2)
anes_clean[['vote', 'ftbiden', 'fttrump', 'age', 'age2']]


# A warning: if you want to perform a calculation that uses a column you create, you must create the columns you will use first, then use them in a separate call to `.assign()`. Suppose that I had called `age` directly to create `age2` as follows:
# ```
# anes_clean.assign(age = 2020 - anes_clean.birthyr,
#                   age2 = anes_clean.age**2)
# ```
# This code will not work because `age` is not yet defined until the end of the entire call to `.assign()`, so it cannot be used to create `age2`.
# 
# ### Changing a Column's Data Type
# One important way we might need to create a new column or revise an existing one is by **casting** the column to a different data type. Every column in the dataframe has a data type, which we can see listed with the `.dtypes` attribute. If we want to change the data type, we can use the `.astype()` method applied to the column whose type we want to change. To convert the column's values to strings type `.astype('str')`, to convert the column's values to integers type `.astype('int')`, and to convert the column's values to floats type `.astype('float')`. `pandas` also recognizes a categorical data type, and to convert a column to categorical type `.astype('category')`. As an example, let's convert the Joe Biden thermometer scores to each data type:

# In[56]:


anes_clean = anes_clean.assign(ftbiden_float = anes_clean.ftbiden.astype('float'),
                              ftbiden_cat = anes_clean.ftbiden.astype('category'),
                              ftbiden_str = anes_clean.ftbiden.astype('str'))
anes_clean[['ftbiden', 'ftbiden_float', 'ftbiden_cat', 'ftbiden_str']].dtypes


# By default, missing values `np.nan` are stored as floats, so it is not possible to convert a column to integer if there are missing values.
# 
# We can convert all of the categorical columns in `anes_clean` to categorical data types as follows:

# In[57]:


catcolumns = ['liveurban', 'vote16', 'protest', 'vote','confecon', 'ideology', 'partyID',
       'universal_income', 'family_separation', 'free_college','forgive_loans', 'race', 'sex', 'education']
anes_clean[catcolumns] = anes_clean[catcolumns].astype('category')
anes_clean.dtypes


# ### Using Logical Operators
# Logical expressions can be used to create new columns. Columns that are set equal to a logical condition are populated by values that are either `True` when the logical condition is true, or `False` when the logical condition is false. To create a binary column indicating the participants who like Biden more than Trump, we can type

# In[58]:


anes_clean['prefersbiden'] = anes_clean.ftbiden > anes_clean.fttrump
anes_clean[['vote','ftbiden', 'fttrump', 'prefersbiden']]


# Or using `.assign()`:

# In[59]:


anes_clean = anes_clean.assign(prefersbiden = anes_clean.ftbiden > anes_clean.fttrump)
anes_clean[['vote','ftbiden', 'fttrump', 'prefersbiden']]


# Logical expressions can work in two ways: **elementwise** or **objectwise**. When a logical expression is evaluated elementwise, it matches the corresponding elements in multiple columns and returns a column of equal length that is populated by `True` and `False` values depending on the values on the same row. When a logical expression is evaluated objectwise, it considers whether a statement is true regarding a column as a whole. For example, the `==` sign asks whether the first object is equal to the second object. If I define two lists, `[1,2,3]` and `[3,2,1]` and evaluate them using `==`, I get:

# In[60]:


[1,2,3] == [3,2,1]


# The output is false because `[1,2,3] == [3,2,1]` is evaluated *objectwise*. The question Python answered was: is the list `[1,2,3]` the same as the list `[3,2,1]`? These two lists are not the same, so the answer is `False`. If we convert these two lists to `numpy` arrays instead, then the same comparison is *elementwise*:

# In[61]:


np.array([1,2,3]) == np.array([3,2,1])


# In this case, we compare corresponding elements and find that the first elements are not the same, the second elements are the same, and the third elements are not the same, so the answer is a list: `[False, True, False]`. Because `pandas` dataframes are built using `numpy` under the hood, individual columns are `numpy` arrays, and some logical operators - namely `<`, `<=`, `>`, `>=`, `~`, `&`, and `|` - work elementwise. That's why the commands listed above to generate Boolean features in `anes_clean` work. 
# 
# However, some operators do not work elementwise, even within `numpy` arrays. Python includes two versions of "and", for example: in addition to `&`, there is also `and`. While `&` works elementwise, `and` only works objectwise. For example the following expression

# In[62]:


(np.array([1,2,3,4]) >= np.array([4,3,2,1])) & (np.array([1,2,3,4]) == np.array([5,4,3,2]))


# yields an array of logical values, but switching the "and" operator:
# ```
# (np.array([1,2,3,4]) >= np.array([4,3,2,1])) and (np.array([1,2,3,4]) == np.array([5,4,3,2]))
# ```
# yields an error: "The truth value of an array with more than one element is ambiguous. Use a.any() or a.all()". The only really important logical operator we will want to use that does not work elementwise in `pandas` is `in`. To create a new column that uses an objectwise operator like `in`, we have to loop across the rows of the dataframe using the `.apply()` method and a `lambda` function. `lambda` defines the operation that will be evaluated on each row, and constructs the sequence of logical values one row at a time. Using a loop is computationally inefficient, but it gets the job done. 
# 
# For example, if we want to create the `worried_econ` column using `in`, we can use the following code:

# In[63]:


anes_clean['worried_econ'] = anes_clean.confecon.apply(
        lambda x: x in ["Moderately worried","Extremely worried"]
    )
anes_clean[['confecon', 'worried_econ']]    


# The first line creates the `worried_econ` column and sets it equal to the output of the loop that is applied to the rows of `confecon`. Inside the loop, `lambda x` defines `x` as an index that represents each individual row. The function `x in ["Moderately worried","Extremely worried"]` returns `True` if the value of `confecon` on a particular row is "Moderately worried" or "Extremely worried" and `False` otherwise.
# 
# As another example, let's create a column that identifies the voters that favor a universal basic income, at least a little, and also favor free college tuition. In this case, we have to specify that `axis=1` so that the loop works down columns and applies the function on every row in the dataframe. The following code works:

# In[64]:


anes_clean['favor_both'] = anes_clean.apply(
    lambda x: x['universal_income'] in ["Favor a little","Favor a moderate amount","Favor a great deal"] and
    x['free_college'] in ["Favor a little","Favor a moderate amount","Favor a great deal"],
    axis=1
)
anes_clean[['universal_income', 'free_college', 'favor_both']]


# ## Data Aggregation
# Data aggregation is the process of collapsing a dataframe to have one row for every group of a given categorical column, where other columns are summarized with statistics like the sum, mean, and median of values within each group. In `pandas`, data aggregation follows a **split-apply-combine** approach. First, the data are split into subsets for every group in the grouping column. Then a function, such as the mean, is applied to the same columns in each subset and each subset is compressed to have just one row. Then the subsets are combined into the final resulting dataframe.
# 
# The general syntax for aggregating a dataframe is
# ```
# df.groupby('groupcolumn').aggfunctions.sort_values()
# ```
# 
# Commands to aggregate dataframes can get confusing very quickly. It helps to break down the syntax for data aggregation into parts for each method listed in the syntax. First, `df` is the name of the dataframe we want to compress. Second, `.groupby('groupcolumn')` specifies the column whose categories will define the rows of the aggregated dataframe. If more than one column defines these groups (examples below), then the syntax becomes `.groupby(['groupcolumn1', 'groupcolumn2'])`. Third, `.aggfunctions` defines how other columns in the data can be included and summarized in the aggregated data. Finally, `.sort_values()` is optional, but often helps to generate a better presentation for the aggregated data table.
# 
# As an example, let's collapse the ANES data by the candidates that people report they will vote for. We start with `anes_clean` and set the grouping variable with `.groupby('vote')`. We apply the `.size()` function, which reports the number of rows in each group, and we use `.sort_values(ascending=False)` to list these counts from biggest to smallest (no `by` argument is needed because there is only one column in the aggregated data). In all, this command provides a tally of people's voting intentions as of December 2019:
# 

# In[65]:


anes_clean.groupby('vote').size().sort_values(ascending=False)


# So according to the ANES data, the election is close, but Joe Biden has the most votes in the sample.
# 
# To use aggregation functions other than `.size()`, the best option is to use the `.agg()` method instead. `.agg()` takes a dictionary as its argument, and this dictionary should contain the names of the columns we want to summarize, as keys, and the functions we want to use to collapse these columns, as values. For example, we can construct a table in which the rows are the voting groups, and the columns contain the mean feeling thermometers for Trump, Biden, immigrants, and journalists:

# In[66]:


anes_clean.groupby('vote').agg({'fttrump':'mean',
                               'ftbiden':'mean',
                               'ftimmig':'mean',
                               'ftjournal':'mean'})


# There are aggregation functions other than `'mean'` available: `count` gives the number of nonmissing values within the group, `sum` takes the sum of the values in each group, `min` and `max` report the minimum and maximum values, `median` reports the 50th percentile, `std` and `var` calculate the standard deviation and variance, `sem` takes the standard error of the mean, and `first` and `last` report the first and last value that appear in the subset defined by each group. For example, we can report all of these statistics for `ftbiden` across voting groups. If we want more than one statistic for a column, we can specify all of these functions in a list within the dictionary as follows:

# In[67]:


anes_clean.groupby('vote').agg({'ftbiden':['count','mean','sum','min','max','median','std','var','sem','first','last']})


# More than one column may define the groups. For example, we might want to count the number of voters for each candidate in cities, in rural areas, in suburbs, and in towns. In that case, we can specify `groupby(['vote','liveurban'])` and `.size()` to count the number of voters of each type:

# In[68]:


anes_clean.groupby(['vote','liveurban']).size()


# This table looks nicer as a `pandas` dataframe:

# In[69]:


pd.DataFrame(anes_clean.groupby(['vote','liveurban']).size())


# The table looks even nicer if we also apply the `.unstack()` method to move the data into different columns:

# In[70]:


pd.DataFrame(anes_clean.groupby(['vote','liveurban']).size().unstack())


# Biden has more voters than Trump in cities, and Trump has more in rural areas. Trump has a slight lead among people in towns, and Trump and Biden are within three votes among people in suburbs. It looks like the election will depend on voters from the suburbs.
# 
# The standard functions in `.agg()` will usually suffice, but there are situations in which we might want to use a custom aggregation function. For that, we can use `.apply()` and a `lambda` function. The following code searches the `most_important_issue` column, which is a free text entry field in which respondents wrote their answer for the most important issue in the country today, and counts the number of times the word "trump" is mentioned in these responses:

# In[71]:


anes_clean.groupby('vote').most_important_issue.apply(
    lambda x: x.str.contains("trump", case=False).sum()
).sort_values(ascending=False)


# Biden voters mentioned "trump" 325 times, and Trump voters only mentioned "trump" 59 times. This code groups by voting group, then selects the `most_important_issue` column and uses the `.apply()` method on this column which creates a loop across groups. Within `.apply()`, the `lambda` function denotes a token `x` that represents the `most_important_issue` column within each group. On this column, the function uses the `.str.contains("trump", case=False)` function, which outputs `True` if the string "trump" is found within each value of `most_important_issue` without case sensitivity, and `False` otherwise. Finally,the `.sum()` function counts the number of times these searches were `True`.

# Finally, we can save the cleaned ANES data as a separate CSV:

# In[72]:


anes_clean.to_csv('anes_pilot2019_clean.csv', index=False)

