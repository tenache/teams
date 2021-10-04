# teams
A program to try to create teams to allow for a more competitive match. Good for any sport. 

Often when playing pick-up like games, I've found myself in situations where we want to quickly divide into teams. Although usually this isn't a problem, I've been in groups
where a few bad apples hog all the best players. One way to avoid this is to completely randomize the teams, which we can do on an excel sheet. But since we're doing that, 
why not make a program that keeps track of all the players wins/losses, thus deliberately avoiding lob-sided games? Since we're at it, let's take into account the performance 
of certain combinations of players. For example, in basketball, you might have one big strong guy that plays well as a center, and one small guy that plays well as a point-guard
who separately are OK, but together are unbeatable (thus creating lob-sided and boring results). The program will take the profficiency of all combinations of players into account. 

## Getting started 
 In order to get started, you can use the main function, but you want to get to know the methods and functions in order to make use of everything in the package. 
 To get started, you need a csv file named 'players.csv', which will have one column with the players names on them, one column with their 'talents' (initially you will 
 be required to subjectively rate them, but this rating will change as players win or loose more than their share). Talents should be regarded ideally as a percentile, so 
 a talent score of 50 means that there are approximately half of the players are better, while half are worse. On the other hand, a talent score of 100 means this player is
 better than all the other players uploaded. Try not to be too kind, at the end, around half of the players should have scores above 50, and the other half below 50 for the program 
 to work ideally. In the third column you should include a list of the players possible positions (for example: center,power_forward, or : point_guard,shooting_guard). 
 If a player can play in any position you can put the word wildCard. The last two columns are optional, as you only require the first. If there is no second or third column, the
 default is for talent: 50, and for positions: wildCard. 
 two columns are optional. If the 
 The program should save the results in a file with the name of the user {username}.pkl. 
 ##The classes
 ###Class player
 Class player has the following attributes:
 1.name
 2.talent (initially taken from the csv file, later adjusted according to wins/losses)
 3.positions (taken also from the csv file)
 4.wins 
 5.losses
 6.winMargin (which is (wins - losses)/(wins+losses))
 It also has the method: calculateTalent, which updated the talent according to wins and losses
 
 
 
