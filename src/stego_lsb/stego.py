#!/usr/bin/env python
# coding=utf-8
#
#
# Copyright 2021 Carlos Panduro
#
#

import random
import os
# import sys
from optparse import OptionParser
from PIL import Image

""" if "darwin" in sys.platform:
    os.system("clear")
elif "win" in sys.platform:
    os.system("cls")
elif "linux" in sys.platform:
    os.system("clear")"""


def main():
    # datos iniciales
    #################
    flag = 1  #
    firma = "0100110001010011010000100111001101110100011001010110011101101111"  #
    #################

    parser = OptionParser()
    parser.add_option("-E", dest="extract", action="store_true", help="Extract hidden message")
    parser.add_option("-i", dest='image', help="Image to analyze", metavar="<image>")
    parser.add_option("-s", dest="secret", help="Text file to hide", metavar="<secret text>")
    (opts, args) = parser.parse_args()

    if opts.extract is None:
        print("""
-----------------------------------------------------
           Running STEGO code to encrypt:                
           image: """ + str(opts.image) + """   
           text: """ + str(opts.secret) + """
-----------------------------------------------------""")
    else:
        print("""
-----------------------------------------------------
           Running STEGO code to decrypt:                
           image: """ + str(opts.image) + """   
-----------------------------------------------------""")

    if opts.extract is None:
        flag = 0
        if opts.image is None or opts.secret is None:
            exit(
                "[+] Error [+] \n[+]Both parameters must be declarated, example: \n\nHide:\n\t>>>python "
                "stego.py -i image.png -s secret.txt \nExtract:\n\t>>>python stego.py -E -i image.png")
    else:
        if opts.image is None:
            exit(
                "[+] Error [+] \n[+]A parameter must be entered, example: \n\nHide:\n\t>>>python stego.py -i "
                "image.png -s secret.txt \nExtract:\n\t>>>python stego.py -E -i image.png")

    try:
        img = Image.open(opts.image)
        print("Loading image...")
        im = img.load()
        print("Indexing image...")
    except:
        exit("Error opening the image, please check it")

    tamx, tamy = img.size
    rand = random.randrange(100)

    if flag == 0:

        info = extract_text(opts.secret)
        bits = len(info)
        print(bits, int2bin(bits))
        info = int2bin(bits) + firma + info

        print("Hiding data...")

        for x in range(0, tamx):
            for y in range(0, tamy):
                for h in range(0, 3):

                    if len(info) != 0:
                        Alpha = im[x, y][h]
                        bAlpha = int2bin(Alpha)
                        copy = list(im[x, y])
                        copy[h] = int(secret(bAlpha, info[0]), 2)
                        im[x, y] = tuple(copy)
                        info = info[1:]
                    else:
                        break

        print("\nProcess finished...\n\n\tHided: \t", bits,
              " information bits \n\tUsed: \t", bits / 3, " pixels\n")
        print("Saving the information...\n\n"
              "\tOriginal Image: ", opts.image, "\n"
              "\tSecret File:    ",opts.secret, "\n"
              "\tSecret Image:   quic_stego/examples/htdocs/icon.png")


        root_dir = os.path.dirname(os.path.abspath(__file__)).replace("src/stego_lsb", "")

        img.save(str(root_dir) + "examples/htdocs/icon.png")
        exit()

    else:
        img_bin = bin_image(im, tamx, tamy)
        search = img_bin.find(firma)

        if search != -1:

            print("Signature Found")
            bsize = img_bin[:search]
            size = int(bsize, 2)
            img_bin = img_bin[search + len(firma):]
            n = size / 8
            salida = ""
            letra = ""
            print("Extracting Data...")

            for i in range(0, int(n)):
                letra = img_bin[0:8]
                salida += chr(int(letra, 2))
                img_bin = img_bin[8:]
            search_secret(salida, rand)
        else:

            print("Signature NOT Found, everything will be extracted")
            n = len(img_bin) / 8
            size = len(img_bin)
            salida = ""
            letra = ""
            print("Extracting Data...")

            for i in range(0, n):
                letra = img_bin[0:8]
                salida += chr(int(letra, 2))
                img_bin = img_bin[8:]

            search_secret(salida, rand)
        print("\nFinished process: \n\n\tExtracted: \t", size,
              " infromation bits\n\tUsed: \t", size / 3, " pixels\n")
        print("Saving information...\n\n"
              "\tOriginal Image: " + str(opts.image) +"\n"
              "\tExtracted Secret: result_resources/secret" + str(rand) + ".txt")


def search_secret(dato, rand):
    salida = open("result_resources/secret" + str(rand) + ".txt", "a")
    salida.write(dato)
    salida.close()


def bin_image(image, m, n):
    print("Creating Binary Image...")
    text_ext = ""
    for x in range(0, m):
        for y in range(0, n):
            for h in range(0, 3):
                text_ext += str(int2bin(image[x, y][h]))[-1]
    return text_ext


def secret(binario, bit):
    lsb = binario[:7] + bit
    return lsb


def int2bin(n):  # conversion del entero a binario
    b = bin(n)
    bina = b[2:]
    resto = len(bina) % 8
    if resto != 0:
        bina = "0" * (8 - resto) + bina
    return bina


def extract_text(path):  # extrae los datos a esconder
    try:
        archivo = open(str(path), "r")
        datos = archivo.read()
        print("Loading text...")
        dt_bin = ""
        for x in datos:
            dt_bin += int2bin(ord(x))
        print("Generating binary file...")
        return dt_bin
    except:
        exit("Error opening text file, please check")


if __name__ == "__main__":
    main()
