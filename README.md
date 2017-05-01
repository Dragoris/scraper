# Scraper
A web scraper to gather NBA data from basketballreference.com. Per-Game, Roster, Advanved, and Salary tables are scraped and formatted into a JSON object that is then written to the nbaJSON file.
The data structure is then run through a simple validation that uses type, length, and Regex to varify all stats match up to the correct categorey. Once validated, I use this JSON file to power my NBA Trade App.

The key to this script is the get_data() function, which accepts a table name and two lists, one for the index of desired categorey in BBR's table and one for the index of the stats. get_data() is able to pull info for teams or players from any table on the BBR/teams page. When build_nba() is called it accepts a variable number of argumenets (tables) and will stitch those tables together for each player on each team in the NBA. 

I would like to thank basketballreference.com for making this data available. BBR is an amazing site that provides up to date information on a huge number of stats. If you have any intrest in further exploring NBA data I highly recommend checking out their site.



