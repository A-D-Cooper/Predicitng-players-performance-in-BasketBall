# Predicitng players performance in BasketBall

#### This is one of my perosnal projects and right now it's incomplete.

## Data Collection

##### Most of the data used in this project is obrained from stathead.com. stathead.com has historical data available for most sports league played in North Ameirca. 
##### I used Selenium and BeautifulSoup4 to extract data becuase the data isn't available in .csv format and you can't download it in bulk either. web_scraper.py has the code necesasry for that.

## Data Processing

##### Data processing is quite hard and I used Pandas and NumPy to accomplish it. Reading the data from the file using Pandas then converting it into .csv. A huge problem with using vanilla neural network is that each example that is fed to the model is assumed to be independent. But the performance of a player depends on his/her past performances thus I used some of their previous games to predict the performance in the current game and putting more empahsis on recent games. I tried a few number of different games to see what performance I can get.

## Neural Network.

#### I tried a variety of hyperparameters and got better performance when I increased the number of layers and neurons but it flatlined pretty quick as well. For some reason I was getting much better result with absolute difference loss as opposed to squared difference loss.

## Thougts

#### Overall it was a pretty good experience even though I didn't get the result that I wanted. I plan to retry it with hidden variable models.  
