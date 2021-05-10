stego_lsb
===========

This tool allows us to perform the LSB technique in images, with which we can hide texts (and other things) in the least significant bits of the image and, reciprocally, reveal them.


* **Hide Information**: it will save secret image in secretImageXX.png.
  
  example.png : it is the image where the secret will be hidden.
  secret.txt : it is the message that we want to embed in the image.
  
  >python stego.py -i image.png -s file.txt  

* **Extract information**: it will save the secret in secretXX.txt.
  
  image.png : it is the image with the hidden text, with the -E option it is revealed.

  >python stego.py -E -i secretimageXX.png
