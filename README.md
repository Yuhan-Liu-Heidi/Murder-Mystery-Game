# Murder-Mystery-Game
Inspired by the board game *Who is the Murderer*, we developed a website to 
host the game and allow players to have happy hours with friends while 
maintaining social distancing.

## User Guide
### Rules
The game puts the player into the scenario of a murder or a tragic event, and 
the goal is to find out the murderer or the culprit. The game requires 3-8 
players. While all of them are suspects, one of them will be the murderer. Each
player chooses a character to play out and acquires three parts of information
at the beginning of the game, which are (1) memories of major events, (2) 
timeline of own actions and witnessed events and (3) own tasks.

### How to play
#### 1. Set up and Log in
Use the recommended browser to open the link provided by the Game Manager, then
click **start**.(Recommended: Google Chrome on a PC)<br>
For each new game, please sign up with a user ID and password combination of 
choice. You can use the same combination to log in throughout the game.
#### 2. Choose character
After logging in, the website re-directs to a character choosing page to
display all characters that will appear in the game. Click on **choose** to
go to the play page, and the character cannot be changed once selected.
#### 3. Read, search, discuss and vote!
There are three sections on the play page: a image containing all the info a
player needs to know, a set of buttons and displaying windows to search and see
clues, and a set of buttons to vote for the murderer.<br>

A typical game follows these steps:
1. Do self introduction
2. Search for clues
3. Deduct based on the events and the clues searched
4. Vote for the murderer when every player is ready

The website shows update to players who have finished voting, and announces the
result after all players voted. Once voted, a player cannot go back to play
page.

## Game Manager Guide
### Prepare a story
This website does not come with a scenario and characters, so you need to have
a story ready.
### How to use the website
Write the story into files as directed below.<br>
Download the project, add your story file and run the file [gui.py](). Then
inform the players of the link, which should be http://(your Public IP):5000
<br>
Do not shut down once the game has begun.
> Format Guide:
> * Information for each user should comes in an image
> * Other game information should be stored in a JSON file with the following
aspects: (See [sample_game.json]() for an example)
>  1. Player number
>  2. Characters
>  3. Places
>  4. Clues allocated to places