# Pi Pong 2.0
## A game of battle pong played between 2 raspberry pi's using the Sense HAT LED display.
### Set Up Instructions
*At the moment you must change the Ip's set in the proram the match the corasponding ip's of the pi's playing the game.*
```
RIGHTPI_IP = "10.41.10.??"
LEFTPI_IP = "10.41.10.??"
```
**Please ensure sense hat is installed on the pi using this command**
`sudo apt install sense-hat`
### How To Play 
- Run GameMain.py to start the game.
- A screen displaying 3 letters will show R, L, S
- Use the analog stick to select a letter by pushing the stick in that letters direction.
- Select R If you are the player on the right.
- Select L if you are the player on the left.
- Select S if you would like to play single player mode.
- Push straght down on the analog stick to confirm selection.
- The game will then start.
- If the game is multiplayer, a (waiting...) screen will scroll by until the other player connects.
- Once both players connect a countdown starts and the game begins.
- Use your the analog stick to move your paddle up and down to block the moving ball.
### Rules
- If the ball touches behind your paddle you will lose a life.
- Once 3 lives are lost you lose the game
- Every time the ball hits a paddle it has a 50% chance for the ball to speed up.
- Once the ball is at its top speed and the ball hits a players paddle, that player will gain a  point.
- Once a player has reached 5 pionts that player wins and the other player loses.


  
 Writen by *Caroline Chamberlain*
    
