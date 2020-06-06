# Question Answering System

This project centres on adding QA System to Gotcha, an open source search engine.Whenever user asks a question system collects related content from wikipedia and searches the best answer from that content.

## Requirements
 * python >=3.5
 * pytorch(includes torch and torchvision)
 * numpy
 * scikit-learn
 * msgpack
 * spacy language model
 * SpeechRecognition
 * gtts
 * wikipedia
 * regex
 * smtplib
 * playsound
 * unicodedata
 * nltk
 * tqdm
  
  You can install requirements by executing : pip install -r requirements.txt

  ## Preprocessing and Training
[comment]: Skip This if you have already trained model.
### Download
  You have to download SQuAD dataset dev-v1.1.json and train-v1.1.json and word to vector file glove.840B.300d.txt (https://www.kaggle.com/takuok/glove840b300dtxt)
  ### Preprocessing
   ```bash
python prepro.py
```
### Training
```bash
python train.py -e 50 -bs 32
```
## Execution
Go to Project directory where manage.py resides
execute following commnad to run project
  ```bash
python manage.py runserver
```
Open https://localhost:8000 and enjoy it.
