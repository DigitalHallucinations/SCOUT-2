import math

class Bayesian:
    def __init__(self, p_a, p_b_given_a, p_b_given_not_a):
        self.p_a = p_a
        self.p_b_given_a = p_b_given_a
        self.p_b_given_not_a = p_b_given_not_a

    def calculate_posterior(self):
        p_not_a = 1 - self.p_a
        p_b = (self.p_b_given_a * self.p_a) + (self.p_b_given_not_a * p_not_a)
        p_a_given_b = (self.p_b_given_a * self.p_a) / p_b
        return p_a_given_b

    def calculate_prior(self):
        p_not_a = 1 - self.p_a
        p_b_given_not_a = (self.p_b_given_a * self.p_a) / self.p_b
        p_a_given_not_b = (p_b_given_not_a * self.p_a) / p_not_a
        return p_a_given_not_b

    def calculate_likelihood(self):
        p_not_a = 1 - self.p_a
        p_b_given_not_a = (self.p_b_given_a * self.p_a) / self.p_b
        p_not_b_given_not_a = 1 - p_b_given_not_a
        p_not_a_given_not_b = (p_not_b_given_not_a * p_not_a) / (1 - self.p_b)
        return p_not_a_given_not_b

    def calculate_evidence(self):
        p_not_a = 1 - self.p_a
        p_b_given_not_a = (self.p_b_given_a * self.p_a) / self.p_b
        p_not_b_given_not_a = 1 - p_b_given_not_a
        p_not_a_given_b = (p_not_b_given_not_a * p_not_a) / (1 - self.p_b)
        p_evidence = (self.p_b_given_a * self.p_a) + (p_not_a_given_b * (1 - self.p_a))
        return p_evidence

    def calculate_odds_ratio(self):
        p_not_a = 1 - self.p_a
        p_b_given_not_a = (self.p_b_given_a * self.p_a) / self.p_b
        p_not_b_given_not_a = 1 - p_b_given_not_a
        odds_ratio = (self.p_b_given_a * p_not_a) / (p_not_b_given_not_a * self.p_a)
        return odds_ratio

    def calculate_bayes_factor(self):
        p_not_a = 1 - self.p_a
        p_b_given_not_a = (self.p_b_given_a * self.p_a) / self.p_b
        p_not_b_given_not_a = 1 - p_b_given_not_a
        bayes_factor = (self.p_b_given_a * self.p_a) / (p_not_b_given_not_a * p_not_a)
        return bayes_factor

    def calculate_posterior_interval(self, confidence_level):
        p_not_a = 1 - self.p_a
        p_b = (self.p_b_given_a * self.p_a) + (self.p_b_given_not_a * p_not_a)
        p_a_given_b = (self.p_b_given_a * self.p_a) / p_b

        z_score = self.calculate_z_score(confidence_level)
        standard_error = self.calculate_standard_error(p_a_given_b, p_b)

        lower_bound = p_a_given_b - z_score * standard_error
        upper_bound = p_a_given_b + z_score * standard_error

        return lower_bound, upper_bound

    def calculate_z_score(self, confidence_level):
        if confidence_level == 0.9:
            return 1.645
        elif confidence_level == 0.95:
            return 1.96
        elif confidence_level == 0.99:
            return 2.576
        else:
            raise ValueError("Invalid confidence level. Supported values: 0.9, 0.95, 0.99")

    def calculate_standard_error(self, p_a_given_b, p_b):
        return ((p_a_given_b * (1 - p_a_given_b)) / p_b) ** 0.5
