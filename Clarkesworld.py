#!/usr/bin/env python
# coding: utf-8

# # Clarkesworld
# 
# Source: https://clarkesworldmagazine.com/
# 
# Description: Sci-fi/fantasy magazine
# 
# **Topics:**
# 
# * Scraping

# ## Scrape the Clarkesworld homepage `4 points`
# 
# I want a CSV file that includes a row for each story, including the columns:
# 
# * Title
# * Byline
# * URL to story
# * Category (fiction/non-fiction/cover art)
# * Issue number (e.g. 180)
# * Publication date (e.g. September 2021)

# In[1]:


import requests
from bs4 import BeautifulSoup
import pandas as pd
import re


# In[2]:


df = pd.read_csv("clarkesworld.csv")


# In[3]:


response = requests.get("https://clarkesworldmagazine.com")
doc = BeautifulSoup(response.text, 'html.parser')


# In[4]:


stories = doc.select('.index-col1, .index-col2')

rows = []

for story in stories:
    print("-----")
    row = {}
    
    row['title'] = story.select_one('.story').text.strip()
    row['byline'] = story.select_one('.byline').text.strip()
    row['url'] = story.select_one('a')['href']
    row['category'] = story.parent.select_one('p').text.strip()
    row['issue_number'] = re.search(r"(?<=ISSUE\s)(.*?)(?=\s\–)", story.parent.parent.select_one('.issue').text.strip()).group(0)
    row['date'] = re.search(r"(?<=\–\s)(.*)", story.parent.parent.select_one('.issue').text.strip()).group(0)

    print(row)
    rows.append(row)


# In[5]:


# df = pd.DataFrame(rows)
df.append(rows)
df


# In[6]:


df.drop_duplicates(keep="first", inplace=True)


# In[7]:


df.to_csv("clarkesworld.csv")


# ## Auto-updating scraper `3 points`
# 
# Using GitHub Actions, implement a scraper that will keep track of everything posted to the Clarkesworld homepage. For example, when issue 181 comes out it should *add to the CSV* instead of just replacing it.
# 
# > Tip: `drop_duplicates` might save you a lot of effort at one point or another.

# In[ ]:




