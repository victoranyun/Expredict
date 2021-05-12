## Expredict
A Tensorflow/Keras powered prediction tool along with the latest web scraper tool for Instagram. Identifies the best performing image out of a set of images given to the model.

## Goals
- Finish writing the API, add private profiles (signin using Instagram)
- Optimize CNN
- Fix the outdated scraper

# Expredict

1. [ Introduction ](#intro)
2. [ Tech ](#tech)
3. [ Usage ](#usage)
4. [ Future Improvements ](#tests)
5. [ License ](#license)

<a name="intro"></a>
## 1. Description

I created a machine learning model and web backend to identify social media trends (specifically on Instagram). <br> <br>
I have found a lot of success with this model and application, successfully growing my account to 161K+ followers.
Upload a set of images (more than 1), and the Python backend will display what image is predicted to work the best if you post it on social media. <br>

<a name="tech"></a>
## 2. Technologies Used

I used Python, Tensorflow, Keras (ML), Flask, HTML/CSS (Web).

<a name="usage"></a>
## 3. Usage

```bash
git clone https://github.com/victoranyun/Expredict
cd Expredict
python3 module.py
```

Navigate to http://localhost:5000 using your favorite browser!

<a name="improvements"></a>
## 4. Future improvements
1. Improve the accuracy of the ML model by trying different types of regressions and modeling.

2. Currently, the model requires human intelligence to identify certain niches on a certain account before scraping. We can create another model that categorizes these niches and skips the human intelligence step.

<a name="license"></a>
## 5. License 
MIT License
