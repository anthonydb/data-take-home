import csv
import datetime
import collections


def clean_date(date):
    """Test for valid date strings. If valid, return ISO date."""
    try:
        date_out = datetime.datetime.strptime(date, '%Y-%m-%d').date()
    except ValueError:
        try:
            date_out = datetime.datetime.strptime(date, '%m/%d/%Y').date()
        except ValueError:
            try:
                date_out = datetime.datetime.strptime(date, '%B %d, %Y').date()
            except ValueError:
                date_out = None
    return date_out


def main():
    # Read the state abbreviations CSV into an object for lookup.
    with open('../../files/state_abbreviations.csv') as state_csv_file:
        state_abbreviations = csv.DictReader(state_csv_file)
        state_list = []
        for row in state_abbreviations:
            d = collections.OrderedDict()
            d['state_abbr'] = row['state_abbr']
            d['state_name'] = row['state_name']
            state_list.append(d)

    # Open, read and process the source data.
    with open('../../files/data.csv') as csv_in_file:
        file_reader = csv.DictReader(csv_in_file)
        dict_list = []

        # Iterate through each row in the source CSV.
        for row in file_reader:
            # Create an ordered dictionary to hold processed rows for output.
            d = collections.OrderedDict()

            # These columns are unchanged from the source.
            d['name'] = row['name']
            d['gender'] = row['gender']
            d['birthdate'] = row['birthdate']
            d['address'] = row['address']
            d['city'] = row['city']
            d['zipcode'] = row['zipcode']
            d['email'] = row['email']
            d['job'] = row['job']

            # Remove excess white space, line feeds, etc. from bio.
            d['bio'] = ' '.join(row['bio'].split())

            # Search state_list for abbreviation that matches state in
            # source CSV.
            state_lookup = (item for item in state_list
                            if item['state_abbr'] == row['state'])
            identified_state = next(state_lookup)
            # Use full state name in output row for state.
            d['state'] = identified_state['state_name']

            # Call function to test for valid date. If function returns a date,
            # place ISO-formatted date in start_date. If function returns None,
            # move invalid dates to new column called start_date_description.
            start_date_cleaned = clean_date(row['start_date'])
            if start_date_cleaned:
                d['start_date'] = start_date_cleaned
                d['start_date_description'] = ''
            else:
                d['start_date'] = ''
                d['start_date_description'] = row['start_date']

            # Append new row to list.
            dict_list.append(d)

    # Create an output CSV file and write new rows to it.
    with open('enriched.csv', 'w', newline='') as csv_out_file:
        fieldnames = ['name', 'gender', 'birthdate', 'address', 'city',
                      'state', 'zipcode', 'email', 'bio', 'job',
                      'start_date', 'start_date_description']
        file_writer = csv.DictWriter(csv_out_file, fieldnames=fieldnames)
        file_writer.writeheader()

        for item in dict_list:
            file_writer.writerow(item)


if __name__ == '__main__':
    main()
