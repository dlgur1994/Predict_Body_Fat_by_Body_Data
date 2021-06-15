import pandas as pd
import numpy as np
from scipy.stats import skew
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import pickle

# train data file load
# delete 'Index' because it is provided when converted to a data frame, and delete 'Standard_Weight' because it is determined by the hegith
file_df = pd.read_csv('./train_data.csv')
target_name = 'Body_Fat_Rate'
no_need_features = ['Index', 'Standard_Weight']
category_features = ['Sex']

# arrange X and y
file_df.drop(no_need_features, axis=1, inplace=True)
y_target = file_df[target_name]
X_features = file_df.drop([target_name],axis=1,inplace=False)

# visualize data to find outliers
outlier_name = 'Height'
cond1 = file_df[outlier_name] < 60
cond2 = file_df[target_name] < 30
outlier_index = X_features[cond1 & cond2].index
X_features.drop(outlier_index , axis=0, inplace=True)
y_target.drop(outlier_index, axis=0, inplace=True)

# figure out the extent of distortion in features --> if the degree of distortion is high(>1 or <-1), log transformation is performed.
# 'Height' needs the log transformation
features_index = file_df.drop(category_features, axis=1, inplace=False).dtypes.index
skew_features = file_df[features_index].apply(lambda x : skew(x))
# print(skew_features.sort_values(ascending=False))
skew_features_change = skew_features[skew_features < -1]
file_df[skew_features_change.index] = np.log1p(file_df[skew_features_change.index])

# change the category feature to One-Hot Encoding --> 'Sex'
X_features_ohe = pd.get_dummies(X_features, columns=category_features)

# the log transformation is applied on the target column to form a normal distribution
y_target_log = np.log1p(y_target)

# split train/test data based on feature dataset with One-Hot encoding
X_train, X_test, y_train, y_test = train_test_split(X_features_ohe, y_target_log, test_size=0.2, random_state=0)

# single model
model = rf_reg = RandomForestRegressor(max_depth=14, min_samples_leaf=2, min_samples_split=2, n_estimators=700, n_jobs=-1)
model.fit(X_train, y_train)

# make a pkl file
pickle.dump(model, open('model.pkl','wb'), protocol=2)
print('done')