import json, ast, re, pprint

with open(r'C:\Users\Matt\Desktop\Python\nbaJSON.json') as data_file:    
    load =  json.load(data_file)
    data = ast.literal_eval(json.dumps(load))
    
    teams = data.keys()
    invalid = {}
    invalid_teams = set()

    #check each stat, for each player, in each team.
    #if a test fails record the player and team
    for team in teams:   
        for player in data[team]:
            for stat in data[team][player]:
                try:
                    value = data[team][player][stat]
                    
                    if (stat == "Name"):
                        if (isinstance(value, str) and bool(re.search('\D[-]', value)) and len(value) > 3):
                            pass 
                        else:
                            invalid[player] = data[team][player]
                            invalid_teams.add(team)
                            print "STAT ERROR", stat, value
                            
                    elif (stat == "Pic"):
                        if (isinstance(value, str) and bool(re.search('[a-z][0-9]'))):
                            pass 
                        else:
                            invalid[player] = data[team][player]
                            invalid_teams.add(team)
                            print "STAT ERROR", stat, value
                        
                    elif (stat == "Pos"):
                        if (isinstance(value, str) and len(value) < 3):
                            pass
                        else:
                            invalid[player] = data[team][player]
                            invalid_teams.add(team)
                            print "STAT ERROR", stat, value
                        
                    elif (stat == "Ht"):
                        if( isinstance(value, str) and bool(re.search('\d[-]', value)) and len(value) >= 3):
                            pass 
                        else:
                            invalid[player] = data[team][player]
                            invalid_teams.add(team)
                            print "STAT ERROR", stat, value
                        
                    elif (stat == "Salary"):
                        if (isinstance(value, str) and bool(re.search('\$', value))):
                            pass
                        else:
                            invalid[player] = data[team][player]
                            invalid_teams.add(team)
                            print "STAT ERROR", stat, value
                        
                    elif (stat == "AST" or stat == "STL" or stat == "Age" or
                        stat == "VORP" or stat == "Wt" or stat == "PER" or
                        stat == "BLK" or stat == "PTS/G" or stat == "WS" or
                        stat == "No." or stat == "TRB"):
                        
                        if (isinstance(value, float) and bool(re.search('\d[.]', value))):
                            pass
                        else:
                            invalid[player] = data[team][player]
                            invalid_teams.add(team)
                            print "STAT ERROR", stat, value
                    
                    elif (stat == "TS" or stat == "3P" or stat == "FG" or stat == "eFG" or stat == "FT"):
                        if (isinstance(value, float) and value <= 1):
                            pass
                        else:
                            invalid[player] = data[team][player]
                            invalid_teams.add(team)
                            print "STAT ERROR", stat, value
                                    
                    else: print "missed one", stat
                    
                except (KeyError, TypeError):
                    pass
    #remove invalid players from the data structure
    for invalid_team in invalid_teams:   
        for player in data[invalid_team].items():
            print player[0], invalid_team
            if (player[0] in invalid.keys()):
                del data[invalid_team][player[0]]
        
    #re-write the file without the invalid entries
    with open(r'C:\Users\Matt\Desktop\Python\nbaJSON.json', 'w') as new_JSON:
        new_JSON.write(json.dumps(data, sort_keys=True, indent=4, separators=(',', ': ')))
