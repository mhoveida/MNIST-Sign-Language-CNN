from networkx import non_neighbors
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import AdaBoostClassifier
from matplotlib import colormaps
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

class Classifiers():
    def __init__(self,data):
        ''' 
        TODO: Write code to convert the given pandas dataframe into training and testing data 
        # all the data should be nxd arrays where n is the number of samples and d is the dimension of the data
        # all the labels should be nx1 vectors with binary labels in each entry 
        '''
        self.data = data
        self.training_data = None
        self.training_labels = None
        self.testing_data = None
        self.testing_labels = None
        self.outputs = []

        X= data[['A' , 'B']].values
        Y= data['label'].values.reshape(-1,1)

        self.training_data, self.testing_data, self.training_labels, self.testing_labels = train_test_split(X, Y, test_size=0.4, random_state=42)
        """print("Data successfully split:")
        print(f"Training data shape: {self.training_data.shape}")
        print(f"Training labels shape: {self.training_labels.shape}")
        print(f"Testing data shape: {self.testing_data.shape}")
        print(f"Testing labels shape: {self.testing_labels.shape}")"""

    def visualize_data(self):
        plt.figure(figsize=(8,6))
        class_0 =self.data[self.data['label']==0]
        plt.scatter(class_0['A'],class_0['B'], label='Class 0', marker='o')
        class_1 =self.data[self.data['label']==1]
        plt.scatter(class_1['A'],class_1['B'], label='Class 1', marker='x')
        plt.title('Part a--Scatter Plot of Dataset')
        plt.xlabel('A')
        plt.ylabel('B')
        plt.legend()
        plt.grid(True)
        #plt.savefig('part1a.png', dpi=300)
        plt.show()

    def test_clf(self, clf, parameters, classifier_name=''):
        # TODO: Fit the classifier and extrach the best score, training score and parameters

        grid_search = GridSearchCV(clf, parameters, cv=5, scoring='accuracy')
        grid_search.fit(self.training_data, self.training_labels.ravel())

        # extract best score, training score, and parameters
        best_classifier = grid_search.best_estimator_
        best_training_score = grid_search.best_score_
        best_parameters = grid_search.best_params_

        testing_score = best_classifier.score(self.testing_data, self.testing_labels)
        self.outputs.append(f"{classifier_name}, {best_training_score:.4f}, {testing_score:.4f}")

        # Use the following line to plot the results
        self.plot(self.testing_data, best_classifier.predict(self.testing_data),model=best_classifier,classifier_name=classifier_name)
        #print("Name, parameters, traning score, testing score", classifier_name, best_parameters, best_training_score, testing_score)


    def classifyNearestNeighbors(self):
        # TODO: Write code to run a Nearest Neighbors classifier
        parameters = {
            'n_neighbors': range(1, 20, 2),
            'leaf_size': range(5, 35, 5)
        }
        self.test_clf(KNeighborsClassifier(), parameters, classifier_name='KNN')

    def classifyLogisticRegression(self):
        # TODO: Write code to run a Logistic Regression classifier
        parameters = {
            'C': [0.1, 0.5, 1, 5, 10, 50, 100]
        }
        self.test_clf(LogisticRegression(), parameters, classifier_name='Logistic Regression')

    def classifyDecisionTree(self):
        # TODO: Write code to run a Logistic Regression classifier
        parameters = {
            'max_depth': list(range(1, 51)),
            'min_samples_split': list(range(2, 11))
        }
        # Test Decision Tree classifier
        self.test_clf(DecisionTreeClassifier(), parameters, classifier_name='Decision Tree')


    def classifyRandomForest(self):
            # TODO: Write code to run a Random Forest classifier
            parameters = {
                'max_depth': [1, 2, 3, 4, 5],
                'min_samples_split': list(range(2, 11))
            }
            # Test Random Forest classifier
            self.test_clf(RandomForestClassifier(), parameters, classifier_name='Random Forest')

    def classifyAdaBoost(self):
            # TODO: Write code to run a AdaBoost classifier
            parameters = {
                'n_estimators': list(range(10, 81, 10))
            }
            # Test AdaBoost classifier
            self.test_clf(AdaBoostClassifier(algorithm='SAMME'), parameters, classifier_name='AdaBoost')

    def plot(self, X, Y, model,classifier_name = ''):
        X1 = X[:, 0]
        X2 = X[:, 1]

        X1_min, X1_max = min(X1) - 0.5, max(X1) + 0.5
        X2_min, X2_max = min(X2) - 0.5, max(X2) + 0.5

        X1_inc = (X1_max - X1_min) / 200.
        X2_inc = (X2_max - X2_min) / 200.

        X1_surf = np.arange(X1_min, X1_max, X1_inc)
        X2_surf = np.arange(X2_min, X2_max, X2_inc)
        X1_surf, X2_surf = np.meshgrid(X1_surf, X2_surf)

        L_surf = model.predict(np.c_[X1_surf.ravel(), X2_surf.ravel()])
        L_surf = L_surf.reshape(X1_surf.shape)

        plt.title(classifier_name)
        plt.contourf(X1_surf, X2_surf, L_surf, cmap = plt.cm.coolwarm, zorder = 1)
        plt.scatter(X1, X2, s = 38, c = Y)

        plt.margins(0.0)
        # uncomment the following line to save images
        plt.savefig(f'{classifier_name}.png')
        plt.show()

    
if __name__ == "__main__":
    #df = pd.read_csv('input.csv')
    df = pd.read_csv('/Users/hoveida/Downloads/AI/HW4/Coding/starter/input.csv')
    models = Classifiers(df)
    #print('Visualizing Data...')
    models.visualize_data()
    print('Classifying with NN...')
    models.classifyNearestNeighbors()
    print('Classifying with Logistic Regression...')
    models.classifyLogisticRegression()
    print('Classifying with Decision Tree...')
    models.classifyDecisionTree()
    print('Classifying with Random Forest...')
    models.classifyRandomForest()
    print('Classifying with AdaBoost...')
    models.classifyAdaBoost()

    with open("output.csv", "w") as f:
        print('Name, Best Training Score, Testing Score',file=f)
        for line in models.outputs:
            print(line, file=f)