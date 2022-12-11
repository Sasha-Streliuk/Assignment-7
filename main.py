import argparse


def country_year_validate(file_name, country, year):
    pass


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
    pass


def get_total_medals(medalists):
    pass


def save_to_file(file_name, first_10, total_medals):
    pass
