# COVID-19 Twitter Discourse Analysis


## Code

`collect_tweets.py` must be successfully invoked with the following command:

`python collect_tweets.py -b "BEARER TOKEN HERE"`

Everytime you run it, it produces a CSV file of raw data. Then, run `generate_file_from_raw.py` to get csv files for annotation. 

After annotating, run `generate_words.py` and `word_counts.py`, which will produce JSON files based on annotated data. 

Then, run `compute_frequency.py`, which will produce more JSON files. 

Finally, run `plot.py` to get plots from analysis, which are all shown in the `/images/` folder. 