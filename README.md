Eyes that follow you around.

It's far from a perfect program but it helped me learn alot about `pygame` & `openCV`

There's not much to say about this repository. It uses the Haar Cascade face detectors to detect faces, 
which is in the *FaceDet.xml* file.

Takes each single frame from the live video provided by the webcam of the device and used the Haar Cascade to check for faces. Saparately it creates a pygame window and draws 2 eyes (here they're just circles because I ain't no artist) and then it takes the ratio of the dimentions of the camera to the dimentions of the window and plots eyes on the screens. It also shows your camera in a different window.

This is quite far from efficient, since it is a python repository that much must be clear. OpenCV is originally a `C` or `C++` library and it would obviously be faster in those language. I am currently working on that version of the repository.

If it exists then the link is : -------