# Project: Identify Fraud from Enron Email
## Introduction

In 2000, Enron was one of the largest companies in the United States. By 2002, it had collapsed into bankruptcy due to widespread corporate fraud. In the resulting Federal investigation, a significant amount of typically confidential information entered into the public record, including tens of thousands of emails and detailed financial data for top executives. In this project, we would like to build a person of interest identifier based on financial and email data. The machine learning algorithms that we are about to use include `Logistic Regression`, `Decision Tree` and `K Nearest Neighbors`.

### Install

This project requires **Python 2.7** and the following Python libraries installed:

- [NumPy](http://www.numpy.org/)
- [Pandas](http://pandas.pydata.org)
- [matplotlib](http://matplotlib.org/)
- [scikit-learn](http://scikit-learn.org/stable/)

You will also need to have software installed to run and execute a [Jupyter Notebook](http://ipython.org/notebook.html)

If you do not have Python installed yet, it is highly recommended that you install the [Anaconda](http://continuum.io/downloads) distribution of Python, which already has the above packages and more included. Make sure that you select the Python 2.7 installer and not the Python 3.x installer. 

### Code

Template code is provided in the `final_project.ipynb` notebook file and the rest `.py` files.

### Run

In a terminal or command window, navigate to the top-level project directory `final_project/` (that contains this README) and run one of the following commands:

```bash
ipython notebook final_project.ipynb
```  
or
```bash
jupyter notebook final_project.ipynb
```

This will open the Jupyter Notebook software and project file in your browser.

## Dataset
By default, the missing values here would be converted to 0, which may be a little confusing because we cannot tell which are missing values and which really stand for value 0. Hence, we would like to keep `nan` at the beginning and calculate the proportion of actual of missing values. The table below shows the proportions of missing values of different variables.

|         variable        | missing pct |          variable         | missing pct |         variable        | missing pct |
|:-----------------------:|:-----------:|:-------------------------:|:-----------:|:-----------------------:|:-----------:|
|          salary         |    34.93    |  shared_receipt_with_poi  |    41.10    | from_this_person_to_poi |    41.10    |
|        to_message       |    41.10    | restricted_stock_deferred |    87.67    |      director_fees      |    88.36    |
|    deferral_payments    |    73.29    |     total_stock_value     |    13.70    |     deferred_income     |    66.44    |
|      total_payments     |    14.38    |          expenses         |    34.93    |   long_term_incentive   |    54.79    |
| exercised_stock_options |    30.14    |       loan_advances       |    97.26    | from_poi_to_this_person |    41.10    |
|           bouns         |    43.84    |       from_messages       |    41.10    |                         |             |
|     restricted_stock    |    24.66    |           other           |    36.30    |                         |             |

The table below shows the proportion of actual 0 values of different variables.

|         variable        | zero pct |          variable         | zero pct |         variable        | zero pct |
|:-----------------------:|:--------:|:-------------------------:|:--------:|:-----------------------:|:--------:|
|          salary         |     0    |  shared_receipt_with_poi  |     0    | from_this_person_to_poi |   13.70  |
|        to_message       |     0    | restricted_stock_deferred |     0    |      director_fees      |     0    |
|     deferral_payment    |     0    |     total_stock_value     |     0    |     deferred_income     |     0    |
|      total_payments     |     0    |          expenses         |     0    |   long_term_incentive   |     0    |
| exercised_stock_options |     0    |       loan_advances       |     0    | from_poi_to_this_person |   8.22   |
|          bouns          |     0    |       from_messages       |     0    |                         |          |
|     restricted_stock    |     0    |           other           |     0    |                         |          |


