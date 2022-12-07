from sklearn.linear_model import LogisticRegression
import pandas as pd
import numpy as np


# Test prediction with a Female, 19 years old, earning 20000
fixed_value = [1, 19, 20000]


def preprocess(df: pd.DataFrame) -> pd.DataFrame:
    def _gender_to_int(gender):
        if gender == "Female":
            return 1
        return 0

    df["GenderNum"] = df["Gender"].apply(_gender_to_int)

    return df


def train(dataset):
    # X (features) are "GenderNum", "Age", "EstimatedSalary"
    X = dataset[["GenderNum", "Age", "EstimatedSalary"]]

    # Y is "Purchased"
    Y = dataset[["Purchased"]]

    # Let's split the dataset: the first 50 will be used for training,
    # the rest will be for testing
    split = 50
    X_train, Y_train = X[:split], Y[:split]
    X_test, Y_test = X[split:], Y[split:]

    # Using scikit-learn default
    regression = LogisticRegression(random_state=0).fit(X_train, Y_train)

    # Accuracy of our model:
    print(f"intercept: {regression.intercept_} coefficients: {regression.coef_}")
    print(f"train accuracy: {regression.score(X_train, Y_train)}")
    print(f"test accuracy: {regression.score(X_test, Y_test)}")  # We aim for > 0.8...

    return regression


def predict(x, regression: LogisticRegression):
    variables = np.array(x).reshape(1, -1)
    result = regression.predict(variables)
    print(f"for: {variables}, the prediction is {result}")
    return result


if __name__ == "__main__":
    # Testing
    df = pd.read_csv("data/data.csv")
    df = preprocess(df)
    model = train(df)
    print(predict(fixed_value, model))
