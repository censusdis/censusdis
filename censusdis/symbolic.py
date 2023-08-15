# Copyright (c) 2022 Darren Erik Vengroff

"""
Utilities for creating symbolic names.

This module processes data sets from the US Census
and their respective symbolic names for
documentation purposes.
"""

import os


class symbolic:
    def __init__(self):
        self.dictionary = {}

    def store_dataset(self, dataset_list: list, url_list: list):
        for item in dataset_list:
            if item not in self.dictionary.values():
                index = dataset_list.index(item)
                link = url_list[index]
                temp = item.split("/")
                if len(temp) == 1:
                    if temp[0][:3] == "ecn" or temp[0][:3] == "abs":
                        name = temp[0][:3].upper() + "_" + temp[0][3:].upper()
                    else:
                        name = temp[0].upper()
                elif len(temp) == 2:
                    if temp[0][:3] == temp[1][:3]:
                        name = temp[1].upper()
                    else:
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
        with open(destination_file, "a") as destfile:
            print("\n", file=destfile)
            for key in sorted(self.dictionary.keys()):
                content = key + " = " + self.dictionary[key][0]
                print(content, "\n", file=destfile)

            print("\n", file=destfile)
            print("DATASET_REFERENCE_URLS = { \n", file=destfile)

            for key in sorted(self.dictionary.keys()):
                value = self.dictionary[key][1]
                print("\t%s: %s," % (key, value), file=destfile)
            print("\n}", file=destfile)
        os.chdir("..")
