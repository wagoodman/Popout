Popout
======

A connect4-like game which plays against you via a minimax search.

Usage
-----
Run popout.py to play. Make moves by typing 'd1' to drop a piece in the first column, or 'p5' to pop out your own piece 
from the bottom of the board.

Edit the top of the file to change the size of the board.

About
-----
This was created to explore implementation of Minimax + alpha-beta pruning in a zero-sum game (for an AI player). 

The V2 directory does not quite work, however, it was an experiment to see if board operations could be expressed entirely
of binary (cheap) operations and a lookup cache to save time. Unfortunately the current implementation does not account for the other players 
pieces while scoring hypothetical moves, so the AI makes some pretty silly moves. 
