'''
GOAL: This application aims to hide a secret message ,given by the user, in a picture. 
STEPS:
1. The message is taken from the user.
2. The message gets encrypted using The Caesar Cipher Method.
3. The encrypted message is converted to binary.
4. The binary message will be inputted in the image using the LSB approach.
5. The binary message will be extracted from the image using the LSB approach.
6. The binary message gets converted to text.
7. The text gets decrypted.
'''
#Importing the needed libraries for Caesar Cipher Encryption and Decryption implementation
import random #a module for generating random numbers and performing random operations including shuffling
import string #a module that contains all the chararcters, useful for working with functions/ with strings needed
#Importing the image processing library need to manipulate the picture
from PIL import Image
 
# Caesar Cipher Encryption and Decryption Class
class Encrypting_and_Decrypting:
    #Class's shared attributes
    characters = string.punctuation + string.ascii_letters + string.digits #gets all the characters
    characters = list(characters) #converts them to a list
    characters.append(" ")  # add space as a character to the list
    key = characters.copy() #copied the character's list and called it key
    random.shuffle(key)  # shuffle the key
 
    # Encryption Method
    def encryption(self, text):
        cipher = "" #empty string to add on
        for letter in text: #iterates over each letter in the unencrypted text
            if letter in self.characters: #check if the letter is in the characters list, the following operation will happen
                index = self.characters.index(letter) #gets the letter's index in the original list which is characters
                shifted = (index + 13) % len(self.characters)  # shifts the index by 13, whenever the list is done,repeat it 
                cipher += self.key[shifted] #add on to cypher text from the shuffeled list which is key using the updated index
            else: #if the letter is NOT in the characters list, the following operation will happen
                cipher += letter  # leave unsupported characters unchanged
        return cipher #the function outputs the encrypted version of the given text
 
    # Decryption Method
    def decryption(self, cipher):
        plain = "" #empty string to add on
        for letter in cipher: #iterates over each letter in the unencrypted text
            if letter in self.key: #check if the letter is in the key list, the following operation will happen
                index = self.key.index(letter) #gets the letter's index in the copied,shuffeled list: key
                unshifted = (index - 13) % len(self.characters) #de-shifts the index by 13, whenever the list is done,repeat it 
                plain += self.characters[unshifted] #add on to plain text from the original list which is characters using the updated index
            else:
                plain += letter  # leave unsupported characters unchanged
        return plain #the function outputs the decrypted version of the given text
 
# Convert text to binary
def text_to_binary(text): 
    # convert each character in the text to its 8-bit binary representation using its ascii and join them into one string
    binary = "".join(format(ord(i), '08b') for i in text)
    return binary
 
# Convert binary to text (ASCII characters)
def binary_to_text(binary): 
    message = "" #empty string to add on
    for i in range(0, len(binary), 8): #increments by 8 each time
        byte = binary[i:i + 8] # Extract 8 bits (1 byte) each time
        if len(byte) == 8: #ensures that the bits are equal to 8
            message += chr(int(byte, 2)) #converts the byte binary values to int values then changes them as characters
    return message # outputs the final decoded message
 
# Hide Message in Image
def hide_message_in_image(image_path, binary_message, output_image_path):
    image = Image.open(image_path) #opens the image 
    image = image.convert("RGB") #converts the image to RGB (Red,Green,Blue) to have bits based on the shades of the pictures
 
    # Include the length of the binary message as a 32-bit integer
    message_length = len(binary_message)
    length_binary = format(message_length, '032b')  # 32-bit length
    binary_message = length_binary + binary_message  # Prepend length
 
    message_bits = list(map(int, binary_message)) #converts each character (either '0' or '1') in the binary message into an integer and turns them into a list
    width, height = image.size # gets the width and height of the image in pixels, so we know how many pixels are available for embedding the message
    bit_index = 0  #intilaizing the number of bits of the message
    for y in range(height): #iterate over every pixel in the image (width by height).
        for x in range(width): #iterate over every pixel in the image (width by height).
            pixel = list(image.getpixel((x, y))) #retrieves the pixel at position (x, y) as a tuple of (R, G, B) values
            for i in range(3):  #  3 RGB channels
                if bit_index < len(message_bits): #checks if we still have bits left in the message to embed
                    pixel[i] = (pixel[i] & 0xFE) | message_bits[bit_index] #this operation ensures that the LSB is cleared (set to 0) without affecting the other bits.
                    bit_index += 1 #increments the index to move to the next bit in the message.
            image.putpixel((x, y), tuple(pixel)) # the pixel is updated using image.putpixel((x, y), tuple(pixel)) where tuple(pixel) converts the list back to a tuple to be compatible with the image format.
            if bit_index >= len(message_bits): #if all bits of the message have been embedded, the loop breaks early to avoid unnecessary pixel processing.(for the nested loop)
                break
        if bit_index >= len(message_bits): #if all bits of the message have been embedded, the loop breaks early to avoid unnecessary pixel processing.(for the original loop)
            break
 
    image.save(output_image_path) #saves the image in the desired path
    image.show() #shows the picture to the user
    print(f"Message hidden in image: {output_image_path}")
 
# Extract Message from Image
def extract_message_from_image(image_path): 
    image = Image.open(image_path) # opens the image
    width, height = image.size # gets the image dimensions
    extracted_bits = [] # initializes an empty list to store extracted bits
    for y in range(height):
        for x in range(width):
            pixel = list(image.getpixel((x, y)))
            for i in range(3):
                extracted_bits.append(pixel[i] & 0x01) # extracts LSB and append it to extracted_bits
 
    # Extract the first 32 bits for the message length
    length_bits = extracted_bits[:32]
    message_length = int("".join(map(str, length_bits)), 2)
 
    # Extract the actual message bits
    message_bits = extracted_bits[32:32 + message_length]
    binary_message = "".join(map(str, message_bits)) #converts each element of message_bits to a string and concatenate them into a single binary string
    return binary_message
 
# User Code
if __name__ == "__main__":
    # Step 1: User Input
    secret_message = input("Enter your secret message: ")
 
    # Step 2: Encrypt the Message
    cipher_tool = Encrypting_and_Decrypting() #instance from the class
    encrypted_message = cipher_tool.encryption(secret_message)
    print(f"Encrypted Message: {encrypted_message}")
 
    # Step 3: Convert Encrypted Message to Binary
    binary_message = text_to_binary(encrypted_message)
    print(f"Binary Representation: {binary_message}")
 
    # Step 4: Hide Binary Message in Image
    input_image_path = r"C:\Users\HALA AHMED\Desktop\year 1\python\original pic.bmp" # original image path
    output_image_path = r"C:\Users\HALA AHMED\Desktop\year 1\python\test image.bmp"  # output image path
    hide_message_in_image(input_image_path, binary_message, output_image_path)
 
    # Step 5: Extract Binary Message from Image
    extracted_binary_message = extract_message_from_image(output_image_path)
    print(f"Extracted Binary Message: {extracted_binary_message}")
 
    # Step 6: Convert Binary to Text
    extracted_encrypted_message = binary_to_text(extracted_binary_message)
    print(f"Extracted Encrypted Message: {extracted_encrypted_message}")
 
    # Step 7: Decrypt the Extracted Message
    decrypted_message = cipher_tool.decryption(extracted_encrypted_message)
    print(f"Decrypted Message: {decrypted_message}")

