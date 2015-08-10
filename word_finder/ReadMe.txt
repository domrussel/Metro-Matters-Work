README

Using University of Michigan Access to the Proquest newspaper database to pull and analyze article mentions of Detroit


Purpose -

The purpose of this project is to create a simple, automated term searcher for newspaper articles about the city of Detroit from non-local papers. The original purpose of the searcher was to make conclusions about national coverage of Detroit's businesses/revitilization - specifically the race of the owners. The program allows us to take a csv of many words or phrases and run one search that pulls up any article that mentions any of them within certain perameters.

One of our primary research interests was the number of times popular black businesses were mentioned in national newspapers compared to popular white businesses. Using the program and a csv that included the names of black and white businesses (compiled from community conversations and other online listings), we were able to draw simple conclusions about mentions of white- and black-owned businesses.


Required Downloads -

Modules: csv, splinter, regex, string, webbrowser
Browsers: firefox, phantomjs


Calls -

Calls are made through the word_count_paging function. It takes:
A publication_id (an example list is given at the top)
A single search term that defines what articles the user wants to search within
A list of words that the user wants to use to pull articles
An optional year parameter to narrow searches
An optional sports parameter that leaves out sports articles by default (useful for efficiency purposes because Detroit sports are often mentioned in other local papers, but were not useful for our queries)
An optional phantom parameter that if true will search for articles using a non-visible phantom window, if false (by default) will use a firefox browser
A umich username
A umich password


Functionality -

The program uses splinter to open a browser, enter a user's login information, conduct a search for a term, open each newspaper article, and use a regex to determine whether or not the article includes a word or phrase within a word list. If the phantom module is chosen, the fuction will pull up a firefox browser everytime it encouters a match with the word list. Because Proquest requires reauthentication every 100 articles, we created a paging system. After 100 articles, the browser is closed and a newbrowser opens and starts where the old one left off.


Output -

For our purposes, the primary output was the firefox webbrowser windows that came up for every match. These could be analyzed by a human researcher to determine the context of the mention. But the program also returns a dictionary of all of the words in the searched word list and the number of times each was used.


Example Call -

The last three lines show an example call of the function and a way to print the outputted dictionary to the screen.
It looks for articles about Detroit in the 2012 Chicago Tribune that include mentions of a business in the file us_too_detroit.csv, plus three additional businesses: Shinola, Slows, and Bridgewater.


