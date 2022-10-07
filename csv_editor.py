import csv
import sys
import os
import ast

sys.dont_write_bytecode = True


class CSVEditor():
    """DEALS WITH THE CSV FILE"""

    def __init__(self, filename, *args):
        # args are the fieldnames here

        self.cwd = os.getcwd()

        # If filename augrument does not have .csv extension, ass it to filename string
        if '.csv' in filename:
            self.filename = filename
        else:
            self.filename = filename + '.csv'

        self.fieldnames = []
        for i in args:
            self.fieldnames.append(i)

        # If file not found, make one
        if self.filename not in os.listdir(self.cwd):
            self.make_file()


    def make_file(self):
        # Creates the CSV file with given fieldnames
        with open(self.filename, 'w') as f:
            writer = csv.DictWriter(f, fieldnames = self.fieldnames)
            writer.writeheader()

    def add_entry(self, *args):
        # Adds an entry to the created file
        # For people_data file args would be: function(email, name, [anime1, anime2])
        # For anime_data file args would be: function(anime_name, latest_episode)

        if self.check_entry(args[0]): # Check if entry already in database
            print(f"entry -- {args[0]} -- already exists")
        else:
            data = []
            for i in args:
                data.append(i)

            with open(self.filename, 'a') as f:
                writer = csv.writer(f)
                writer.writerow(data)

                print(f"Added --{args[0]}-- to database")

    def remove_entry(self, identifier):
        # Removes a entry based on a identifier i.e email (people_data) or anime_name (anime_data)

        if not self.check_entry(identifier):
            print(f"The identifier --{email}-- does not exist in database\n")

        else:
            # Add all entries to a list. If entry == identifier, remove the entry from list
            # Then re-write the new data to the file

            lines = list()

            with open(self.filename, 'r') as readFile:
                reader = csv.reader(readFile)
                for row in reader:
                    lines.append(row)
                    for field in row:
                        if field == identifier:
                            lines.remove(row)

            with open(self.filename, 'w') as f:
                writer = csv.writer(f)
                writer.writerows(lines)

            print(f"Removed entry --{identifier}-- from database")

    def check_entry(self, identifier):
        # Checks if an entry exists already or not

        with open(self.filename, 'r') as f:
            reader = csv.DictReader(f)

            for row in reader:
                if row[self.fieldnames[0]].lower() == identifier.lower():
                    return True

            return False

    def get_all_entries(self):
        # Groups all the data from CSV into a dictionary so it can be used

        self.entries = {}

        for i in range(len(self.fieldnames)):
            self.entries[self.fieldnames[i]] = []

        with open(self.filename, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                for i in range(len(self.fieldnames)):
                    self.entries[self.fieldnames[i]].append(row[self.fieldnames[i]])

        try:
            x = [ast.literal_eval(i) for i in self.entries['anime']]
            self.entries['anime'] = x

        except:
            pass

        return self.entries

    def get_single_entry(self, identifier):
        # Gets only one entry as a dictionary

        if not self.check_entry:
            return None
        else:
            entry = {}
            for i in range(len(self.fieldnames)):
                entry[self.fieldnames[i]] = list()

            with open(self.filename, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    for i in range(len(self.fieldnames)):
                        if row[self.fieldnames[0]].lower() == identifier.lower():
                            # entry['name'] = row['name']
                            try:
                                entry[self.fieldnames[i]].append(ast.literal_eval(row[self.fieldnames[i]]))
                            except:
                                entry[self.fieldnames[i]].append(row[self.fieldnames[i]])

        return entry


    def update_entry(self, identifier, **kwargs):
        if not self.check_entry(identifier):
            print(f"The identifier --{identifier}-- does not exist in database\n")

        else:
            # Add all entries to a list. If entry == identifier, update the entry from list
            # Then re-write the new data to the file

            for k, v in kwargs.items():
                new_header = k
                new_value = v

            lines = self.get_all_entries()

            for key, value in lines.items():
                for i in range(len(lines[self.fieldnames[0]])):
                    if lines[key][i] == identifier:
                        index = lines[key].index(lines[key][i])
                        lines[new_header][index] = new_value

            with open(self.filename, 'w') as f:
                writer = csv.writer(f)
                writer.writerow(self.fieldnames)

                for x in range(len(lines[self.fieldnames[0]])):
                    individual_entries = []
                    for key, value in lines.items():
                        for i in range(len(value)):
                            if i == x:
                                individual_entries.append(lines[key][i])

                    writer.writerow(individual_entries)



animeEditor = CSVEditor('anime_data', 'anime', 'episode', 'aniDB_ID')

# animeEditor.add_entry('Enen no Shouboutai Ni no Shou', '12', 'https://anidb.net/anime/15335')
# animeEditor.add_entry('Tonikaku Kawaii', '7', 'https://anidb.net/anime/15421')
# animeEditor.add_entry('Haikyuu!! To the Top', '9', 'https://anidb.net/anime/15283')

# print(animeEditor.get_all_entries())
# animeEditor.update_entry('Tonikaku Kawaii', episode = 5)
# animeEditor.update_entry('Enen no Shouboutai Ni no Shou', episode = 5)
# animeEditor.update_entry('Black Clover', episode = 5)
# animeEditor.add_entry('Jujutsu Kaisen', '8', 'https://anidb.net/anime/15275')
