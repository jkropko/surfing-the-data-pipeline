# Reshaping and Merging Data and Working with Strings, Dates, and Times

```{contents} Table of Contents
:depth: 4
```

<div style= "float:left;position: relative; padding: 20px">
<a href="https://xkcd.com/1409/"><img src="https://i.imgflip.com/45ymyw.jpg" width="300"></a>
</div>

## Introduction: `pandas` or SQL?

As we saw in module 7, read operations in SQL not only extract data from a database, but they can select and rename columns, filter and sort rows, join tables, and aggregate data. With `pandas`, we can also select and rename columns, filter and sort rows, join tables, and aggregate data. So the question is, should we be using SQL or `pandas` to perform all these data manipulation steps? 

SQL is sometimes referred to as **server-side** data manipulation, because databases are often stored on remote servers and SQL queries are processed on the server instead on on a local machine. Data manipulation that is conducted using `pandas` on a local Python installation is called **client-side** data manipulation.

The question of SQL vs. `pandas` (or SQL vs. the tidyverse in R) is the subject of a lot of debate among professionals who use data. The question [comes up](https://www.quora.com/In-what-situations-should-you-use-SQL-instead-of-Pandas-as-a-data-scientist) [frequently](https://towardsdatascience.com/sql-and-pandas-268f634a4f5d) on [various](https://www.reddit.com/r/Python/comments/1tqjt4/why_do_you_use_pandas_instead_of_sql/) [coding forums](https://datascience.stackexchange.com/questions/34357/why-do-people-prefer-pandas-to-sql). Some [blog posts](https://blog.thedataincubator.com/2018/05/sqlite-vs-pandas-performance-benchmarks/) have tried to compare SQL and `pandas` in terms of the [speed](https://wesmckinney.com/blog/high-performance-database-joins-with-pandas-dataframe-more-benchmarks/) with which they complete equivalent operations, with differing results. [Tina Wenzel and Kavya Gupta](https://medium.com/carwow-product-engineering/sql-vs-pandas-how-to-balance-tasks-between-server-and-client-side-9e2f6c95677) note that many factors influence the relative speed of SQL and `pandas` operations, including the configuration of a PostgreSQL database and the bandwidth available in a network connection. They take the mixed evidence into account and conclude that

> SQL is the best tool to use for basic data retrieval and the better you know it, the more it will speed up your workflow. More advanced data manipulation tasks can be performed both on the server and client side and it is up to the analyst to balance the workload optimally.

In short, the existing evidence does not overwhelmingly support one option or the other as best practice for data manipulation. The reality is that both SQL and `pandas` are extremely useful and widely-used, and both tools will become part of your workflow. It will take some time and experience with end-to-end projects in data science to learn how to balance SQL and `pandas` in a way that is most comfortable for you in your workflow. But at this stage, there are some important points to keep in mind when thinking about these tools. 

First, there are many situations in which the question of SQL vs. `pandas` might be moot. For a given project, our data might not come from a database, but instead from a CSV file, from a JSON document acquired via an API, or from raw HTML that we scraped from a webpage. So in order to use SQL, we would have to take the additional step of creating a database. If we hold ourselves to the principles that E. F. Codd and others laid out about the organization of relational databases, it can take a significant amount of work to create this database. If there is no database involved for a specific data project, there is no role for SQL, but because `pandas` works on dataframes it can be a primary tool for data manipulation regardless of the original source for the data.

Second, while there are differences in speed, these differences only become a significant factor for projects that involve big data, and in those cases, we will almost certainly be working with data stored on remote servers. If the data are organized using a database, then SQL may well be faster than `pandas`, but it very much depends on how the database is [configured](https://severalnines.com/database-blog/guide-postgresql-server-configuration-parameters) and on the myriad factors that determine the speed with which code runs through a remote connection. `pandas` can also be used in scripts or Jupyter notebooks that are run on remote servers. Sometimes it makes sense to pull selections of remotely stored data into a local environment so that we can manipulate the data without having to seek permission from a database manager, and in that case, a mix of SQL to choose a selection and `pandas` to manipulate the local data can be very effective.

Third, `pandas` simply has more functionality and flexibility than SQL. For example, it is fairly straightforward to reshape (e.g. pivot) data using `pandas`, and it is [much more difficult to reshape data](https://stackoverflow.com/questions/2444708/sqlite-long-to-wide-formats) in SQL. `pandas` has better functionality for working with strings and time and date features than SQL, and `pandas`, being part of a Python environment, works well with any other Python package that works with dataframes or arrays. In contrast, while various DBMSs add specific additions to the base SQL language, SQL extensions tend to be fairly limited because of the inherent tension between expanding the functionality of a query language and staying close enough to base SQL to still be considered SQL. The easiest way to bring SQL query results into a Python enviromnent uses an `sqlalchemy` engine and the `pd.read_sql_query()` funtion from `pandas`. 

Fourth, both `pandas` and SQL enable us to work as part of larger teams that share tools, but we might choose or be required to use one tool over the other to work better as part of the team. `pandas` is essential for projects in which the whole team works within Python. SQL is readable and usable for people who do not use Python but still work with databases.

Fifth, and most importantly, the choice of SQL vs. `pandas` should be made based on how comfortable we feel with each tool. Both SQL and `pandas` can perform data manipulation correctly, and it will probably be the case that we can remember the code with one tool better than with the other. We should try as much as we can to do the work that comprises 80% of our time as data scientists more quickly.

For now, we need to practice both `pandas` and SQL and get comfortable with these tools, and we need to be flexible in the future as different situations will call for SQL or `pandas`.

## Joining Dataframes
Joining dataframes is also called merging dataframes, and I will use the words "join" and "merge" interchangeably below. Every kind of merge that is possible in SQL is possible in `pandas`: inner, outer, left, right, natural, cross, and anti-joins. One important difference between joining in SQL and merging in `pandas` is that dataframes might not be as carefully curated as data tables in a relational database, and we should not assume that the join worked properly even if there is no error. Primary keys might not uniquely identify rows in general, and joins might turn into cross joins. Some of values of keys that should match might not match due to differences in coding and spelling. And if we attempt a natural join, the wrong columns might be automatically selected as the keys.

Too many discussions of merging data provide clean examples. Here I will show you how merging works when the data contain some common problems that may invalidate the merge. In the following discussion, we will discuss how to perform merges in `pandas`, and also how to check that the merge worked in the way we want to.

First, for the following examples, we load these packages:

import numpy as np
import pandas as pd

### Example: Merging Data on U.S. State Election Results, Income, Economies, and Area
The "state_elections.csv" file contains information about the result of presidential elections by state for every presidential election between 1964 and 2004. In this dataset, the primary keys are `State` and `year`:

elect = pd.read_csv("https://github.com/jkropko/DS-6001/raw/master/localdata/state_elections.csv")
elect.head()

"state_income.txt" contains varous summary statistics (percentiles and means, broken down separately for men, for women, and for the overall population) about personal incomes within each state. In this dataset, the primary keys are `stcode` (the post office's two letter abbreviation for states) and `year`:

income = pd.read_csv("https://github.com/jkropko/DS-6001/raw/master/localdata/state_income.txt", sep="\t", header=2) # tab separated (note the header in this file)
income.head()

"state_economics.txt" contains information about the macro-level economy in each state and year, including overall and per capita gross domestic product, and GDP broken down by industry. In this dataset, the primary keys are `fips` (a standard numeric code that identifies countries and provinces within countries) and `year`:

econ = pd.read_csv("https://github.com/jkropko/DS-6001/raw/master/localdata/state_economics.txt", sep=";") # semi-colon separated
econ.head()

"state_area.csv" contains various measures of the total, land, and water areas of each state. In this dataset, the primary key is `state`:

area = pd.read_csv("https://github.com/jkropko/DS-6001/raw/master/localdata/state_area.csv") 
area.head()

Because the datasets above contain three ways to identify states - by name, with two-letter abbreviations, and with FIPS codes - we also need a dataset that matches each state by name to its abbreviation and FIPS code. Datasets that exist solely for the purpose of matching values of keys across datasets are called **crosswalks**:

crosswalk = pd.read_csv("https://github.com/jkropko/DS-6001/raw/master/localdata/crosswalk.csv")
crosswalk.head()

Our goal is to merge all five of these datasets together.

### Using the `pd.merge()` Function
When using a crosswalk to merge dataframes together, the first step is to merge a dataframe with the crosswalk. Here we start by joining the `elect` and `crosswalk` dataframes together. To join dataframes, we use the `pd.merge()` function. The following code works:

merged_data = pd.merge(elect, crosswalk, on='State')
merged_data

The `merged_data` dataframe now contains the features from `elect` and from `crosswalk`, which means we've added `stcode` and `fips` to the `elect` data, and that enables us to merge `merged_data` with `income` and `econ`.

Before moving on to the rest of the example, we should discuss some properties of the `pd.merge()` function. Recall from module 7 that there are many different kinds of joins that differ only in how they treat unmatched observations. `pd.merge()` conducts an inner join by default, leaving only the matched observations in the merged data. To change the type of merge, use the `how` argument:

`how='outer'` performs an outer or full join. It brings all rows from both dataframes into the merged data, and replaces the features for the unmatched rows with `NaN` for the columns without data.
```
merged_data = pd.merge(elect, crosswalk, on='State', how='outer')
```

`how='left'` performs a left join. It brings all rows from the first dataframe listed into the merged data, and only those in the second dataframe that are matched to the first.
```
merged_data = pd.merge(elect, crosswalk, on='State', how='left')
```

`how='right'` performs a right join. It brings all rows from the second dataframe listed into the merged data, and only those in the first dataframe that are matched to the second.
```
merged_data = pd.merge(elect, crosswalk, on='State', how='right')
```

There are two ways to specify the key or keys on which to match rows. If the key or keys have the same name in both dataframes, use the `on` argument. If there is one key, pass this name as a string to `on` like we did above. If there is more than one key, pass these names as a list to `on`. For example, if we merge on both `State` and `year`, we will type `on = ['State', 'year']`.

If the keys have different names in each dataframe, we use `left_on` to specify the names of these keys in the first dataframe listed in the `pd.merge()` function, and `right_on` to specify the names of these keys in the second dataframe listed. Suppose, for example, that the keys are named "State" and "year" in the first dataframe, and "st" and "yr" in the second dataframe. We would type `left_on = ['State', 'year'], right_on = ['st', 'yr']`.

Depending on the type of join we use, a row can be matched, or can come from just the first or just the second dataframe listed in `pd.merge()`. To see which rows come from which sources, specify `indicator='newname'`, where `'newname'` is a name you choose for a new column that contains this information. For example, the following code repeats the merge we performed above, but uses an outer join instead of an inner join and adds a column `matched` that tells us how each row is matched:

merged_data = pd.merge(elect, crosswalk, on='State', how='outer', indicator='matched')
merged_data

### Checking for Problems That Can Occur Without Errors
Whenever we apply `pd.merge()`, there's a great risk that the merge was incorrect even if the function runs without error. There are two ways that a merge can fail.

**Problem 1:** what we *thought* was a unique ID was not a unique ID. 

If we merge two dataframes on a column (or set of columns) that fail to uniquely identify the rows in either dataframe, then `pd.merge()` returns all pairwise combinations of rows with matching IDs. To see this, consider the following two example dataframes:

dict1 = {'id': ['A', 'A', 'B', 'B'],
         'data1': [150, 200, 50, 25]}
df1 = pd.DataFrame.from_dict(dict1)
df1

dict2 = {'id': ['A', 'A', 'B', 'B'],
         'data2': [-20, -75, -125, -250]}
df2 = pd.DataFrame.from_dict(dict2)
df2

Note that the two dataframes share a column "id", but that "id" is not a unique identifier in either dataframe. If I try to merge the two based on "id", the result is:

df_merge = pd.merge(df1, df2, on='id')
df_merge

Because we did not have a unique ID in either dataframe, we artificially increased the number of rows from 4 to 8. At first glance, the merged data looks nice, but with double the number of rows we are supposed to have the data is in fact corrupted, and we cannot use it for any subsequent analysis. Also, note that the merge ran without any errors. If we aren't careful, we might move forward with data that cannot be used.

The above example is an instance of a **many-to-many** merge, in which rows in the left dataframe can match to more than one row in the right dataframe, and rows in the right dataframe can match to more than one row in the left dataframe. In these cases `pandas` performs a cross join within the subsets of the two dataframes that share the same key, inflating the number of rows. But a many-to-many join is almost never what we want to do with data, and if it happens, it is usually a mistake.

The other types of merges are 
* **one-to-one**, in which every row in the left dataframe matches to at most one row in the right dataframe, and every row in the right dataframe matches to at most one row in the left dataframe,
* **many-to-one**, in which rows in the left dataframe can match to more than one row in the right dataframe, and every row in the right dataframe mnatches to at most one row in the left dataframe,
* and **one-to-many**, in which every row in the left dataframe matches to at most one row in the right dataframe, and rows in the right dataframe can match to more than one row in the left dataframe.

The best way to prevent this mistake is to first think about whether the two dataframes should constitute a one-to-one, many-to-one, or one-to-many merge. It is important to have a clear expectation. Then use the `validate` argument to have `pandas` automatically check to see whether this expectation is met. If not, the code will generate an error, which will bring our attention to problems in the data we might not have caught otherwise. If we write

* `validate = 'one_to_one'` then `pandas` checks to see whether the merge keys are unique in both dataframes,
* `validate = 'many_to_one'` then `pandas` checks to see whether the merge keys are unique in the right dataframe,
* `validate = 'one_to_many'` then `pandas` checks to see whether the merge keys are unique in the left dataframe.

There are many reasons why our expectations might be incorrect. In messy, real-world data, mistakes like duplicated keys often make it past review processes and exist in the data without any clue of it in the codebook. The `validate` argument is an important check for these kinds of issues. For example, we expect that merging `elect` and `crosswalk` will be a many-to-one merge, so we confirm that the merge is many-to-one as follows:

merged_data = pd.merge(elect, crosswalk, on='State', how='outer', 
                       indicator='matched', validate='many_to_one')
merged_data

**Problem 2**: rows should be matched, but aren't.

This problem is especially common when matching on strings, such as names. With countries, it's possible for one dataframe to write "USA" and the other to write "United States". You will have to go back into a dataframe to edit individual ID cells so that they match. But to identify the cells that need to be edited, we have to construct a dataframe of the rows that were unmatched in one or the other dataframe. The easiest way to see this is to use an anti-join: a merge that keeps only the rows in the left dataframe that have no match in the right dataframe. Like SQL, there is no anti-join function built in to `pandas`, but there are ways to program our own anti-join. The easiest way is to perform an outer join with the `indicator='matched'` argument, then to filter the data to those rows for which `matched` is not equal to "both". 

For this step, I recommend creating a second, working version of the data `merge_test` to contain the first attempt at the merge. If there are issues, it is easier to fix the problems and recreate the working dataframe than to restart the kernel. If there are no problems, then we can assign the `merged_data` dataframe to be equal to the working version.

merge_test = pd.merge(elect, crosswalk, on='State', how='outer', indicator='matched', validate='many_to_one')
merge_test.query("matched!='both'")

There are no rows in `crosswalk` with no match to `elect`, and there are no rows in `elect` without a match in `crosswalk`. But if there were unmatched rows, there are two reasons why some rows may have been unmatched: rows can be unmatched due to differences in coverage, and they might be unmatched due to differences in coding or spelling. `pandas` cannot tell the difference between these two reasons why rows might be unmatched, and an inner join will drop unmatched rows regardless of the reason. Using an outer join with `indicator='matched'` is best practice for seeing the unmatched rows and thinking about whether any rows that should be matched are for some reason unmatched. We can use the category relabeling functionality in `pandas` to fix issues of mispelled and miscoded keys, as we will do in the examples in the next section.

After performing this check, if we intend to perform another merge, we will either need to choose a new name for the indicator column, or we can drop the `matched` column so that we can reuse this name later. We set `merged_data` to the working dataframe `merge_test` without the `matched` column:

merged_data = merge_test.drop('matched', axis=1)

### Merging all of the Dataframes Together While Checking for Problems
The `merged_data` and `income` dataframes share keys named `stcode` and `year`. Joining these two dataframes should be a one-to-one merge because there should be only one occurrence of the same state and year in each dataframe. We use `how='outer'` and `indicator='matched'` (since we deleted the previous `matched` column) to enable us to filter the result to the unmatched rows, and we use `validate='one_to_one'` to catch anomolies that violate our expectation that this is a one-to-one merge:

merge_test = pd.merge(merged_data, income, on=['stcode','year'], how='outer', indicator='matched', validate='one_to_one')
merge_test.query("matched!='both'")

There are no unmatched rows so there are no issues with miscoded or mispelled ID values. The merged data now contain information on both state election results and state incomes:

merge_test

Since there are no problems, we set `merged_data` equal to `merge_test`. Because we intend to merge the data with another dataframe, we drop the `matched` column. 

merged_data = merge_test.drop('matched', axis=1)

Next we merge this result with the `econ` dataframe. These two dataframes share `fips` and `year` as keys, and should also be a one-to-one merge. We check to see whether there are unmatched rows:

merge_test = pd.merge(merged_data, econ, on=['fips','year'], how='outer', indicator='matched', validate='one_to_one')
merge_test.query("matched!='both'")

Again, there are no unmatched rows so there are no issues with miscoded or mispelled ID values. The merged data now contain information on state election results, state incomes, and state economies:

merge_test

Again, we set `merged_data` equal to `merge_test`, dropping the `matched` column so that we can reuse this name in the next join:

merged_data = merge_test.drop('matched', axis=1)

Finally we merge the data with the `area` dataframe. This merge matches `State` in `merged_data` to `state` in area: this subtle difference is easy to miss and will result in an error if we fail to notice the lowercase s and write `on='State'`. This merge should be a many-to-one merge, as there are many rows for each state in `merged_data` (for many years), but only one row for each state in `area`. As 

merge_test = pd.merge(merged_data, area, how="outer",
                      left_on='State',right_on='state', 
                      indicator='matched', 
                      validate='many_to_one')
merge_test.query("matched!='both'")[['State', 'state',
                                     'year','matched']]

In this case, one of our validation checks failed: we have unmatched rows. Some of these rows are due to differences in coverage: we will not bring Puerto Rico, the Northern Mariana Islands, the United States Virgin Islands, American Samoa, Guam, or the United States Minor Outlying Islands into the merged data as these territories do not receive votes in the electoral college. We will however bring the District of Columbia into the merged data as D.C. does get 3 votes in the electoral college. D.C. is unmatched due to spelling discrepancies, and we must correct this mistake before we can proceed. The easiest way to fix the error is to replace values of "District of Columbia" in the `area` dataframe with "D. C.", as it is written in the merged data. We can use the `.replace()` method (because we only want to replace one `state` category and `.replace()` leaves unlisted categories alone, as opposed to `.map()` which would replace unlisted categories with missing values), as we discussed in module 8:

area.state = area.state.replace({'District of Columbia':'D. C.'})

Now if we repeat the test, we will only see the rows that are unmatched due to differences in coverage:

merge_test = pd.merge(merged_data, area, left_on='State', how="outer", right_on='state', indicator='matched', validate='many_to_one')
merge_test.query("matched!='both'")[['State', 'state','year','matched']]

We replace the `merged_data` dataframe with `merge_test`, keeping only the rows for which `matched='both'`, then dropping the `matched` column:

merged_data = merge_test.query("matched=='both'").drop('matched', axis=1)

Now `merged_data` contains all of the data we need, including state election results, income, economic data, and area:

merged_data

## Reshaping Data
**Reshaping** a dataframe refers to turning the rows of a dataframe into columns (also known as a long-to-wide reshape), or turning columns into rows (also known as a wide-to-long reshape), in a way that cannot be accomplished by simply transposing the data matrix. It is also called **pivoting** for a long-to-wide reshape, **melting** for a wide-to-long reshape. It's a notoriously tricky skill to master, and it helps a lot to understand every part of the function we need, so that we're not blindly trying every combination of parameters hoping one of these combinations works.

### Example: Gross domestic product by state, 1997-2015
To demonstrate the method for pivoting a dataframe, we use example data from the U.S. Bureau of Economic Affairs (www.bea.gov) on economic output for the American states. We load the data, skipping the last four rows as these rows contain attribution information and notes, and are not part of the data. We also use the `.str.strip()` method to remove all the leading and trailing whitespace in the `Description` column: 

gsp = pd.read_csv("https://github.com/jkropko/DS-6001/raw/master/localdata/gsp_naics_all.csv", skipfooter=4)
gsp['Description'] = gsp['Description'].str.strip()
gsp

For this example, we only want to save three features besides the primary keys:

* state GDP,
* state GDP per capita,
* state GDP from private industries

We only want the 50 states, no regions, territories, or districts (sorry DC!). Notice that the features we want are contained in rows, and the years are contained in columns. We need to switch that: the features must be in columns, and years must be stored in the rows. We will need to perform both a wide-to-long and a long-to-wide reshape. In addition, we will give the columns concise but descriptive names, and we will create a new column that contains the percent of GDP from private industry in each state and each year.

First we need to reduce the data to only the features we need: state GDP, state GDP per capita, and state GDP from private industries. Right now, however, the features are not stored in the columns, but in the rows. Specifically, the data we need are contains in the rows in which `Description` is "All industry total" or "Private industries" and `ComponentName` is "Gross domestic product (GDP) by state" or "Per capita real GDP by state". We use `.query()` to isolate these rows:

gsp_clean = gsp.query(
    "Description in ['All industry total', 'Private industries']"
).query(
    "ComponentName in ['Gross domestic product (GDP) by state','Per capita real GDP by state']")
gsp_clean

Next, we only want the 50 states, no regions, territories, or districts, so we issue another `.query()` to remove the territories. To see these non-states, we call up a list of the unique values of `GeoName`:

gsp_clean['GeoName'].unique()

We need to remove the rows in which `GeoName` is "United States", "District of Columbia", "New England", "Mideast", "Great Lakes", "Plains", "Southeast", "Southwest", "Rocky Mountain", or "Far West":

gsp_clean = gsp_clean.query("GeoName not in ['United States', 'District of Columbia', 'New England', 'Mideast', 'Great Lakes', 'Plains', 'Southeast', 'Southwest', 'Rocky Mountain', 'Far West']")
gsp_clean

### Melting: Turning Columns to Rows
Notice that many of the columns refer to particular years. We want to move these columns to the rows, so that each state has one row for each year covered in the data. The best function to use when we need to turn columns into rows is `pd.melt()`:
```
pd.melt(df, id_vars, value_vars)
```
This function takes three parameters:

1. The name of the dataframe you wish to edit

2. `id_vars`: A list of the names of the columns that we want to continue to exist as columns after the dataframe is melted. In our example, this list will contain both IDs that currently uniquely identify the rows (`GeoName`, `ComponentName`, `Description`), synonyms for the IDs (`GeoFIPS`) that we want to keep, and features that vary across ID but not across the columns (`Region`).

3. `value_vars`: A list of the names of the columns we want to store in the rows. If the columns have numeric names and can be sequentially ordered, as is the case in our example with years, a shortcut for creating a list of these column names is `[str(i) for i in range(1997,2015)]`, which loops over intergers from 1997 to 2015, placing each year as a string in the list.

Any column that is not listed under either `id_vars` or `value_vars` will be deleted in the melted data. 

For example, we melt the `gsp_clean` dataframe with the following code:

gsp_clean = pd.melt(gsp_clean, id_vars = ['GeoName', 'GeoFIPS', 'Region',
                             'ComponentName', 'Description'], 
        value_vars = [str(i) for i in range(1997,2015)])
gsp_clean

Note that the old column names (1997 through 2015 in this case) will always by stored in a column named "variable" after melting, and the datapoints that populated those columns will be contained in a column named "value". 

Before moving on, let's rename some of the columns to avoid confusion in the next step:

gsp_clean = gsp_clean.rename({'GeoName':'State',
                             'GeoFIPS':'FIPS',
                             'variable':'Year'}, axis=1)
gsp_clean

### Pivoting: Turning Rows to Columns
The rows contain features that we want to move to the columns. Specifically, we need separate columns for the different combinations of `ComponentName` and `Description` since the feature names are contained in two columns, so we can combine these two columns by concatenating them together and creating a new column called "feature". Then we can drop `ComponentName` and `Description`:

gsp_clean = gsp_clean.assign(feature = gsp_clean['ComponentName'] + gsp_clean['Description'])
gsp_clean = gsp_clean.drop(['ComponentName', 'Description'], axis=1)
gsp_clean

To move these features from the rows to columns, apply the `.pivot_table()` method to a dataframe:
```
df.pivot_table(index, columns, values)
```
To understand this method, pay close attention to its parameters:

1. `index` - a list containing the names of the current columns that we want to remain columns in the reshaped data. These include the primary keys (`State` and `Year` in this example), synonyms for a key (`FIPS`), and features that vary only by ID (`Region`).

2. `columns` - the name of the column that contains the **names** of the new columns we are trying to create.

3. `values` - the name of the column that contains the **datapoints** we are trying to move to the new columns.

There is one important issue to keep in mind when using the `.pivot_table()` method. `.pivot_table()` contains default behavior to handle cases in which the keys in `index` do not uniquely identify the rows of a dataframe. By default, `.pivot_table()` takes the mean within group. If the column specified within `values` is non-numeric, however, the mean is not defined. So first make sure that any columns that are numeric are recognized as a numeric data type. If a column contains text, categories, or other non-numeric data, specify `aggfunc='first'` inside `.pivot_table()`. Writing `aggfunc='first'` tells `.pivot_table()` to use the first cell within a group instead of calculating the mean within a group, and the first cell is defined for non-numeric columns. If the columns in `index` do uniquely identify rows, there is only one cell per group anyway, so it is fine to take the first cell.

Presently within `gsp_clean` the datapoints are contained within the `value` column. Unfortunately, `value` is not currently understood to be numeric:

gsp_clean.dtypes

Following our code from module 8, we convert value to a numeric class:

gsp_clean.value = gsp_clean.value.astype('float')
gsp_clean.dtypes

 Now we can reshape the data with `.pivot_table()`:

gsp_clean['value'] = gsp_clean['value'].astype(int) # first convert this column to int 
gsp_clean = gsp_clean.pivot_table(index=['State','FIPS', 'Region','Year'], 
                                  columns='feature', 
                                  values='value')
gsp_clean

Alternatively, if we choose to leave the `value` column as an `object` data type, we can use this code instead to perform the wide-to-long reshape:
```
gsp_clean = gsp_clean.pivot_table(index=['State','FIPS', 'Region','Year'], 
                                  columns='feature', 
                                  values='value', 
                                  aggfunc='first')
```
Note that the dataframe is not formated in a flat way, because the IDs and related features are stored in the row-indices instead of in columns. To convert the dataframe back to a standard format, use the `.to_records()` method within the `pd.DataFrame()` function:

gsp_clean = pd.DataFrame(gsp_clean.to_records())
gsp_clean

All that's left to clean the data is to rename the columns and to create a new column containing the percent of the state's GDP that comes from private industry:

gsp_clean = gsp_clean.rename({'Gross domestic product (GDP) by stateAll industry total':'GDP',
                             'Gross domestic product (GDP) by statePrivate industries':'GDPprivate',
                             'Per capita real GDP by stateAll industry total':'GDPpc'}, 
                             axis=1)
gsp_clean = gsp_clean.assign(percent_private = 100* gsp_clean.GDPprivate / gsp_clean.GDP)
gsp_clean

## Working with Strings (Example: the 2019 ANES Pilot Study)
In module 8, we worked with the 2019 American National Election Study pilot survey and saved the cleaned data in a separate CSV file:

anes = pd.read_csv("https://github.com/jkropko/DS-6001/raw/master/localdata/anes_clean.csv")
anes

The data contain a column `most_important_issue` which records individuals' responses to the question of what they feel is the most important issue facing the United States as of December 2019. These responses are in the respondents' own words. For example, one response is

anes.most_important_issue[5]

These responses are strings, and we can employ the suite of string operations to manipulate the data in this column. String methods are contained in the `.str` module of `pandas`, and we will have to call the `.str` attribute in order to use string methods.

One important technique is to alter the case within the text so that we can identify words without worrying about case sensitivity. To turn all responses to lowercase, use `.str.lower()`:

anes.most_important_issue.str.lower()

And to turn all the text to uppercase, use `.str.upper()`:

anes.most_important_issue.str.upper()

One issue that can inhibit our ability to search through text is the existence of leading and trailing whitespace in the responses. White space can exist, invisibily, for several reasons. It is possible that the data authors included white space in order to standardize the number of spaces that the column takes up in the data file. To remove both leading and trailing white spaces, use `.str.strip()`

anes.most_important_issue = anes.most_important_issue.str.strip()

The `str.replace()` method finds and replaces specific whole strings with different strings. For example, we can replace every response that reads "health care" with "hospital stuff":

anes.most_important_issue.str.lower().replace('health care', 'hospital stuff')

If we want to replace pieces of these strings, we can specify the `regex=True` argument. The following line of code replaces all occurrences of "trump" when the strings are converted to lowercase to "twimp". With `regex=True`, the method replaces the pattern "trump" anywhere it appears, as opposed to the default `regex=False` which only replaces entire entries that are exactly "trump":

anes.most_important_issue.str.lower().replace('trump', 'twimp', regex=True)

To create a new column that identifies when particular words are used, use either the `.str.match()` or `.str.contains()` method. `.str.match()` is true if the entire entry matches the provided string, 

anes.most_important_issue.str.lower().str.match('trump')

and `.str.contains()` is true if the provided string exists anywhere within the entry. 

anes.most_important_issue.str.lower().str.contains('trump')

These columns of logical values can be placed into the data to filter or for other purposes. For example, we can see the number of Democrats, Republicans, and independents who use the word "trump" in their statement of the country's most important problem:

anes['problem_trump'] = anes.most_important_issue.str.lower().str.contains('trump')
pd.DataFrame(anes.groupby(['partyID', 'problem_trump']).size().unstack())

The `.str.replace()`, `.str.match()`, and `.str.contains()` methods can also accept regular expressions for identifying additional patterns within the string. Regular expressions are beyond our scope in this document, but here is a [good discussion of regular expressions in Python](https://docs.python.org/2/howto/regex.html).

To calculate the length of each response in terms of the number of characters, use `.str.len()`. In this case, it is important to make sure the whitespace is removed first with `.str.strip()`, otherwise the spaces will count towards the length: 

anes.most_important_issue.str.len()

We can use the length to display, for example, the single longest response in the data. To display the whole string, turn off the display limit by typing `pd.options.display.max_colwidth = None`. Here I set the limit to 500, because it sort of goes off the rails and I'd rather not display it:

anes['length'] = anes.most_important_issue.str.len()
pd.options.display.max_colwidth = 500
anes.sort_values(by = 'length', ascending = False).most_important_issue.head(1)

After all that, we set the string display limit back to the default of 50 characters:

pd.options.display.max_colwidth = 50

In some cases it might be necessary to split entries into different features according to a delimiter or pattern. It doesn't make sense to split the `most_important_problem` column in this example, but as an illiustration, we can split the responses on periods:

anes.most_important_issue.str.split('.')

The `expand=True` argument displays these split strings in different columns in a dataframe:

anes.most_important_issue.str.split('.', expand=True)

Writing `n=1` only splits on the first occurrence of the delimiter, `n=2` splits on the first and second occurrence, and so on:

anes.most_important_issue.str.split('.', expand=True, n=2)

An individual string can be indexed according to character number. These indices can be applied to every entry in a string column as well. To pull just the first five characters out of each response in `most_important_issue`, we can type:

anes.most_important_issue.str[0:5]

To pull characters 6 through 10, we type

anes.most_important_issue.str[6:11]

To pull the last four characters, use a negative number to begin the range, and leave the end of the range blank:

anes.most_important_issue.str[-4:]

## Working with Dates and Times (Example: Twitter)
In module 4 we discussed Twitter as an example of how to use an API in Python. We save the four credentials we need to access the API (the consumer key, the consumer secret, the access token, and the access token secret) in a .env file, and we load those keys into Python without displaying them in our notebooks by using the `dotenv` package:

import dotenv
import os
os.chdir('/Users/jk8sd/Box Sync/Practice and Applications 1 online/Module 9 - Data Managenent in pandas Part 2')
dotenv.load_dotenv()
ConsumerKey = os.getenv('ConsumerKey')
ConsumerSecret = os.getenv('ConsumerSecret')
AccessToken = os.getenv('AccessToken')
AccessTokenSecret = os.getenv('AccessTokenSecret')

Then we use the `tweepy` package to work with the Twitter API and we create a Twitter cursor with our credentials:

import tweepy
auth = tweepy.OAuthHandler(ConsumerKey, ConsumerSecret)
auth.set_access_token(AccessToken, AccessTokenSecret)
api = tweepy.API(auth)

The following code extracts 1000 tweets that contain the hashtag "#uva":

msgs = []
msg =[]

for tweet in tweepy.Cursor(api.search, q='#uva').items(1000):
    msg = [tweet.text, tweet.created_at, tweet.user.screen_name] 
    msg = tuple(msg)                    
    msgs.append(msg)

tweets = pd.DataFrame(msgs, columns = ['text', 'created_at', 'user'])
tweets

### Extracting Year, Month, Day, and Time from a Timestamp Column
Note that the data contain timestamps that include the date and time, to the second, of each tweet. The `created_at` column has a `datetime64` data type:

tweets.dtypes

The difference between a `datetime64` data type and an `object` or numeric type is that we have the ability to extract individual elements of time from a `datetime64` value. To pull out the year, month, day, hour, minute, and second of the timestamp, we use the following attributes:

[tweets.created_at[0].month, tweets.created_at[0].day, 
 tweets.created_at[0].year, tweets.created_at[0].hour, 
 tweets.created_at[0].minute, tweets.created_at[0].second]

The easiest way to create new columns with these elements for all the values in the dataframe is to use comprehension loops:

tweets['month'] = [x.month for x in tweets.created_at]
tweets['day'] = [x.day for x in tweets.created_at]
tweets['year'] = [x.year for x in tweets.created_at]
tweets['hour'] = [x.hour for x in tweets.created_at]
tweets['minute'] = [x.minute for x in tweets.created_at]
tweets['second'] = [x.second for x in tweets.created_at]
tweets

### Generating Timestamps from Separate Month, Day, and Year Columns
Sometimes raw data will come to us with these time elements already placed in separate columns, so that we have a `month`, `day`, and `year` column but no `date` column. There are important advantages to placing all this information in one column in values that Python understands as timestamps: timestamps are easier to filter, manipulate, index, and plot. To create one timestamp from separate columns that contain the month, day, and year (and optionally the hour, minute, and second), use the `pd.to_datatime` function:
```
pd.to_datetime(df)
```
where `df` is a subset of the dataframe that contains the separate columns for the time elements. In order for this function to work, these columns must be named `year`, `month`, and `day`, and optionally `hour`, `minute`, and `second`. If these columns are named something else, first use the `.rename()` method to change the names to the ones listed above.

To create a timestamp from the individual time element columns, we can type:

tweets['timestamp'] = pd.to_datetime(tweets[['year', 'month', 'day', 'hour', 'minute', 'second']])
tweets

Like `created_at`, the new `timestamp` column is also of the `datetime64` data type:

tweets.dtypes

### Converting String Columns to Timestamps
Sometimes information about the date and time of an event in the data will be coded as a string. In that case, to use the time series functionality on the dates in a dataframe, a string column that contains the dates and times will need to be converted to the `datetime64` data type. The best way to do that is to use the `pd.to_datetime()` function once again. This time, we pass the column that contains the dates in string format to the `pd.to_datetime()` function. This function can identify the year, month, day, hour, minute, and second from many different formats. 

For example, we can write the date Sunday, June 19, 2016 at 8:00 PM (the date and time of game 7 of the 2016 NBA finals, the greatest moment in sports history) in many different ways such as:

* "Sunday, June 19, 2016, 8:00 PM"
* "6-19-2016 8PM"
* "6/19/16 8 p.m."
* "19/6/16 8pm"

The `pd.to_datetime()` function reads all of these formats:

pd.to_datetime("Sunday, June 19, 2016, 8:00 PM")

pd.to_datetime("6-19-2016 8PM")

pd.to_datetime("6/19/16 8 p.m.")

pd.to_datetime("19/6/16 8pm")

The `pd.to_datetime()` function can feel like a magic trick because it automatically detects where the different elements of the date and time are located in the string. However, it can go wrong, and it is important to check that the date was correctly understood by `pd.to_datetime()`. Suppose for example that the date was June 19, 1945, coded as "6/19/45". `pd.to_datetime()` reads the date as 2045:

pd.to_datetime("6/19/45")

The easiest way to fix this problem would be to break the timestamp up into separate columns for year, month, and day, subtract 100 from the years that were placed in the wrong century, and recombine these columns into a new timestamp with `pd.to_datetime()`. But the real danger here is assuming the `pd.to_datetime()` function worked without confirmation.

The `pd.to_datetime()` function also works on an entire column of dates coded as strings. For example, let's convert the `created_at` column to string:

tweets['created_at'] = tweets.created_at.astype('str')
tweets.dtypes

To convert the `created_at` column back to a timestamp, we can apply `pd.to_dataframe()`:

tweets['created_at'] = pd.to_datetime(tweets.created_at)
tweets.dtypes

### Filtering Rows Based on Date Ranges
If every row in the data has a unique timestamp, then one convenient way to use the times to filter the data is to set the **index** (the row labels) to be equal to the timestamps:

tweets.index = tweets['created_at']

A `pandas` dataframe uses `pd.to_datetime()` to read dates and times in many formats, and we can pass any of these formats to the index of `tweets`. For example, to see all the tweets made on June 30, we can type:

tweets['June 30, 2020']

If these row labels are in chronological order, then we can extract slices of the data that fall within a time range. We write two dates separated by a colon, and the output extracts all rows from the row that matches the first date through the row that matches the last date. Because the rows are generally listed with the most recent ones first, we write the ending timestamp first and the ending timestamp second. If these exact dates and times do not exist in the data, the syntax still finds the locations where these rows would exist and extracts the rows in between these two locations. Here is code to extract all tweets that were posted between 2pm and 3pm on June 29:

tweets['6/29/2020 15:00':'6/29/2020 14:00']

To extract all tweets before point in time, write the timestamp before the colon and write nothing after the colon. To extract all tweets after a point in time, write nothing before the colon and write the timestamp after the colon. To extract all tweets posted after June 29 at 3pm:

tweets[:'6/29/2020 15:00']

### Leads and Lags
In time series data in which the rows represent particular points in time in descending chronological order, a **lag** is a column that contains the values of another column shifted up one cell. That is, if the rows represent days, and a column represents today's high temperature, the lag represents yesterday's high temperature. A **lead** is a existing column with its values shifted one row down: tomorrow's high temperature. 

To create a lead or a lag, apply the `.shift()` method to a dataframe. The argument of `.shift()` is an integer: positive integers shift values down, creating leads, and negative values shift values up, creating lags. Whenever we shift values up or down, we create new missing values at the top or bottom of the dataframe for the lead or lagged column. 

For example, in the `tweets` dataframe we can create two new columns, `previous_tweet` and `next_tweet` to compare with `text` by using `.shift(-1)` and `.shift(1)`:

tweets['previous_tweet'] = tweets.shift(-1).text
tweets['next_tweet'] = tweets.shift(1).text
tweets[['text', 'previous_tweet', 'next_tweet']]