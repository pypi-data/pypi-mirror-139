# topsis_dilmanpreet_101903506

# TOPSIS

Submitted By: **Dilmanpreet Singh**.<br>
Roll Number: **101903506**.<br>
Type: **Package**.<br>
Title: **TOPSIS for multiple-criteria decision making (MCDM)**.<br>
Version: **1.0**.<br>
Date: **2022-2-24**.

Description: **Evaluation of alternatives based on multiple criteria using TOPSIS method.**.

---

## What is TOPSIS?

TOPSIS or **T**echnique for **O**rder **P**reference by **S**imilarity to **I**deal **S**olution is a method of compensatory aggregation that compares a set of alternatives by identifying weights for each criterion, normalising scores for each criterion and calculating the geometric distance between each alternative and the ideal alternative, which is the best score in each criterion.

<br>

## How to install this package:

```
>> pip install Topsis-Dilmanpreet-101903506
```

### In Command Prompt

```
>> topsis data.csv "1,1,2,1,1" "+,-,+,+,-" result.csv
```

## Input file (data.csv)

![input](https://user-images.githubusercontent.com/83512136/155395288-72ef06f5-d407-4dc5-ae3f-954110a36fed.JPG)


Weights (`weights`) if not already normalised, will be normalised later in the code.

The information of benefit positive(+) or negative(-) impact criteria should be provided in `impacts`.

<br>

## Output -- (result.csv)

![result](https://user-images.githubusercontent.com/83512136/155395048-9ae09f09-47b6-4ad3-9e7d-46010384bbb7.JPG)


<br>
The output file contains columns of input file along with two additional columns for Topsis_score and Rank
