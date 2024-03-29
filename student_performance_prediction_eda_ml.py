
# import libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# set style of visualization
sns.set_style("whitegrid")
sns.set_palette("RdBu")

# read data set

data = pd.read_csv("/kaggle/input/student-performance-multiple-linear-regression/Student_Performance.csv")

# see top 5 rows

data.head()

# see column data type and some info

data.info()

# see precentege of missing value in each column

data.isna().sum() / data.shape[0]

# see dimensions

data.shape

# check if duplicated in data

data.duplicated().any()
data.describe()

# see quick info of category values

data.describe(include = object)

"""**We Can see :**
   - Dataset no missing values
   - Dataset has no complete duplicates
   - We need to modify some column data type

## Univariate Analysis & Visualizations
"""

# create function to visualized categorical column using count plot

def count_plot(column_name, hue = None, rotation = 0):
    """
    1) input : column name, column data type must be object or categorical
    3) output : cout plot using seaborn modules, unique values in x-axis and frequency in y-axis
    4) i use bar_label to show frequency of each unique values above each column in graph
    """
    graph = sns.countplot(x = column_name, data = data, hue = hue, order = data[column_name].value_counts().index)
    for container in graph.containers:
        graph.bar_label(container)


    plt.xticks(rotation = rotation)
    plt.show()

# create function that visualized numeric columns using box plot

def box_plot(x_axis = None, y_axis = None, hue = None, col = None):
    """
    input : x_axis, y_axis and hue column, column data type must be numeric in y_axis
    output : box plot to see distribution of column values such as min,max,mean,medien,std
    """
    sns.catplot(x = x_axis, y = y_axis, data = data, hue = hue, kind = "box", col = col)
    plt.xlabel(x_axis)
    plt.ylabel("FRQ")
    plt.show()

"""### Discovering `Hours Studied` column"""

# see uniqie values

data["Hours Studied"].unique()

# number of unique values is relatively large, count plot more suitable for it

# first set figure size
plt.figure(figsize = (15,6))

# call function i create it in cell 10
count_plot(column_name = "Hours Studied")

"""**We can see :**
   - Most student studied "1" hour
   - Other students studied Similar numbers of hours

### Discovering `Previous Scores` column
"""

# see distribution

box_plot(y_axis = "Previous Scores") # call function i create it in cell 11

"""**We can see :**
   - 50 % of students scored above 65
   - No student obtained the final grade

### Discovering `Extracurricular Activities` column
"""

# see unique values

data["Extracurricular Activities"].unique()

# output number of values count

plt.pie(data["Extracurricular Activities"].value_counts(), labels = data["Extracurricular Activities"].value_counts().index,
        shadow = True, autopct = "%1.1f%%")
plt.show()

"""**We can see :**
   - Most student "don't" participate in extracurricular activities

### Discovering `Sleep Hours` column
"""

# see unique values

data["Sleep Hours"].unique()

# number of unique values is relatively large, count plot more suitable for it

# first set figure size
plt.figure(figsize = (15,6))

# call function i create it in cell 10
count_plot(column_name = "Sleep Hours")

"""**We can see :**
   - Most student Sleep 8 hours
   - Other students sleep Similar numbers of hours

### Discovering `Sample Question Papers Practiced` column
"""

# see unique values

data["Sample Question Papers Practiced"].unique()

# number of unique values is relatively large, count plot more suitable for it

# first set figure size
plt.figure(figsize = (15,6))

# call function i create it in cell 10
count_plot(column_name = "Sample Question Papers Practiced")

"""**We can see :**
   - All student have Similar The number of sample question papers the practiced.
   - **There are students who did not practice any questions**

## Bivariate Analysis & Visualizations
"""

# What is "Hours Studied" and "Performance Index" distribution

box_plot(x_axis = "Hours Studied", y_axis = "Performance Index") # call function i create it in cell 11

"""- As we can see, the more hours you study, the greater the success rate"""

# What is "	Extracurricular Activities" and "Performance Index" distribution

box_plot(x_axis = "Extracurricular Activities", y_axis = "Performance Index") # call function i create it in cell 11

"""- Participation in extracurricular activities helps to a very small extent in obtaining high grades"""

# What is "Extracurricular Activities" and "Performance Index" distribution

avg_performance_by_hours = data.groupby('Hours Studied')['Performance Index'].mean()
plt.plot(avg_performance_by_hours.index, avg_performance_by_hours.values)
plt.show()

"""- The more hours you sleep, Performance index increase

### Heatmap of Correlation
"""

# first visualize correlation matrix between numerical columns

plt.figure(figsize = (10,6))
sns.heatmap(data.select_dtypes(exclude = object).corr(), annot = True, fmt = ".2f", linewidths = 0.2)
plt.show()

"""There's a lot of Strong Positive Relationships between Performance Index and Features

##  Data Preprocessing
"""

# import libraries to model

from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error,r2_score

# create object from labelencoder

encoder = LabelEncoder()

data["Extracurricular Activities"] =  encoder.fit_transform(data["Extracurricular Activities"])

# see sample of data

data.sample(2)

# Splitting data into Indipendent and Dependent Variable

Train = data.drop(columns = "Performance Index")
Target = data["Performance Index"]

# see sample of train data

Train.sample(3)

# see sample of target label

Target

X_train, X_test, y_train, y_test = train_test_split(Train, Target, test_size = 0.3, random_state = 24)

# see shape of splited data

print("x_train shape: ", X_train.shape)
print("y_train shape: ", y_train.shape)
print("x_test shape: ", X_test.shape)
print("y_test shape: ", y_test.shape)

"""## Modeling"""

# create object from RandomForestRegressor

model = LinearRegression()

# fit model

model.fit(X_train,y_train)

"""## Evaluating Results"""

# Calculate the score of the model on the training data

model.score(X_train, y_train)

# see predicted values

predict = np.round(model.predict(X_test), decimals = 1)

# Real Values vs Predicted Values

pd.DataFrame({"Actual Performance" : y_test, "Predicted Performance" : predict})

# Create scatter plot to see distribution

plt.scatter(y_test, predict)
plt.show()

# see mean absolute error

mean_absolute_error(y_test,predict)

# see score

r2_score(y_test,predict)

# see coefficients values

model.coef_

# see y intercept

model.intercept_

"""**Equation of our multiple linear regression model is :**
   - 2.85 × Hours Studied + 1.02 × Previous Scores + 0.61 × Extracurricular Activities + 0.48 × Sleep Hours + 0.19 × Sample Question Papers Practiced - 33.92
"""

