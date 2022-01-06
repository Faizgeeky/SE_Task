# Import the needed libraries 
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.svm import SVC

def SpamFilter(message):
    # Create empty dict to return with results 
    result ={}
    # file location 
    file1 = open(r"SMSSpamCollection.txt","r")
    lines = file1.readlines()
    
    # Use Pandas dataframe
    df = pd.DataFrame()
    print("Reading Data ....")

    # As it is TXT file, Use String Manupulation to seprate labels from Message
    for line in lines:
      
        df = df.append({'Type': line[:4], 'Message': line[4:]}, ignore_index=True)
    
    # ML model to train X, y cordinate , X is feature and y is Target 
    X = df["Message"]
    y = df["Type"]

    print("Model Training... ")
    # To train with any ML model need to seprate in Training and testing split 
    X_train , X_test , y_train , y_test = train_test_split(X,y,test_size=0.2, random_state=0)

    # Using SVM Model to train, test and predict the Results 
    cv = CountVectorizer()
    X_train = cv.fit_transform(X_train)
    X_test = cv.transform(X_test)


    # train the model using SVM 
    model = SVC(kernel = "rbf", random_state = 10,probability=True)
    model.fit(X_train,y_train)

    # Append results to Dict return 
    # Entire Model Score
    result["Model_Score"] = round((model.score(X_test,y_test)),2)

    # Message Prediction Score
    result["Message_Accuracy"] = model.predict_proba(cv.transform([message]))

    if result["Message_Accuracy"][0][1] >= 0.7:
        result["Message_Prediction"] = "SPAM"
    else:
        result["Message_Prediction"] = "NOT SPAM"


    return result
    
# Initiate
if __name__ =="__main__":
    message = input("Please enter your Message :- ")
    # will return Dictonary with 3 values "Model_Score" ,"Message_Accuracy","Message_Prediction"
    result = SpamFilter(message)

    print("Score of Message :","{:.2f}".format(result["Message_Accuracy"][0][1]))
    print("Result : ",result["Message_Prediction"])
    
