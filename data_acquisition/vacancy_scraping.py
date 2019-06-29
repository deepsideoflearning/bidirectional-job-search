from IndeedScraper import IndeedScraper
import os
import shutil
import csv
import tarfile

path = './raw_data/'
file_name = 'job_postings.csv'

def main():
    locations = {
        'Portland, OR': '15',
        'Nashville, TN': '15',
        'Charlotte, NC': '15',
        'St. Louis, MO': '15',
        'Phoenix, AZ': '25',
        'Pittsburgh, PA': '25',
        'Miami, FL': '25',
        'Plano, TX': '10',
        'Columbus, OH': '10',
        'Austin, TX': '10',
        'Houston, TX': '15',
        'Raleigh, NC': '15',
        'Los Angeles, CA': '15',
        'Denver, CO': '15',
        'San Jose, CA': '10',
        'San Francisco, CA': 'Exact location only',
        'Berkeley, CA': '10',
        'New York City, NY': 'Exact location only',
        'Seattle, WA': 'Exact location only',
        'Boston, MA': 'Exact location only',
        'Arlington, VA': '10',
        'Washington, DC': '5',
        'Fairfax, VA': '5',
        'Irvine, CA': '15',
        'Chicago, IL': 'Exact location only',
        'Minneapolis, MN': '15',
        'San Diego, CA': '15',
        'Baltimore, MD': '15',
        'Atlanta, GA': '15',
        'Dallas, TX': '15',
        'Philadelphia, PA': '15',
        'Cleveland, OH': '25',
        'Tampa, FL': '15',
        'Orlando, FL': '25',
        'San Antonio, TX': '25'
    }

    key_words = [
        'scientist',
        'research',
        'engineer',
        'analyst',
        'data',
        'stat'
    ]
    starting_page = 1

    # Removing the directory if it exists
    try:
        shutil.rmtree(path)
    except FileNotFoundError:
        pass

    os.mkdir(path)

    for location in locations.keys():
        scraper = IndeedScraper('Data Scientist',
                                location=location,
                                key_words=key_words,
                                starting_page=starting_page,
                                radius=locations[location]
                                )
        count = starting_page

        if starting_page <= 1:
            scraper.search_jobs()

        while True:
            data = scraper.get_data()
            try:
                keys = data[0].keys()
            except IndexError:
                print(f'No data on page {count} for {location}')
                count += 1
                scraper.restart_driver()

                # If this error occurs, the page was full of ads and
                # no data is returned and we move onto the next page
                res = scraper.next_page()
                if not res:
                    break

                continue

            with open(path+file_name, 'a') as file:
                dict_writer = csv.DictWriter(file, keys)
                if count == 1:
                    dict_writer.writeheader()
                dict_writer.writerows(data)

            del data

            print(f'Finished with page {count} for {location}')
            count += 1

            res = scraper.next_page()

            if not res:
                break

        # I don't need the this scraper anymore
        scraper.close()
    # Compressing the file
    with tarfile.open('./raw_data.tar.gz', 'w:gz') as tar:
        tar.add(path, arcname='raw_data')


if __name__ == '__main__':
    main()
