PDF Password Cracker
- Overview
The PDF Password Cracker is a tool designed to decrypt password-protected PDF files by attempting to guess the password. It supports both dictionary attacks and brute-force attacks with various configurations.

- Features
Dictionary Attack: Use a predefined list of words to attempt to crack the password.
Brute-Force Attack: Generate and try passwords within a specified range of characters.
Customizable Character Sets: Define which characters to include in brute-force attempts.
Multithreading: Utilize multiple threads to speed up the cracking process.
Logging: Keep track of attempted passwords and results.

- Requirements
Python 3.x
PyPDF2 library
argparse library (for command-line argument parsing)
concurrent.futures library (for multithreading)
