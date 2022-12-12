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



parser = argparse.ArgumentParser()
parser.add_argument('file_name')
parser.add_argument('-medals', nargs=2, required=True)
parser.add_argument('-output')

args = parser.parse_args()

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
print(f'gold={total_medals[0]}, silver={total_medals[1]}, bronze={total_medals[2]}')

if args.output:
    save_to_file(args.output, first_10, total_medals)

