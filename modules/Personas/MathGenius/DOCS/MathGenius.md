# Structure

**MathGenius: An Advanced Mathematical Problem Solver**

MathGenius is a GPT-based persona, specializing in solving complex mathematical problems and providing guidance on various mathematical concepts. As a GPT-based persona, MathGenius leverages the capabilities of AI language models to understand and respond to user queries effectively.

**Development Credits**

This sophisticated tool was developed by Digital Hallucinations. The company's expertise in cutting-edge technology and its commitment to advancing the field of artificial intelligence has led to the creation of this advanced problem-solving solution.

**Robust_Calculator**

To enhance its functionality and performance in the MathGenius role, a Robust_Calculator is provided in the form of Python modules. These tools are designed to allow the GPT to manipulate and utilize them during its role as MathGenius, making it more effective in solving mathematical problems and providing guidance.

- Probability and Statistics: Modules for handling various probability and statistics-related concepts and operations.
- Algebra: Modules for solving algebraic equations, factoring, and performing other algebra-related operations.
- Geometry: Modules for solving problems related to geometry, including area, perimeter, and coordinate geometry.
- Trigonometry: Modules for working with trigonometric functions and solving trigonometric equations.
- Calculus: Modules for handling concepts in calculus, such as limits, derivatives, and integrals.
- Linear Algebra: Modules for working with linear algebra operations, such as matrix and vector manipulations.
- Number Theory: Modules for working with number theory concepts, such as primes, factorization, and modular arithmetic.

## Features

- **Tools**: User input and visualization tools to help users interact with the library and visualize their results.
- **Probability and Statistics**: Covers conditional probability, discrete probability, continuous probability distributions, permutations and combinations, and probability theorems.
- **Statistics**: Central tendency, correlation and regression, and dispersion.
- **Algebra**: Basic operations, equations, factoring, functions, inequalities, and systems of equations.
- **Geometry**: Area, perimeter, surface area, volume, coordinate geometry, and trigonometry.
- **Trigonometry**: Identities, inverse trig functions, right triangle trig, trig equations, and unit circle.
- **Calculus**: Limits, derivatives, integrals, differential equations, and multivariable calculus.
- **Linear Algebra Operations**: Determinants, eigenvalues, eigenvectors, matrix operations, vector operations, and linear transformations.
- **Number Theory Calculations**: Primes, factorization, GCD and LCM, modular arithmetic, Diophantine equations, congruences, and continued fractions.
- **Extras**: Confidence intervals, goodness of fit tests, hypothesis testing, non-parametric tests, regression analysis, sampling, statistical inference, and time series analysis.

## Usage

MathGenius uses openAi function calling to perform operations within the modules.

To use MathGenius, simply import the required modules and start performing operations using JSON format. Here's an example of using the `mean` function from the `central_tendency` module:

```python
from MathGenius.Robust_Calculator.Statistics.central_tendency import mean

data = [1, 2, 3, 4, 5]
mean_value = mean(data)

print(mean_value)  # Output: 3.0
```

## Documentation

For detailed documentation on each module and its functions, please refer to the `docs` folder. The documentation is organized by module and includes examples and explanations for each function.

## Tests

Tests for each module are located in the `tests` folder. To run the tests, navigate to the `tests` folder and run the following command:

```
python -m unittest discover
```

This will execute all the test files and provide a summary of the results.

## Contributing

We welcome contributions to MathGenius! If you have an idea for a new feature, optimization, or bug fix, please open an issue or submit a pull request. We also appreciate contributions to the documentation and tests.

## Folder Structure

```
Main_app.modules
│
MathGenius/
│  │
│  ├── Toolbox/
│  │   ├── __init__.py
│  │   ├── user_input.py
│  │   ├── visualization.py
│  │   │   ├── Docs/
│  │   │   │ ├── user_input.md
│  │   │   │ └── visualization.md
│  │   │   │
│  ├── Robust_Calculator/
│  │   ├── Probability_and_statistics/
│  │   │   ├── conditional_probability/
│  │   │   │   ├── __init__.py
│  │   │   │   ├── bayesian.py
│  │   │   │   ├── joint_probability.py
│  │   │   │   ├── markov_chains.py
│  │   │   │   ├── monty_hall.py
│  │   │   │   ├── multiple_events.py
│  │   │   │   ├── simple.py
│  │   │   │   ├── independence_testing.py
│  │   │   │   ├── total_prob.py
│  │   │   │   └── Docs/
│  │   │   ├── discrete_probability/
│  │   │   │   ├── __init__.py
│  │   │   │   ├── binomial.py
│  │   │   │   ├── cdf.py
│  │   │   │   ├── expt_variance.py
│  │   │   │   ├── geometric.py
│  │   │   │   ├── hypergeometric.py
│  │   │   │   ├── multinomial.py
│  │   │   │   ├── neg_bi.py
│  │   │   │   ├── par_est.py
│  │   │   │   ├── poisson.py
│  │   │   │   ├── random_gen.py
│  │   │   │   ├── skellam.py
│  │   │   │   ├── zeta.py
│  │   │   │   └── Docs/
│  │   │   ├── continuous_probability_distributions/
│  │   │   │   ├── __init__.py
│  │   │   │   ├── chi_squared.py
│  │   │   │   ├── exponential.py
│  │   │   │   ├── f_distribution.py
│  │   │   │   ├── log_normal.py
│  │   │   │   ├── normal.py
│  │   │   │   ├── pareto.py
│  │   │   │   ├── students_t.py
│  │   │   │   ├── weibull.py
│  │   │   │   └── Docs/
│  │   │   ├── permutations_combinations/
│  │   │   │   ├── __init__.py
│  │   │   │   ├── circular_permutations.py
│  │   │   │   ├── combinations.py
│  │   │   │   ├── combinations_with_repetitions.py
│  │   │   │   ├── permutations.py
│  │   │   │   ├── permutations_with_repetitions.py
│  │   │   │   └── Docs/
│  │   │   ├── probability_theorems/
│  │   │   │   ├── __init__.py
│  │   │   │   ├── chebyshevs_inequality.py
│  │   │   │   ├── conditional_expectation.py
│  │   │   │   ├── inclusion_exclusion.py
│  │   │   │   ├── jensens_inequality.py
│  │   │   │   ├── law_of_large_numbers.py
│  │   │   │   ├── prob_theorems.py
│  │   │   │   └── Docs/
│  │   ├── Statistics/
│  │   │   ├── central_tendency/
│  │   │   │   ├── __init__.py
│  │   │   │   ├── mean.py
│  │   │   │   ├── median.py
│  │   │   │   ├── mode.py
│  │   │   │   └── Docs/
│  │   │   ├── correlation_and_regression/
│  │   │   │   ├── correlation_coefficient.py
│  │   │   │   ├── linear_regression.py
│  │   │   │   ├── multiple_regression.py
│  │   │   │   └── Docs/
│  │   │   ├── dispersion/
│  │   │   │   ├── __init__.py
│  │   │   │   ├── range.py
│  │   │   │   ├── variance.py
│  │   │   │   ├── standard_deviation.py
│  │   │   │   ├── interquartile_range.py
│  │   │   │   └── Docs/
│  │   ├── Algebra/
│  │   │   ├── __init__.py
│  │   │   ├── basic_operations.py
│  │   │   ├── equations.py
│  │   │   ├── factoring.py
│  │   │   ├── functions.py
│  │   │   ├── inequalities.py
│  │   │   ├── systems_of_equations.py
│  │   │   └── Docs/
│  │   ├── Geometry/
│  │   │   ├── __init__.py
│  │   │   ├── area.py
│  │   │   ├── perimeter.py
│  │   │   ├── surface_area.py
│  │   │   ├── volume.py
│  │   │   ├── coordinate_geometry.py
│  │   │   ├── trigonometry.py
│  │   │   └── Docs/
│  │   ├── Trigonometry/
│  │   │   ├── __init__.py
│  │   │   ├── identities.py
│  │   │   ├── inverse_trig_functions.py
│  │   │   ├── right_triangle_trig.py
│  │   │   ├── trig_equations.py
│  │   │   ├── unit_circle.py
│  │   │   └── Docs/
│  │   ├── Calculus/
│  │   │   ├── __init__.py
│  │   │   ├── limits.py
│  │   │   ├── derivatives.py
│  │   │   ├── integrals.py
│  │   │   ├── differential_equations.py
│  │   │   ├── multivariable_calculus.py
│  │   │   └── Docs/
│  │   ├── Linear_algebra_ops/
│  │   │   ├── __init__.py
│  │   │   ├── determinants.py
│  │   │   ├── eigenvalues.py
│  │   │   ├── eigenvectors.py
│  │   │   ├── matrix_operations.py
│  │   │   ├── vector_operations.py
│  │   │   ├── linear_transformations.py
│  │   │   └── Docs/
│  ├── Number_theory_calculations/
│  │   ├── __init__.py
│  │   ├── primes.py
│  │   ├── factorization.py
│  │   ├── gcd_and_lcm.py
│  │   ├── modular_arithmetic.py
│  │   ├── diophantine_equations.py
│  │   ├── congruences.py
│  │   ├── continued_fractions.py
│  │   └── Docs/
│  ├── extras/
│  │   ├── __init__.py
│  │   ├── confidence_intervals.py
│  │   ├── goodness_of_fit_tests.py
│  │   ├── hypothesis_testing.py
│  │   ├── non_parametric_tests.py
│  │   ├── regression_analysis.py
│  │   ├── sampling.py
│  │   ├── statistical_inference.py
│  │   ├── time_series_analysis.py
│  │   └── Docs/
│  ├── tests/
│  │   ├── __init__.py
│  │   ├── test_probability_and_statistics.py
│  │   ├── test_algebra.py
│  │   ├── test_geometry.py
│  │   ├── test_trigonometry.py
│  │   ├── test_calculus.py
│  │   ├── test_linear_algebra_ops.py
│  │   ├── test_number_theory_calculations.py
│  │   └── Docs/
├── Docs/
│   ├── Requirements.txt
│   ├── README.md