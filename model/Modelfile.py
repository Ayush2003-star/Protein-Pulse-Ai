# importing librararies 
#pandas is use for (data cleaning,loading)
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
from sklearn.preprocessing import LabelEncoder,StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score
from sklearn.pipeline import Pipeline
import joblib

#reading the file
protien_pulse_dataframe = pd.read_csv('protein_dataset.csv')

# for knowing the rows and collumns of the data
protien_pulse_dataframe.shape

# for knowing the top 5 records ofo the data
protien_pulse_dataframe.head()

# for  knowing the last 5 records of the data
protien_pulse_dataframe.tail()

# for checking the name of the coluumns
protien_pulse_dataframe.columns

#checking the unique value in the coluum
# to check the count of unique values like how many time male come and female come
protien_pulse_dataframe['gender'].value_counts()
# to inly check the unique value 
protien_pulse_dataframe['gender'].unique()
# to return the count of the only unique values
protien_pulse_dataframe['gender'].nunique()
# to check the all colummns information like nulls,count,datatypes
protien_pulse_dataframe.info()

# describe (finding mean/average,max,min count values of numerical colummns)
protien_pulse_dataframe.describe()
#for checking in variable
a  = protien_pulse_dataframe.describe()
#for checking particular coluumns
particular_colummns = protien_pulse_dataframe.describe()['age']

#more methods to check the null data in dataframe
protien_pulse_dataframe.isnull()
#to get the sum means the count of the nulls
protien_pulse_dataframe.isnull().sum()
# avaerage of the nulls
protien_pulse_dataframe.isnull().mean()

#if you want to drop all the data is null (remove the rows)
protien_pulse_dataframe.dropna(inplace=True)  


#how to select collums with dtype integer and float
cols = protien_pulse_dataframe.select_dtypes(include=['int64','float64']).columns
print(cols)

#data preprocessing
#deviding dependent and independent       
x_protein = protien_pulse_dataframe.drop(['protein_g'],axis=1)
y_protien = protien_pulse_dataframe['protein_g']
x_protein.info()


#encoding
le1 = LabelEncoder()
le2 = LabelEncoder()
le3 = LabelEncoder()
x_protein['gender']=le1.fit_transform(x_protein['gender'])
x_protein['activity_level']=le2.fit_transform(x_protein['activity_level'])
x_protein['purpose']=le3.fit_transform(x_protein['purpose'])
#saving in the job lib file because it is needed in the time of prediction
joblib.dump(le1,'gender_encoder.joblib')
joblib.dump(le2,'activity_level.joblib')
joblib.dump(le3,'purpose_encoding.joblib')

#making boxplot for checking outliers
for i in x_protein:
    sns.boxplot(x_protein[i])
    plt.show()
#making histpllot for count the values
for i in x_protein:
    sns.histplot(x_protein[i],kde=True)
    plt.show()
#making distplot for checking the distribution
for i in x_protein:
    sns.distplot(x_protein[i])
    plt.show()
    
#feature selection using corelation
corr = x_protein.corrwith(y_protien)        
#dropping the feature which ae not useful
x_protein.drop(['lean_to_total_ratio'],axis=1,inplace=True)
x_protein.drop(['age_protein_factor'],axis=1,inplace=True)



#Scaling
standard_scaler = StandardScaler()
x_protein = standard_scaler.fit_transform(x_protein)

#train test split
x_train,x_test,y_train,y_test=train_test_split(x_protein,y_protien,test_size=0.2,random_state=42)

model = RandomForestRegressor()
model.fit(x_train,y_train)
y_prediction = model.predict(x_test)
r2 = r2_score(y_test,y_prediction)

#createing a pipeline

pipeline_d = Pipeline([
    
    ('standard_scaler',StandardScaler()),
   ( 'model',RandomForestRegressor()),
   ])
pipeline_d.fit(x_protein,y_protien)

pipeline_d.predict(x_protein)

joblib.dump(pipeline_d,'protein_pipeline.joblib')