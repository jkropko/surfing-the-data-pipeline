#!/usr/bin/env python
# coding: utf-8

# # Database Queries

# ```{contents} Table of Contents
# :depth: 4
# ```

# ## Introduction: The History of the Structured Query Language (SQL)
# 
# <div style= "float:right;position: relative; padding: 10px">
# <a href="https://xkcd.com/1409/"><img src="https://imgs.xkcd.com/comics/query.png" width="400"></a>
# </div>
# 
# The structured query language (SQL) was invented by Donald D. Chamberlin and Raymond F. Boyce in 1974. Chamberlain and Boyce were both young computer scientists working at the IBM T.J. Watson Research Center in Yorktown Heights, New York, and they met E. F. Codd at a research symposium that Codd organized there. Codd, four years prior, had published the [seminal article that defined the relational model](https://www.seas.upenn.edu/~zives/03f/cis550/codd.pdf) for databases. Codd's relational model is defined using relational algebra and relational calculus, two notational standards that Codd himself created to elaborate on set theory as applied specifically to data tables. One important property of set theory is that highly abstract mathematical expressions can be expressed in plain language. For example, consider the set $A$ of holidays in the United States during which banks are closed:
# 
# $$ A = \{\text{New Year's Day}, \text{Birthday of Martin Luther King, Jr.}, \\  \text{Washington’s Birthday}, \text{Memorial Day}, \text{Independence Day}, \\  \text{Labor Day}, \text{Columbus Day}, \text{Veterans Day},  \\ \text{Thanksgiving Day}, \text{Christmas}\}$$
# 
# Also consider the set $B$ of holidays in the United Kingdom during which banks are closed:
# 
# $$ B = \{\text{New Year's Day}, \text{Good Friday}, \text{Easter Monday}, \\ \text{Early May bank holiday}, \text{Spring bank holiday}, \\\text{Summer bank holiday}, \text{Christmas}, \text{Boxing Day}\}$$
# 
# The intersection between sets $A$ and $B$ is a set that consists of all elements that exist with both set $A$ and set $B$:
# 
# $$ A \cap B = \{\text{New Year's Day}, \text{Christmas}\}$$
# 
# The notation $A\cap B$ is a mathematical abstraction of an idea that can be expressed in plain-spoken language: $\cap$ means "and", and $A\cap B$ means $A$ *and* $B$, or all elements that are in both $A$ *and* $B$. Put another way, $A\cap B$ is the set of all holidays during which banks are closed in both the United States *and* the United Kingdom. Likewise, every piece of set notation can be expressed semantically.
# 
# Although Codd laid out the broad parameters of the relational model in mathematical terms, he did not design software or a physical architecture for a relational database. He explicitly left that work up to future research:
# 
# > Many questions are raised and left unanswered. For example, only a few of the more important properties of the data sublanguage . . . are mentioned. Neither the purely linguistic details of such a language nor the implementation problems are discussed. Nevertheless, the material presented should be adequate for experienced systems programmers to visualize several approaches (p. 387).
# 
# Chamberlin and Boyce took up the challenge of writing a programming language to implement Codd's relational model. [As Chamberlin explains](https://ieeexplore.ieee.org/document/6359709), their primary goal was to create a version of Codd's set-theoretical relational model that could be expressed in plain language:
# 
# > The more difficult barrier was at the semantic level. The basic concepts of Codd's languages were adapted from set theory and symbolic logic. This was natural given Codd's background as a mathematician, but Ray and I hoped to design a relational language based on concepts that would be familiar to a wider population of users (p. 78).
# 
# In short, the idea behind SQL is to implement Codd's abstract system of using logical statements with set theoretical notation to narrow down the specific records and features in a dataset that a user wishes to read or edit, but to phrase these operations in accessable, plain language. One of the best things about SQL is that once you are used to the language, it reads just like English. That said, Chamberlin admits that SQL "has not proved to be as accessible to untrained users as Ray and I originally hoped" ([p. 81](https://ieeexplore.ieee.org/document/6359709)).
# 
# Another benefit of SQL is that this language is one of the most universal programming languages in existence. It is designed to work with database management systems on any platform, and it works seamlessly within Python, R, C, Java, Javascript, and so on. While the standards for languages and platforms change, SQL has been in continuous use for relational database management since the 1980s and shows no sign of becoming antiquated or being replaced. The SQL syntax exists outside of any individual DBMS, and is maintained by the [American National Standards Institute (ANSI)](https://en.wikipedia.org/wiki/American_National_Standards_Institute) and the [International Organization for Standardization (ISO)](https://en.wikipedia.org/wiki/International_Organization_for_Standardization), two non-profit organizations that facilitate the development of [voluntary consensus standards](https://en.wikipedia.org/wiki/Standardization) for things like programming languages and hardware. Despite the universality of SQL, however, different DBMSs use slightly different versions of SQL, adding some unique functionality in some cases, and failing to implement the entire SQL standard in others. MySQL for example [lacks the ability to perform a full join](https://stackoverflow.com/questions/4796872/how-to-do-a-full-outer-join-in-mysql). PostgreSQL distinguishes itself from other RDBMSs by striving to implement as much of the global SQL standard as possible. While there some important differences in the version of SQL used by different DBMSs, the differences generally apply to very specific situations and all implementations of SQL use mostly the same syntax and can do mostly the same work. 

# ### Declarative and Procedural Languages
# 
# SQL is considered to be a [declarative language](https://en.wikipedia.org/wiki/Declarative_programming), which means that it defines the broad task that a particular computer system must carry out, but it does not define the mechanism through which the system completes the task. For example, SQL can tell a system to access two tables and join them together, but that command must tell a DBMS to access additional code that tells the system how exactly to search and operate on the rows and columns of each data table. A language that provides specific instructions to a system on how to carry out a task - by changing the system state in some way, including how the data exist in the system - is a [procedural language](https://en.wikipedia.org/wiki/Procedural_programming). The code that a procedural language uses to make these changes on the system is called [imperative code](https://en.wikipedia.org/wiki/Imperative_programming). A DBMS can be thought of as a function that takes declarative SQL code as an input, finds and runs the imperative code that carries out the declarative task, and returns the output. MySQL, for example, [uses imperative C and C++ code](https://dev.mysql.com/doc/refman/8.0/en/features.html) to carry out SQL queries.

# ### Popularity of SQL
# Common standards and the most popular programming languages and environments change all the time. It's an eternal struggle for data scientists as well as programmers of all kinds, and a matter of consistent anxiety. Presently, Python is the most widely used tool for data science, but will we all have to drop Python soon and [teach ourselves Julia](https://towardsdatascience.com/bye-bye-python-hello-julia-9230bff0df62)? 
# 
# In this context, it is stunning that SQL has been so widely used since the 1970s. According to a [Stack Overflow survey](https://insights.stackoverflow.com/survey/2017), SQL is the one of most widely used programming languages among the people who filled out the survey, second only to Javascript. Taking into account the high-tech biases in this specific sample, it is probably the case the SQL is more widely used than any other language mentioned in this survey. What accounts for this popularity?
# 
# This [blog post](https://blog.sqlizer.io/posts/sql-43/) argues that SQL achieved this level of longevity because it came to prominence during a time in which many of the baseline standards for the development of computer systems were being invented. As more and more systems were developed in a way that depends on SQL, it became harder to change this standard. But SQL is also simple and highly functional because it is a semantic language that expresses set-theoetical and logical operations. As long as relational databases are used, there's not much functionality that can be added to a query language beyond these foundational mathematical operations, and whatever additional functionality is needed can be added to a version of SQL by a particular DBMS. There are also many different open source and proprietary DBMSs that all employ SQL, so different users can have a choice over many different DBMSs and platforms without having to learn a query language other than SQL.
# 
# That said, there's much less of a reason to use SQL when the database is not organized according to the relational model. NoSQL databases have much more flexible schema in general, and can store the data in one big table or in as many tables as there are records, or even datapoints, in the database. In fact, without a relational schema, the notion of a data table makes less sense in general. For example, a document store is a collection of individual records encoded using JSON or XML, and not as tables. These records can be sharded: stored in many corresponding servers in a distributed system to address challenges with the size of the database and the speed with which database transactions are conducted. Without tables, NoSQL DBMSs do not usually use SQL. MongoDB, for example, works with queries that are themselves in JSON format.

# ## Create, Read, Update, and Delete (CRUD) Operations
# **Persistent storage** refers to a system in which [data outlives the process that created it](https://en.wikipedia.org/wiki/Persistence_(computer_science)). When you work with software that allows you to save a file, the file is stored in persistent storage because it still exists even after you close the software application. Hard drives are examples of persistent storage, as are local and remote servers that store databases. Any persistent storage mechanism must have methods for creating, reading (or loading), updating (or editing), and deleting the data in that storage device. Create, Read, Update, and Delete are the CRUD Operations.
# 
# We've previously employed CRUD operations using the `requests` library to use an API or to do web scraping. Like `requests`, SQL and other query languages have CRUD operations. The following table, adapted from a similar one that appears on the [Wikipedia page for the CRUD operations](https://en.wikipedia.org/wiki/Create%2C_read%2C_update_and_delete), shows these operations in the `requests` package, SQL, and the MongoDB query language:
# 
# |Operation|`requests` method|SQL|MongoDB|
# |:-|:-|:-|:-|
# |Create|`requests.put()` or `requests.post()`|`INSERT`|`Insert`|
# |Read|`requests.get()`|`SELECT`|`Find`|
# |Update|`requests.patch()`|`UPDATE`|`Update`|
# |Delete|`requests.delete()`|`DELETE`|`Remove`|
# 
# As a data scientist, you will most often use read operations to obtain the data you need for your analysis. However, if you are collecting original data for your project, the create, update, and delete operations become much more important. We will discuss all four operations and their variants in the context of SQL and MongoDB below.
# 
# We can work with SQL using `pandas` if we first create an engine that links to a specific DBMS, server, and database with `create_engine` from `sqlalchemy`. Once we do, the `pd.read_sql_query()` function makes read operations straightforward, and the `.execute()` method applied to the engine lets us easily issue create, update, and delete commands.

# ## SQL Style: Capitalization, Quotes, New Lines, Indentation
# There are many ways to write an SQL query, and when you look at someone else's SQL code you will see a variety of styles. Mostly, with the exception of quotes in some cases, stylistic differences don't change the behavior of the code, but they can have an impact on how easy the code is for other people to read and understand.
# 
# One requirement for SQL code is that the query must end with a semi-colon, and that no semi-colons appear elsewhere in the query. As long as that requirement is met, other stylistic choices are possible.
# 
# The least readable way to write an SQL query is to write the entire code on one line, with no capitalization or indentation. The following code is valid SQL code:
# ```
# select t.id, t.column1, t.column2, t.column3, r.column4 from table1 t inner join table2 r on t.id = r.id where column1>100 order by column2 desc;
# ```
# We will discuss exactly what this query does. But for now, let's focus on the presentation of code. SQL uses **clauses** to represent particular functions for reading and writing data. In the above query, `select`, `from`, `inner join`, `on`, `where`, and `order by` are all clauses, and `desc` is an option applied to the `order by` clause. 
# 
# One stylistic choice many people make is to write SQL clauses in capital letters. That helps readers to quickly see the parts of the code that are clauses as opposed to the rest of the code that contains column names, table names, values, and aliases. If we capitalize the clauses and options in the SQL query, it looks like this:
# ```
# SELECT t.id, t.column1, t.column2, t.column3, r.column4 FROM table1 t INNER JOIN table2 r ON t.id = r.id WHERE column1>100 ORDER BY column2 DESC;
# ```
# Another stylistic choice people make to present the code in a more reabable way is to put clauses that are considered distinct enough from other clauses on new lines. The one common exception is `FROM`, which is considered to be closely related to `SELECT` and is often written on the same line as `SELECT`. If we put each clause other than `FROM` on a new line, the query looks like this:
# ```
# SELECT t.id, t.column1, t.column2, t.column3, r.column4 FROM table1 t 
# INNER JOIN table2 r 
# ON t.id = r.id 
# WHERE column1>100 
# ORDER BY column2 DESC;
# ```
# Some clauses are considered to be elaborations upon a previous clause. Column names after `SELECT` are usually written on the same line as `SELECT`, but if these columns themselves require functions that take up more space, it is useful to put them on new lines. Likewise, `ON` is considered an elaboration of `INNER JOIN`. These lines of code are often indented to express the dependence on the previous line. If we include indentation in the code, the query is
# ```
# SELECT 
#     t.id, 
#     t.column1, 
#     t.column2, 
#     t.column3, 
#     r.column4 
# FROM table1 t 
# INNER JOIN table2 r 
#     ON t.id = r.id 
# WHERE column1>100 
# ORDER BY column2 DESC;
# ```
# I encourage you to develop good habits with how you write the SQL queries, both for other people to read your code, but more importantly, to make it easier for you yourself to read your code. You will be spending a lot of time developing and debugging SQL queries, and anything you do that cuts down the time to understand your own code will save you a lot of time and frustration in the long-run.
# 
# Quotes are only used in SQL code when referring to values of a character feature in one of the data tables. When using quotes while working in Python, it is important to use single quotes, not double quotes, to ensure that the quote that is internal to SQL is not read as a termination of the Python variable that contains the SQL code. That is, it is fine to write a clause that looks like `WHERE column = 'value'`, but not `WHERE column = "value"`.
# 
# For all of the queries we will write in the following examples, we will store the query as a string variable in Python. We will use the triple-quote syntax, which allows us to write a string that exists on multiple lines. So our SQL query definitions will look like this:
# ```
# myquery = """
# SELECT 
#     t.id, 
#     t.column1, 
#     t.column2, 
#     t.column3, 
#     r.column4 
# FROM table1 t 
# INNER JOIN table2 r 
#     ON t.id = r.id 
# WHERE column1>100 
# ORDER BY column2 DESC;
# """
# ```
# We will then be able to pass the `myquery` variable to functions like `pd.read_sql_query()` to be evaluated.

# ## SQL Joins
# The simplest SQL commands for reading data from a database are `SELECT` and `FROM`. In module 6, we issued the following query to read the entire "reviews" entity from the wine reviews database:
# ```
# SELECT * FROM reviews
# ```
# But this query does not read data from the other entities in the database. It pulls all of the rows and columns from "reviews" and it does not manipulate the data within "reviews" in any way. That might not be the best way to create a dataframe to conduct analyses.
# 
# SQL read operations get data, but they can also clean data at the same time. Cleaning data is an important challenge. Even when the data are stored in a well-organized database, that organization might not be the right format for the data given the analyses we intend to do. "[Tidy Data](https://www.jstatsoft.org/article/view/v059i10)" by Hadley Wickham lays out a philosophy of what it means to clean a dataset. The goal is to put data into a format in which modeling and visualization is as easy as possible. There are two steps: first we create **tidy data** and then we manipulate the data to fit our specific needs. Tidy data is defined as follows:
# 
# > A dataset is messy or tidy depending on how rows, columns and tables are matched up with observations, [features] and types. In tidy data:
# > 1. Each [feature] forms a column.
# > 2. Each observation forms a row.
# > 3. Each type of observational unit forms a table (p. 2).
# 
# In other words, the dataset we will use in an analysis must exist in one table, the rows of the table must represent records (also called observations), the columns of the table must represent features, and the rows must represent comparable units. For example, if the data contain records from the 50 U.S. States, there should be a row for each state, and there should not be a row for regions or for the whole country as these units are not comparable to states. Data from a relational database are not generally in tidy format because the relevant data exists in multiple tables. The first step is to combine these tables into one dataset using **join** functions within SQL read operations. There are many different kinds of joins, and the easiest way to see the difference between these types is to see what they do to real data. 
# 
# Before we discuss specific examples of how to use SQL, we load the following libraries:

# In[1]:


import numpy as np
import pandas as pd
import sys
import os
import psycopg2
from sqlalchemy import create_engine
import dotenv


# ### Example Database: NFL and NBA Teams
# As an example, I create a PostgreSQL database that contains two tables: "nfl" contains the location and team name of all 32 NFL teams:

# In[2]:


nfl_dict = {'city':['Buffalo','Miami','Boston','New York','Cleveland','Cincinnati',
                       'Pittsburgh','Baltimore','Kansas City','Las Vegas','Los Angeles','Denver',
                       'Nashville','Jacksonville','Houston','Indianapolis','Philadelphia','Dallas',
                       'Washington','Atlanta','Charlotte','Tampa Bay','New Orleans','San Francisco',
                       'Phoenix', 'Seattle','Chicago','Green Bay','Minneapolis','Detroit'],
           'footballteam':['Buffalo Bills','Miami Dolphins','New England Patriots',
                           ['New York Jets', 'New York Giants'],'Cleveland Browns','Cincinnati Bengals',
                          'Pittsburgh Steelers','Baltimore Ravens','Kansas City Chiefs',
                           'Las Vegas Raiders',['L.A. Chargers','L.A. Rams'],'Denver Broncos',
                          'Tennessee Titans','Jacksonville Jaguars','Houston Texans',
                           'Indianapolis Colts','Philadelphia Eagles','Dallas Cowboys',
                           'Washington Skins','Atlanta Falcons','Carolina Panthers',
                           'Tampa Bay Buccaneers','New Orleans Saints', 'San Francisco 49ers',
                           'Arizona Cardinals','Seattle Seahawks','Chicago Bears',
                           'Green Bay Packers','Minnesota Vikings','Detroit Lions']}
nfl_df = pd.DataFrame(nfl_dict)
nfl_df


# This table is not in first normal form because the data are non-atomic (two teams from New York and two in Los Angeles), but this form is useful for illustrating what different SQL joins do. The second table contains the same information about NBA teams:

# In[3]:


nba_dict = {'city':['Boston','New York','Philadelphia','Brooklyn','Toronto',
                   'Cleveland','Chicago','Detroit','Milwaukee','Indianapolis',
                   'Atlanta', 'Washington','Orlando','Miami','Charlotte',
                   'Los Angeles','San Francisco','Portland','Sacramento',
                   'Phoenix','San Antonio','Dallas','Houston','Oklahoma City',
                   'Minneapolis','Denver','Salt Lake City','Memphis','New Orleans'],
           'basketballteam':['Boston Celtics','New York Knicks','Philadelphia 76ers',
                             'Brooklyn Nets','Toronto Raptors',
                            'Cleveland Cavaliers','Chicago Bulls','Detroit Pistons',
                             'Milwaukee Bucks','Indiana Pacers',
                            'Atlanta Hawks','Washington Wizards','Orlando Magic',
                             'Miami Heat','Charlotte Hornets',
                            ['L.A. Lakers','L.A. Clippers'],'Golden State Warriors',
                             'Portland Trailblazers','Sacramento Kings',
                            'Phoenix Suns','San Antonio Spurs','Dallas Mavericks',
                             'Houston Rockets','Oklahoma City Thunder',
                            'Minnesota Timberwolves','Denver Nuggets',
                             'Utah Jazz','Memphis Grizzlies','New Orleans Pelicans']}
nba_df = pd.DataFrame(nba_dict)
nba_df


# To create a PostgreSQL database with entities for the NFL and NBA teams, I first connect to the PostgreSQL server running on my local computer (see module 6 for a more detailed discussion of how this works). First I bring my PostgreSQL password into the local environment:

# In[4]:


dotenv.load_dotenv()
pgpassword = os.getenv("pgpassword")


# Then I access the server and establish a cursor for the server:

# In[5]:


dbserver = psycopg2.connect(
    user='jk8sd', 
    password=pgpassword, 
    host="localhost"
)
dbserver.autocommit = True
cursor = dbserver.cursor()


# I create an empty "teams" database:

# In[6]:


try:
    cursor.execute("CREATE DATABASE teams")
except:
    cursor.execute("DROP DATABASE teams")
    cursor.execute("CREATE DATABASE teams")


# And I use the `create_engine()` function from `sqalchemy` to allow queries to the "teams" database:

# In[7]:


engine = create_engine("postgresql+psycopg2://{user}:{pw}@localhost/{db}"
                       .format(user="jk8sd", pw=pgpassword, db="teams"))


# I add the `nfl_df` and `nba_df` dataframes to the "teams" database:

# In[8]:


nfl_df.to_sql('nfl', con = engine, index=False, chunksize=1000, if_exists = 'replace')
nba_df.to_sql('nba', con = engine, index=False, chunksize=1000, if_exists = 'replace')


# I can now issue queries to the database. To read all of the data in the NFL table, for example, I type:

# In[9]:


myquery = "SELECT * FROM nfl"
pd.read_sql_query(myquery, con=engine)


# ### Types of Joins
# Joining data tables is the act of *adding columns* to an existing data table - that is, adding more features to existing records - by matching the rows in one table to the corresponding rows in another table. In a relational database, data tables can include a foreign key which serves as the primary key for another data table. Joins require matching a foreign key in one table to the corresponding primary key in another table. During the join, this foreign key and this primary key are both called **indices**. To perform a join with an SQL query, we specify the two tables in the database we want to join and the index in each table we will match on.
# 
# In the teams database, `city` is a primary key in both the "nfl" and "nba" tables, which also makes it a foreign key in both tables. Joining the "nfl" and "nba" tables by matching on `city` creates one data table in which the rows still represent cities and the columns list both the NBA and NFL teams in each city. 
# 
# Not every city has both an NFL and an NBA team. Green Bay, for example, has a football team but no basketball team, and Sacramento has a basketball team but no football team. In a join, every row in a table either **matches** with one or more rows in the other table, or is **unmatched**. In this case, Cleveland in the NFL table is matched to a row in the NBA table because Cleveland has both a football and basketball team, but Oklahoma City in the NBA table is unmatched because there is no row for Oklahoma City in the NFL table.
# 
# The main difference between types of joins in SQL is their treatment of unmatched records. The following table summarizes the types of joins:
# 
# | Type of join | Definition                                                                                                                                  |
# |--------------|---------------------------------------------------------------------------------------------------------------------------------------------
# | Inner join   | Only keep the records that exist in both tables|
# | Left join    | Keep all the records in the first table listed, and keep only the records in the second table listed that have matches in the first table   |
# | Right join   | Keep all the records in the second table listed, and keep only the  records in the first table listed that have matches in the second table |                     
# | Full join    | Keep all of the records in both tables whether they are matched or not                                                                      |                     
# | Anti join    | Keep only the records in the first table that are not matched in the second table                                                           |                     
# |Natural join | The same as any of the joins listed above, but no need to specify the indices as these are determined automatically by finding columns with the same name. If no columns share the same name, a natural join performs a cross join. If more than one pair of columns share names across the two data tables, natural joins assume that both are part of the index to match on. Use caution.|
# |Cross join | Also called a **Cartesian product**. If the first dataframe has $M$ rows and the second dataframe has $N$ rows, the result has $M\times N$ rows. Every row is a pairwise combination of values of each index.|

# ### Inner Joins
# The syntax for an inner join is
# ```
# SELECT * FROM table1
# INNER JOIN table2
#     ON table1.index_name = table2.index_name;
# ```
# where `table1` and `table2` are the data tables we are joining, and `table1.index_name` and `table2.index_name` are the columns that contain the indices for tables 1 and 2. Alternatively, inner join is the default type of join, so that this syntax
# ```
# SELECT * FROM table1
# JOIN table2
#     ON table1.index_name = table2.index_name;
# ```
# also produces an inner join. I recommend typing `INNER JOIN`, however, to avoid confusing this type of join with other types.
# 
# In the case of the teams database, an inner join of the NFL and NBA tables yields a dataframe with one row for every city that has both a basketball and a football team. The SQL query that generates this data frame is:

# In[10]:


myquery = """
SELECT * FROM nfl
INNER JOIN nba
    ON nfl.city = nba.city;
"""
pd.read_sql_query(myquery, con=engine)


# The three quotations that come before and after the SQL code is Python syntax that allow for a string to be entered on multiple lines. With just one quote, Python would assume that the next line should be read as Python code, and will produce an error. Three quotes allows us to space out the components of the SQL query on separate lines to make the SQL code easier to read and understand.
# 
# SQL queries can be written on multiple lines, but the last line (and only the last line) must conclude with a semicolon.
# 
# Another way to write the inner join query is to use **aliasing**: specifying a smaller name or a single letter next to each data table in the query to simplify the syntax for `ON`. For example, I can alias the NFL data with `f` and the NBA data with `b`:

# In[11]:


myquery = """
SELECT * FROM nfl f
INNER JOIN nba b
    ON f.city = b.city;
"""
pd.read_sql_query(myquery, con=engine)


# The two indices we match on do not necessarily have to have the same name. Supposing that the "city" column in each data table was named "location" in the NFL table and "town" in the NBA table, the syntax for the inner join would have been:
# ```
# SELECT * FROM nfl f
# INNER JOIN nba b
#     ON f.location = b.town;
# ```

# ### Left and Right Joins
# The syntax for a left join is
# ```
# SELECT * FROM table1
# LEFT JOIN table2
#     ON table1.index_name = table2.index_name;
# ```
# and the syntax for a right join is
# ```
# SELECT * FROM table1
# RIGHT JOIN table2
#     ON table1.index_name = table2.index_name;
# ```
# In the case of the teams database, if we list the NFL table next to `FROM` and the NBA data with the `JOIN` statement, then left join lists all of the cities with an NFL team, and also displays the NBA team in that city if one exists. Otherwise, the syntax places `None` in the cell where the NBA team would be. For the teams database, the syntax for a left join is:

# In[12]:


myquery = """
SELECT * FROM nfl f
LEFT JOIN nba b
    ON f.city = b.city;
"""
pd.read_sql_query(myquery, con=engine)


# Likewise, the right join displays all the cities with an NBA team, along with the NFL team in that city, if one exists:

# In[13]:


myquery = """
SELECT * FROM nfl f
RIGHT JOIN nba b
    ON f.city = b.city;
"""
pd.read_sql_query(myquery, con=engine)


# For the left and right joins, changing which data table appears along with `FROM` and which data table appears along with `JOIN` accomplishes the same thing as changing a left join to a right join. 
# 
# ### Full (Outer) Join
# A full join, also called an outer join, keeps all of the records that exist in both tables, whether or not they are matched. Full joins will return a data frame with at least as many rows as the larger of the two data tables in the join because it contains all records that appear in either data frame. Most tutorials on SQL offer a warning about full joins that these queries can result in massive amounts of data being returned, and full joins are not implemented for MySQL databases. For systems like PostgreSQL in which full joins are allowed, the syntax for a full join is
# ```
# SELECT * FROM table1
# FULL JOIN table2
#     ON table1.index_name = table2.index_name;
# ```
# For the teams database, a full join produces a data frame with one row for every city with an NFL team or an NBA team or both:

# In[14]:


myquery = """
SELECT * FROM nfl f
FULL JOIN nba b
    ON f.city = b.city;
"""
pd.read_sql_query(myquery, con=engine)


# Although there are 30 cities with at least one NFL team and 29 cities with at least one NBA team, there are 41 cities with at least one team from one of these two leagues.

# ### Anti-Joins
# An anti-join leaves us with all of the records in the first data table that do not appear in the second table. There is no "ANTI JOIN" syntax in SQL, but the behavior of an anti-join can be generated by including the `WHERE` clause along with `LEFT JOIN`. The syntax for an anti-join is
# ```
# SELECT * FROM table1
# LEFT JOIN table2
#     ON table1.index_name = table2.index_name
# WHERE table2.index_name is NULL;
# ```
# The `WHERE` statement is used to draw a selection of rows from a data table that make a specified logical condition true. After performing a left join we have a data table with all of the rows in the first table along with the data for those rows in the second table if the row had a match in the second table. Typing `WHERE table2.index_name is NULL` restricts this data table to only the rows that do not have a value of the index in the second table, meaning there was no match. For the teams database, the anti-join of the NFL and NBA tables yields a dataframe of all the cities with an NFL team but no NBA team:

# In[15]:


myquery = """
SELECT * FROM nfl f
LEFT JOIN nba b
    ON f.city = b.city
WHERE b.city is NULL;
"""
pd.read_sql_query(myquery, con=engine)


# ### Natural Joins
# One annoying thing about all of the joins shown above is that we end up with two columns that contain the same information. In the case of the team database, we have two `city` columns that are always either equal, or else one is missing. But when one of the `city` columns says "None", the team from that table also says "None", so the missingness in the `city` column does not provide additional information.
# 
# It might make sense to use a different kind of join that understands that the two `city` columns contain the same information and includes only one of these columns. A natural join does two things differently from the other joins described here:
# 
# 1. A natural join removes duplicated columns from the output data.
# 
# 2. A natural join detects the indices automatically by assuming columns that share the same name are part indices.
# 
# If done correctly, a natural join saves some work constructing the query as the indices are detected automatically, and provides cleaner output. Any of the joins described above can be done as a natural join by adding `NATURAL` in front of `INNER`, `LEFT`, `RIGHT`, or `FULL`. If there are no columns that share the same name, a natural join instead performs a cross join (described below). 
# 
# The following query performs a natural inner join:

# In[16]:


myquery = """
SELECT * from nfl
NATURAL INNER JOIN nba
"""
pd.read_sql_query(myquery, con=engine)


# Natural joins are controversial, however, and many data scientists choose not to use them at all. The danger is that if two columns unexpectedly have the same name (it can be hard to keep track of all of the features' names in big databases) then a natural join will match on the wrong indices. This [Stack Overflow post](https://stackoverflow.com/questions/8696383/difference-between-natural-join-and-inner-join#8696402) gets into this debate, and one response made a forceful argument against natural joins:
# 
# > Collapsing columns in the output is the least-important aspect of a natural join. The things you need to know are (A) it automatically joins on fields of the same name and (B) it will f--- up your s--- when you least expect it. In my world, using a natural join is grounds for dismissal. . . . Say you have a natural join between `Customers` and `Employees`, joining on `EmployeeID`. Employees also has a `ManagerID` field. Everything's fine. Then, some day, someone adds a `ManagerID` field to the `Customers` table. Your join will not break (that would be a mercy), instead it will now include a second field, and work incorrectly. Thus, a seemingly harmless change can break something only distantly related. VERY BAD. The only upside of a natural join is saving a little typing, and the downside is substantial.
# 
# Personally, I disagree with this statement as I think natural joins can be elegant and convenient, especially when I want to match on multiple indices. But I agree that natural joins do make it easier to mess up a join, and more caution is needed. To demonstrate how a natural join can go wrong, suppose that in both the NFL and NBA tables the columns were named `city` and `team`. The following code creates versions of these tables with `footballteam` and `basketballteam` each renamed to `team` and stores these tables in the database as "nfl2" and "nba2": 

# In[17]:


nfl2 = pd.read_sql_query("SELECT city, footballteam as team FROM nfl;", con=engine)
nba2 = pd.read_sql_query("SELECT city, basketballteam as team FROM nba;", con=engine)
nfl2.to_sql('nfl2', con = engine, index=False, chunksize=1000, if_exists = 'replace')
nba2.to_sql('nba2', con = engine, index=False, chunksize=1000, if_exists = 'replace')


# Now a natural inner join between "nfl2" and "nba2" yields a dataframe with no records:

# In[18]:


myquery = """
SELECT * FROM nfl2 
NATURAL INNER JOIN nba2;
"""
pd.read_sql_query(myquery, con=engine)


# The reason why there are no records is that the natural join automatically chooses both `city` and `team` to be part of the index, and records are only kept in the inner join if they match on both city and team. There are many matches for city, but no matches for both city and team.
# 
# In contrast, a regular inner join still works fine:

# In[19]:


myquery = """
SELECT * FROM nfl2 f
INNER JOIN nba2 b
    ON f.city = b.city;
"""
pd.read_sql_query(myquery, con=engine)


# To safely use natural joins, first make certain that the indices you intend to match on have the same name, and then make sure that no other columns in the two data tables share a name.

# ### Cross Joins
# A **round robin** is a method of organizing a competitive tournament. In a round robin, every team or participant plays every other team or participant once. A cross join, also called a Cartesian product, is a round robin for matching values of the index in one data table to values of the index in the other data table. Every value of the index in the first data table is matched once to every distinct value of the index in the second data table. Cross joins are memory-intensive: if the first data table has $M$ rows and the second data table has $N$ rows, the cross join output is a data table with $M\times N$ rows. In general cross joins are not good ways to combine data entities, and they fail to match strictly like units. But cross joins are useful for constructing data that contain all possible pairings, if that's what a situation calls for.
# 
# The syntax for generating a cross join is
# ```
# SELECT * FROM table1
# CROSS JOIN table2;
# ```
# There is no `ON` statement in this query because it is not needed to match each row in `table1` to every row in `table2`. For the teams database, the cross join generates the following output:

# In[20]:


myquery = """
SELECT * FROM nfl
CROSS JOIN nba;
"""
pd.read_sql_query(myquery, con=engine)


# ### Multiple Joins in One Query
# All of the examples above show a single join between two data tables, but many situations will require you to join multiple tables. it is possible to join many tables in one SQL query. The syntax to perform an inner join between two tables, then an inner join between the result and a third table is
# ```
# SELECT * FROM table1
# INNER JOIN table2
#     ON table1.index_name = table2.index_name
# INNER JOIN table 3
#     ON table1.index_name = table3.index_name;
# ```
# To demonstrate how multiple joins can work, I add a third table to the teams database that contains all of the Major League Baseball teams:

# In[21]:


mlb_dict = {'city': ['New York', 'Boston', 'Toronto', 'Baltimore', 'Tampa Bay',
                     'Cleveland', 'Chicago', 'Kansas City', 'Minneapolis', 'Detroit',
                     'Houston', 'Anaheim', 'Dallas', 'Seattle', 'Oakland',
                     'Philadelphia', 'Miami', 'Washington', 'Atlanta', 'Cincinnati',
                     'Milwaukee', 'St. Louis', 'Pittsburgh', 'Los Angeles', 'San Francisco',
                     'San Diego', 'Denver', 'Phoenix'],
           'baseballteam': [['New York Mets', 'New York Yankees'], 'Boston Red Sox', 'Toronto Blue Jays',
                            'Baltimore Orioles', 'Tampa Bay Rays', 'Cleveland Indians', 
                             ['Chicago White Sox', 'Chicago Cubs'], 'Kansas City Royals', 'Minnesota Twins',
                            'Detriot Tigers', 'Houston Astros', 'Anaheim Angels', 'Texas Rangers', 
                            'Seattle Mariners', 'Oakland Athletics', 'Philadelphia Phillies',
                            'Miami Marlins', 'Washington Nationals', 'Atlanta Braves', 'Cincinnati Reds',
                            'Milwaukee Brewers', 'St. Louis Cardinals', 'Pittsburgh Pirates', 'Los Angeles Dodgers',
                            'San Francisco Giants', 'San Diego Padres', 'Colorado Rockies', 'Arizona Diamondbacks']}
mlb_df = pd.DataFrame(mlb_dict)
mlb_df.to_sql('mlb', con = engine, index=False, chunksize=1000, if_exists = 'replace')


# We can first inner join the NFL and NBA data tables to keep only the cities with both an NFL and an NBA team, then we can inner join the result with the MLB data to keep only the cities with teams in all three sports:

# In[22]:


myquery = """
SELECT * FROM nfl f
INNER JOIN nba b
    ON f.city = b.city
INNER JOIN mlb m
    ON f.city = m.city;
"""
pd.read_sql_query(myquery, con=engine)


# Things get more complicated when we consider left, right, and full joins in a multiple table context. The trick is to think about the set of records that is required, to express that set in set theoretical notation, and to find the right combination of joins that matches that set theoretical statement. 
# 
# For example, to obtain all cities with both an NFL and NBA team, also listing the MLB team if one exists in that city, we first inner join the NFL table to the NBA table, then we left join either the NFL's or NBA's city index to the MLB's city column:

# In[23]:


myquery = """
SELECT * FROM nfl f
INNER JOIN nba b
    ON f.city = b.city
LEFT JOIN mlb m
    ON f.city = m.city;
"""
pd.read_sql_query(myquery, con=engine)


# To narrow the records to teams with a baseball team and a basketball team, but no football team, first we inner join the MLB and NBA data tables, then perform an anti-join with the NFL data:

# In[24]:


myquery = """
SELECT * FROM mlb m
INNER JOIN nba b
    ON m.city=b.city
LEFT JOIN nfl f
    ON m.city = f.city
WHERE f.city is NULL;
"""
pd.read_sql_query(myquery, con=engine)


# ### Joins on More Than One Index
# Sometimes more than one column comprises the primary key for a table. The general syntax for joining two tables on more than one index adds the `AND` clause to the standard SQL join syntax:
# ```
# SELECT * FROM table1
# INNER JOIN table2
#     ON table1.index1 = table2.index2
#         AND table1.anotherindex1 = table2.anotherindex2;
# ```
# Suppose for example that the NBA table and MLB table also contained records for minor league teams in the NBA G-League or the MLB AAA system. Some cities have both major and minor league teams in the same sport. Washington, for example, has a major league NBA team, the Wizards, and a minor league basketball team, the Capital City Go-Gos. Suppose that both the NBA and MLB tables have a column `leaguetype` that marks each team as "major" or "minor", and that we want to match on both city and league type. The syntax to do so is
# ```
# SELECT * FROM nba b
# INNER JOIN mlb m
#     ON b.city = m.city
#         AND b.leaguetype = m.leaguetype;
# ```

# ## SQL Create, Update, and Delete Operations
# Once a database exists and is populated with data, most changes to the data will be small and incremental. We might add a few records, edit a couple, or delete one or two. There are straightforward SQL commands for creating, updating, and deleting records. To issue these queries, however, we cannot use the `pd.read_sql_query()` function as this function is only for read operations. Instead, we can use the `.execute()` method as applied to either the cursor for the database we are working with, or the `sqlalchemy` engine. Specific examples are shown below.

# ### Creating New Records
# An existing database has a schema, an overarching organizational blueprint for the database, that describes the different tables in the database, and within each table what the columns are and what kinds of data can be input into the columns. Creating new data generally works within an established schema. That means we enter new datapoints into existing columns, matching the data type that must exist in those columns.
# 
# The SQL syntax to create new data is
# ```
# INSERT INTO table (column1, column2, ...)
#     VALUES (value1, value2, ...);
# ```
# This syntax requires us to specify the key elements of the schema that identify a location in the database: the table and the columns. The values need to be listed in the same order as the columns, and character values need to be enclosed in single quotes.
# 
# To add a new observation to the NBA table (bring back the Sonics!) we can type:

# In[25]:


myquery = """
INSERT INTO nba (city, basketballteam)
    VALUES ('Seattle', 'Seattle Supersonics');
"""
engine.execute(myquery)


# Here the `engine` variable is the `sqlaclchemy` connection we previously established for the teams database. We can use the `execute()` method to pass SQL queries to the database, just as we can with a cursor. Now, when we look at the data, we see the Seattle Supersonics included along with all the other NBA teams:

# In[26]:


pd.read_sql_query("SELECT * FROM nba", con=engine)


# ### Editing Existing Records
# Instead of creating a new record, there are situations in which we want to edit an existing record. To revise a record, we use the following SQL syntax:
# ```
# UPDATE table
#     SET column2 = newvalue
#     WHERE logicalcondition;
# ```
# In this case, `SET` specifies the change we want to make to a particular column. But we don't want to change *all* of the values of the column, so we use `WHERE` to specify a logical condition to identify the rows we want to change. A logical condition is a statement that is true on some rows and false on others, and the data update happens only on the rows for which the condition is true. 
# 
# Suppose we want to change the name of the Charlotte Hornets back to the Charlotte Bobcats (sorry, Charlotte). We can use the following code:

# In[27]:


myquery = """
UPDATE nba
    SET basketballteam = 'Charlotte Bobcats'
    WHERE city = 'Charlotte';
"""
engine.execute(myquery)


# Here the query says to update values in the NBA table by changing `basketballteam` to Charlotte Bobcats, but only when `city` is Charlotte. This update now appears in the NBA data:

# In[28]:


pd.read_sql_query("SELECT * FROM nba", con=engine)


# ### Deleting Records
# Sometimes you might need to delete records from a database. These situations should be rare. If a record is no longer relevant for a particular use, it is always better to leave the record in the database and use another column to denote new information that can be used to filter records later. If there are mistakes in data entry, it's better to edit existing records than to delete those records outright. If you must delete a record, the syntax to do so is
# ```
# DELETE FROM table WHERE logicalcondition;
# ```
# First specify the table, then the logical condition that identifies the rows you intend to delete. 
# 
# In the teams database, suppose we want to delete the Baltimore Ravens (go Browns!) from the NFL table. The code to do that is:

# In[29]:


myquery = """
DELETE FROM nfl WHERE city = 'Baltimore'; 
"""
engine.execute(myquery)


# In this case, `city = 'Baltimore'` identifies the rows we want to delete in the NFL table. The NFL data now no longer contains a row for the Ravens:

# In[30]:


pd.read_sql_query("SELECT * FROM nfl", con=engine)


# ## Cleaning and Manipulating Data with SQL Read Operations
# After using joins to combine data tables in the database, the data needs to be manipulated to make the data more convenient to use. That might involve narrowing down the data to a specific subset of interest, performing calculations on the data to generate new features, and changing the appearance of the data. In "[Tidy Data](https://www.jstatsoft.org/article/view/v059i10)", Hadley Wickham defines four essential "verbs" of data manipulation:
# 
# > * Filter: subsetting or removing observations based on some condition.
# > * Transform: adding or modifying variables. These modifications can involve either a single variable (e.g., log-transformation), or multiple variables (e.g., computing density from weight and volume).
# > * Aggregate: collapsing multiple values into a single value (e.g., by summing or taking means).
# > * Sort: changing the order of observations (p. 13).
# 
# In addition it may be necessary to pull only a selection of the columns into the output, or to change the names of the columns to more readable and useful ones. These operations can be performed within SQL read commands by using the `WHERE` clause for filtering, mathematical operators to transform columns, the `GROUP BY` syntax for aggregation, the `ORDER BY`, `ASC`, or `DESC` clauses for sorting, and the `AS` keyword for renaming columns.

# ### Example: Wine Reviews
# To illustrate how to issue queries to read data while manipulating and cleaning the data, we will use the PostgreSQL version of the wine review database that we created in module 6. If you want to follow along with these example, follow the instructions in the "Using PostgreSQL" subsection of module 6 to get a local wine database running on your system.
# 
# For read operations, we can use the `pd.read_sql_query()` function. For that, we first have to use `sqlalchemy` to set up an engine that connects `pandas` to the database: 

# In[31]:


engine = create_engine("postgresql+psycopg2://{user}:{pw}@localhost/{db}"
                       .format(user="jk8sd", pw=pgpassword, db="winedb"))


# The logical ER diagram for the wine reviews database is
# 
# <img src="https://github.com/jkropko/DS-6001/raw/master/localimages/wine_er4.png" width="400">

# ### Selecting Columns
# `SELECT` and `FROM` are the primary SQL verbs for reading data. In many of the examples up to this points, we've issued queries like
# ```
# SELECT * FROM table;
# ```
# that pull all of the rows and all of the columns from a single data table. The `*` character is called a [wildcard character](https://en.wikipedia.org/wiki/Wildcard_character). When typed by itself, the wildcard captures all of the columns in a table. But sometimes we are interested in only a selection of the columns. In that case, we replace the wildcard with the columns we want to include in the output. The following syntax includes three columns from a specified data table:
# ```
# SELECT col1, col2, col3 FROM table;
# ```
# Suppose that I want to know the title, variety, price, points, country, and reviewer for all of the wines in the data. Title, variety, price, and points are all in the reviews table, country is in the locations table, and the reviewer (`taster_name`) is in the tasters table. To produce the data I need to join these three tables while also using `SELECT` to identify only the rows I am interested in. Inner joins are appropriate because every wine in the data has both a location and a reviewer. 
# 
# The best way to select columns across multiple tables is to use aliasing, the same way we did for joins. In this case, if we alias the reviews table as `r`, locations as `l`, and tasters as `t`, we can use these same aliases to inform SQL where to find each column in the `SELECT` syntax. 
# 
# The code to return this dataframe is:

# In[32]:


myquery="""
SELECT r.title, r.variety, r.price, r.points, l.country, t.taster_name FROM reviews r
INNER JOIN locations l
    ON r.location_id = l.location_id
INNER JOIN tasters t
    ON r.taster_id = t.taster_id;
"""
pd.read_sql_query(myquery, con=engine)


# ### Logical Statements
# Most programming languages have the capacity to evaluate a statement as being either true or false, or true for some values and false for others. A logical statement uses **logical operators** that define how values should be compared. In SQL, logical statements are used in conjunction with the `WHERE` statement to select the rows to include in the output.
# 
# For SQL, logical statements either compare a column to another column, or compare a column to one or more reference values. The following logical operators are available:
# 
# * `=` - is equal to?
# * `<` - is less than?
# * `>` - is greater than?
# * `<=` - is less than or equal to?
# * `>=` - is greater than or equal to?
# * `<>` - is not equal to?
# * `BETWEEN a AND b` - true if a value exists within the range from a to b, including a and b 
# * `IN ('element1','element2','element3')` - true if a value is one of the elements in the given set
# * `NOT` - true if the rest of the logical statement is false, false if the rest of the logical statement is true
# * `AND` - links separate logical statements together such that the overall statement is true only when all of the linked statements are true
# * `OR` - links separate logical statements together such that the overall statement is true when any of the linked statements are true
# * `LIKE pattern` - true if the string value matches the given pattern:
#     * `LIKE '%%text'` captures all rows in which a given column ends with 'text'
#     * `LIKE 'text%%'` captures all rows in which a given column begins with 'text'
#     * `LIKE '%%text%%'` captures all rows in which a given column contains 'text' somewhere in its string value
# * `()` - parts of the logical statement that are contained within parentheses are evaluated first
# 
# I will show examples of how to use these logical statements for filtering rows, in the next section.

# ### Filtering Rows
# Suppose we wanted to know the title, the variety, and the price of the French wines that Roger Voss scored as 100. It's a simple semantic sentence, but it connects to a more complicated set of SQL functions. First consider all of the columns we need to use to process the sentence:
# 
# * title, from the reviews table
# * variety, from the reviews table
# * price, from the reviews table
# * French, a value of country, from the locations table
# * Roger Voss, a value of taster name, from the tasters table,
# * and 100, a value of points, from the reviews table.
# 
# Because we need to use data from the reviews, locations, and tasters tables, we need to inner join reviews, locations, and tasters. 
# 
# But then on top of this join, we need to restrict both the columns and rows. We only want title, variety, and price in the final data, so we use `SELECT` to keep only these columns. 
# 
# To restrict the rows, we use `WHERE` along with a logical condition. This logical condition has a few parts: we want wines in which `country='France'`, `taster_name='Roger Voss'`, and `points=100`. All three conditions need to be true for us to want to keep the row, so we connect the three statements with `AND`.
# 
# The SQL query that returns the title, the variety, and the price of the French wines that Roger Voss scored as 100 is:

# In[33]:


myquery = """
SELECT r.title, r.variety, r.price FROM reviews r
INNER JOIN locations l
    ON r.location_id = l.location_id
INNER JOIN tasters t
    ON r.taster_id = t.taster_id
WHERE l.country='France' AND t.taster_name='Roger Voss' AND r.points=100;
"""
pd.read_sql_query(myquery, con=engine)


# I like my wine local or low-cost. So as another example, suppose we want the title, variety, price, points, country, and providence for all of the wines with scores of 90 or more that either cost between 5 and 10 dollars or are from Virginia. In this case, we need to join the reviews and locations data together, and write a logical statement that matches these specific conditions. The logical condition is
# ```
# points >= 90 AND (price BETWEEN 5 AND 10 OR province = 'Virginia')
# ```
# The entire SQL query is

# In[34]:


myquery = """
SELECT r.title, r.variety, r.price, r.points, l.country, l.province FROM reviews r
INNER JOIN locations l
    ON r.location_id = l.location_id
WHERE r.points >= 90 AND (r.price BETWEEN 5 AND 10 OR l.province = 'Virginia');
"""
pd.read_sql_query(myquery, con=engine)


# The parentheses in this last query are needed to ensure that the DBMS evaluates the `OR` statement first. Without the parentheses,
# ```
# points >= 90 AND price BETWEEN 5 AND 10 OR province = 'Virginia'
# ```
# the DBMS evaluates the first two conditions first, then considers the third, so the statement is equivalent to
# ```
# (points >= 90 AND price BETWEEN 5 AND 10) OR province = 'Virginia'
# ```
# and it returns data with all wines that have scores of at least 90 and prices between 5 and 10 dollars, along with all wines from Virginia whether or not those wines have scores of at least 90:

# In[35]:


myquery = """
SELECT r.title, r.variety, r.price, r.points, l.country, l.province FROM reviews r
INNER JOIN locations l
    ON r.location_id = l.location_id
WHERE r.points >= 90 AND r.price BETWEEN 5 AND 10 OR l.province = 'Virginia';
"""
pd.read_sql_query(myquery, con=engine)


# Suppose I'm open to many wines, but I have a thing against wines from the U.S., and I don't like Pinot Noir, Pinot Gris, or Chardonnay. I want to query the wines database to return data on the title, variety, country, and price of all of these wines except for the American ones and the ones I dislike. The SQL query requires joining the reviews and locations tables, and using negation in the logical statement with the `<>` and `NOT` operators, like this:

# In[36]:


myquery = """
SELECT r.title, r.variety, r.price, l.country FROM reviews r
INNER JOIN locations l
    ON r.location_id = l.location_id
WHERE country <> 'US' AND variety NOT IN ('Pinot Noir', 'Pinot Gris', 'Chardonnay');
"""
pd.read_sql_query(myquery, con=engine)


# If we want all of the columns from the reviews table for wines whose descriptions contain the words "smoke" and "chocolate" - taking case sensitivity into account by converting the descriptions to all lower case in the `WHERE` clause so that "chocolate" and "Chocolate" are both matched - the following query returns those wines:

# In[37]:


myquery = """
SELECT * FROM reviews 
WHERE LOWER(description) LIKE '%%smoke%%' AND LOWER(description) LIKE '%%chocolate%%';
"""
pd.read_sql_query(myquery, con=engine)


# There are situations in which we want to display only some of the records that match a particular query. For that, we can use the `LIMIT` and `OFFSET` clauses. `LIMIT` sets the number of records to extract, and `OFFSET` set the starting row. For example, adding
# ```
# LIMIT 10
# ```
# to a query instructs the DBMS to extract only the first 10 rows of the output data. Adding
# ```
# LIMIT 10 OFFSET 5
# ```
# tells the DBMS to extract 10 rows, after first skipping the first 5 rows: so these clauses together return rows 6 through 15. To see the 4th through 7th rows from the previous query to the wine reviews database, we can type:

# In[38]:


myquery = """
SELECT * FROM reviews 
WHERE LOWER(description) LIKE '%%smoke%%' AND LOWER(description) LIKE '%%chocolate%%'
LIMIT 4 OFFSET 3;
"""
pd.read_sql_query(myquery, con=engine)


# ### Sorting Data
# Sorting data refers to rearranging the rows of a dataframe. Sorting is a cosmetic thing to do to data because the order of the rows should not change the meaning of the data both in terms of storage (rearranging the rows should NOT change the meaning of each row), or for most analytical models (rearranging rows won't change the parameter estimates from a linear regression, for example). But sorting is a way to visualize important characteristics about the data and to quickly see important records with maximum and minimum values of key features.
# 
# To sort the output data, use the `ORDER BY` syntax within an SQL query. The general syntax for `ORDER BY` is
# ```
# ORDER BY column1, column2, column3
# ```
# Writing more than one column is optional. If more than one column is entered, then the second column is used to *break ties* between rows that have the same value of the first column. If a third column is entered, it's used to break ties between rows that have the same value for both the first and second columns. In addition, each column can be sorted in ascending or descending order by typing either `ASC` (this is the default, so typing `ASC` is optional, but useful for making the SQL code more readable) or `DESC` immediately after the column name.
# 
# For example, what are the top rated wines from Virginia? And of these top rated wines, which ones are cheapest? To find out, we issue a query that joins the reviews and locations tables, filters the data to just wines from Virginia, narrows down the columns to just title, points, and price, and sorts first by points, then by price. We sort by points in descending order so the best wines appear first, and we sort by price in ascending order so that the cheapest wines appear first. The syntax for this query is:

# In[39]:


myquery = """
SELECT r.title, r.points, r.price FROM reviews r
INNER JOIN locations l
    ON r.location_id = l.location_id
WHERE province = 'Virginia'
ORDER BY points DESC, price ASC;
"""
pd.read_sql_query(myquery, con=engine)


# ### Renaming Columns and Transforming Data Values
# Sometimes it is useful to rename the columns in the output data within a query. To rename a column, use the `AS` syntax while referencing the columns in `SELECT`. For example, we can load the title, variety, and points columns from the reviews table, but we can rename these columns name, type, and score respectively:

# In[40]:


myquery = """
SELECT title AS name, variety AS type, points AS score FROM reviews;
"""
pd.read_sql_query(myquery, con=engine)


# In other situations, we might want to transform a column arithmetically or in another way. SQL supports the standard arithmetic operators: `+` for addition, `-` for subtraction, `*` for multiplication, and `/` for division. SQL also supports the modulo operator `%` to return the remainder after division (`16 % 5` equals 1, for example, because 16 divided by 5 yields a remainder of 1). SQL also allows the following [arithmetic functions](https://www.w3schools.com/sql/func_sqlserver_pi.asp):
# 
# * `EXP(a)` - raises `a` the argument to the power of $e = 2.718...$
# * `POWER(a,b)` - raises `a` to the power of `b`
# * `LOG(a)` - takes the natural (base $e$) logarithm of `a`
# * `LOG10(a)` - takes the common (base 10) logarithm of `a`
# * `SQRT(a)` - takes the square root of `a`
# * `ABS(a)` - takes the absolute value of `a`
# * `CEILING(a)` - rounds values of `a` up to the next whole number
# * `FLOOR(a)` - rounds values of `a` down to a whole number
# * `ROUND(a, k)` - rounds values of `a` up or down to the nearest number with `k` decimals
# * `SIGN(a)` - returns 1 if `a` is positive, -1 if `a` is negative, and 0 if `a` is 0
# 
# In addition, if you need them, there are many trigonometric functions built into standard SQL.
# 
# When using a function that operates on a column, it is important to use `AS` to name the new column, as SQL has no way to choose a logical name automatically for constructed columns and uses `?column?` be default.
# 
# For example, we can convert the price of each wine from dollars to Euros by multiplying the price by the .91 USD to Euro exchange rate. We keep the original price in the query but rename it `price_dollars`, and we name the converted price `price_euros`:

# In[41]:


myquery = """
SELECT title, variety, price AS price_dollars, .91*price AS price_euros FROM reviews;
"""
pd.read_sql_query(myquery, con=engine)


# For no reason other than to demonstrate the use of the various mathematical functions, we can put many transformations of price in one dataframe:

# In[42]:


myquery = """
SELECT price,
    EXP(price/1000) as price_exp,
    LOG(price) as price_natlog,
    LOG10(price) as price_commonlog,
    ROUND(LOG(price)) as price_loground,
    SQRT(price) as price_sqrt,
    POWER(price, 2) as price_squared,
    POWER(price, 3) as price_cubed,
    SIGN(price - 50) as price_morethan50
FROM reviews;
"""
pd.read_sql_query(myquery, con=engine)


# Another useful operation for transforming columns in a read query is `CASE`, which maps numeric values to categories. The syntax that uses `CASE` within `SELECT` is
# ```
# SELECT CASE
#     WHEN logicalstatement1 THEN value1
#     WHEN logicalstatement2 THEN value2
#     WHEN logicalstatement3 THEN value3
#     ELSE value4
#     END AS name
# ```
# This code evaluates each logical statement, and fills in the datapoint with the specified value if the logical statement is true. If more than one of the logical statements is true, then the first statement/value pair entered in takes precedence. If none of the logical statements are true, then the datapoint is filled in with the value listed with `ELSE`. As before, it is important to name the new column with `AS`.
# 
# For example, if we want to categorize wines as cheap when the price is under 20 dollars, moderately priced if the price is between 20 and 50 dollars, and expensive if the price is more than 50 dollars, we can type:

# In[43]:


myquery="""
SELECT title, variety, price, CASE
    WHEN price < 20 THEN 'cheap'
    WHEN price BETWEEN 20 AND 50 THEN 'moderately priced'
    WHEN price > 50 THEN 'expensive'
    ELSE NULL
    END AS price_level
FROM reviews;
"""
pd.read_sql_query(myquery, con=engine)


# There's an important **point of caution** when using `CASE`. Unless you account for missing values explicity in your query, the missing values will be matched to the entered last in `CASE`. That will corrupt the data. It is best practice to write conditions for the full set of observed values of a column, and to end the call to `CASE` with `ELSE NULL`, so that when none of the conditions apply, the new column is also missing.

# There are also functions that apply to columns with [character](https://www.geeksforgeeks.org/sql-character-functions-examples/) values:
# 
# * `LOWER(a)` - converts all characters in `a` to lowercase
# * `UPPER(a)` - converts all characters in `a` to uppercase
# * `INITCAP(a)` - converts the first letter of every word in `a` to uppercase
# * `CONCAT(a,b,c)` - appends the string `b` to the end of `a`, and `c` (if included) to the end of `b`
# * `LENGTH(a)` - reports the number of characters in the string `a`
# * `SUBSTR(a, start, length)` - restricts the string `a` to a substring, beginning at the position denoted by `start`, and including the next `length` characters 
# * `TRIM(a)` - removes spaces at the beginning and end of string `a`
# * `REPLACE(a, oldtext, newtext)` - searches values of `a` for occurrences of `oldtext` and replaces them with `newtext`
# 
# For example, we can replace the descriptions in the reviews table with all capitals, all lower-case letters, or capitals for the first letter of each word:

# In[44]:


myquery = """
SELECT title, variety, price, 
    UPPER(description) as description_upper, 
    LOWER(description) as description_lower, 
    INITCAP(description) as description_initcap 
FROM reviews;
"""
pd.read_sql_query(myquery, con=engine)


# We can use `REPLACE()` to make the writing less artful, for example, by replacing the word "aroma" with "good smell" everywhere it appears in the wine descriptions. Note that `REPLACE()` is case-sensitive, so it is a good idea to convert the values to a consistent case like lowercase first:

# In[45]:


myquery = """
SELECT title, variety, price, description,
    REPLACE(LOWER(description), 'aroma', 'good smell') as description_replace 
FROM reviews
WHERE description LIKE '%%aroma%%';
"""
pd.read_sql_query(myquery, con=engine).description[0]


# In[46]:


pd.read_sql_query(myquery, con=engine).description_replace[0]


# The `SUBSTR()` function can be used to extract parts of a string. The following code reduces the `description` column to substrings beginning at the 5th character and proceeding 10 characters in length:

# In[47]:


myquery = """
SELECT title, variety, price, description,
    SUBSTR(description, 5, 10) as description_substr 
FROM reviews;
"""
pd.read_sql_query(myquery, con=engine)


# In the wine database, province and country are stored in separate columns in the locations table. If we wanted to put these two pieces of information together in one readable column, we can use `CONCAT()`. In this example, I type `CONCAT(l.province, ', ', l.country)` which appends three strings - the province from the locations table, a comma and a space, and the country from the locations table - and names the new column `place`:

# In[48]:


myquery = """
SELECT r.title, r.variety, r.price, 
    CONCAT(l.province, ', ', l.country) as place 
FROM reviews r
INNER JOIN locations l
    ON r.location_id = l.location_id;
"""
pd.read_sql_query(myquery, con=engine)


# What are the shortest descriptions in the data? To find out we use the `LENGTH()` function to count the number of characters in each description, and sort these lengths in ascending order:

# In[49]:


myquery = """
SELECT title, points, price, description,
    LENGTH(description) as length
FROM reviews
ORDER BY length ASC;
"""
pd.read_sql_query(myquery, con=engine)


# ### Data Aggregation
# If there are columns in the data output that have repeated values, then each distinct value forms a group in the data. Data aggregation is the process of collapsing the data to one row for each group, while summarizing other columns by taking the within-group mean, sum, count, or another statistic. 
# 
# Aggregating data requires more attention to the ordering of the clauses in an SQL query than is necessary with other tasks. That is, certain clauses must be entered into the query in a particular order. An SQL query that aggregates data should follow this template:
# ```
# SELECT aggregationfunctions FROM table
# (any joins happen here)
# (filtering rows with the WHERE clause happens here)
# GROUP BY groupingcolumns
# HAVING (a logical condition involving aggregation functions)
# (sorting with ORDER BY happens here);
# ```
# Let's break down this template line by line. First,
# 
# * `SELECT aggregationfunctions FROM table`
# 
# Aggregation functions work like the arithmetic functions described above. The difference is that instead of working with a single value, like `SQRT()` and `POWER()` do, aggregation functions work with vectors of data and generate summary statistics. They describe how existing columns should be summarized when the data are collapsed. The aggregation functions are:
# 
# * `COUNT(*)` - an overall count of the number of rows within each group
# * `COUNT(a)` - a count of the number of non-missing observations of column `a` within each group
# * `COUNT(DISTINCT a)` - a count of the number of distinct observations of column `a` within each group
# * `AVG(a)` - the mean of the values of `a` within each group
# * `SUM(a)` - the sum of the values of `a` within each group
# * `MAX(a)`- the maximum value of `a` within each group
# * `MIN(a)`- the minimum value of `a` within each group
# * `VARIANCE(a)` and `VAR_SAMP(a)` - the population and sample variances, respectively, of the values of `a` within each group
# * `STDDEV(a)` and `STDDEV_SAMP(a)` - the population and sample standard deviations, respectively, of the values of `a` within each group
# 
# Additional statistics, like the median, mode, and various quantiles are not included in standard SQL but are available in extensions that are specific to a DBMS, such as the [quantile extension](https://pgxn.org/dist/quantile/) for PostgreSQL.
# 
# One important point about the aggregation functions is that, with the exception of `COUNT()`, they **ignore NULL values**. Suppose that we have a data vector with values (1,3,8,NULL). Because we do not know the value of the fourth value, we cannot calculate the true sum and true mean of the values. However the `SUM()` function in SQL ignores the NULL value and reports the sum as 12, which makes a strong tacit assumption that the NULL value is equal to 0. The `AVG()` function calculates the mean from the observed values, and reports (1+3+8)/3 = 4, but this too makes a strong assumption that the NULL value is exactly 4. There are situations in which calculations from the non-NULL values are appropriate, but it is not correct to make broad claims from these summary statistics when there are missing values in the columns being summarized.
# 
# The next two lines in the template are placeholders for the syntax we use to join data tables and the syntax we use to filter rows with the `WHERE` clause. There is a great deal of similarity between `WHERE` and `HAVING`, which we will discuss shortly.
# 
# The fourth line in the template,
# 
# * `GROUP BY groupingcolumns`
# 
# is the key line for activating the aggregation functionality of SQL. `groupingcolumns` can include one or more columns. If one column is listed, the unique values of that column define the groups that will comprise the rows of the output data. If there is more than one column listed, the unique combinations of values from the columns define the groups.
# 
# The fifth line in the template uses the `HAVING` clause. `HAVING` is very similar to `WHERE` in that both use logical conditions to identify a selection of the rows to include in the output data. The difference between `WHERE` and `HAVING` is that `WHERE` operates on rows in the original data prior to aggregation, and `HAVING` works on rows after aggregation has occurred. One limitation of `HAVING` is that it will not recognize new column names defined in `SELECT`, so the same aggregation functions used in `SELECT` need to be used again in the logical conditions for `HAVING`. Finally, if we want to sort, we can include the `ORDER BY` clause last.
# 
# For example, let's find out which country produces wines with the highest average score. To do that, we need a query that joins reviews and locations together, includes country name, the average score across wines from that country, and for good measure, a count of the number of wines reviewed from that country. To collapse on country, we can use `GROUP BY`, and to produce the average score and the count of wines we use the `AVG()` and `COUNT()` functions. For presentation purposes, I choose to round the average score to one decimal and to sort the rows from the highest to lowest average score, so that we can immediately see which countries produce the highest-rated wines. The query is:

# In[50]:


myquery = """
SELECT l.country,
    ROUND(AVG(points),1) as average_points,
    COUNT(*) as numberofwines
FROM reviews r
INNER JOIN locations l
    ON r.location_id = l.location_id
GROUP BY l.country
ORDER BY average_points DESC;
"""
pd.read_sql_query(myquery, con=engine)


# So the country that produces the best wine is . . . England? Wait, that can't be right. Looking at the results, I see that some of the countries only have a small number of wines reviewed. China, for example, only has one wine review in the database, so we definitely should not put as much confidence in China's mean score as we can for countries with many more reviews like France and the U.S. For a more fair comparison, let's restrict the output to only those countries with at least 500 wines in the database. To filter rows on this condition, we use `HAVING` and not `WHERE` because the condition involves an aggregation function - specifically the count of the number of wines per country. We can rerun the previous query, including the `HAVING` clause:

# In[51]:


myquery = """
SELECT l.country,
    ROUND(AVG(points),1) as average_points,
    COUNT(*) as numberofwines
FROM reviews r
INNER JOIN locations l
    ON r.location_id = l.location_id
GROUP BY l.country
    HAVING COUNT(*) >= 500
ORDER BY average_points DESC;
"""
pd.read_sql_query(myquery, con=engine)


# Suppose we were interested in ranking the countries according to their scores for a particular type of wine. To filter rows from the original data, we use a `WHERE` clause prior to `GROUP BY`. If we write `WHERE r.variety = 'Riesling'` prior to `GROUP BY`, the DBMS first extracts only the rows from the reviews table that refer to Riesling wines, then proceeds with the rest of the query. The following code ranks the countries based on their average scores for Rieslings, given at least 100 Rieslings from that country in the database:

# In[52]:


myquery = """
SELECT l.country,
    ROUND(AVG(points),1) as average_points,
    COUNT(*) as numberofwines
FROM reviews r
INNER JOIN locations l
    ON r.location_id = l.location_id
WHERE r.variety = 'Riesling'
GROUP BY l.country
    HAVING COUNT(*) >= 100
ORDER BY average_points DESC;
"""
pd.read_sql_query(myquery, con=engine)


# Sometimes the groups in the data are formed by more than one column. In that case, simply add the second column name to the `GROUP BY` clause. For example, if we wanted to know the top rated combination of country and variety (with a minimum of 50 wines for that combination), we can use the following code:

# In[53]:


myquery = """
SELECT l.country, r.variety,
    ROUND(AVG(points),1) as average_points,
    COUNT(*) as numberofwines
FROM reviews r
INNER JOIN locations l
    ON r.location_id = l.location_id
GROUP BY l.country, r.variety
    HAVING COUNT(*) >= 50
ORDER BY average_points DESC;
"""
pd.read_sql_query(myquery, con=engine)


# ### Subqueries
# There are situations in which it makes sense to use data aggregation techniques to generate new columns filled with group-level summary statistics, then to place these summary statistics into the original data table. To do this work, we can use **subqueries**. A subquery is a full SQL query that is used inside another SQL query. There are three types of subquery:
# 
# 1. Subqueries, like the ones for the mean and standard deviation above, that yield a single datapoint. These subqueries can be used anywhere we might write a value in the query, such as when defining new columns in `SELECT` or filtering rows with `WHERE` or `HAVING`.
# 
# 2. Subqueries that yield a list of values that can be used inside logical statements that include the `IN` operator.
# 
# 3. Subqueries that yield a data table that can be joined to existing data tables.
# 
# Suppose for example that we wanted to generate a Z-score standardized version of the wine review points. A Z-score subtracts the mean of a column from every value in the column, then divides every value by the standard deviation of the column. When a Z-score equals 1, it means that the original value is one standard deviation above the mean of the column. To calculate the Z-score, we need to calculate the mean of the points column,

# In[54]:


myquery = """
SELECT AVG(points) FROM reviews;
"""
pd.read_sql_query(myquery, con=engine)


# and the sample standard deviation of the points column,

# In[55]:


myquery = """
SELECT STDDEV_SAMP(points) FROM reviews;
"""
pd.read_sql_query(myquery, con=engine)


# We can type these values in manually with a query that looks like:
# ```
# SELECT title, variety, points,
# (points - 88.612107))/(2.955039) as points_z 
# FROM reviews;
# ```
# The problem with typing these values in by hand is that it is easy to make a mistake and accidentially corrupt the `points_z` column because of a typo. Also these values will have to be changed by hand every time the data inside the database is updated. A better solution is to have SQL do the work of calculating the mean and standard deviation for us by using subqueries. All we need to do is replace the values with the queries (contained in parentheses) that generate those single values. In this case, the query is 

# In[56]:


myquery = """
SELECT title, variety, points,
(points - (SELECT AVG(points) FROM reviews))/(SELECT STDDEV(points) FROM reviews) as points_z 
FROM reviews;
"""
pd.read_sql_query(myquery, con=engine)


# Suppose that we wanted to restrict the rows to only the wines from wineries with at least 100 wines in the data. The problem is we don't know which wineries have at least 100 reviewed wines. But we can find out with a query:

# In[57]:


myquery = """
SELECT winery_id FROM reviews
GROUP BY winery_id
    HAVING COUNT(*) >= 100;
"""
pd.read_sql_query(myquery, con=engine)


# This query gives us a list of winery ID numbers that match the wineries with at least 100 reviewed wines in the data. We can now use this list inside another query that restricts the reviews data to only the wines from this list of wineries:

# In[58]:


myquery = """
SELECT winery_id, title, variety, points, price FROM reviews
WHERE winery_id IN (
    SELECT winery_id FROM reviews r
    GROUP BY winery_id
        HAVING COUNT(*) >= 100
    );
"""
pd.read_sql_query(myquery, con=engine)


# Suppose we wanted a data table with the top rated wine from each winery. The problem is we don't know which wine is the top rated for each winery. Again, we can find out with a query that groups the reviews data by winery ID and uses the `MAX()` aggregation function to identify the maximum score achieved for any wine from that winery: 

# In[59]:


myquery = """
SELECT winery_id, MAX(points) as maxpoints
FROM reviews
GROUP BY winery_id;
"""
pd.read_sql_query(myquery, con=engine)


# Suppose that this last table already existed in the database with the name "bestscores". We would be able to join bestscores and reviews, then filter the rows to only those wines whose scores are equal to the maximum scores achieved by the winery with the following code:
# ```
# SELECT r.title, r.variety, r.points, r.price FROM reviews r
# INNER JOIN bestscores b
#     ON r.winery_id = b.winery_id
# WHERE r.points = b.maxpoints;
# ```
# But because we do not have a table named "bestscores", we can replace the reference to this table with the subquery that generates this table:

# In[60]:


myquery = """
SELECT r.title, r.variety, r.points, r.price FROM reviews r
INNER JOIN (
    SELECT winery_id, MAX(points) as maxpoints
    FROM reviews
    GROUP BY winery_id) b
    ON r.winery_id = b.winery_id
WHERE r.points = b.maxpoints;
"""
pd.read_sql_query(myquery, con=engine)


# Finally, once we are finished working with the PostgreSQL server, we close it:

# In[61]:


dbserver.close()


# ## SQL Security
# One criticism of SQL is that it can be manipulated to give unauthorized and hostile users access to perform CRUD operations on the data. This kind of [attack](https://en.wikipedia.org/wiki/SQL_injection) is called an **SQL injection attack**, and the best illustration of this attack comes from an [XKCD](https://xkcd.com) web comic:
# 
# <a href="https://xkcd.com/327/"><img src="https://imgs.xkcd.com/comics/exploits_of_a_mom.png" width="500"></a>
# 
# The following discussion borrows heavily from [this blog's](https://explainxkcd.com/wiki/index.php/327:_Exploits_of_a_Mom) explaination of this XKCD comic. 
# 
# An SQL injection attack starts with an entry field on the user interface of an application that works with a database, like a field where users write their name. The application reads the name and creates an SQL INSERT operation to create a new record in the data with the name. If I were to enter Jonathan into the name field, the app should generate an SQL command that looks like this:
# ```
# INSERT INTO Students (firstname) VALUES ('Jonathan');
# ```
# This command specifically places the value "Jonathan" into the `firstname` attribute of the `Students` entity. In SQL, different commands are separated by semicolons, so if I wanted to issue two SQL commands I could type:
# ```
# INSERT INTO Students (firstname) VALUES ('Jonathan'); INSERT INTO Students (lastname) VALUES ('Kropko');
# ```
# An SQL injection attack works by writing SQL code in a field that is designed to collect data to input into a database. So If I type my name as `Jonathan'); DROP TABLE Students; --;`, then the SQL create operation becomes
# ```
# INSERT INTO Students (firstname) VALUES ('Jonathan'); DROP TABLE Students; --;');
# ```
# This line consists of three commands
# * `INSERT INTO Students (firstname) VALUES ('Jonathan');` which inputs "Jonathan" into the database,
# * `DROP TABLE Students;` which deletes the entire `Students` table, and
# * `--;');`: the `--` symbol is an SQL comment, and tells the parser to ignore the remainder of the code, which would avoid a parsing error.
# 
# So just by inserting specific code into a seemingly innocuous field, like name, I can delete the entire `Students` entity in the database.
# 
# There are two ways to combat SQL injection attacks. First, it is possible to "sanitize" database inputs by using code that automatically places a slash before a single quote. That puts an [escape character](https://en.wikipedia.org/wiki/Escape_character) in front of the quote, which makes it part of the input string and prevents it from being read as the end of the input string. Another approach is to use [prepared statements](https://en.wikipedia.org/wiki/Prepared_statement) when converting user-entered data into an SQL query. A prepared statement uses placeholders to stand in for the user-supplied data, and treats the data like input into a function: treating the user data this way prevents the entire SQL query from being read as a single string, and prevents SQL injection. For example, instead of inputing the name directly into the query, the database manager can construct the query in Python code (where a database cursor exists and is named `curs`) like this:
# ```
# cmd = "INSERT INTO Students (firstname) VALUES (%s)"
# curs.execute(cmd, (name,))
# ```
# In MySQL and PostgreSQL, `%s` stands in for a parameter to be passed into the query (in SQlite, the stand-in symbol is `?` instead of `%s`). Constructing a query in this way prevents SQL injection attacks. More information about formatting secure SQL code is available at https://bobby-tables.com/, named in honor of this XKCD comic.
# 
# As a data scientist mostly issuing read operations, it is unethical for you to attack a database in this way. If you are testing whether a database is secured against SQL injection attacks, don't try to issue any `DROP` commands as other commands like `SELECT` will reveal the insecurity but won't make changes in the database. If you are building a database that is connected to an interface for users to enter data, please be aware of the SQL injection vulnerability and use prepared statements to guard against it.

# ## MongoDB Queries
# SQL is a universal language for issuing queries to relational databases, whether the database is managed by SQLite, MySQL, PostgreSQL, or another RDBMS. For NoSQL databases, however, there is no universal query language. Every DBMS has its own query language, and will provide a guide for learning that language. Some of these guides include the ones for key-value stores in [Redis](https://redis.io/commands) and wide column stores in [Cassandra](https://cassandra.apache.org/doc/latest/cql/index.html). Neo4j has developed a programming language called [Cypher](https://neo4j.com/developer/cypher-query-language/) that is explicitly for issuing queries to graph databases. Of all of these query protocols, the language used by [MongoDB](https://docs.mongodb.com/guides/server/read_queries/) for issuing queries to document stores is one of the most universal because it works entirely with JSONs: queries are written in JSON format and the output is organized in JSON format. All of these query languages include methods for all of the CRUD operations.
# 
# The most important difference between relational and NoSQL databases is the rigidity of the schema that organizes the data. The advantage of the strict organization of a relational database, as illustrated in an ER diagram, is that the data that can be extracted from the database using an SQL query will be clean and mostly immediately ready to be analyzed. The disadvantage is that relational databases have schema that are hard to change once they've been created and populated with data. SQL also, despite the best intentions of the originators of SQL, can be very difficult for people use for some tasks. For extremely large datasets with many tables, it can be extremely difficult to keep track of what data exists in which table. In contrast, NoSQL databases generally have flexible schema that can be changed easily and can vary even from record to record. There are no rules, like the normalization rules, that require that the data be split into different tables, so there is no need for visual maps like ER diagrams. Also, because all of the data for one record exists in the same JSON dictionary, it is easy to use remote, distributed storage to store all of the records. The disadvantage of NoSQL databases is that the data are rarely ready for analysis after a query. It's a buy-now-pay-later situation: the price we pay for the convenience of NoSQL storage and organization is that the output requires more work to use.
# 
# Some concepts that are crucial to SQL are not relevant to NoSQL. There are **no joins** in a document store because all the data for a record exist in the same JSON code. As such, we don't have to worry about accomplishing these tasks within a NoSQL query. NoSQL queries in general focus narrowly on the CRUD operations, although MongoDB provides some advanced functionality for searching for patterns within text and ranking documents based on their relevance to given search terms.
# 
# For the following examples, I will use the document store database that we created in module 6, containing the same data on wine reviews that we practiced with above, only in JSON format. First I load the `pymongo` package and the `dumps()` and `loads()` functions from the `json_util` module of the `bson` package:

# In[62]:


import pymongo
from bson.json_util import dumps, loads


# The wine reviews database is stored as a collection `winecollection` within the `winedb` database on my local machine. I load it with the following code:

# In[63]:


myclient = pymongo.MongoClient("mongodb://localhost/")
winedb = myclient["winedb"]
winecollection = winedb["winecollection"]


# We will discuss more advanced read techniques below, but to see one record, we can issue a query using JSON code and we can see the output in JSON format. To see all of the data for the "Nicosia 2013 Vulkà Bianco", we search for the record based on the title of this wine with the following code:

# In[64]:


myquery = { 'title': 'Nicosia 2013 Vulkà Bianco  (Etna)'}
mywine = winecollection.find(myquery) 
for x in mywine:
    print(x)


# Notice that all of the data for this wine exists in this JSON dictionary, including data from the reviews, locations, wineries, and tasters tables in the PostgreSQL database. When we created this MongoDB database, the DBMS automatically created a unique ID for each record designated with the key `_id`. 
# 
# We can now use the methods in `pymongo` for creating, reading, updating, and deleting records and we will apply these methods to the `winecollection` variable that accesses the data.

# ### Creating and Deleting Records
# Did you know that former NBA all-star Dwyane Wade has a winery? It's called [D Wade Cellars](https://dwadecellars.com/) and it is based in the Napa Valley in California. Let's add the [2016 Napa Valley Three By Wade Red Blend](https://dwadecellars.vinespring.com/purchase/detail?item=2016-napa-valley-three-by-wade-red-blend) into the database. The first step is to express all of the data we want to associate with a new record in JSON format:

# In[65]:


dwadewine = {'title': '2016 Napa Valley Three By Wade Red Blend', 
'description': "This wine goes great with dinner just like Dwyane Wade goes great with LeBron James or Shaq.", 
'taster_name': 'Jonathan Kropko', 
'taster_twitter_handle': '@jmk5131', 
'price': '35', 
'variety': 'Red Blend', 
'location':{
    'region_1': 'Napa Valley', 
    'region_2': None, 
    'province': 'California', 
    'country': 'U.S.', 
    'winery': 'D Wade Cellars'}}


# In creating this JSON record, I tried to follow the standards that exist elsewhere in the data by using the same feature names. I departed from the format of other records in two ways. First, I omitted the points and designation features. Second, I placed all the information about the location and name of the winery under the "location" key, which induces some nesting structure.
# 
# To add this one record to the database, I use the `.insert_one()` method on the `winecollection` database, with the following code:
# ```
# winecollection.insert_one(dwadewine)
# ```
# By default, the `insert_one()` method automatically checks to see whether the record already exists in the data, and throws an error if it does, unless we specify the `bypass_document_validation=True` argument, which allows duplicate records to be input into the database. For the purposes of this notebook, I rerun these cells many times while writing, and I don't want to place many duplicate records into the database. Instead, I can delete the record if it already exists. The code
# ```
# winecollection.count_documents({'title': '2016 Napa Valley Three By Wade Red Blend'})
# ```
# generates a count of the records of wines in the database that have this title. If there are any existing records, I can delete all of these records with the `.delete_many()` method, in which the argument is a JSON with enough fields specified to exactly match the records we want to delete:
# ```
# winecollection.delete_many({'title': '2016 Napa Valley Three By Wade Red Blend'})
# ```
# In constrast, the `.delete_one()` method will only delete the first record, when sorting by `_id`, that matches the query. If there are no documents that match the query, he `.delete_all()` or `.delete_one()` methods will both still process the query without error, but will not change anything in the database.
# 
# We first delete any records of wines with the title "2016 Napa Valley Three By Wade Red Blend" with `.delete_all()`, then we insert the entire record of this wine with `.insert_one()`:

# In[66]:


winecollection.delete_many({'title': '2016 Napa Valley Three By Wade Red Blend'})
winecollection.insert_one(dwadewine)


# Now that this record exists in the database, we can find this record by any of the fields associated with the record, such as the title of the wine for example:

# In[67]:


myquery = {'title': '2016 Napa Valley Three By Wade Red Blend'}
mywine = winecollection.find(myquery) 
for x in mywine:
    print(x)


# Note that MongoDB automatically generates a unique ID value for this document and includes it under the `_id` field in the JSON output.
# 
# Wikipedia lists [93 other celebrities](https://en.wikipedia.org/wiki/List_of_celebrities_who_own_wineries_and_vineyards) other than Dwyane Wade who own wineries and vineyards, including [Antonio Banderas](https://www.decanter.com/wine-news/antonio-banderas-32255/), [Drew Barrymore](https://thewinesiren.com/drew-barrymore-vintner/), and [Lil Jon](http://www.today.com/id/23945035/ns/today-today_entertainment/t/rapper-lil-jon-starts-his-own-wine-label/#.XtV1BZp7l24). If we want to add more than one record to the wine collection database, we need to create a list of individual JSON dictionaries with code that looks like
# ```
# newrecords = [{JSON dictionary 1}, {JSON dictionary 2}, {JSON dictionary 3}]
# ```
# In this case, I can create entries for Antonio Banderas, Drew Barrymore, and Lil Jon's wines and store them in one list:

# In[68]:


newwines = [{'title': 'Anta Banderas A 10 2008', 
             'description': "This wine will make you speak differently. Maybe not with a charming Spanish accent, but you might think you sound that way.", 
             'taster_name': 'Jonathan Kropko', 
             'taster_twitter_handle': '@jmk5131', 
             'price': '40.99', 
             'variety': 'Red Blend', 
             'location':{
                 'region_1': 'Ribera del Duoro', 
                 'region_2': None, 
                 'province': 'Valladolid', 
                 'country': 'Spain', 
                 'winery': 'Anta Banderas'}},
           {'title': 'Barrymore Rose 2013', 
             'description': "Someone drank my entire bottle of wine!", 
             'taster_name': 'Jonathan Kropko', 
             'taster_twitter_handle': '@jmk5131', 
             'price': '14.99', 
             'variety': 'Rose', 
             'location':{
                 'region_1': 'Monterey', 
                 'region_2': None, 
                 'province': 'California', 
                 'country': 'U.S.', 
                 'winery': 'Barrymore Vineyard'}},
           {'title': '2006 Little Jonathan Winery Cabernet Sauvignon', 
             'description': "This upscale crunk juice is OOOKAAAAAAY.", 
             'taster_name': 'Jonathan Kropko', 
             'taster_twitter_handle': '@jmk5131',  
             'variety': 'Cabernet Sauvignon', 
             'location':{
                 'region_1': 'Central Coast', 
                 'region_2': 'Paso Robles', 
                 'province': 'California', 
                 'country': 'U.S.', 
                 'winery': 'Little Jonathan Winery'}}]


# To add these three records to the database with one line of code, we use the `.insert_many()` method. To avoid duplicates, we first delete any records of wines titled "Anta Banderas A 10 2008", "Barrymore Rose 2013", or "2006 Little Jonathan Winery Cabernet Sauvignon":

# In[69]:


winecollection.delete_many({'title': 'Anta Banderas A 10 2008'})
winecollection.delete_many({'title': 'Barrymore Rose 2013'})
winecollection.delete_many({'title': '2006 Little Jonathan Winery Cabernet Sauvignon'})
winecollection.insert_many(newwines)


# ### Reading Data and Selecting Records
# To read all of the records in a MongoDB collection, use the `.find()` method and pass an empty JSON dictionary to this method. For the wine reviews collection, we can query the entire collection by typing

# In[70]:


myquery = winecollection.find({})


# Here, the queried data exist within the variable `cursor`. The data are not displayed automatically. To see the data in JSON format, we can employ the `print()` function on elements of the cursor. To see the first element:

# In[71]:


print(myquery[0])


# And to see more elements, we can use a loop. Here's code to view the first three wines:

# In[72]:


for i in myquery[0:3]:
    print(i)


# Displaying the query output data as a list of JSON dictionaries, however, is not the most useful way to store the data. We need a way to put these data into a dataframe. For that we can use the `dumps()` and `loads()` functions from the `bson` library. These functions work exactly like the `dumps()` and `loads()` functions from the `json` library, but they remove some of the extra components of these JSON dictionaries associated with the database. To query all of the data and to place all of it into a dataframe, we pass the query output to `dumps()`, which converts the query output to plain text. Next we pass this text to `loads()`, which registers the text as a list of JSON dictionaries. Finally we use this list as the argument of `pd.DataFrame.from_records()` to convert the output to a dataframe. For the wine collection, this code is:

# In[73]:


myquery = winecollection.find({})
wine_text = dumps(myquery)
wine_records = loads(wine_text)
wine_df = pd.DataFrame.from_records(wine_records)
wine_df


# Like SQL, read operations in MongoDB can filter records based on logical conditions. Unlike SQL, MongoDB uses different symbols for the common logical operators, and these symbols need to be listed within the JSON formatted query.  A couple of the operators are implicit in the JSON syntax. To search on an equality condition, the general syntax is
# ```
# {'key' : value}
# ```
# For example, to find all of the wines in the database that are from virginia, we can use the following query:
# ```
# {'province' : 'Virginia'}
# ```
# The other implicit operator is "and", which is expressed simply by including more than one key-value pair within the syntax. To specify that a feature `key1` is equal to `value1` AND that `key2` is equal to `value2`, type:
# ```
# {'key1' : value1,
#  'key2' : value2}
# ```
# For example, to filter the data to Pinot Noir wines from Virginia, we can type
# ```
# {'variety' : 'Pinot Noir',
#  'province' : 'Virginia'}
# ```
# For all other logical operators, MongoDB uses special syntax, described below. To use these operators in a query, the general template is general syntax for using an operator within a MongoDB query is
# ```
# {'key' : {'$operator' : value } }
# ```
# The operators are listed in the following table:
# 
# | Operator                                                              | Syntax                                              | Example query                                                                                                      | Example code                                                                      |
# |-----------------------------------------------------------------------|-----------------------------------------------------|--------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------|
# | Equal to                                                              | implicit                                            | All wines with scores of 100                                                                                       | `{'points': 100}`                                                                 |
# | Greater than                                                          | `'$gt'`                                               | All wines that are more expensive than \\$30                                                                         | `{'price': {'$gt': 30}}`                                                            |
# | Greater than or equal to                                              | `'$gte'`                                              | All wines with scores of 95 or higher                                                                              | `{'points': {'$gte': 95}}`                                                          |
# | Less than                                                             | `'$lt'`                                               | All wines that are cheaper than \\$20                                                                                | `{'price': {'$lt': 20}}`                                                            |
# | Less than or equal to                                                 | `'$lte'`                                              | All wines with scores of 85 or lower                                                                               | `{'points': {'$lte': 85}}`                                                          |
# | Not equal                                                             | `'$ne'`                                               | Wines that are not red blends                                                                                      | `{'variety': {'$ne': 'Red Blend'}`                                                  |
# | And                                                                   | implicit                                            | All wines with scores of 100 and prices of \\$20 or less                                                             | `{'points': 100, 'price': {'$lte': 20}}`                                            |
# | Or                                                                    | `'$or': [{condition1}, {condition2}]`                 | All wines with scores of 100, or prices of \\$20 or less                                                             | `{'$or': [{'points': 100}, {'price: {'$lte': 20}}]}`                                  |
# | Exists in a set                                                       | `'$in': [value1, value2, ...]`                        | All wines from Virginia, Maryland, or North Carolina                                                               | `{'province': {'$in': ['Virginia', 'Maryland', 'North Carolina']}}`                 |
# | Not in a set                                                          | `'$nin'`                                              | All wines except those from Virginia, Maryland, and North Carolina                                                 | `{'province': {'$nin': ['Virginia', 'Maryland', 'North Carolina']}}`                |
# | Use logical conditions that compare two or more keys                  | `{'$expr': <expression>}`                             | All wines whose price is greater than their score                                                                  | `{'$expr': {'$gt': ['$price', '$points']}}`                                             |
# | Logical negation (only recommended for use with `$text` and `$regex`) | `'$not'`                                              | All wines whose descriptions do not contain the word "chocolate", treating capital and lower-case letters the same | `{'$not': {'description': {'$text': {'$search': 'chocolate', '$caseSensitive': false}}}}` |
# 
# To quickly see the data that is output by queries that use these operators, I write a function that takes a JSON dictionary as an input, and outputs a `pandas` dataframe:

# In[74]:


def mongo_read_query(col, q):
    qtext = dumps(col.find(q))
    qrec = loads(qtext)
    qdf = pd.DataFrame.from_records(qrec)
    return qdf


# To see all wines with a score of 100

# In[75]:


myquery = {'points': 100}
mongo_read_query(winecollection, myquery)


# To see wines with a score of 100 and a cost of less than \\$100, we can use the `$lt` operator:

# In[76]:


myquery = {'points': 100, 'price': {'$lt': 100}}
mongo_read_query(winecollection, myquery)


# To see wines that are from Ohio or North Carolina, we use the `$in` operator:

# In[77]:


myquery = {'province': {'$in': ['Ohio','North Carolina']}}
mongo_read_query(winecollection, myquery)


# To illustrate the "or" operator, we can query all wines that are either from Virginia, or have a score of 100:

# In[78]:


myquery = {'$or': [{'points': 100}, {'province': 'Virginia'}]}
mongo_read_query(winecollection, myquery)


# `$expr` requires an operator that compares two keys, and creates a sentence like "X is greater than or equal to Y". Next it requires a list that specifies what X in the sentence should be, then what Y should be. To search for all wines in which the price is greater than the score we use the `$expr` operator as follows:

# In[79]:


myquery = {'$expr': {'$gt': ['$price', '$points']}}
mongo_read_query(winecollection, myquery)


# In the previous section, we entered a record for a wine released by former NBA all-star Dwyane Wade, and we purposely included a nested structure in this JSON record. The `location` key has subkeys `region_1`, `region_2`, `province`, `country`, and `winery`:

# In[80]:


dwadewine


# To query a subrecord, use dot notation of the form `'key.subkey'` to identify the path to the value you need. To query for the winery name "D Wade Cellars", we can type:

# In[81]:


myquery = {'location.winery': 'D Wade Cellars'}
mongo_read_query(winecollection, myquery)


# ### Selecting Features
# A read query in MongoDB will return the entire JSON dictionary for every record that matches the query. Sometimes, however, the entirety of the data for one record will be more information than we can feasibly work with. In some situations there might be an unmanagable number of features contained within each dictionary, and we only want to use a couple of these features. In other situations a feature might contain values that are so large that we want to avoid dealing with this feature if possible.
# 
# To extract only a selection of the features, add a second JSON clause to the `.find()` method. The general syntax for selecting features is
# ```
# db.collection.find({query}, {'feature'=1}}
# ```
# where `{query}` is code, as described above, for extracting a selection of the records, and `{'feature'=1}` instructs MongoDB to include only the field named `feature` in the output. Alternatively, it is possible to list as many keys in this second clause as we want, so `{'feature1'=1, 'feature2'=1}` extracts `feature1` and `feature2`. In addition, setting the key equal to 0 instead of 1 instructs MongoDB to extract all features *except* the one specified with `'feature'=0`.
# 
# In the wine collection, we can extract only the titles of Merlot wines with the following code:

# In[82]:


cursor = winecollection.find({'variety': 'Merlot'}, {'title': 1})
qtext = dumps(cursor)
qrec = loads(qtext)
pd.DataFrame.from_records(qrec)


# By default, the only field that is extracted other than the ones we directly specify is `_id`, but we can exclude `_id` as well by typing

# In[83]:


cursor = winecollection.find({'variety': 'Merlot'}, {'title': 1, '_id': 0})
qtext = dumps(cursor)
qrec = loads(qtext)
pd.DataFrame.from_records(qrec)


# To keep the title, variety, points, and price, we type

# In[84]:


cursor = winecollection.find({'variety': 'Merlot'}, 
                             {'title': 1,
                             'variety': 1,
                             'points': 1,
                             'price': 1,
                             '_id': 0})
qtext = dumps(cursor)
qrec = loads(qtext)
pd.DataFrame.from_records(qrec)


# ### Updating Records
# Updating records in MongoDB is similar to selecting records in that we use the same logical conditions we use for selecting records for identifying the records we want to edit. The `.update_one()` method, applied to a collection, has two arguments. First we specify a logical condition that identifies the records we want to edit. Then we use the `$set` operator to choose specific fields within the existing JSON record to change. If we want, we can even write an entire replacement dictionary for this record, and write it along with `$set`. For example, to identify the record of the wine from Dwyane Wade's winery, we can query `{'location.winery': 'D Wade Cellars'}` as we did in the previous section. Suppose that we want to edit this record so that the price increases to \\$45. We can do so with the following code:

# In[85]:


winecollection.update_one({'location.winery': 'D Wade Cellars'},
                     {'$set' : {'price': 45}})
mongo_read_query(winecollection, {'location.winery': 'D Wade Cellars'})


# Suppose that we wanted to add a field that does not currently exist in the record, like `points`. We can use the same syntax to add fields:

# In[86]:


winecollection.update_one({'location.winery': 'D Wade Cellars'},
                     {'$set' : {'score': 90}})
mongo_read_query(winecollection, {'location.winery': 'D Wade Cellars'})


# We can change more than one field at a time within one call to the `$set` operator. To change both the score and the price of the Dwyane Wade wine, we can type:

# In[87]:


winecollection.update_one({'location.winery': 'D Wade Cellars'},
                     {'$set' : {'score': 95,
                               'price': 50}})
mongo_read_query(winecollection, {'location.winery': 'D Wade Cellars'})


# Suppose that the wine is reviewed by LeBron James, NBA star and noted [wine connoisseur](https://twitter.com/KingJames/status/1239424365621469184?s=20), who provided a new score and description. We can update the entire record by first defining a Python variable that contains the record:

# In[88]:


dwadewine2 = {'title': '2016 Napa Valley Three By Wade Red Blend', 
'description': "This wine is very good. Not as great as me. But plenty great enough for Miami.", 
'taster_name': 'LeBron James', 
'taster_twitter_handle': '@kingjames', 
'price': 45,
'score': 99,
'variety': 'Red Blend', 
'location':{
    'region_1': 'Napa Valley', 
    'region_2': None, 
    'province': 'California', 
    'country': 'U.S.', 
    'winery': 'D Wade Cellars'}}


# We can replace the existing record for this wine by specifying this dictionary as the second argument of the `.update_one()` method:

# In[89]:


winecollection.update_one({'location.winery': 'D Wade Cellars'},
                     {'$set' : dwadewine2})
mongo_read_query(winecollection, {'location.winery': 'D Wade Cellars'})


# A second method for editing records is `.update_all()` which revises every document that matches a query. I don't recommend using this method except in very specific cases, because it is easy to destroy large portions of a database with a mistyped query. But for the sake of illustration, suppose we wanted to change the names of the "Red Blend" varieties of wines to "R. Blend". We can do that with the following code:

# In[90]:


winecollection.update_many({'variety': 'Red Blend'},
                          {'$set': {'variety': 'R. Blend'}})
mongo_read_query(winecollection, {'variety': 'R. Blend'})


# ### Performing Text Searches
# One of the great advantages of a document store database is the ability to search through the text within the documents and extract records that match a certain pattern. A text search in MongoDB involves two steps:
# 
# * First, we will create a **text index**: a particular field in the records that contains the text we want MongoDB to search within.
# 
# * Second, we will use the `$text` operator within a call to `.find()` to specify the search terms.
# 
# To create a text index, we can use the syntax
# ```
# collection.create_index[('keytosearch', 'text')]
# ```
# We will replace `'keytosearch' with the name of the field in the JSON dictionaries on which we want to search, but we will leave `'text'` as is because this code tells MongoDB to search for text. The code to set the `description` field as the text index in the `winecollection` database is:

# In[91]:


winecollection.create_index([('description', 'text')])


# Now that we've set the text index, we can search the text in that field. The general syntax for a query with a text search is
# ```
# {'$text': {'$search': 'searchterms', '$caseSensitive': False}}
# ```
# where `'searchterms'` contains the terms we want to search for, and `'$caseSensitive': False` tells MongoDB to ignore cases in the search, so that a search term of "chocolate" also matches to "Chocolate". Alternatively, `'$caseSensitive': True` takes case into account when matching records to a query. If a search is not case sensitive, and if it is not diacritic sensitive (taking things like accents into account, which it can do by adding the `$diacriticSensitive=True` option), then `$search` matches on the **stems** of words: the [first several letters in the word](https://en.wikipedia.org/wiki/Stemming), allowing a search term of "blueberry" to also match with "blueberries".
# 
# As a simple example, now that `description` has been set as the text index, we can find all wines with descriptions that contain the word "chocolate". Here I save the output as a dataframe and display the description for the first wine in the output:

# In[92]:


df = mongo_read_query(winecollection, {'$text': {'$search':'chocolate', '$caseSensitive': False}})
df['description'][0]


# To search on more than one term, include the terms in the same string after `'$search'`, separated by spaces. By default, these terms are combined using the "or" operator, so that the query returns any document with at least one of the terms. The following code finds all wines whose descriptions contain "chocolate" or "leather":

# In[93]:


df = mongo_read_query(winecollection, {'$text': {'$search':'chocolate leather', '$caseSensitive': False}})
df[df['wine_id']==109396]['description'] # a leathery one


# To search for documents with a phrase that contains a space, enclose the phrase in double quotes, and precede each double-quote with an \ escape character. The following code captures descriptions with the phrase "very good":

# In[94]:


df = mongo_read_query(winecollection, {'$text': {'$search':'\"very good\"', '$caseSensitive': False}})
df['description'][0]


# To search for documents that contain multiple search terms at once (an "and" operator), enclose each search term in double quotes with escape characters. We can search for descriptions that contain both "leather" and "chocolate" with the following code: 

# In[95]:


df = mongo_read_query(winecollection, {'$text': {'$search':'\"leather\" \"chocolate\"', '$caseSensitive': False}})
df['description'][0]


# To exclude a term, we add a negative sign in front of the term we want to exclude. To find all wines whose descriptions contain the word "dark" but not "chocolate", we type

# In[96]:


df = mongo_read_query(winecollection, {'$text': {'$search':'dark -chocolate', '$caseSensitive': False}})
df['description'][0]


# Text searches can also be used to construct a search engine. We provide the search terms, and MongoDB generates a score for every document that represents the extent to which the search terms are relevant to the document. Once these scores have been generated, it is possible to sort the documents by the score to find the documents that are most highly related to the search terms.
# 
# To rank documents by search-relevancy, we add `{'score': {'$meta': 'textScore'}}` to the query we pass to the `.find()` method. Here we enter five search terms, "chocolate", "leather", "wood", "dark", and "smoke": 

# In[97]:


cursor = winecollection.find(
            {'$text': {'$search': 'chocolate leather wood dark smoke'}},
            {'score': {'$meta': 'textScore'}})


# Next we apply the `.sort()` method to the output, arranging the documents by relevancy score, with the following code:

# In[98]:


cursor.sort([('score', {'$meta': 'textScore'})]) 


# Finally we can convert the output to a dataframe with the following code:

# In[99]:


qtext = dumps(cursor)
qrec = loads(qtext)
df = pd.DataFrame.from_records(qrec)


# Among all the wine reviews in the data, here is the wine whose description had the highest relevancy score for "chocolate", "leather", "wood", "dark", and "smoke":

# In[100]:


df['description'][0]


# To wrap up our work with the database, we apply the `.close()` method to the MongoDB server:

# In[101]:


myclient.close()

