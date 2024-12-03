'''
GOAL: This application aims to hide a secret message ,given by the user, in a picture. 
ALGORITHM/STEPS:
1. The message is taken from the user.
2. The message gets encrypted using The Caesar Cipher Method.
3. The encrypted message is converted to binary.
4. The binary message will be inputted in the image using the LSB approach.
5. The binary message will be extracted from the image using the LSB approach.
6. The binary message gets converted to text.
7. The text gets decrypted.
8. The functions get tested.
'''
#Importing the needed libraries for Caesar Cipher Encryption and Decryption implementation
import random #a module for generating random numbers and performing random operations including shuffling
import string #a module that contains all the chararcters, useful for working with functions/ with strings needed
#Importing the image processing library needed to manipulate the picture
from PIL import Image #PIL= pillow (should be installed in a new terminal with the "pip install Pillow")
import unittest # a module to verify that individual functions in the program work as expected

# Caesar Cipher Encryption and Decryption Class:
class Encrypting_and_Decrypting:
    #Class's shared attributes
    characters = string.punctuation + string.ascii_letters + string.digits #gets all the characters
    characters = list(characters) #converts them to a list
    characters.append(" ")  # add space as a character to the list
    key = characters.copy() #takes a copy of the character's list and calls it key
    random.shuffle(key)  # shuffles the key
 
    # Encryption Method
    def encryption(self, text): #"self": serving as a pointer , "text"= hidden message
        cipher = "" #empty string to add on the encrypted characters
        for letter in text: #iterates over each letter in the unencrypted text
            if letter in self.characters: #check if the letter is in the characters list, the following operation will happen
                index = self.characters.index(letter) #gets the letter's index in the original list which is characters
                shifted = (index + 13) % len(self.characters)  # shifts the index by 13 & whenever the list is done,repeats it 
                cipher += self.key[shifted] #add on to the cipher variable from key using the shifted index
            else: #if the letter is NOT in the characters list, the following operation will happen
                cipher += letter  # leave unsupported characters unchanged
        return cipher #the function outputs the encrypted version of the given text
 
    # Decryption Method
    def decryption(self, cipher):
        plain = "" #empty string to add on the decrypted characters
        for letter in cipher: #iterates over each letter in the encrypted text
            if letter in self.key: #check if the letter is in the key list, the following operation will happen
                index = self.key.index(letter) #gets the letter's index in key
                unshifted = (index - 13) % len(self.characters) #de-shifts the index by 13 & whenever the list is done,repeat it 
                plain += self.characters[unshifted] #add on to plain text from characters using the shifted index
            else:
                plain += letter  # leave unsupported characters unchanged
        return plain #the function outputs the decrypted version of the given text

#Text and Binary conversions class:
class Conversion:
    # Convert text to binary method
    def text_to_binary(self,text): 
        # convert each character in the text to its 8-bit binary representation using its ascii and joins them into one string
        binary = "".join(format(ord(i), '08b')for i in text)
        return binary
    
    # Convert binary to text method
    def binary_to_text(self,binary): 
        message = "" #empty string to add on
        for i in range(0, len(binary), 8): #increments by 8 each time
            byte = binary[i:i + 8] # Extracts 8 bits (1 byte) each iteration
            if len(byte) == 8: #ensures that the bits are equal to 8
                message += chr(int(byte, 2)) #converts the byte binary values to int values then changes them as characters
        return message # outputs the final decoded message
 
# Hide Message in Image Function
def hide_message_in_image(image_path, binary_message, output_image_path):
    image = Image.open(image_path) #opens the image 
    image = image.convert("RGB") #converts the image to RGB (Red,Green,Blue) to have bits based on the shades of the pictures
 
    # Include the length of the binary message as a 32-bit integer 
    message_length = len(binary_message) #calculates the length of the binary message 
    length_binary = format(message_length, '032b')  # puts the length of the message in 32-bit length format
    binary_message= length_binary + binary_message  # Prepend length(adding it to the beginning of a string)
 
    message_bits = list(map(int, binary_message)) #converts each character (either '0' or '1') in the binary message into an integer and turns them into a list
    width, height = image.size # gets the width and height of the image in pixels
    bit_index = 0  #intilaizing the number of bits of the message
    for y in range(height): #iterate over every pixel in the image (width by height).
        for x in range(width): 
            pixel = list(image.getpixel((x, y))) #get the pixel at position (x, y) as a list of  tuples of (R, G, B) values
            for i in range(3):  #  3 RGB channels
                if bit_index < len(message_bits): #checks if we still have bits left in the message to embed
                    pixel[i] = (pixel[i] & 0xFE) | message_bits[bit_index] # the LSB is cleared (set to 0 without affecting the other bits) and changed with the message's bit.
                    bit_index += 1 #increments the index  (message's next bit)
            image.putpixel((x, y), tuple(pixel)) # the pixel is updated and converted to a tuple to be compatible with the image format.
            if bit_index >= len(message_bits): #if all bits of the message have been embedded, the loop breaks early to avoid unnecessary pixel processing.(for the nested loop)
                break
        if bit_index >= len(message_bits): # same previous condition(for the original loop)
            break
    image.save(output_image_path) #saves the image in the desired path
    image.show() #shows the picture to the user
    print(f"Message hidden in image: {output_image_path}")
 
# Extract Message from Image Function
def extract_message_from_image(image_path): 
    image = Image.open(image_path) # opens the image
    width, height = image.size # gets the image dimensions
    extracted_bits = [] # initializes an empty list to store extracted bits
    for y in range(height):#iterate over every pixel in the image (width by height)
        for x in range(width):#iterate over every pixel in the image (width by height)
            pixel = list(image.getpixel((x, y)))#get the pixel at position (x, y) as a list of  tuples of (R, G, B) values
            for i in range(3): #  3 RGB channels
                extracted_bits.append(pixel[i] & 0x01) # extracts LSB and append it to extracted_bits
 
    # Extract the first 32 bits for the message length
    length_bits = extracted_bits[:32] # slicing the list to get the first 32 elements
    message_length = int("".join(map(str, length_bits)), 2) #converts the length_bits into a binary string, then to an integer.
 
    # Extract the actual message bits
    message_bits = extracted_bits[32:32 + message_length] #extracts the message from the list of bits
    binary_message = "".join(map(str, message_bits)) #converts each element of message_bits to a string and concatenate them into a single binary string
    return binary_message #returns the final binary message

# User Code
if __name__ == "__main__": #main function: all functions start/get provoked after it (could be removed but better for clarity and organization)
    # Step 1: User Input
    secret_message = input("Enter your secret message: ") #the input is taken as a string

    # Step 2: Encrypt the Message
    cipher_tool = Encrypting_and_Decrypting() #instance from the class
    encrypted_message = cipher_tool.encryption(secret_message) #encrypting the message using the function in the class's instance
    print(f"Encrypted Message: {encrypted_message}")
 
    # Step 3: Convert Encrypted Message to Binary
    text_x_binary_instance1=Conversion() #instance from the class
    binary_message = text_x_binary_instance1.text_to_binary(encrypted_message) #converting the message using the function in the class's instance
    print(f"Binary Representation: {binary_message}")
 
    # Step 4: Hide Binary Message in Image
    input_image_path = input("Enter input image path please: ") # user's original image path
    output_image_path = input("Enter output image path please: ") # user's output image path
    hide_message_in_image(input_image_path, binary_message, output_image_path) #calling/ provoking the function
 
    # Step 5: Extract Binary Message from Image
    extracted_binary_message = extract_message_from_image(output_image_path) #calling/ provoking the function while saving its return value in a variable
    print(f"Extracted Binary Message: {extracted_binary_message}")
 
    # Step 6: Convert Binary to Text
    extracted_encrypted_message = text_x_binary_instance1.binary_to_text(extracted_binary_message) #converting the message using the function in the class's instance
    print(f"Extracted Encrypted Message: {extracted_encrypted_message}")
 
    # Step 7: Decrypt the Extracted Message
    decrypted_message = cipher_tool.decryption(extracted_encrypted_message) #decrypting the message using the function in the class's instance
    print(f"Decrypted Message: {decrypted_message}")

class TestMessageFunctions(unittest.TestCase): #class that inherits from unittest.TestCase module

    def test_encryption_decryption(self): #the word "test" is added before the function as a pointer to the unittest module
        # Test encryption and decryption results
        cipher_tool1 = Encrypting_and_Decrypting() #instance
        original_message1 = "Hello, World!"
        encrypted_message1 = cipher_tool1.encryption(original_message1)
        decrypted_message1 = cipher_tool1.decryption(encrypted_message1)
        self.assertEqual(original_message1, decrypted_message1) #checks that both the input and output is the same/equal
        
    def test_text_to_binary(self):
        # Test if text is correctly converted to binary
        text1 = "AB"
        expected_binary1 = '0100000101000010'  # 'A'= 01000001,'B'= 01000010
        binary_message1 = text_x_binary_instance1.text_to_binary(text1)#conversion process
        self.assertEqual(binary_message1, expected_binary1) #checks that both the expected output and the actual output is the same

    def test_binary_to_text(self):
        # Test if binary is correctly converted back to text
        binary_message2 = '0100000101000010'
        expected_text2 = 'AB'
        text2 =text_x_binary_instance1.binary_to_text(binary_message2)#conversion process
        self.assertEqual(text2, expected_text2) #checks that both the expected output and the actual output is the same

    def test_hide_and_extract_message(self):
        # Create a new  image in memory for testing
        original_image = Image.new('RGB', (10, 10), color='white')
        image_path = "hala_image.bmp"
        original_image.save(image_path)
        
        #Converts the message to its binary representation
        secret_message = "Hidden Message"
        binary_message = text_x_binary_instance1.text_to_binary(secret_message) #text to binary conversion process
        
        # Hide message in image
        output_image_path = "output_image.bmp" 
        hide_message_in_image(image_path, binary_message, output_image_path) 
        
        # Extract message from image
        extracted_binary_message = extract_message_from_image(output_image_path) #extracts binary message from the image
        extracted_message = text_x_binary_instance1.binary_to_text(extracted_binary_message)#binary to text conversion process
        
        # Assert the extracted message is the same as the original
        self.assertEqual(secret_message, extracted_message) 
if __name__ == '__main__': 
    unittest.main() #runs all test cases defined in the code, outputing their results 

