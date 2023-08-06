import numpy as np
import pandas as pd
import urllib.request
from bs4 import BeautifulSoup
import copy

def get_dataframes(url, by_class= 'wikitable', raw=False):
    """Extract information from tables on a Wikipedia page.
    Handles table cells with non-conflicting rowspan and colspan attributes.
    Parameters:
       url (str): wikipedia page url (e.g., https://en.wikipedia.org/wiki/List_of_UFC_events);
       by_class (str):  class name of table to fetch; if None, fetches all tables;
       raw (bool):  get raw inner html or get raw text from each cell;
    Returns:
       list: list of dataframes extracted from tables in wikipedia page;
    """

    list_pds= []

    ##read webpage
    page= urllib.request.urlopen(url)
    soup= BeautifulSoup(page, "lxml")
    if by_class is None:
        tables= soup.find_all('table')
    else:
        tables= soup.find_all('table', class_=by_class)

    for table in tables:
        trs = table.findAll('tr')

        ##1. assumes top row is header
        header= []
        children = trs[0].findChildren(recursive=False)
        for child in children:
            header.append(child.find(text= True).strip())

        ##2. create dataframe to capture table values
        df_table_values = pd.DataFrame(index=np.arange(len(trs)), columns=header)
        df_table_values = df_table_values.replace({np.nan: None})

        ##3. prepare tds that have both rowspan and colspan
        for i in range(1, len(trs)):
            children= trs[i].findChildren('td', recursive=False)
            for j in range(0, len(children)):
                cspan = int(children[j].get('colspan')) if children[j].get('colspan') else 1
                rspan = int(children[j].get('rowspan')) if children[j].get('rowspan') else 1
                if cspan > 1 and rspan > 1:
                    del children[j]['colspan']
                    for c in range(1, cspan):
                        td_copy = copy.copy(children[j])
                        children[j].insert_after(td_copy)

        ##4. assign cell values bases on table spans
        for i in range(1, len(trs)):
            val_row = i
            children= trs[i].findChildren('td', recursive=False)
            for j in range(0, len(children)):
                ##what value to assign to cell(s)
                if raw:
                    val = children[j].decode_contents()
                else:
                    val = children[j].find(text=True).strip()

                val_col = j
                while True:
                    if df_table_values.iloc[val_row, val_col] is None:
                        break
                    val_col= val_col + 1
                df_table_values.iloc[val_row, val_col]= val

                cspan = int(children[j].get('colspan')) if children[j].get('colspan') else 1
                rspan = int(children[j].get('rowspan')) if children[j].get('rowspan') else 1

                ##handle when colspan alone is present
                if cspan > 1 and rspan == 1:
                    for c in range(val_col+1, val_col+cspan):
                        df_table_values.iloc[val_row, c] = val

                ##handle when rowspan alone is present
                if rspan > 1 and cspan == 1:
                    c= val_col
                    for r in range(val_row+1, val_row+rspan):
                        while True:
                            if df_table_values.iloc[r, c] is None:
                                break
                            c = c + 1
                        df_table_values.iloc[r, c] = val


        ##4. drop first row and add to list
        df_table_values= df_table_values.iloc[1:, :]
        list_pds.append(df_table_values)

    return list_pds


