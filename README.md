# BitBotPathFollow
Use micro Python on micro:bit to program your bit:bit to retrace a path

Concieved and written by Philip Meitiner - @PragmaticPhil.

Do with it what thou wilt.

Thanks to several people who helped me discover the vagaries of Python.  
No names though, cos I don't want your esteemed reps to be denigrated by my humble scratchings.
And also to 4Tronix for giving me a bit:bot :)

Note - I expect that the code will work with similar robots.
You may need to make a few minor tweaks to bitBot_PostPath_1.py for each though.
Key is:
... there are 4 pins, 1 forward left, 1 back left, 1 forward right, 1 back right
... the robot is a state machine (are they all - I don't know) - by this I mean, when a command is sent to the robot it will persist until another command is sent
Happy to test it our on other devices (its just that I don't have any atm ;)


This app actually does 2 things:
1 - it is a quite decent straight up RC - moves quite nicely, especially corners.
2 - once you've driven it, SHAKE your RC then push A - the bibot will now retrace the path you drove.  Its cool!

Some notes:
... you will need 2 microbits - one is your Remote Controller (RC) the other controls the bit:bot
... load RC_StorePath_1.py onto your RC
... load bitBot_PostPath_1.py onto your bitbot.

More Notes:
... I had to remove comments from the long one - was getting memory errors.  It worked, but comments are sparse.  Sorry.
... neopixels are a bit erratic - have limited their use on this basis.

What Next:
... for me on this, nothing.  This was a POC for a bigger project I am planning.
... Would be interesting to have a reverse path option (was my original idea)
... analog out to vary speed
... better neo-pixel support.

What is good about this:
... the RC actually has a not-so shabby implementation of button_down and button_up.
... it also drives quite nicely, although you may want to set the tilt active level to your tastes.
... efficiency of radio transmits... only send 1 per event.  I like that - early iteration appeared to have issued with radio commands stacking up.

BUGS:
... every so often the button release does not process properly and the robot spins despite button release. Can;t replicate but I think that some events are clashing.
... once the path has been retraced once thats it.  WiP.
... there is an upper limit on the size of the path - not really quantified yet
... some radio packets are dropped / missed.  I don't think this is the code, but it could be.
