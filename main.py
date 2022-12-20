import argparse


def country_year_validate(file_name, country, year):
    is_country = False
    is_year = False
    with open(file_name) as file:
        attributes = file.readline()
        for line in file:
            row = line.split('\t')
            if country in (row[6].strip(), row[7].strip()):
                is_country = True
            if int(row[9].strip()) == year:
                is_year = True
            if is_country and is_year:
                return is_country, is_year
    return is_country, is_year


def get_medalists(file_name, country, year):
    # ID-0, Name-1, Sex-2, Age-3, Height-4, Weight-5, Team-6, NOC-7, Games-8, Year-9, Season-10, City-11, Sport-12, Event-13, Medal-14
    medalists = []
    with open(file_name) as file:
        attributes = file.readline()

        for line in file:
            row = line.split('\t')

            if row[14].strip() != 'NA' and int(row[9].strip()) == year and country in (row[6].strip(), row[7].strip()):
                medalists.append(row)
    return medalists


def get_first_10(medalists):
    # ID-0, Name-1, Sex-2, Age-3, Height-4, Weight-5, Team-6, NOC-7, Games-8, Year-9, Season-10, City-11, Sport-12, Event-13, Medal-14
    first_10_str = []
    for i in range(10):
        first_10_str.append(f'{medalists[i][1]}-{medalists[i][12]}-{medalists[i][14]}'.strip())

    return first_10_str


def get_total_medals(medalists):
    # ID-0, Name-1, Sex-2, Age-3, Height-4, Weight-5, Team-6, NOC-7, Games-8, Year-9, Season-10, City-11, Sport-12, Event-13, Medal-14
    gold = 0
    silver = 0
    bronze = 0
    for item in medalists:
        if item[14].strip().lower() == 'gold':
            gold += 1
        elif item[14].strip().lower() == 'silver':
            silver += 1
        elif item[14].strip().lower() == 'bronze':
            bronze += 1

    return gold, silver, bronze


def save_to_file(file_name, first_10, total_medals):
    with open(file_name, 'w') as file:
        file.write('\n'.join(first_10))
        file.write(f'\ngold={total_medals[0]}, silver={total_medals[1]}, bronze={total_medals[2]}')


def all_countries_medals(file_name, year):
    # ID-0, Name-1, Sex-2, Age-3, Height-4, Weight-5, Team-6, NOC-7, Games-8, Year-9, Season-10,
    # City-11, Sport-12, Event-13, Medal-14
    countries = {}
    with open(file_name) as file:
        attributes = file.readline()
        for line in file:
            row = line.split('\t')
            if int(row[9].strip()) != year:
                continue
            country = row[6].strip()
            if not countries.get(country):
                countries[country] = {'gold': 0, 'silver': 0, 'bronze': 0 }
            medal = row[14].strip().lower()
            if medal == 'gold':
                countries[country]['gold'] += 1
            elif medal == 'silver':
                countries[country]['silver'] += 1
            elif medal == 'bronze':
                countries[country]['bronze'] += 1

    res = []
    for country, medals in countries.items():
        if medals['gold'] == 0 and medals['silver'] == 0 and medals['bronze'] == 0:
            continue
        res.append(f"{country}-{medals['gold']}-{medals['silver']}-{medals['bronze']}")
    return res


def countries_medals_best_year(file_name, countries_lst):
    # ID-0, Name-1, Sex-2, Age-3, Height-4, Weight-5, Team-6, NOC-7, Games-8, Year-9, Season-10, City-11, Sport-12, Event-13, Medal-14
    countries = {}
    for item in countries_lst:
        countries[item] = {}

    with open(file_name) as file:
        attributes = file.readline()
        for line in file:
            row = line.split('\t')
            if row[6].strip() not in countries_lst:
                continue

            country = row[6].strip()
            year = int(row[9].strip())

            if not countries[country].get(year):
                countries[country][year] = 0

            if row[14].strip() != 'NA':
                countries[country][year] += 1

    res = {}
    for country, years in countries.items():
        best_year = max(years)
        res[country] = (best_year, years[best_year])
    return res


def get_country_statistic(file_name, country):
    # ID-0, Name-1, Sex-2, Age-3, Height-4, Weight-5, Team-6, NOC-7, Games-8, Year-9, Season-10, City-11, Sport-12, Event-13, Medal-14
    country_statistic = {}

    with open(file_name) as file:
        attributes = file.readline()
        for line in file:
            row = line.split('\t')
            if country in (row[6].strip(), row[7].strip()):
                city = row[11].strip()
                year = int(row[9].strip())
                if not country_statistic.get((year, city)):
                    country_statistic[(year, city)] = {'gold': 0, 'silver': 0, 'bronze': 0 }

                medal = row[14].strip().lower()
                if medal == 'gold':
                    country_statistic[(year, city)]['gold'] += 1
                elif medal == 'silver':
                    country_statistic[(year, city)]['silver'] += 1
                elif medal == 'bronze':
                    country_statistic[(year, city)]['bronze'] += 1
    return country_statistic


def get_first_year(country_statistic):
    keys = list(country_statistic.keys())
    min_year = keys[0]
    for year, city in keys:
        if year < min_year[0]:
            min_year = (year, city)
    return min_year


def best_year_city(country_statistic):
    year_city = None
    best_total = -1
    for key, medals in country_statistic.items():
        total = sum(medals.values())
        if best_total < total:
            best_total = total
            year_city = key
    return *year_city, best_total


def worse_year_city(country_statistic):
    year_city = None
    worse_total = None
    for key, medals in country_statistic.items():
        total = sum(medals.values())
        if total == 0:
            return *key, total

        if not worse_total:
            worse_total = total
            year_city = key
            continue

        if worse_total > total:
            worse_total = total
            year_city = key


    return *year_city, worse_total


def average_year_city(country_statistic):
    year_city_avg = {}
    for key, medals in country_statistic.items():
        year_city_avg[key] = sum(medals.values())/3
    return year_city_avg


parser = argparse.ArgumentParser()

parser.add_argument('file_name')
parser.add_argument('-medals', nargs=2)
parser.add_argument('-output')
parser.add_argument('-total', nargs=1, type=int)
parser.add_argument('-overall', nargs='*')
parser.add_argument('-interactive', nargs=1, type=bool)

args = parser.parse_args()

if args.interactive:
    while True:
        command = input('Name of country, stop - for exit: ')
        if command.strip().lower() == 'stop':
            break
        country_statistic = get_country_statistic(args.file_name, command.strip())
        first_year = get_first_year(country_statistic)
        best_year = best_year_city(country_statistic)
        worse_year = worse_year_city(country_statistic)
        average_year = average_year_city(country_statistic)
        print(f'First time: {first_year[0]}-{first_year[1]}')
        print(f'Best year: {best_year[0]}-{best_year[1]}-{best_year[2]}')
        print(f'Worse year: {worse_year[0]}-{worse_year[1]}-{worse_year[2]}')
        for key, value in average_year.items():
            print(key, value)


elif args.medals:
    country, year = args.medals
    is_country, is_year = country_year_validate(args.file_name, country, int(year))
    if not is_country:
        print(f'{country} not exists')
        exit()

    if not is_year:
        print(f'In {year} {country} did not take part')
        exit()

    medalists = get_medalists(args.file_name, country, int(year))

    if len(medalists) < 10:
        print(f'In {country} in {year} less than 10 medalists')
        exit()
    else:
        first_10 = get_first_10(medalists)
        print('\n'.join(first_10))

    total_medals = get_total_medals(medalists)
    print('----------------------------------')
    print(f'|gold={total_medals[0]},| silver={total_medals[1]},| bronze={total_medals[2]}|')
    print('----------------------------------')

    if args.output:
      save_to_file(args.output, first_10, total_medals)

elif args.total:
    res = all_countries_medals(args.file_name, *args.total)
    print('\n'.join(res))

if args.overall:
    res = countries_medals_best_year(args.file_name, args.overall)
    for country, best_result in res.items():
        print(f'{country}: {best_result}')


