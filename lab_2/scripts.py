import sqlite3 as sql
import pandas as pd
import argparse
import pdb

def Q2Pandas():
    df = pd.read_csv('data/synsets-clean.txt')

    return df['split1'].nunique()

def Q3Pandas():
    world_cup = pd.read_csv('data/worldcup-awk.txt')
    condition = (world_cup["rank"] == 1)
    wc_filter = world_cup[condition]

    res = wc_filter.groupby('country').count().rename({"year": "num_champ"}, axis = 'columns')

    return res["num_champ"]

def Q7Pandas():
    wmbr = pd.read_csv('data/wmbr-11-awk.txt', delimiter = '|')
    condition = wmbr.Song.str.contains("WMBR") | wmbr.Album.str.contains("WMBR")
    condition = condition | wmbr.Song.str.contains("Wmbr") | wmbr.Album.str.contains("Wmbr")
    wmbr_filtered = wmbr[condition]

    return wmbr_filtered["Artist"].unique()

def Q8Pandas():
    wmbr = pd.read_csv('data/wmbr-11-awk.txt', delimiter = '|')
    condition = wmbr.Album != ""
    condition = condition & (wmbr.Album.str.contains("Stranger Things"))
    print(condition)
    wmbr_filtered = wmbr[condition]

    fields = ["DJ", "Song"]
    res = wmbr_filtered[fields].groupby(fields[0]).nunique()

    return res

def Q9Pandas():
    wmbr = pd.read_csv('data/wmbr-awk.txt', delimiter = '|')
    time_condition = (wmbr.Date.str.contains('2017') | wmbr.Date.str.contains('2018') | wmbr.Date.str.contains('2019'))
    condition = (wmbr.Artist == "Billie Eilish") & time_condition

    wmbr["Year"] = wmbr.Date.apply(lambda x: x[len(x)-4:])
    wmbr = wmbr[time_condition]
    wmbr_filtered = wmbr[condition]

    fields = ["Song"]
    
    eilish = wmbr_filtered.groupby("Year")[fields].count()
    eilish = eilish.rename({"Song": "Eilish"}, axis = 'columns')
    overall = wmbr.groupby("Year").count()[fields]
    overall = overall.rename({"Song": "Total"}, axis = 'columns')

    joined = pd.merge(left = eilish, right = overall,
                      left_on = ["Year"], right_on = ["Year"])

    joined["ratio"] = joined['Eilish']/joined["Total"] 
    
    return joined

def Q10Pandas():
    lizzo = pd.read_csv('data/lizzo_awk_final.txt', delimiter = '|')
    wmbr = pd.read_csv('data/wmbr-11-awk.txt', delimiter = '|')

    lizzo = lizzo[lizzo.Title.str.contains('Show')]
    years = set(lizzo.Year.unique())
    year_st = set([str(i) for i in years])
    wmbr["Year"] = wmbr.Date.apply(lambda x: x[len(x)-4:])

    year_condition = wmbr.Year.isin(year_st)
    eilish = wmbr.Artist == "Lizzo"

    wmbr_filtered = wmbr[year_condition & eilish]

    fields = ["Song", "Year"]

    res = wmbr_filtered[fields].groupby("Song").count().rename({"Year": "Frequency"}, axis = 'columns')
    
    return res.sort_values('Frequency', ascending = False)

def Q11Pandas():
    wmbr = pd.read_csv('data/wmbr-11-awk.txt', delimiter = '|')
    top = pd.read_csv('data/top2018-q11.csv')

    wmbr_artists = set(pd.unique(wmbr.Artist))
    
    condition = top.artists.isin(wmbr_artists)

    top_filtered = top[condition]
    fields = ["name", "artists", "danceability"]

    return top_filtered[fields].sort_values("danceability", ascending = False)

print(Q10Pandas())



print(other())

# wmbr['Year'] = pd.to_datetime(wmbr['Date']).dt.year
# noDoubles = wmbr.groupby('Date').min()
# billie = noDoubles[noDoubles['Artist'] == 'Billie Eilish'].groupby(['Year'])['Song'].count().sort_index(ascending=False)
# all = noDoubles[noDoubles['Year'] > 2016].groupby('Year')['Song'].count().sort_index(ascending=False)
