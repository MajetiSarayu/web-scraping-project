from bs4 import BeautifulSoup
import requests
import pandas as pd


library_site_url = "http://publiclibraries.com/state/"

response = requests.get(library_site_url)
if response.status_code == 200:
    contents = response.content
    soup = BeautifulSoup(contents, "html.parser")

    # getting all the state names and their library urls

    state_libraries_elements = soup.select(".dropdown > .dropdown-content > a")
    states_and_library_urls = [[state_libraries_elements[i].get_text(), state_libraries_elements[i].get("href")] 
                                    for i in range(len(state_libraries_elements))]

    if states_and_library_urls:
        for i in range(len(states_and_library_urls)):
            state_name = states_and_library_urls[i][0]
            library_url = states_and_library_urls[i][1]

            # getting each state libraries and their details

            response = requests.get(library_url)
            content = response.content
            if response.status_code == 200:
                soup = BeautifulSoup(content, "html.parser")

                library_details = {}
                library_row_elements = [i.select('td') for i in soup.select("#libraries tr")]
                library_row_elements = library_row_elements[1:]

                # getting library details

                library_details["city"] = [library_row_elements[i][0].get_text() for i in range(len(library_row_elements))]
                library_details["library"] = [library_row_elements[i][1].get_text() for i in range(len(library_row_elements))]
                library_details["address"] = [library_row_elements[i][2].get_text() for i in range(len(library_row_elements))]
                library_details["zip"] = [library_row_elements[i][3].get_text() for i in range(len(library_row_elements))]
                library_details["phone"] = [library_row_elements[i][4].get_text() for i in range(len(library_row_elements))]

                if library_details:
                    
                    df = pd.DataFrame(library_details)
                    file_path = f"milestone1/task1/libraryinfo/{state_name}.csv"
                    df.to_csv(file_path)

                else:
                    print("Did not scrape the details successfully")

            else:
                response.raise_for_status()

    else:
        print("something went wrong somewhere. Not able to scrape states and their library urls")

else:
    print("please check your code again!!!")
    response.raise_for_status()


