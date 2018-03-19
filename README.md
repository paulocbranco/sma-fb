# Script for search posts in facebook

Python script developed under the Social Media Analytics course project where we have to colect data from facebook for further text and sentiment analysis.

### Required libraries

```shell
pip install facebook-sdk
pib install pandas 
```

### How to use

Put your own twitter consumer and access token keys in the following code
```python
APP_ID = 'xxxxxxxxxxxxxxxxxxxx'
APP_SECRET = 'xxxxxxxxxxxxxxxxxxxxxxxx'
```
Replace the searching words
```python
def main():
    # query by page id
    # search the pages ids here: https://lookup-id.com/
    search(query='1726708387545466')
```
Execute the script

```bash
python3 sma-fb.py
```