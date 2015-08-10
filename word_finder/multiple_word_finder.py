import csv
from splinter import Browser
import regex as re
import string
import webbrowser

#####Michigan proquest login url
url = 'http://search.proquest.com.proxy.lib.umich.edu/?accountid=14667'

#####Collection of possible newspapers to call
nyt_id = 'pubid(11561)'  
wall_st_id = 'pubid(10482)'
usa_id = 'pubid(15008)'
lat_id = 'pubid(46999)'
nydn_id = 'pubid(14434)'
wapost_id = 'pubid(10327)'
chicago_trib_id = 'pubid(46852)'
    
    
def login(brows, user_name, password):
    brows.visit(url)
    brows.fill('login', user_name)
    brows.fill('password', password)

#####runs the advanced search and pulls up the first results page
def advanced_search(pub_id, search_term, year=None, sports=False, phantom=False, user_name, password):
    if phantom == True:
        browser = Browser('phantomjs')
    else:
        browser = Browser('firefox')
    login(browser, user_name, password)
    button = browser.find_by_name('doLogin').first.click()
    browser.click_link_by_href('advanced')
    browser.fill('queryTermField', pub_id)
    browser.fill('queryTermField_0', search_term)
    browser.select('fieldsSelect_0', 'all')
    if sports == False:
        browser.select('opsSelect_0', 'NOT')
        browser.fill('queryTermField_1', 'sports')
        browser.select('fieldsSelect_1', 'ti')
    if year != None:
        browser.select('select_multiDateRange', 'ON')
        browser.fill('year2', year)
    search_but = browser.find_by_name('searchToResultPage').first.click()
    return browser


def find_number_of_articles(search_result_brows):
    span_list = search_result_brows.find_by_css('span')
    p = re.compile('^\d+\sResults')
    numb = re.compile('\d')
    for i in range(len(span_list)):
        span_txt = span_list[i].value
        match_tst = p.match(span_txt)
        if match_tst:
            number_of_articles = numb.findall(span_txt)    
            number_of_articles = int("".join(number_of_articles))
            return number_of_articles

#print find_number_of_articles(nyt_browser)
            
def clean_text(text):
    text = text.lower()
    text = re.sub(ur"\p{P}+", "", text)
    return text

def find_if_match(word, text):
    word_p = re.search(word, text)
    if word_p:
        return True
    else:
        return False

def word_count_single_page(brows, wrd_lst, nxt_clicks):
    count_dict = {}
    for word in wrd_lst:
        count_dict[word] = 0
    for i in range(nxt_clicks):
        print i+1
        try:
            article_body = brows.find_by_css('text').first.value
            article_body = clean_text(article_body)
            for word in wrd_lst:
                match = find_if_match(word, article_body)
                if match == True:
                    count_dict[word] += 1
                    print 'MATCH for %s' % word
                    webbrowser.open(brows.url) ###opens the link for human check
        except:
            print "Text was unreadable"
        try:
            brows.click_link_by_partial_text('Next')
        except:
            break
    return count_dict

        
###################final search function
def word_count_paging(pub_id, search_term, wrd_lst, year=None, sports=False, phantom=False, user_name, password): ###number of articles with a certain word
    browser = advanced_search(pub_id, search_term, year, sports, phantom, user_name, password)
    numb_of_articles = find_number_of_articles(browser)
    print "Total number of articles about %s from %d is %d" % (search_term, year, numb_of_articles)
    pages = numb_of_articles/100 + 1
    final_page = numb_of_articles - numb_of_articles/100 * 100
    total_dict = {}
    for word in wrd_lst:
        total_dict[word] = 0
    for page in range(pages):
        print "analyzing page %d out of %d" % (page+1, pages)
        if page == 0:
            browser.click_link_by_partial_href('/docview/')            
        else:
            browser = advanced_search(pub_id, search_term, year, sports, phantom)
            browser.select('itemsPerPage', '50')
            browser.find_by_name('submit_11').first.click()
            nxt_page_clcks = page*2
            for i in range(nxt_page_clcks):
                browser.click_link_by_partial_text('Next page')
            browser.click_link_by_partial_href('/docview/')  
        if page < pages-1:
            page_dict = word_count_single_page(browser, wrd_lst, 100)
            for word in page_dict:
                total_dict[word] +=  page_dict[word]
        else:
            page_dict = word_count_single_page(browser, wrd_lst, final_page-1)
            for word in page_dict:
                total_dict[word] +=  page_dict[word]
        browser.quit()
    return total_dict


####example call with a list of businesses from the csv "us_too_detroit.csv"    
    
aa = open('us_too_detroit.csv')
csv_aa = csv.reader(aa)

biz_list = []
for biz in csv_aa:
    biz_list += [biz[0]]

biz_list += ['shinola', 'slows', 'bridgewater']    
    
    
a = word_count_paging(chicago_trib_id, 'Detroit', biz_list, 2012, phantom=True, #user_name, #password) ####user_name and password are removed
for word in a:
   print "%s : %d" % (word, a[word])