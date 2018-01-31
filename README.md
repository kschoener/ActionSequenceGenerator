# ActionSequenceGenerator

This will create an action sequence from a bunch of images that you input to the imageStack.py script.

Requirements: OpenCv2 and PIL (Python Image Library)

If the camera wasn't steady during the photographs, first use imageAlign.py to align all of the images with a specified image.
Ex: python imageAlign.py alignWithThisImage.jpg alignTheseImages/

Now, to create the Action Sequence you simply run the script and point to the directory that holds the images you wish to make an action sequence out of.
Ex: python imageStack.py path/to/pictures/

*NOTE: this is not a perfect solution. If the background changes in the slightest, there will be some deformation in the resulting image (see skateboarder in sample output).
