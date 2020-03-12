#!/opt/local/bin/python
# -*- coding: utf-8 -*-
"""
DESCRIPTION OF THE SCRIPT

Version:
Created:
Compiler: python

Author: Dr. Samia Drappeau (SD), drappeau.samia@gmail.com
Affiliation:
Notes: 
"""
import argparse
import pandas as pd
import sys
import numpy as np
import subprocess


def loadData():
    df = pd.read_csv('../coronavirus-france-dataset/patient.csv', sep=',')
    df.dataframeName = 'patient.csv'
    nRow, nCol = df.shape
    print(f'There are {nRow} rows and {nCol} columns.')
    return df, nRow


def saveData(data):
    fname = './_tmp/patient-tmp.csv'
    del data['_confirmed_date']
    data.to_csv(fname, sep=',', index=False)
    print('Data saved to {}'.format(fname))

def evolutionRegion(data):
    lRegions = data['region'].unique().tolist()
    # TODO -- Improve on hardcoding 'France' in columns mapping because we only have one country.
    res = data.groupby(['_confirmed_date', 'region'])['country'].value_counts().unstack().rename(columns={'France': 'evolution_count'}).reset_index()
    full_data = []
    for date, _res in res.groupby(['_confirmed_date']):
        missing_regions = list(set(lRegions)- set(_res['region'].tolist()))
        for region in missing_regions:
            dd = {'region': region, 'evolution_count': 0, '_confirmed_date': date}
            _res = _res.append(dd, True)
        full_data.append(_res)
    res_full = pd.concat(full_data)
    # TODO -- Somehow, `res` has a name equal to 'country'. Can't get rid of that
    res_full['date_of_confirmed_infection'] = res_full['_confirmed_date'].apply(lambda row: row.strftime("%d-%b-%Y"))
    res_full['evolution_cumcount'] = res_full.groupby('region')['evolution_count'].transform(pd.Series.cumsum)
    return res_full

def dict_cleaning(data):
    return {k: v if v is not None else np.nan for k, v in data.items()}


def patientsDB():
    # Parsing command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', type=str, choices=['stats', 'add'],
                        required=True)

    # dataframe columns
    parser.add_argument('--patientID', type=int, default=None, required=False)
    parser.add_argument('--sex', type=str, default=None, required=False)
    parser.add_argument('--birth_year', type=int, default=None, required=False)
    parser.add_argument('--country', type=str, default='France')
    parser.add_argument('--region', type=str, choices=['Auvergne-Rhône-Alpes',
                                                       'Bourgogne-Franche-Comté',
                                                       'Bretagne',
                                                       'Centre-Val de Loire',
                                                       'Corse',
                                                       'Grand-Est',
                                                       'Guyane',
                                                       'Hauts-de-France',
                                                       'Ile-de-France',
                                                       'La Reunion',
                                                       'Martinique',
                                                       'Normandie',
                                                       'Nouvelle-Aquitaine',
                                                       'Occitanie',
                                                       'PACA',
                                                       'Pays-de-la-Loire',
                                                       'Saint-Barthélémy',
                                                       'Saint-Martin'],
                        required=True)
    parser.add_argument('--departement', type=str, default=None, required=False)
    parser.add_argument('--city', type=str, default=None, required=False)
    parser.add_argument('--group', type=str, default=None, required=False)
    parser.add_argument('--infection_reason', type=str, default=None, required=False)
    parser.add_argument('--infection_order', type=str, default=None, required=False)
    parser.add_argument('--infected_by', type=str, default=None, required=False)
    parser.add_argument('--contact_number', type=str, default=None, required=False)
    parser.add_argument('--confirmed_date', type=str, default=None,
                        required=False)
    parser.add_argument('--released_date', type=str, default=None, required=False)
    parser.add_argument('--deceased_date', type=str, default=None, required=False)
    parser.add_argument('--status', type=str, default=None, required=False)
    parser.add_argument('--health', type=str, default=None, required=False)
    parser.add_argument('--source', type=str, default=None, required=False)
    parser.add_argument('--comments', type=str, default=None, required=False)
    parser.add_argument('--occurrence', type=int, default=1)


    args = parser.parse_args()

    entry_data = vars(args)

    mode = args.mode

    patient_id = args.patientID
    sex = args.sex
    birth_year = args.birth_year
    country = args.country
    region = args.region
    departement = args.departement
    city = args.city
    group = args.group
    infection_reason = args.infection_reason
    infection_order = args.infection_order
    infected_by = args.infected_by
    contact_number = args.contact_number
    confirmed_date = args.confirmed_date
    released_date = args.released_date
    deceased_date = args.deceased_date
    status = args.status
    health = args.health
    source  = args.source
    comments = args.comments
    occurrence = int(args.occurrence)

    del entry_data['mode']
    del entry_data['occurrence']

    # Loading data
    df, nRows = loadData()

    print(df['region'].unique())

    # Cleaning Date columns
    df['_confirmed_date'] = pd.to_datetime(df['confirmed_date'])

    if mode == 'stats':
        df_total = evolutionRegion(df[df['region']==region])

        print('\nEvolution sur le temps pour la région {}'.format(region))
        print(df_total[['date_of_confirmed_infection', 'evolution_cumcount']])

        print('\nStatistiques pour ses départements infectés')
        print(df[df['region']==region].fillna('Non Specifié').groupby('departement')['country'].value_counts())

        print('\nStatistiques pour ses villes infectés')
        print(df[df['region']==region].fillna('Non Specifié').groupby('city')['country'].value_counts())
        return df

    elif mode == 'add':
        entry_data = dict_cleaning(entry_data)
        entry_data['id'] = entry_data.pop('patientID')
        print(entry_data)

        for i in range(occurrence):
            edata = pd.DataFrame(entry_data, index=[nRows+i])
            df = pd.concat([df, edata])
        saveData(df)
        return df
    else:
        pass


def main():
    df = patientsDB()



if __name__ == '__main__':
    main()


