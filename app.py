from flask import Flask, request, render_template, send_file
from PIL import Image
import pickle
import cv2
import pytesseract
import re
import os
import subprocess

#pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
#pytesseract.pytesseract.tesseract_cmd = r"/usr/bin/tesseract"


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        image=request.files['image']
        image_name=image.filename
        if '.jpg' in image_name:
            image.save(image_name)
            extract_text_from_image(image_name)
            input_file = 'recognized.txt'
            output_file = 'output.txt'
            start_word = 'NGREDIENT'

            extract_ingredients_paragraphs(input_file, start_word, output_file)

            input_file = 'output.txt'
            pred = clean_file(input_file, output_file)
            
            

            return render_template('result.html', presence=pred[0], allergens=pred[1])
        elif '.jpeg' in image_name: 
            image.save(image_name)
            extract_text_from_image(image_name)
            

            return {"response":"file saved successfully in your current durectory"}
        else:
            return {"error":"select you image file"}
    except Exception as e:
        return {"error":str(e)}

        
def extract_text_from_image(image_name):

    img = cv2.imread(image_name)
    print(img)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)

    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 18))
    dilation = cv2.dilate(thresh1, rect_kernel, iterations=1)

    contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    im2 = img.copy()

   
    with open("recognized.txt", "w") as file:
        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)
            rect = cv2.rectangle(im2, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cropped = im2[y:y + h, x:x + w]
            
            text = pytesseract.image_to_string(cropped)
            file.write(text + "\n")




def extract_ingredients_paragraphs(input_file, start_word, output_file):
    # Flag to indicate whether to start extracting paragraphs
    extract_flag = False
    # Counter to track consecutive empty lines
    empty_line_count = 0
    # Store the extracted paragraphs
    matched_paragraphs = []

    with open(input_file, 'r') as file:
        for line in file:
            # Normalize line endings and remove unwanted characters
            line = re.sub(r'[^A-Za-z\s,]', '', line.strip())

            # Check if the line contains the start_word
            if start_word.upper() in line.upper():
                extract_flag = True
                matched_paragraphs.append(line)
            
            # If extraction flag is True, add the line to the matched_paragraphs list
            elif extract_flag:
                matched_paragraphs.append(line)
                # Reset the empty line counter if a non-empty line is encountered
                if line.strip():
                    empty_line_count = 0
                else:
                    # Increment the empty line counter
                    empty_line_count += 1
                    # If 5 consecutive empty lines are encountered, it marks the end of the paragraph
                    if empty_line_count >= 2:
                        break

    # Write the matched paragraphs to the output file
    with open(output_file, 'w') as file:
        for paragraph in matched_paragraphs:
            file.write(paragraph + '\n')


def clean_paragraph(paragraph):
    # Split the paragraph into words
    words = paragraph.split()
    cleaned_words = []
    # Iterate through the words
    for word in words:
        # Check if the word is "INGREDIENTS"
        if word == 'NGREDIENTS':
            continue  # Skip this word
        # Check if the word starts with a comma followed by a space
        elif ', ' in word:
            # Split the word by comma and space and add each part on a new line
            cleaned_words.extend(word.split(', '))
        else:
            # Add the word as is
            cleaned_words.append(word)
    # Join the cleaned words
    cleaned_paragraph = ' '.join(cleaned_words)
    return cleaned_paragraph

def clean_file(input_file, output_file):
    # Read input from the input file
    with open(input_file, 'r') as file:
        input_paragraph = file.read()

    # Clean the paragraph
    cleaned_text = clean_paragraph(input_paragraph)

    # Write the cleaned text to the output file
    with open(output_file, 'w') as file:
        file.write(cleaned_text)
    

    file_path = 'output.txt'


    with open(file_path, 'r') as file:
        file_contents = file.read()


    with open('bin_class.pkl', 'rb') as f:
        bin_class = pickle.load(f)

        bin_labels = {1:"Does not Contain Allergens",0:"Contains Allergens"}
        string = file_contents
        string = string.replace(',','')
        string = [string]
        y_pred = bin_class.predict(string)
        print(y_pred)
        bin_res = bin_labels[y_pred[0]]
        print(bin_res)
        if y_pred == 0:
            with open('mul_lab.pkl', 'rb') as f:
                clf3= pickle.load(f)
                mul_labels = {0:'Alcohol',1:'Almonds',2:'Anchovies',3:'Celery',4:'Chicken',5:'Cocoa',6:'Coconut',7:'Diary',8:'Eggs',9:'Fish',10:'Ghee',11:'Milk',12:'Mustard',13:'None',14:'Nuts',15:'Oats',16:'Peanuts',17:'Pine nuts',18:'Pork',19:'Rice',20:'Shellfish',21:'Soybeans',22:'Strawberries',23:'Wheat'}
                y_mul_pred = clf3.predict(string)
                y_mul_pred = y_mul_pred.toarray()
                print(y_mul_pred)
                ans = []
                for i in range(24):
                    if y_mul_pred[0][i] == 1:
                        ans.append(mul_labels[i])
                print(ans)
    return [bin_res,ans]
     
        
if __name__ == "__main__":
    st = subprocess.getoutput('which tesseract')
    pytesseract.pytesseract.tesseract_cmd = st

    #os.system('apt install tesseract-ocr')
    app.run(debug=True)
