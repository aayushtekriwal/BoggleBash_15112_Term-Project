-------------------------------------------------------------------------------
Boggle Bash read-me
Release version: 1.0
Last updated:    2013-04-29
By: Aayush Tekriwal
contact: atekriwa@andrew.cmu.edu
-------------------------------------------------------------------------------


Table of contents
-----------------
1.0) About
2.0) Contacting
 * 2.1) Reporting bugs
3.0) Supported platforms
4.0) Installing and running Boggle Bash
 * 4.1) General Usage Notes
 * 4.2) (Not-Required) 3rd party libraries 
5.0) Boggle Bash features and How the game works
 * 5.1) Files and Modules


1.0) About
---- -----

Boggle Bash is a intuitive word game based on the popular game Boggle/ scramble
with friends, by parker brothers. It attempts to mimic the original game
as closely as possible while adding a few new features that are unique to only
this game. 


2.0) Contacting
---- ----------
The easiest way to contact me (Aayush Tekriwal) is by writing bug reports or
e-mailing comments through my website www.aayusht.com. 

The BoggleBash homepage is http://www.aayusht.com/#!bogglebash/c1uvs


2.1) Reporting bugs
---- --------------
First of all, check whether the bug is not already known. Do this by looking
through the forum of this game on the website:
	http://www.aayusht.com/#!bogglebash/c1uvs

When you are sure it is not already reported you should:
 * Make sure you are running the latest version.
 * If the bug still exists, go to the contact page of the website, and
  elaborately explain under what conditions, or circumstances the bug
  is observed.

After you have done all that you can report the bug. Please include the
following information in your bug report:
 * Game version __.__
 * Bug details, including instructions how to reproduce it
 * Platform (Windows, Linux, Mac, ...) and compiler (including version)


3.0) Supported platforms
---- -------------------
Boggle Bash can be compiled and run on several platforms. However, it runs best
on Macintosh, and Windows computers because it was designed for them. 
- Some objects and widgets may seem oversized or undersized on UNIX platforms.


4.0) Installing and running Boggle Bash
---- ----------------------------------
Installing Boggle Bash is fairly straightforward. 
- First you need to obtain, and download the BoggleBash zip file. 
   Available on http://www.aayusht.com/#!bogglebash/c1uvs
- Extract all files and save the folder as it is in the desired directory,
   Preferably the desktop.
- Open the file "boggleBash.py" using IDLE or any other python compiler/ SDK.
- Compile the code
- A canvas with the game running live should appear
- You are good to go!
	* Read the Game Rules and Instructions before you play
	* Refer to the help buttons in the Game for further info


4.1) General Usage Notes
---- -------------------
- The peripherals needed to play the game are a keyboard and mouse. 
- There's no need for anything beyond that. 
- Also, make sure you are running 
	Python 2.7.3 (v2.7.3:70274d53c1dd, Apr 9 2012, 20:52:43) or any version of
	python after that.


4.2) (Not Required) 3rd party libraries
---- ----------------------------------
This Game has no third party library requirements. It uses python, and its 
inbuilt graphics tkinter, along with other modules that generally come along
with Python. 



5.0) Boggle Bash Features and How the Game works:
---- --------------------------------------------
As may be obvious from the functionality of the game, the main crux of the game
revolves around the dictionary, and the backtracking algorithm which searches 
for every possible solution in the board. 

The rest is a manipulation of sets, dictionaries, loops, math and iterations.
Another aspect of the game which plays an essential role in making as realistic,
and replicative of the original game is the fact that instead of simply 
randomizing the board with a random set of characters, the board is made as 
follows:
- First the set of dice (16, or 25 based on dimensions) is randomly assigned to
	various positions of the board
- Then a random side of each dice is used to represent the displayed character. 
- Putting, all of the above, every user input is verified with the solution set,
	and given points for accordingly. 


5.1) Files and Modules
---- -----------------
Some of the python modules used to make the game are:
- Tkinter : (More Specifically: Tk, Canvas, Frame, Button), used for the 
	graphical aspectof the game. All the visuals
- ttk : themed widgets such as buttons…
- tkMessageBox: TO display dialog's for instructions and Game Rules, and sharing
	info
- random: for randomizing the board
- optparse
- dice - is an independent file that stores all the dice combinations for a 4x4
	board and for a 5x5 board in one file. It is a replication of the real 
	game's dice
- os - to handle the file writing function. Mainly for the Flex game sharing 
	feature.
- dictionary set - is an independent file that contains the entire english 
	dictionary in a set, for quick access. It is a combination of the oxford and
	webster dictionaries.
- share - is an independent file that contains data to do with a shared game 
	(Multiplayer). It is overwritten every time a new game is shared. 

