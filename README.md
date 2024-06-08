#Food Allergen Prediction and Detection using Machine Learning

This repository contains a Flask web application that takes an image of an ingredient label from packaged food products and predicts whether the product contains allergens. If allergens are detected, it also identifies the specific allergens present.

##Table of Contents
Installation
Usage
Model Training
Project Structure
Dependencies
[Contributing](docs/CONTRIBUTING.md)

##Installation

###1.Clone the Repository
`git clone https://github.com/your-username/food-allergen-detection.git
cd food-allergen-detection`

###2.Install Required Packages
`pip install -r requirements.txt`

###3.Download and Install Tesseract OCR

Tesseract OCR Download Link
Ensure that tesseract.exe is properly installed and set in your environment variables.

###4.Place Model Files

Ensure the bin_class.pkl and mul_lab.pkl model files are in the root directory of the project.

##Usage

###1.Run the Flask Application
`python app.py`

###2.Open the Web Application
Open your browser and go to http://127.0.0.1:5000/

###3.Upload an Image

Upload an image of a food product ingredient label in JPG or JPEG format. The application will process the image and display the results indicating the presence of allergens and identifying them if present.

##Model Training
###Binary Classification Model
The binary classification model predicts whether a product contains allergens.

###Multi-label Classification Model
The multi-label classification model identifies the specific allergens present in the product if the binary classification model predicts the presence of allergens.

###Training Steps
**1.Preprocess the Data**
 -Clean and prepare the dataset.
 -Split the data into training and test sets.
  
**2.Train the Binary Classification Model**
`clf.fit(X_train, z_train)`

**3.Train the Multi-label Classification Model**
`clf.fit(X_train, z_train)`

**4.Evaluate Models**

Evaluate both models using appropriate metrics such as accuracy, precision, recall, F1 score, and Hamming loss.

##Dependencies
Flask
OpenCV
Tesseract OCR
scikit-learn
scikit-multilearn
Pandas
NumPy
Pillow
TensorFlow
Gensim

**Install dependencies using:**
`pip install -r requirements.txt`

##Contributing
Contributions are welcome! Please fork this repository and submit a pull request for any improvements, bug fixes, or additional features.
