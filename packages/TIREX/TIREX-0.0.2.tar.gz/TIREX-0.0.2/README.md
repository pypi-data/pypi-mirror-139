# Tirex

Tirex package is a tool for dimensionality reduction in a regression context. More precisely, Tirex extracts the features that explains the extreme values of Y , where Y is the target variable. To illustrate our claim, consider a problem of risk management, where one wants to predict accuratly large values. In this case, using standard dimensionality reduction methods (PCA,SVD, Locally linear embedding,etc.) before a regression can give a very poor performance in the region of interest (Y large). Tirex comes in hand to tackle this problem by extracting the necessary features for predicting large values.

The package we provide is also compatible with sickit-learn Pipelines.

Calling fit will fit the model on the training data X.


Calling fit_transform will fit the model and perform the dimensionality reduction task.


Calling transform will 
