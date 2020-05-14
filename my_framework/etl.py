import pandas as pd


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
    return join_df_confirm_recover_death(df_confirm, df_recover, df_death),  get_number_population(get_info_population_df(), country)
