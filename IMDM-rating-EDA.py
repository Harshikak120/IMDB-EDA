#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd


# In[2]:


df=pd.read_excel('netflix_dataset_10k.xlsx')


# In[5]:


df.shape


# 

# In[7]:


df.head(5)


# In[8]:


# 1. Movies vs TV Shows: split, and change by release year
print(df["type"].value_counts())
print((df["type"].value_counts(normalize=True) * 100).round(1))


# In[21]:


# 2. Most common genres
print(df["genre"].value_counts(ascending=True))


# In[12]:


# 3. Spread across maturity ratings
print(df["maturity_rating"].value_counts(ascending=True))


# In[13]:


print(df["release_year"].value_counts().head(10))


# In[34]:


print(df)


# In[17]:


df2 = df[df["director"] != "Not Listed"] #  Who directed the most titles? (excluding the "Not Listed" placeholder)
print(df2["director"].value_counts().head(10))


# In[18]:


df2.head(5)


# In[19]:


# 2. Highest average rating, with a minimum number of titles
stats = df2.groupby("director")["imdb_rating"].agg(["mean", "count"])
top = stats[stats["count"] >= 10].sort_values("mean", ascending=False)
print(top.head(10).round(2))


# In[20]:


# 3. How many titles have "Not Listed" as director?
print((df["director"] == "Not Listed").sum())           
print((df["director"] == "Not Listed").mean() * 100)        


# In[22]:


# Create a decade column: 2016 -> 2010, 1998 -> 1990
df["decade"] = (df["release_year"] // 10) * 10

#  Average rating by decade
print(df.groupby("decade")["imdb_rating"].agg(["mean", "count"]).round(2))


# In[28]:


# 2. Genre share (%) within each decade
genre_mix = pd.crosstab(df["decade"], df["genre"], normalize="index") * 100
print(genre_mix.round(1).T)


# In[30]:


# Plot 1: Movies vs TV Shows per year (stacked)
import matplotlib.pyplot as plt
d = df[df["release_year"] >= 2000]
ct = pd.crosstab(d["release_year"], d["type"])
ct.plot(kind="bar", stacked=True, figsize=(10, 5))
plt.title("Titles released per year")
plt.show()

# Plot 2: titles per genre
df["genre"].value_counts().sort_values().plot(kind="barh", figsize=(8, 5.5))
plt.title("Titles per genre")
plt.show()


# In[31]:


# Plot 3: titles per maturity rating
df["maturity_rating"].value_counts().plot(kind="bar", figsize=(8.5, 4.5), color="#2a78d6")
plt.title("Titles per maturity rating")
plt.ylabel("Titles")
plt.xticks(rotation=0)
plt.show()


# In[32]:


# plot4. Maturity rating mix by decade
import seaborn as sns
mm = (pd.crosstab(df["decade"], df["maturity_rating"], normalize="index") * 100)
mm = mm.loc[[2000, 2010, 2020], ["TV-MA", "TV-14", "R", "PG-13"]]
mm = mm.reset_index().melt(id_vars="decade", var_name="rating", value_name="pct")
plt.figure(figsize=(8, 4.5))
sns.barplot(data=mm, x="decade", y="pct", hue="rating")
plt.ylim(0, 36)
plt.legend(ncol=4, loc="upper center", frameon=False)
plt.title("Maturity rating mix by decade")
plt.show()


# In[33]:


# 5. Genre share change, 2000s to 2020s
gm = pd.crosstab(df["decade"], df["genre"], normalize="index") * 100
change = (gm.loc[2020] - gm.loc[2000]).sort_values().reset_index()
change.columns = ["genre", "change"]
plt.figure(figsize=(8, 5.5))
sns.barplot(data=change, x="change", y="genre", hue=change["change"] > 0,
            palette={True: "#2a78d6", False: "#eb6834"}, legend=False)
plt.axvline(0, color="gray")
plt.title("Genre share change, 2000s to 2020s")
plt.show()


# In[ ]:




