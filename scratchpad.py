# To add a new cell, type '#%%'
# To add a new markdown cell, type '#%% [markdown]'
#%%
from library import Catalogue
import zipfile
import pprint as pp
import re

Catalogue = Catalogue()
book_list = Catalogue.filter_books(1)
unpacked = []

for book in book_list:
    book = zipfile.ZipFile(book, 'r')
    with book as bookzip:
        try:
            content_opf = bookzip.open('content.opf')
            print(content_opf)
        except KeyError as e:
            expanded = bookzip.infolist()
            regx1 = re.compile(r'\.opf|^cover')
            for i in expanded:
                if re.search(regx1, str(i)) == True: pp.pprint(i.filename); print(res)


#%%



