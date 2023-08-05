import codefast as cf


class ClassifierDemos(object):
    """ Some machine learning classifier demos for references.
    """
    def catboost_classifier(self) -> 'CatBoostClassifier':
        import catboost as cb
        return cb.CatBoostClassifier(iterations=1000,
                                     learning_rate=0.1,
                                     eval_metric='Accuracy',
                                     loss_function='MultiClass',
                                     random_seed=42,
                                     verbose=True,
                                     early_stopping_rounds=50,
                                     task_type="GPU",
                                     metric_period=50,
                                     devices='0:1')

    def lightgbm_classifier(self) -> 'LightGBMClassifier':
        import lightgbm
        return lightgbm.LGBMClassifier(
            boosting_type='gbdt',
            learning_rate=0.1,
            n_estimators=300,
            objective='multiclass',
            # metric='auc',
            random_state=42,
            verbose=1,
            n_jobs=-1,
            device='gpu')

    def xgboost_classifier(self) -> 'XGBClassifier':
        import xgboost
        return xgboost.XGBClassifier(
            learning_rate=0.1,
            n_estimators=500,
            objective='multi:softmax',
            #  objective='binary:logistic',
            random_state=42,
            verbose=True,
            device='gpu')

    def extra_tree_classifier(self) -> 'ExtraTreeClassifier':
        from sklearn.ensemble import ExtraTreesClassifier
        return ExtraTreesClassifier(n_estimators=1500,
                                    max_depth=None,
                                    min_samples_split=2,
                                    n_jobs=-1,
                                    random_state=42)

    def random_forest_classifier(self) -> 'RandomForestClassifier':
        from sklearn.ensemble import RandomForestClassifier
        return RandomForestClassifier(n_estimators=500,
                                      max_depth=None,
                                      min_samples_split=2,
                                      random_state=42)

    def logistic_regression(self) -> 'LogisticRegression':
        from sklearn.linear_model import LogisticRegression
        return LogisticRegression(C=1.0,
                                  random_state=42,
                                  solver='liblinear',
                                  multi_class='ovr')

    def svm_classifier(self) -> 'SVC':
        from sklearn.svm import SVC
        return SVC(C=1.0, kernel='rbf', random_state=42)

    def decision_tree_classifier(self) -> 'DecisionTreeClassifier':
        from sklearn.tree import DecisionTreeClassifier
        return DecisionTreeClassifier(max_depth=None,
                                      min_samples_split=2,
                                      random_state=42)

    def gradient_boosting_classifier(self) -> 'GradientBoostingClassifier':
        from sklearn.ensemble import GradientBoostingClassifier
        return GradientBoostingClassifier(n_estimators=500,
                                          learning_rate=0.1,
                                          max_depth=None,
                                          random_state=42)


class Demo(object):
    def __init__(self) -> None:
        self.classifiers = ClassifierDemos()


demo_object = Demo()
