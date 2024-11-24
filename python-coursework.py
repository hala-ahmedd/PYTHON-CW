'''
GOAL: This application aims to hide a secret message ,given by the user, in a picture. 
STEPS:
1. The message is taken from the user.
2. The message gets encrypted using The Caesar Cipher Method.
3. The encrypted message will be inputted in the image using the LSB approach.
4. The encrypted message will be extracted from the image using the LSB approach.
5. The message gets decrypted.
'''
#Importing the needed libraries for Caesar Cipher Encryption and Decryption implementation
import random #a module for generating random numbers and performing random operations including shuffling 
import string #a module that contains all the chararcters, useful for working with functions/ with strings needed

#User's input:
secret_message=input("Enter your secret message: ") 
assert type(secret_message)==str, print("invalid inputs, please enter text(str) only") #testing 

class Encrypting_and_Decrypting():
    #Class's attributes
    characters=string.punctuation+ string. ascii_letters+ string.digits #gets all the characters
    characters=list (characters) #converts them to a list
    characters.append(" ") #added space " " as a character to the list
    key=characters.copy() #copied the character's list and called it key
    random. shuffle (key) #key got shuffled 
    print(f"characters: {characters}") #printing the original list for clarification 
    print (f"key: {key}") #printing the copied & shuffled list (key) for clarification 

    #Class's behavior 
    #Method number 1: Encryption
    def encryption(self,text):
        self.plain_text=text #unencrypted text
        self.cipher="" #empty string to add on
        for letter in self.plain_text: #iterates over each letter in the unencrypted text
            if letter==" ": #including space as a character
                letter=" "
            index=self.characters.index(letter) #checks the letter's index in the original list which is characters
            shifted = (index+13) % len(self.characters) #whenever the list is done,repeat it
            self.cipher+=self.key[shifted] #add on to cypher text from the shuffeled list which is key
        print(f"encrypted message: {self.cipher}") #printing the encryption  for clarification
        return self.cipher  #the function outputs the encrypted version of the given text 
    
    #Method number 2: Decryption
    def decryption(self,cipher):
        self.cipher=cipher #encrypted text
        self.plain="" #empty string to add on
        for letter in self.cipher: #iterates over each letter in the unencrypted text
            if letter==" ": #including space as a character
                letter=" "
            index=self.key.index(letter) #checks the letter's index in the copied list which is key
            unshifted = (index-13) % len(self.characters) #whenever the list is done,repeat it
            self.plain+=self.characters[unshifted] #add on to plain from the original list which is characters
        print(f"original message: {self.plain}") #printing the decryption for clarification
        return self.plain #the function outputs the decrypted version of the given text 
    
#Taking an object/instance from the class
object1=Encrypting_and_Decrypting()
encryption1=object1.encryption(secret_message) #encrypts the user's input: secret message
print(encryption1)  #prints it for clarification

decryption1=object1.decryption(encryption1) #decryptes the encrypted version of the user's input: secret message
print(decryption1)  #prints it for clarification

#Converting text to binary
def text_to_binary(text):
    text = list(text)  #converts the text to a list
    binary = ""  #empty string to add on
    for i in text: #loops through each character in the given text
        # convert character to ASCII value using the built in function ord(), then to binary with 8 bits
        binary += format(ord(i), '08b')  # add the 8 bit binary number to the binary variable
    return binary 
#Calling/Invoking the function
binary_message1 = text_to_binary(encryption1) #saving the result(binary representation of the user's input but the encrypted version) of the function into a variable 
print("Binary representation:", binary_message1) #printing for clarification

from PIL import Image #Importing the image processing library need to manipulate the picture
def hide_message_in_image(image_path, binary_message, output_image_path):
    image = Image.open(image_path) #opens the image 
    #image.show()
    image = image.convert("RGB") #converts the image to RGB (Red,Green,Blue) to have bits based on the shades of the pictures
    message_bits = list(map(int, binary_message)) #this converts each character (either '0' or '1') in the binary message into an integer (0 or 1) and turns them into a list
    width, height = image.size#this gets the width and height of the image in pixels, so we know how many pixels are available for embedding the message
    bit_index = 0 #position of bits of the message
    for y in range(height):
        for x in range(width): #iterate over every pixel in the image (width by height).
            pixel = list(image.getpixel((x, y))) #retrieves the pixel at position (x, y) as a tuple of (R, G, B) values
            for i in range(3):  # RGB has 3 values
                if bit_index < len(message_bits): #checks if we still have bits left in the message to embed
                    pixel[i] = (pixel[i] & 0xFE)| message_bits[bit_index] #this operation ensures that the LSB is cleared (set to 0) without affecting the other bits.
                    bit_index += 1 #increments the index to move to the next bit in the message.
            image.putpixel((x, y), tuple(pixel)) # the pixel is updated using image.putpixel((x, y), tuple(pixel)) where tuple(pixel) converts the list back to a tuple to be compatible with the image format.
            if bit_index >= len(message_bits): #if all bits of the message have been embedded, the loop breaks early to avoid unnecessary pixel processing.(for the nested loop)
                break
        if bit_index >= len(message_bits): #if all bits of the message have been embedded, the loop breaks early to avoid unnecessary pixel processing.(for the original loop)
            break
    image.save(output_image_path) #saves the image in the desired path
    image.show() #shows the picture to the user

#Calling/Invoking the function
hide_message_in_image(r"C:\Users\HALA AHMED\Desktop\year 1\python\original pic.bmp", binary_message1, r"C:\Users\HALA AHMED\Desktop\year 1\python\test image.bmp")


def extract_message_from_image(image_path1):
    image = Image.open(image_path1)  # opens the image
    #image = image.convert("RGB")  # converts it to RGB
    width, height = image.size  # gets the image dimensions
    extracted_bits = []  # initializes an empty list to store extracted bits
    for y in range(height):
        for x in range(width):  # iterates over each pixel
            pixel = list(image.getpixel((x, y)))  # gets the pixel's RGB values
            for i in range(3):  # checks each of the RGB channels
                extracted_bits.append(pixel[i] & 0x01)  # extracts LSB and append it to extracted_bits
    binary_message2 = ""
    for bit in extracted_bits:
        binary_message2 += str(bit)# joins bits to form a binary string
    message = ""
    for i in range(0, len(binary_message2), 8):  # process the binary string and incerements by 8 (one byte)
        byte = binary_message2[i:i + 8] #men el awel leghayat +8
        if len(byte) == 8:  # ensure it's a full byte
            char = chr(int(byte, 2))  # convert the byte to a character by using the built in function chr and int to convert the binary number to decimal
            message += char  # append the character to the message
    return message

image_path1 = r"C:\Users\HALA AHMED\Desktop\year 1\python\test image.bmp"
extracted_message = extract_message_from_image(image_path1)
print("Extracted message:", extracted_message)