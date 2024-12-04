# PYTHON-CW
Modern Use of  Steganography Using Python

Goal:
This application allows users to hide a secret message within an image using the Least Significant Bit (LSB) method. The message is first encrypted using the Caesar Cipher, then converted to binary and embedded in the image. The binary message can later be extracted and decrypted.

Algorithm/Steps:
User Input: The user provides a secret message.
Encryption: The message is encrypted using the Caesar Cipher method.
Binary Conversion: The encrypted message is converted into its binary representation.
Hide in Image: The binary message is embedded into the image using the Least Significant Bit (LSB) method.
Extract from Image: The binary message is extracted from the image using the LSB method.
Binary to Text: The extracted binary message is converted back to text.
Decryption: The decrypted message is displayed.
Testing: The functions are tested to ensure correct functionality.

Install Required Libraries:
random
string
PIL (Pillow for image processing) - install via pip install Pillow
unittest for testing (included in Python standard library)

Run the Program:
When the program starts, the user will be asked to input a secret message.
The program will then encrypt the message using the Caesar Cipher method.
Next, the encrypted message will be converted to binary and hidden inside an image.
You will need to specify the input image and output image paths.
The program will then extract the binary message from the image and decrypt it to reveal the original message.

Example Use Case:
Enter your secret message: "Hello, World!"
Encrypted Message: (Encrypted version of the message)
Binary Representation: (Binary version of the encrypted message)
Enter input image path please: input_image.bmp
Enter output image path please: output_image.bmp
Message hidden in image: output_image.bmp
Extracted Binary Message: (Extracted binary message)
Extracted Encrypted Message: (Extracted encrypted message)
Decrypted Message: "Hello, World!"

Functions and Classes:
1. Encrypting_and_Decrypting Class:
encryption(text): Encrypts the input text using the Caesar Cipher method.
decryption(cipher): Decrypts the encrypted message back to the original text.
2. Conversion Class:
text_to_binary(text): Converts the given text into its binary representation using Ascii.
binary_to_text(binary): Converts a binary string back to text using Ascii.
3. Image Manipulation Functions:
hide_message_in_image(image_path, binary_message, output_image_path): Embeds the binary message into the image using the LSB method and saves the output.
extract_message_from_image(image_path): Extracts the binary message from the image using the LSB method.
4. Unit Testing:
The code includes unit tests to ensure the correct functionality of encryption, decryption, text-to-binary conversion, binary-to-text conversion, and hiding/extracting messages in/from images.

Unit Tests:
The application includes tests for:
Encryption and Decryption: Ensures the message is correctly encrypted and decrypted.
Text to Binary Conversion: Verifies that the message is correctly converted to binary.
Binary to Text Conversion: Verifies that the binary string is correctly converted back to text.
Hide and Extract Message: Ensures the secret message can be successfully hidden in and extracted from an image.