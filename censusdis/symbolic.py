# Copyright (c) 2022 Darren Erik Vengroff

"""
Utilities for creating symbolic names.

This module processes data sets from the US Census
and their respective symbolic names for
documentation purposes.
"""

import os
import censusdis.data as ced
import censusdis.datasets

class symbolic:
    def __init__(self):
        self.dictionary = {}
        self.module_message = [
            "# Copyright (c) 2022 Darren Erik Vengroff\n",'"""\n'
            "This module contains abbreviated names for commonly used data sets.\n",
            "These are typically used as the first argument to :py:func:`censudis.data.download`.\n",
            "There are a lot more data sets available than there are symbolic names here.\n",
            "But you can always use raw strings. For example, even for `ACS5` you can use\n",
            "`acs/acs5` instead.\n", '"""\n' 
        ]

    def store_dataset(self, dataset_list: list, url_list: list):
        for item in dataset_list:
            if item not in self.dictionary.values():
                index = dataset_list.index(item)
                link = url_list[index]
                temp = item.split("/")
                if len(temp) == 1:
                    if temp[0][:3] == "ecn" or temp[0][:3] == "abs":
                        name = temp[0][:3].upper() + "_" + temp[0][3:].upper()
                    elif temp[0] == "surname":
                        name = "DECENNIAL_SURNAME"
                    elif temp[0] == "pubschlfin":
                        name = "PUBLIC_PK12_EDUCATION_FINANCE"
                    else:
                        name = temp[0].upper()
                elif len(temp) == 2:
                    if temp[0][:3] == temp[1][:3]:
                        if temp[0] == "popproj":
                            name = temp[0].upper()
                        else:
                            name = temp[1].upper()
                    else:
                        if temp[0] == "dec":
                            temp[0] = "decennial"
                            if temp[1] == "pl":
                                temp[1] = "PUBLIC_LAW_94_171"
                        name = "_".join(temp).upper()
                else:
                    if temp[0][:3] == temp[1][:3]:
                        name = "_".join(temp[1:]).upper()
                    else:
                        name = "_".join(temp[:2]).upper()
                item, link = f'"{item}"', f'"{link}"'
                self.dictionary[name] = [item, link]
        return self.dictionary

    def write_file(self, destination_file: str):
        os.chdir("censusdis")
        with open(destination_file, "w") as destfile:
            for string in self.module_message:
                destfile.write(string)
                if string != '"""':
                    destfile.write("\n")

            for key in sorted(self.dictionary.keys()):
                destfile.write("\n")
                content = key + " = " + self.dictionary[key][0]
                destfile.write(content)
                destfile.write("\n")

            destfile.write("\n")
            destfile.write("\nDATASET_REFERENCE_URLS = { \n")

            for key in sorted(self.dictionary.keys()):
                value = self.dictionary[key][1]
                destfile.write("\t%s: %s,\n" % (key, value))
            destfile.write("}")

def main():
    df_datasets = ced.variables.all_data_sets()
    dataset_names = df_datasets["DATASET"].to_list()
    dataset_url = df_datasets["API BASE URL"].to_list()
    create_symbolic = symbolic()
    symbolic_names = create_symbolic.store_dataset(dataset_names, dataset_url)
    create_symbolic.write_file("datasets.py")
    print("Updated datasets.py successfully.")

if __name__ == "__main__":
    main()