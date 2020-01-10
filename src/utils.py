import unicodedata
import math
import numpy as np
from haversine import haversine

"""
airbnb utils
"""
    
def equals_bin_value(v, d):
    return 1 if v == d else 0


def contains_bin_value(v, d):
    return 1 if v in d else 0


def get_bin_value_by_char(d):
    if d == 't':
        return 1
    elif d == 'f':
        return 0
    else:
        return np.nan
    

def get_outliers_iqr(ys, iqr_factor=1.5):
    quartile_1, quartile_3 = np.percentile(ys, [25, 75])
    iqr = quartile_3 - quartile_1
    lower_bound = quartile_1 - (iqr * iqr_factor)
    upper_bound = quartile_3 + (iqr * iqr_factor)
    print('outliers between following bounds:', lower_bound, upper_bound)
    return np.where((ys > upper_bound) | (ys < lower_bound))


def remove_outliers(dfr, indexes_arr, debug_col):
    if debug_col:
        print(
            len(indexes_arr), 'outliers to be removed with values:', 
            sorted(set(dfr.loc[indexes_arr][debug_col].values))
        )
    dfr.drop(indexes_arr, inplace=True)
    dfr.reset_index(drop=True, inplace=True)


def remove_accents(input_str):
    if input_str:
        nfkd_form = unicodedata.normalize('NFKD', input_str)
        return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])
    else:
        return ''


def clean_price_eur(p):
    return p.replace(',', '.').replace('€/m2', '').strip()


def clean_price_dollar(p):
    return p.replace(',', '').replace('$', '').strip()


def fix_geojson(data):
    for f in data['features']:
        id = f['properties']['name']
        f['id'] = id
    return data


def get_haversine_distance(lat, lon, poi_coord):
    return haversine(poi_coord, (lat, lon))


def calculate_income_med_occupation(price, cleaning_fee, accommodates, extra_people, guests_included, n_nights):
    accommodates_mean = math.ceil(accommodates / 2) if accommodates > 1 else 1
    accommodates_mean_price = 0
    if accommodates_mean > guests_included:
        accommodates_mean_price = (accommodates_mean - guests_included) * extra_people
    return round((n_nights * (price + accommodates_mean_price) + cleaning_fee), 2)


def calculate_price_med_occupation_per_accommodate(price, cleaning_fee, accommodates, extra_people, guests_included, n_nights):
    income_med_occupation = calculate_income_med_occupation(price, cleaning_fee, accommodates, extra_people, guests_included, n_nights)
    accommodates_mean = math.ceil(accommodates / 2) if accommodates > 1 else 1
    return round(income_med_occupation / accommodates_mean, 2)
