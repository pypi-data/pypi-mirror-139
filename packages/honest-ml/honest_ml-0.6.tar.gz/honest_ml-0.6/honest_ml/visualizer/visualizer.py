import matplotlib.pyplot as plt

class Visualizer:
    def __init__(self, metrics, model_type, coef_names=[]):
        self.metrics = metrics
        self.model_type = model_type
        self.regression_metrics = [
            "mse", "max_error", "mae"
        ]
        if 'coef' in list(metrics[0].keys()):
            self.coefs = self._get_coefs(metrics, coef_names)
        else:
            self.coefs = None

        if model_type == "classification":
            classes = list(metrics[0].keys())
            classes.remove("accuracy")
            classes.remove("mask")
            classes.remove("seed")
            classes.remove("hyperparameters")
            classes.remove("coef")
            self.classes = classes
            self.classification_metrics = [
                "precision", "recall", "f1-score", "support"
            ]
    def _get_coefs(self, metrics, coef_names):
        coefs = {}.fromkeys(coef_names)
        for coef in coefs:
            coefs[coef] = []
        for run in metrics:
            for coef in run['coef']:
                for index in range(len(coef_names)):
                    key = coef_names[index]
                    coefs[key].append(coef[index])
        return coefs

    def visualize_coeficients(self, **kwargs):
        if self.coefs:
            for coeficient_name in self.coefs:
                coef = self.coefs[coeficient_name]
                plt.hist(coef, **kwargs)
                plt.xlabel(coeficient_name)
                plt.ylabel("magnitude")
                plt.show()
            
    def visualize_regression(self, **kwargs):
        for metric in self.regression_metrics:
            metrics = [metrics[metric] for metrics in self.metrics]
            plt.hist(metrics, **kwargs)
            plt.xlabel(metric)
            plt.ylabel("magnitude")
            plt.show()

    def visualize_classification(self, **kwargs):
        for _class in self.classes:
            for metric in self.classification_metrics:
                metrics = [metrics[_class][metric] for metrics in self.metrics]
                plt.hist(metrics, **kwargs)
                plt.xlabel(metric)
                plt.ylabel("magnitude")
                if "avg" in _class:
                    plt.title(_class)
                else:
                    plt.title(f"class {_class}")
                plt.show()
