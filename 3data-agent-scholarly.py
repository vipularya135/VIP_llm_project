from scholarly import scholarly
import pandas as pd

# Function to collect data about a professor
def collect_data(professor_name):
    search_query = scholarly.search_author(professor_name)  # Search for the author
    
    try:
        # Try to get the first result (stop iteration if no results found)
        author = next(search_query)  # Get the first result
        author_info = scholarly.fill(author)  # Get detailed author info

        # Extract relevant information from the author's profile
        name = author_info.get('name', '')
        affiliation = author_info.get('affiliation', '')
        h_index = author_info.get('hindex', 0)
        i10_index = author_info.get('i10index', 0)
        citations = author_info.get('citedby', 0)

        # Store data in a DataFrame (can be saved to a database or CSV)
        data = {
            "Name": name,
            "Affiliation": affiliation,
            "h-index": h_index,
            "i10-index": i10_index,
            "Citations": citations
        }
        return pd.DataFrame([data])
    
    except StopIteration:
        # If no results found, return a message or an empty DataFrame
        print(f"No results found for {professor_name}.")
        return pd.DataFrame()  # Return an empty DataFrame

# Example use case
professor_data = collect_data("S.H.Shabbeer Basha")
print(professor_data)


#         Name          Affiliation  h-index  i10-index  Citations
# 0  Andrew Ng  Stanford University      150        361     273641
# 1  zijun liu  Huazhong university        24         53       3728
# 2  Varsha Apte  IIT Bombay                17         25        928
# S.H. Shabbeer Basha  RV University, Bangalore        8          8        845

# Name,Affiliation,h-index,i10-index,Citations
# Prof Prafulla Kumar  Behera,"Professor of Physics, Indian Institute of Technology Madras",217,1481,244506
# Dr. Bhim Singh,"SERB National Science Chair, Dept of Electrical Engineering, IIT Delhi",107,1115,63815
# Ashutosh Kumar Pandey,"Postdoc at University of Tsukuba, PhD from IIT Bombay",95,294,28560
