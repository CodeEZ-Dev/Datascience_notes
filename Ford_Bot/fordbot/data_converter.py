import pandas as pd
from langchain_core.documents import Document

def dataconverter():

    product_data = pd.read_csv('data/ford.csv')

    data = product_data[["model", "year","price"]]

    product_list = []

    ## Itrate over the rows of the DataFrame

    for index, row in data.iterrows():
        object = {
            "model": row["model"],
            "year": row["year"],
            "price": row["price"]
        }

    ## Append the object to the product list
    product_list.append(object)
    docs = []
    for entry in product_list:
        metadata = {"price": entry['price'],"year":entry['year']}
        page_content= entry['model']
        doc = Document(page_content=page_content, metadata= metadata)
        docs.append(doc)    
    return docs