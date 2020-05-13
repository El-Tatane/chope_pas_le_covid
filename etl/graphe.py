#!/usr/bin/env python
# coding: utf-8

# In[168]:


#Import bibli
import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('max_colwidth',800)





#Modification des csv


#Import csv

def transform(df):
    df.index=df["Country/Region"]
    df=df.drop(columns=["Country/Region",'Lat','Long','Province/State'])
    df=df.groupby("Country/Region").sum()
    return df


def get_confirm():
    confirm=pd.read_csv('/home/covid/dataset/global/time_series_covid19_confirmed_global.csv', sep = ',')
    confirm=transform(confirm)
    return confirm


def get_deaths():
    deaths =pd.read_csv('/home/covid/dataset/global/time_series_covid19_deaths_global.csv', sep = ',')
    deaths=transform(deaths)
    return deaths


def get_recover():
    recover=pd.read_csv('/home/covid/dataset/global/time_series_covid19_recovered_global.csv', sep = ',')
    recover=transform(recover)
    return recover

def get_total():
    total=pd.read_csv('/home/covid/dataset/global/WPP2019_TotalPopulationBySex.csv', sep = ',')
    total=total[total["Time"]==2019]
    return total



# ### Methode

# In[171]:


def conf_by_country(df,country):
    return df.loc[country]
def total_by_country(df,country):
    return int(df.loc[(df["Location"]==country)&(df["Time"]==2019),"PopTotal"].values[0] * 1000)
def Graphe(confirm,recover,deaths,country,total):
    confirm_country=conf_by_country(confirm,country)
    confirm_country.plot.line()



    recover_country=conf_by_country(recover,country)
    recover_country.plot.line()

    country_death=conf_by_country(deaths,country)

    potential_contamination = total_by_country(total,country) - (country_death + recover_country)
    # potential_contamination = 800000 - (country_death + recover_country)
    potential_contamination.plot.line(logy=True)
    #mal.plot.line(logy=True)


# In[ ]:
