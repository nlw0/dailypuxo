dailypuxo
=========

DAILYPUXO is a kind of art project and engineering experiment conducted by Nicolau Werneck in 2013. Tons of pictures from the same monument were taken during a whole year, and published on Twitter. You can see the pictures on http://nwerneck.sdf.org/dailypuxo .

This project contains two things. First is a twitter and twitpic crawler used to generate a large data file that contains information about all the images.

Then there is a website, made with Dart. It's a single stand-alone page that loads a larde data JSON file produced by the previous tools, and lets you navigate through the images. The images are hosted on twitpic.

The quality from this code is not good. I did it in a hurry during my vacations, while I was learning Dart one thing or two about dynamic web page development. I would love to have some more structure and classes in the code, and also maybe to move some of the logic to the server. There is probably a smarter way to do the handling of the clicks, and changes to the view, I believe what I did is a kind of primitive "model-view-controller"...

Enjoy!
