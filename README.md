# _Set!_ game

This repository contains a Python 3.5+ implementation of the [Set! card game](https://en.wikipedia.org/wiki/Set_(card_game)), playable online with people from other computers provided you have a server to connect your clients to, or offline with multiple clients on the same computer, using your own computer as the server.

## Composition

The repository is divided into serverside code, clientside code, and image ressources, in the accordingly named folders. A `Set.bat` batch file, whose purpose is to launch a client without having to open a command prompt for Windows users, is also given.

## Serverside install

Send the `server` folder to the computer that is going to be the server, at your favorite directory. It can be anything from a headless server on the cloud to your own laptop, given it is set up so that it can be seen by the other computers that will be the clients, and given Python 3.5+ is installed.

The server is simply launched by executing `server.py` with Python 3, which can also be done with a double click on `activate_server.bat` on Windows. 

## Clientside install

Each client computer will need the `src` and `images` folders installed in the same directory, and optionally `Set.bat`. Inside that same directory, create a text file named `ip.txt` and write the server's IPv4 address inside that file. The IPv4 address is composed of 4 numbers between 0 and 255 separated by points, for example 128.192.1.1. A fast way to know the IP address of your own computer is to google "what is my ip address".

Each client will need Python 3.5+ as well as the `pygame` module, which can be installed with the `pip install pygame` command.

To launch a client, execute `client.py` with Python 3 or double click `Set.bat`. This can be done multiple times on the same computer, which means you can launch multiple clients on the same computer.

## Rules and gameplay

You can see the rules [here](https://en.wikipedia.org/wiki/Set_(card_game)).

After launching the client, a game window will open. After a few seconds (it has to load the images) it is brought to a grey screen. Click it to try to connect. Failing this step could either mean you copied a wrong IP address, or your server is not properly set up to be visible by the client, or the server is not executing `server.py`.

In this computer version of the game, a spacebar press translates to shouting "Set!". After that press, you have 3 seconds to click on the 3 cards that you think make up a set. If the 3 cards indeed make up a set, the client responsible for that action earns 1 point, otherwise he loses one.

If a client thinks that the 12 cards in game do not contain any set, they can press 5 or Enter or Backspace to "cast a vote", meaning they wish to add 3 more cards to the board. When all clients have cast their vote, 3 more cards are added. This process can be repeated a second time for a total of 18 cards available. The vote process will fail when there are no more cards to add, in which case the game can be ended.

To properly end a game (either because because there are no more cards to add to the board, or your opponents have left), press the Escape key. This will bring the client back to the first screen so they can immediately restart a new game.

By default a game is limited to 4 people. This means if a 5th client tries to connect, they will be sent to a separate game. A potential 6th client will then connect to the 5th client's game.

A game is destroyed when all its clients have left. This means that if 2 clients are playing a game, and player 1 disconnects, and wants to reconnect, they will end up as player 3 in the same game. But if player 2 disconnects before player 1 manages to reconnect, that game would be destroyed so player 1 would join a new game.*
