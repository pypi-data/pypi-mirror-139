from sklearn.model_selection import cross_val_score
from typing import Any,Dict,List,Optional,Set,Tuple
import codefast as cf
from premium.measure import libra

class Classifier(object):
    def __init__(self, clf: Any) -> None:
        self.clf = clf

    def cv(self, X, y, folds=5):
        scores = cross_val_score(
            estimator=self.clf, X=X, y=y, cv=folds)
        cf.info(f'cv scores: {scores}')
        cf.info("score :{:.2f} %".format(scores.mean()*100))
        cf.info("standard deviation:{:.2f} %".format(scores.std()*100))
        return self

    def fit(self, X, y):
        self.clf.fit(X, y)
        return self

    def test(self, Xt, yt):
        y_pred = self.clf.predict(Xt)
        libra.metrics(yt, y_pred)
        return self

    def predict(self, Xt):
        return self.clf.predict(Xt)
