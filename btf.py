import os
import time
import logging
from PyPDF2 import PdfReader
from concurrent.futures import ThreadPoolExecutor, as_completed

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def try_decrypt(pdf_path, password):
    try:
        print(password)
        reader = PdfReader(pdf_path)
        if reader.is_encrypted:
            result = reader.decrypt(password)
            if result == 1:
                logging.info(f"Successfully decrypted with password: {password}")
                return ("SUCCESS", password)
            elif result == 2:
                logging.info(f"Password '{password}' returned a different result (2). Potential match.")
                return ("POTENTIAL", password)
        return None
    except Exception as e:
        logging.error(f"Error decrypting with password '{password}': {e}")
        return None

def decrypt_with_passwords(pdf_path, passwords):
    success_password = None
    potential_password = None
    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_password = {executor.submit(try_decrypt, pdf_path, password): password for password in passwords}
        for future in as_completed(future_to_password):
            password = future_to_password[future]
            try:
                result = future.result()
                if result:
                    if result[0] == "SUCCESS":
                        success_password = result[1]
                        executor.shutdown(wait=False, cancel_futures=True)
                        break
                    elif result[0] == "POTENTIAL":
                        potential_password = result[1]
                        executor.shutdown(wait=False, cancel_futures=True)
                        break
            except Exception as e:
                logging.error(f"Error during decryption attempt with password '{password}': {e}")
    
    return success_password or potential_password

def main():
    pdf_path = "Brain19.pdf"
    passwords_file = "test.txt"
    
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"The file {pdf_path} does not exist.")
    if not os.path.exists(passwords_file):
        raise FileNotFoundError(f"The passwords file {passwords_file} does not exist.")

    try:
        reader = PdfReader(pdf_path)
    except Exception as e:
        logging.error(f"Error opening PDF: {e}")
        return

    if not reader.is_encrypted:
        logging.info("The PDF is not encrypted. No password needed.")
    else:
        logging.info("The PDF is encrypted. Proceeding with decryption attempts.")
        with open(passwords_file, 'r') as file:
            passwords_to_try = [line.strip() for line in file]
        
        logging.info(f"Total passwords to try: {len(passwords_to_try)}")
        
        start_time = time.time()
        result = decrypt_with_passwords(pdf_path, passwords_to_try)
        end_time = time.time()

        if result:
            logging.info(f"The password for the PDF file is '{result}'")
        else:
            logging.info("Could not decrypt the PDF file")
        
        logging.info(f"Time taken: {end_time - start_time:.2f} seconds")

if __name__ == '__main__':
    main()