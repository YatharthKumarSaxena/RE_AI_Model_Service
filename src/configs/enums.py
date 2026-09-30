from enum import Enum


class RequestLocation(Enum):
    BODY = "body"
    QUERY = "query"
    PARAMS = "params"
    HEADERS = "headers"


class ProjectTypes(Enum):
    DEVELOPMENT = "development"
    ENHANCEMENT = "enhancement"
    MAINTENANCE = "maintenance"

class EntityTypeModel(Enum):
    DEFAULT = "linear_svm"
    LINEAR_SVM = "linear_svm"
    SGD_CLASSIFIER = "sgd_classifier"
    RIDGE_CLASSIFIER = "ridge_classifier"
    LOGISTIC_REGRESSION = "logistic_regression"
    COMPLEMENT_NAIVE_BAYES = "complement_naive_bayes"
    BERNOULLI_NAIVE_BAYES = "bernoulli_naive_bayes"
    MULTINOMIAL_NAIVE_BAYES = "multinomial_naive_bayes"
    EXTRA_TREES = "extra_trees"
    RANDOM_FOREST = "random_forest"
    DECISION_TREE = "decision_tree"

class DeviceType(Enum):
    MOBILE = "mobile"
    TABLET = "tablet"
    LAPTOP = "laptop"