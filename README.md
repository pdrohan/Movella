# Kaggle Hockey Goalie Dataset

This is a Python Library for some data analysis I did on a Kaggle Hockey Goalie Dataset. Note the HTML files are outputs from functions within the main.py file.
The files were generated on lines 249:252, but is commented out for simplicty. If you would like to generate the HTML files for the two dataframes, feel free. Otherwise only the
first five rows will be printed in the output. 

## Installation
1. Clone the Repository 
2. Run the pip command


```bash
pip install -e .
```

## Usage
3. Run the test command
```bash
pytest

```
4. Run the file however you like

## Output
The output should be printed as follows: 

Kaggle Data Goalie Analytics:
-> The average win Percentage for all Goalies is 59.51% 
 
-> The average loss Percentage for all Goalies is 56.95%

-> The average games played is: 143.46. The average minutes played per goal against is: 19.67 minutes. Goals against over shots against, as a percentage: 16.48%

|    | playerID   |   W |   GP |   Win % |
|---:|:-----------|----:|-----:|--------:|
|  0 | abrahch01  |  41 |  102 |   40.2  |
|  1 | adamsjo02  |   9 |   22 |   40.91 |
|  2 | aebisda01  | 106 |  214 |   49.53 |
|  3 | aitkean01  |  47 |  106 |   44.34 |
|  4 | andercr01  | 131 |  294 |   44.56 |

|    | tmID   |   W |   GP |   Win Rate % |
|---:|:-------|----:|-----:|-------------:|
|  0 | ALB    |  38 |   84 |        45.24 |
|  1 | ANA    | 381 | 1039 |        36.67 |
|  2 | AND    | 257 |  541 |        47.5  |
|  3 | ATF    | 268 |  667 |        40.18 |
|  4 | ATL    | 342 | 1001 |        34.17 |

The Most Goals Stopped by any Goalie:
-> {'playerID': 'brodema01', 'goals_stopped': 29915.0}

The Most Efficient Goalie:
-> {'playerID': 'mioed01', 'efficiency': 28.23}

## Kaggle csv Link
Link for kaggle: https://www.kaggle.com/open-source-sports/professional-hockey-database?select=Goalies.csv

## License
[MIT](https://choosealicense.com/licenses/mit/)
