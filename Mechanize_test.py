# Example use of mechanize library to pull election data
# adapted from educational notebook in General Assembly Data Science course (Chicago, spring 2016)

# import the html parser that constructs of tree of tags and what's in them
import lxml.html as ET


# Let's make a function that reads tables and gets the useful information
# content_string is the source code for the page
# table_number is which table we should parse if there are multiple tables on the page.
# The default value for table_number is 0, meaning retrieve the first table
def table_reader(source_code, table_number=0):
    # send the page html to the html parser
    doc = ET.fromstring(source_code)

    # make an empty list to save our table into
    data = []

    # look in between the tags that say "table" and find all of the row elements, which are the <tr> tags
    # the table indicates, which table on the page to retreive in case there are many
    rows = doc.xpath("//table")[table_number].findall("tr")

    # go through the list of table rows
    for row in rows:
        # append to our data all of the data in the cells of the row
        data.append([c.text_content() for c in row.getchildren()])

    # return the data list
    return data

import mechanize
br = mechanize.Browser()

# tell the br object to ignore any text files called 'robots.txt' if it exists on the website
br.set_handle_robots(False)
br.set_handle_equiv(False)

# tell mechanize browser object to pretend to be a real Firefox Browser by setting the header information that is
# passed when a request is made
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

# have the mechanize browser open a webpage
br.open("http://www.chicagoelections.com/en/election3.asp")

# print the URL
br.geturl()

# tell the browser to go to 'form1' and enter value for 2016 General Election
br.select_form(name='form1')
br.form['D3'] = ["2016 General Election - 11/8/2016                 "]

# submit form to go to next page
response = br.submit()

# print next page URL
br.geturl()

# select presidential election from form on second page
br.select_form(name="form1")
br.form['D3'] = ["President & Vice President, U.S."]

response = br.submit()
br.geturl()

# pull presidential election results into dataframe
content_string = response.read().encode("utf-8")
tabledata = table_reader(content_string)

# remove unnecessary title headers (first two rows and last 3 rows)
data_no_title = tabledata[2:-4]

import pandas as pd
presidentialvotes_df = pd.DataFrame(data_no_title[1:], columns=data_no_title[0])

presidentialvotes_df.head(10)


# Go back through and do the same thing to get US Senator election results from 2016
br.geturl()
br.back()
# select majoral election from form page
br.select_form(name="form1")
br.form['D3'] = ["Senator, U.S."]

response = br.submit()
br.geturl()

# pull Senator election results into dataframe
content_string = response.read().encode("utf-8")
tabledata = table_reader(content_string)

# remove unnecessary title headers (first two rows and last 3 rows)
data_no_title = tabledata[2:-4]

senatevotes_df = pd.DataFrame(data_no_title[1:], columns=data_no_title[0])
senatevotes_df.head(10)

all_votes = pd.merge(presidentialvotes_df, senatevotes_df, on = 'Ward')
all_votes.head(100)