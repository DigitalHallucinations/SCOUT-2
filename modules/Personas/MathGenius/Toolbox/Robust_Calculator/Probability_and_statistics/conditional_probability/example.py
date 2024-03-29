
from Personas.MathGenius.Toolbox.Robust_Calculator.Probability_and_statistics.conditional_probability.bayesian import Bayesian

# Example usage
p_a = 0.3
p_b_given_a = 0.6
p_b_given_not_a = 0.2

bayesian = Bayesian(p_a, p_b_given_a, p_b_given_not_a)
posterior_probability = bayesian.calculate_posterior()
prior_probability = bayesian.calculate_prior()
likelihood_probability = bayesian.calculate_likelihood()
evidence_probability = bayesian.calculate_evidence()
odds_ratio = bayesian.calculate_odds_ratio()
bayes_factor = bayesian.calculate_bayes_factor()
lower_bound, upper_bound = bayesian.calculate_posterior_interval(0.95)

print(posterior_probability)  # Output: 0.6923076923076923
print(prior_probability)  # Output: 0.42857142857142855
print(likelihood_probability)  # Output: 0.3333333333333333
print(evidence_probability)  # Output: 0.42857142857142855
print(odds_ratio)  # Output: 1.7999999999999998
print(bayes_factor)  # Output: 1.7999999999999998
print(lower_bound, upper_bound)  # Output: (0.3846153846153846, 0.9230769230769231)