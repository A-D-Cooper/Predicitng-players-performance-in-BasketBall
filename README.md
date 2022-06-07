# Predicitng players performance in BasketBall

#### This is one of my perosnal projects and right now it's incomplete. The data I obtained is quite messy and a lot of clean up needed to be done to use it thus you would see multiple files here that do very similar things. I used many different ways to process data, every time making it slightly different that why you would see a lot of commneted out statemnts in the code. 

## Data Collection

##### Most of the data used in this project is obrained from stathead.com. stathead.com has historical data available for most sports league played in North Ameirca. 
##### I used Selenium and BeautifulSoup4 to extract data becuase the data isn't available in .csv format and you can't download it in bulk either. web_scraper.py has the code necesasry for that.

## Data Processing

##### Data processing is quite hard and I used Pandas and NumPy to accomplish it. Reading the data from the file using Pandas then converting it into .csv. A huge problem with using vanilla neural network is that each example that is fed to the model is assumed to be independent. But the performance of a player depends on his/her past performances thus I used some of their previous games to predict the performance in the current game and putting more empahsis on recent games. I tried a few number of different games to see what performance I can get.

#### The problem with getting data from stathead.com is that, either the data is avaiable for each palyer or each team, and overall data of team is redundant so I had to download the data of each game of each player and then use the date and team to match the players to each team and their opponents. Combining the data of past games of each player with each of their teammates and their opponents gave me each example that can be fed to NN. There are a lot of edge cases as the data provided by stathead isn't standardized. so there are multiple files that handles each of those cases.

#### Not all players play the same number of games in their careers so if there is some new player that has played few games I would just put zeros in their long term performance file. Thus the "constants.py" file.

## Prediction

#### I used Nerual netwrok as it the most powerful method available for prediction and I have an RTX 3080 that I could use to train the said Neural Network. I tried a variety of hyperparameters and got better performance when I increased the number of layers and neurons but it flatlined pretty quick as well. For some reason I was getting much better result with absolute difference loss as opposed to squared difference loss. 

## Thoughts

#### Overall it was a pretty good experience even though I didn't get the result that I wanted. Getting the right data is very difficult and expensive. Even though stathead was pretty cheap. Other sites generally don't provide this much raw data, rahter they give already processed data with some important things clumped toghether. As most of those sites desingn their data to be used by sports analyst and not for prediction, and those who do make their data for predictions are also the ones selling those predictions for betting market so they don't provide historical data that could be used for training.  I plan to retry it with hidden variable models.  
