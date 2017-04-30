from operator import itemgetter
from selenium import webdriver
import re
import json
import pprint
import unicodedata

#used to convert scraped unicode to either a string or a float
def num_check(string):
    try:
        float(string)
        return True
    except ValueError:
        pass
    try:
        unicodedata.numeric(string)
        return True
    except (TypeError, ValueError):
        pass
    
    return False


def build_nba():
    
    #launch chrome with selenium
    path_to_chromedriver = '/Users/Matt/Desktop/Python/chromedriver'
    browser = webdriver.Chrome('/Users/Matt/Desktop/Python/chromedriver')

    #pass the table id and cateogies/stats desired
    def get_data(table, add_cats, add_nums):
        cats = []
        nums = []
        
        #pull categories and stats
        stats = browser.find_elements_by_id(table)[0]
        heads = stats.find_elements_by_tag_name('thead')[0]
        categories = heads.find_elements_by_tag_name('th')
        
        #adv stats only accessable by row
        if (table == 'all_advanced'):
            adv_heads = stats.find_elements_by_tag_name('tr')
            #first half of rows given are usless
            #then categories and data are provided in sequence
            half = (len(adv_heads) - 1)  / 2
            
            for i, head in enumerate(adv_heads):
                #get categories
                if (i == half + 1):
                    for category in head.text.split(' '):
                        cats.append(re.sub('%', '', category))
                #get data
                if (i > half +1):
                    number = re.sub('(\D+)\s(\D+[^ 0-9A-Z])', r'\1-\2', head.text)
                    nums.append(number.split(' '))
                    
        #all other tables are easily accessable      
        else:
            for category in categories:
                cats.append(re.sub('%', '', category.text))
        
            rows = stats.find_elements_by_tag_name('tbody')[0]
            numbers = rows.find_elements_by_tag_name('tr')
            
            #add dash between player's name, then split on spaces
            for number in numbers:
                number = re.sub('(\D+)\s(\D+[^ 0-9A-Z])', r'\1-\2',number.text)
                nums.append(number.split(' '))
                
        edited_nums = []
        
        #swap position of name and no. from 'roster', so that number is first
        #for sorting purposes        
        if (table == 'all_roster'):
            for num in nums:
                num[0], num[1] = num[1], num[0]
                
        #account for players without a 3PA or FTA
        if (table == 'all_per_game'):
            for num in nums:
                if (len(num) < len(cats)):
                    num.insert(11, 0.0)
         
        #append desired stats/categories as their proper type
        for player in nums:
            edited_nums.append( [float(v) if num_check(v) else str(v) for i, v in enumerate(player) if i in add_nums])
        
        
        edited_cats = [str(v) for i, v in enumerate(cats) if i in add_cats]
        
        #add picture link and category
        if (table == 'all_per_game'):
            edited_cats.append('Pic')
            
            links = stats.find_elements_by_tag_name('td')
            pics = []
            
            #gather links
            for link in links:
                if link.get_attribute("data-append-csv") != None:
                    pics.append(str(link.get_attribute("data-append-csv")))
            
            #add them to their correct player    
            for i, pic in enumerate(pics):
                edited_nums[i].append(pic)
               
        #return values with info sorted by name, for cross-table consistancy
        return (edited_cats, sorted(edited_nums, key=itemgetter(0)))
    
            

    def build_team(*args):
        team = {}
        final_cats = []
        first_nums = []
        final_nums = []
        
        #full list of categories
        for arg in args:
            final_cats.extend(arg[0])
            
        #start with per game stats
        for arg in args[0][1]:
            first_nums.append(arg)
            
        #for subsequent tables get index of each arrray containing each player's name 
        #(at index 0) from final_nums, then extend the array for each player in every 
        #table that have the same name at index 0 as that base array
        for arg in args[1:]:
            for player in arg[1]:
                index = next(((i, num.index(player[0])) for i, num in enumerate(first_nums) if player[0] in num), None)
                try:
                    first_nums[index[0]].extend(player[1:])
                except(TypeError, ValueError):
                    pass

        final_cats.insert(0, 'Name')
        
        #filter out incomplete results
        for num in first_nums:
            if len(num) == 21: #21 == total number of categories
                final_nums.append(num)
                
        #zip categories and stats into a dict for each player
        for num in final_nums:
            team[str(num[0]).replace('-', '')] = dict(zip(final_cats, num))
            
        #add a logo for each team
        team['Logo'] = abbrv
        
        #add each team full of player to the league
        nba[abbrv] = team
    
    
    abbrvs = ['GSW','BRK','BOS','CHI','CHO','CLE','DAL','DEN','GSW','DET','HOU','IND','LAC','LAL','MEM',
        'MIA','MIL','MIN','NOP','NYK','OKC','ORL','PHI','PHO','POR','SAC','SAS','TOR','UTA','WAS']

    nba = {}
    
    #go to each team's page to pull data
    for abbrv in abbrvs:
        
        url = 'http://www.basketball-reference.com/teams/'+abbrv+'/2017.html'
        browser.get(url)
        
        per = get_data('all_per_game',[2,8,11,15,18,21,22,23,24,27],[1,2,8,11,15,18,21,22,23,24,27]) 
        roster = get_data('all_roster',[0,2,3,4],[0,1,2,3,4])
        salaries = get_data('all_salaries2',[2],[1,2])
        advanced =  get_data('all_advanced',[4,5,20,27],[1,5,6,19,24])
        
        build_team(per,roster,advanced,salaries)
      
    #write to a json file
    with open(r'C:\Users\Matt\Desktop\Python\nbaJSON.json', 'w') as output:
        json.dump(nba, output, sort_keys = True, indent = 4, ensure_ascii = False)
    
    browser.quit()
    pprint.pprint(nba)
    
      
build_nba()

    
    