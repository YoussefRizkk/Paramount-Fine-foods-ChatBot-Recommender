#!/usr/bin/env python
# coding: utf-8

# ### Import Libraries: 

# In[1]:


import pandas as pd 
import seaborn as sns 
import numpy as np

import matplotlib
import matplotlib.pyplot as plt
plt.style.use('ggplot')
from matplotlib.pyplot import figure

get_ipython().run_line_magic('matplotlib', 'inline')
matplotlib.rcParams['figure.figsize']=(12,8) 


# ### Upload and read the data :

# In[2]:


df = pd.read_csv('movies.csv')


# ### Explore Date 

# In[4]:


df.head()


# #### Missing Values 

# In[5]:


# Missing values in columns: 
df.isnull().sum()


# #### Percentage of missing values in columns:

# In[6]:


for col in df.columns:
    pct_missing = np.mean(df[col].isnull())      # kl she 7seb mnst3mllo numoy(np),ma fyyi 3yyt lal column bala 7ddid 
    print('{} - {}%'.format(col, round(pct_missing*100)))  # 2bl ma 3yytlo mn 2yya dataframe 3m 3yytlo
    # See above print, b7t l2shya lfized l7al, brj3 sho bddi 7ot jowwetha b7ttn 3a jnb b3d klmt .format()


# #### Data type for each column: 

# In[7]:


df.dtypes


# #### Deleting NULL rows: 

# In[3]:


df_new= df.dropna()


# #### Change data type of some columns

# In[4]:


#### We notice that the data type of budget,gross,votes,runtime is float64, but the number after the comma is zero
#### to get rid of that, we change the datatype to integer, this nethod wouldn't be ahieved if there are still null values
df_new[['budget','gross','runtime','votes']]=  df_new[['budget','gross','runtime','votes']].astype('int64')


# In[5]:


df_new[['budget','gross','runtime','votes']]


# #### Sort the rows by descending order of gross:

# In[23]:


df.sort_values(by=['gross'],inplace=False, ascending=False)


# #### Showing all the data results

# In[25]:


# We noticed from the above results that sine we have many rows to present, we got first several rows then three points
# then last several rows, but if I want to show all the data results: 
pd.set_option('display.max_rows',None)
# Now, let's try the same above code: 
df.sort_values(by=['gross'],inplace=False, ascending=False)


# #### Extract Distinct Values

# In[27]:


# If we want to know the names of companies in our dataframe, so I want the distinct values only, 
# I want to see the name of each company only one time: 
df['company'].drop_duplicates().sort_values(ascending=False)


# #### Drop any duplicates

# In[6]:


df.drop_duplicates 


# #### Correlation between 'gross' & 'budget' 

# #### Correlation Scatter-plot

# In[7]:


# To get the correlation, we build a scatter plot: 

plt.scatter(x=df['budget'],y=df['gross'])

plt.title('Budget vs Gross earnings')
plt.xlabel('Budget')
plt.ylabel('Gross earnings')
plt.show()


# #### Correlation Regression plot 

# In[8]:


# from the above graph, it seems that they are positively correlated, but we should have a regression plot to tell:
# Regreesion plot is done by seaborn library
sns.regplot(x='budget',y='gross',data=df,scatter_kws= {"color":"red"},line_kws={"color":"blue"})

# From the below results, we notice from the line ( going-up line) that the correlation is positive.


# #### Correlation; how much correlated

# In[12]:


# We knew that bufget and gross are positively correlated, but how much are they correlated: 
# The following shows the correlation between all the columns, not just budget and gross
df_correlation = df.corr()
df_correlation
# We have three methods for correlation: pearson, kendall, spearman, by default is is pearson, they are 
# similar but differs a little, if I want to choose a specific method: df.corr(method='kendall')...


# #### Correlation matrix

# In[13]:


sns.heatmap(df_correlation, annot=True)
plt.title('Correlation matrix for numeric features')
plt.xlabel('Movies Features')
plt.ylabel('Movie Features ')
plt.show()


# #### Correlation in a more readable way, neat way 

# In[17]:


correlation_pairs = df.corr().unstack()
correlation_pairs 


# #### High and low correlations 

# In[28]:


high_correlation = correlation_pairs[(correlation_pairs) >0.5]
high_correlation


# In[29]:


low_correlation = correlation_pairs[(correlation_pairs) <0.5]
low_correlation


# #### Correlation, Numeric presentation of strings 

# In[14]:


# We have columns that are not numeric but we want to see the correlation between them 
#and other numeric columns so we transform all non-numeric columns to numeric columns:
df_numerized = df

for col_name in df_numerized.columns:
    if(df_numerized[col_name].dtype == 'object'):
        df_numerized[col_name] = df_numerized[col_name].astype('category')
        df_numerized[col_name] = df_numerized[col_name].cat.codes
        
df_numerized


# In[15]:


df_numerized.corr()


# In[ ]:


sns.heatmap(df_numerized, annot=True)
plt.title('Correlation matrix for numeric features')
plt.xlabel('Movies Features')
plt.ylabel('Movie Features ')
plt.show()  

# WE didn't run this command, because it was taking alot of time. 


# In[ ]:





# In[ ]:




