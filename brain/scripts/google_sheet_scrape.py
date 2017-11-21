import requests
import re
import csv
from datetime import datetime
import variables


def scrape_sheet(given_url): # Gets Sheet content from csv when you give it a URL
    response = requests.get(given_url)
    assert response.status_code == 200, 'Wrong status code'
    return response.content


# Go through each tuple
    # Save the description so we know where to load the data
    # Go through each item in the dictionary and get the classroom and url
        # Get the content from the URL so that you just have a classroom and content
    # Then, depending on the data_type, go to the function that reads that specific data
        # Make sure the students/classroom matches
            # Remove all case, characters and blank space when matching
            # If not, raise error/email me?
        # Make a list of student objects in the right order
        # Search the header rows for the data I want (Using terms like "Winter" and "Lexile")
        # Go through and add the data for the matching object



def google_sheet_scrape():
    for dictionary, data_type in variables.DATA_DICTIONARIES:
        for classroom, given_url in dictionary.items():
            print("Classroom: {}, Given URL: {}".format(classroom, given_url))
            if given_url != "":
                content = scrape_sheet(given_url)
                print("Scraped")
            else:
                content = "No Content"
                print("No Scrape")
            if data_type == "BehaviorReport":
                print("Behavior Report")
                print(content)


            elif data_type == "HomeworkCompletion":
                pass


            elif data_type == "NWEA":
                pass


            elif data_type == "ENI":
                pass


            elif data_type == "CBA":
                pass


            elif data_type == "DRA":
                pass


            elif data_type == "Writing":
                pass


            elif data_type == "ELAPBA":
                pass


            elif data_type == "Investigations":
                pass


            elif data_type == "CoreKnowledge":
                pass
            else:
                print("data_type didn't match any")




google_sheet_scrape()



