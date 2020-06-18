import pandas as pd
import numpy as np


# Get Data
def get_confirm_df():
    df_confirm = pd.read_csv('/home/covid/dataset/global/time_series_covid19_confirmed_global.csv', sep = ',')
    return df_confirm


def get_death_df():
    df_deaths = pd.read_csv('/home/covid/dataset/global/time_series_covid19_deaths_global.csv', sep = ',')
    return df_deaths


def get_recover_df():
    df_recover = pd.read_csv('/home/covid/dataset/global/time_series_covid19_recovered_global.csv', sep = ',')
    return df_recover


def get_info_population_df():
    df_population_info = pd.read_csv('/home/covid/dataset/global/WPP2019_TotalPopulationBySex.csv', sep = ',')
    return df_population_info[df_population_info["Time"]==2019]


# Cleaning and get_Data

def clean_useless_columns_and_reset_idx(df):
    df.index=df["Country/Region"]
    df=df.drop(columns=["Country/Region",'Lat','Long','Province/State'])
    df=df.groupby("Country/Region").sum()
    return df


def join_df_confirm_recover_death(df_confirm, df_recover, df_death):
    df = pd.concat([df_confirm, df_recover, df_death], axis=1)
    df.columns = ["confirm", "recover", "death"]
    return df

# Methode filtre graphe

def filter_by_country(df, country):
    return df.loc[country]


def get_number_population(df, country):
    return int(df.loc[(df["Location"]==country)&(df["Time"]==2019),"PopTotal"].values[0] * 1000)


def get_dataset(country):
    df_confirm = filter_by_country(clean_useless_columns_and_reset_idx(get_confirm_df()), country)
    df_death = filter_by_country(clean_useless_columns_and_reset_idx(get_death_df()), country)
    df_recover = filter_by_country(clean_useless_columns_and_reset_idx(get_recover_df()), country)
    return delete_first_row(join_df_confirm_recover_death(df_confirm, df_recover, df_death)),  get_number_population(get_info_population_df(), country)


def delete_first_row(df, value=0, column_name="confirm"):
    i = 0
    while df[column_name][i] == value:
        i += 1
    return df.iloc[i:]

def get_idf_df(list_country, col):
    df = df_deaths = pd.read_csv('/home/covid/dataset/global/Human Development Index (HDI).csv', sep = ',', skiprows=1)
    df_res = pd.DataFrame()
    for country in list_country:
        df_tmp = df.loc[(df["Country"] == country )]
        df_res = pd.concat([df_res, df_tmp])
    df_res.rename(columns={'2018': 'IDH'}, inplace=True)
    return df_res[col]


def get_median_age_df(list_country):
    df_age = pd.read_csv('/home/covid/dataset/global/datasets_population_by_country_2020.csv', sep = ',')
    df_res = pd.DataFrame()
    for country in list_country:
        df_tmp = df_age.loc[df_age["Country (or dependency)"] == country, ['Med. Age', "Country (or dependency)"]]
        df_res = pd.concat([df_res, df_tmp])
    return df_res.rename(columns={"Country (or dependency)": "Country"}).set_index("Country")

def get_info_pop_df(list_country, col):
    df_population_info = pd.read_csv('/home/covid/dataset/global/WPP2019_TotalPopulationBySex.csv', sep = ',')
    df_population_info["pourcentage_homme"] = df_population_info["PopMale"] / df_population_info["PopFemale"]
    df_res = pd.DataFrame()
    for country in list_country:
        df_tmp = df_population_info.loc[(df_population_info["Time"]==2019) & (df_population_info["Location"]==country)]
        df_res = pd.concat([df_res, df_tmp])

    return df_res[col]

def get_temp_df(list_country):
    global_temp_country = pd.read_csv('/home/covid/dataset/global/GlobalLandTemperaturesByCountry.csv', sep = ',')
    global_temp_country.head()

    global_temp_country_clear = global_temp_country[~global_temp_country['Country'].isin(
        ['Denmark', 'Antarctica', 'France', 'Europe', 'Netherlands',
         'United Kingdom', 'Africa', 'South America'])]

    global_temp_country_clear = global_temp_country_clear.replace(
       ['Denmark (Europe)', 'France (Europe)', 'Netherlands (Europe)', 'United Kingdom (Europe)'],
       ['Denmark', 'France', 'Netherlands', 'United Kingdom'])


    #countries = np.unique(global_temp_country_clear['Country'])
    mean_temp = []
    for country in np.unique(list_country):
        mean_temp.append(global_temp_country_clear[global_temp_country_clear['Country'] ==
                                                   country]['AverageTemperature'].mean())

    # température data frame
    data = {'country':  list(list_country),
            'temp': mean_temp,
            }
    return pd.DataFrame(data, columns = ['country','temp'])
    return df_recover

def get_comparaison_dataset(list_country):

    df_idh = get_idf_df(list_country, ["Country","IDH"]).set_index('Country')
    df_info_pop = get_info_pop_df(list_country, ["PopDensity", "pourcentage_homme", "PopTotal", "Location"]).set_index('Location')
    df_age = get_median_age_df(list_country)
    return pd.concat([df_idh, df_info_pop, df_age], axis="columns")

def get_dict_df_action(list_country):
    measure=pd.read_csv('/home/covid/dataset/global/utils.csv', sep = ',')
    df_3 = pd.DataFrame()
    pays=list_country

    dPays={}
    df=pd.DataFrame()
    for i in pays:
        try:
            res=measure.loc[(measure["Country"]==i)&(measure["Keywords"]=="testing numbers total")].groupby("Keywords").sum()["Quantity"].values[0]
            measure.loc[(measure["Country"]==i)&(measure["Keywords"]=="testing numbers total")]
            #print(i,": nombre test total",int(res))
            df=df.append({"Pays":i,"nombre test total":int(res)},ignore_index=True)
        except:
            #print(i,": nombre test total",0)
            df=df.append({"Pays":i,"nombre test total":int(0)},ignore_index=True)
        ldf=[]
        lwo=["transport","suspension","ban","isolation","quarantine", "mask"]
        for j in lwo:
            ldf.append(measure.loc[(measure["Country"]==i)&(measure["Keywords"].str.contains(r"\b"+j+r"\b",case=False))])
        df2=pd.concat(ldf)
        df2["nombre test total"]=df.loc[df["Pays"]==i,"nombre test total"].values[0]
        df2=df2[["Keywords","Country","Date Start","Date end intended","nombre test total"]]

        dPays[i]=df2.copy()

    return dPays
