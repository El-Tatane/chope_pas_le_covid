import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('max_colwidth',800)


# Cleaning and get_Data

def Cleaning_begining(df):
    df.index=df["Country/Region"]
    df=df.drop(columns=["Country/Region",'Lat','Long','Province/State'])
    df=df.groupby("Country/Region").sum()
    return df


def get_confirm():
    confirm=pd.read_csv('../../dataset/global/time_series_covid19_confirmed_global.csv', sep = ',')
    confirm=Cleaning_begining(confirm)
    return confirm


def get_deaths():
    deaths =pd.read_csv('../../dataset/global/time_series_covid19_deaths_global.csv', sep = ',')
    deaths=Cleaning_begining(deaths)
    return deaths


def get_recover():
    recover=pd.read_csv('../../dataset/global/time_series_covid19_recovered_global.csv', sep = ',')
    recover=Cleaning_begining(recover)
    return recover

def get_csv_count_population():
    total=pd.read_csv('../../dataset/global/WPP2019_TotalPopulationBySex.csv', sep = ',')
    total=total[total["Time"]==2019]
    return total

def get_unification_Recorvery_Confirm_Death(confirm,recover,deaths):
    confirm["name"]="confirm"
    recover["name"]="recover"
    deaths["name"]="deaths"
    return pd.concat([confirm, recover,deaths])

# Methode filtre graphe

def filter_by_country(df,country):
    return df.loc[country]

def total_by_country(df,country):
    return int(df.loc[(df["Location"]==country)&(df["Time"]==2019),"PopTotal"].values[0] * 1000)

def get_data(all_data,country):
    return filter_by_country(all_data,country)

def get_data(country):
    return filter_by_country(all_data,country), total_by_country(csv_count_population,country)

def plot_result( DataFrame_predict,DataFrame_reel=None ):
    name_type=DataFrame_predict["name"]
    DataFrame_predict=DataFrame_predict.drop(columns="name")
    DataFrame_predict=DataFrame_predict.T
    DataFrame_predict.columns=name_type
    DataFrame_predict.plot.line(subplots=True)
    if DataFrame_reel  is not None:

        name_type=DataFrame_reel["name"]
        DataFrame_reel=DataFrame_reel.drop(columns="name")
        DataFrame_reel=DataFrame_reel.T
        DataFrame_reel.columns=name_type
        DataFrame_reel.plot.line(subplots=True)
