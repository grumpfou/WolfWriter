WolfWriter is a software written by Renaud Dessalles.

It's goal is to help writers to write their novels and to explort it to other formats (for now, only on .txt). The associate files are archives files with the exention .ww .

= Principles =

== WYSIWYM ==
The philosophy of this software is WYSIWYM (What you see is what you mean) like the software LyX (http://www.lyx.org/). What you see on the screen is very close to what you will have, but this software oblige the writer to respect the typography rules of the language. For instance it will prevent to put two consecutive spaces to put a space before a coma, to have curved apostrophe etc. The goal is to have a clean text to work on.

== Writing help ==
The goal is to help, as much as possible the writer to write quickly and clearly. So I introduce auto-corrections (for example, you can transform "sth" in "something" every time you write it), it has some "pluggin" that help for the language you write your book (for example, it bring the dialogs dash and the accentuate capital letters for the French). Other pluggins can be added, for instance to generate some random names, to search and replace in the text etc.

== Encyclopedia ==
Writing a book is not only writing a story, it is to bring a whole imaginary world to life. In order to do so, I created the Encyclopedia which has entry for every characters, places or concepts in the book. Every entry can have a small decription and be link with other concepts.

== Tree-like structure ==
The Book is but in a tree-like structure. For now, it has only 2 levels of leafs : the chapters and the scenes. Every chapters contain one or several scenes. The scene is the basic block of the story (it is even considered as a special file in the .ww archive). A scene cant be moved across the story, changed with an external software etc.

== Statitics ==
I want also a software to make some statistics. For now it is only numers of word in the scenes, in the chapters but I want to improve this feature. For instance, you can now save in the .ww archive a a version of your book at a precise moment. So in the future you can se your evolution in wrtting.

= The script =

== Python and PyQT ==
The script is written with Python 2.7 (http://www.python.org/) using the library PyQt4 (http://www.riverbankcomputing.co.uk/software/pyqt/intro). You must instal them in order to make the software work.

== Way of writting ==
I seperate the script into two main sort of file : WWCore files and WWGui files (you can open WolfWriter_Project.xml in order to see the list).
 - WWCore files represent as much as possible the non vizualised part of the software. The decoding of the structure of the .ww archive file, the dictionary of word structure etc. Normally, it must not deals with PyQt.
 - WWGui files represent as much as possible the vizualised part of the software. The main window, the text editor etc. Normally one of the imported library must be PyQt4.
If I want to sum up in an diagram I would make that:
		the .ww archive file    <-->    WWCore files    <-->    WWGui files    <-->    the user

Usually the names of the files begin with "WolfWriter..." and the class and the function begin with "WW...".
In the structures decribed in the WWGui files, I clearly seperate the slot methods by a englobing comment lines begining like "#####SLOTS#####" and ending with "###############". Moreover, the methods' names begin with "SLOT_..." (except if they are re-writings of PyQt methods).
