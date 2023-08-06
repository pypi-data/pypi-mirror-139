import numpy as np
import typing
import warnings


class BootstrapTestError(RuntimeError):
    """
    Reference value falls outside bootstrapped confidence interval.
    """
    def __init__(self, result: dict):
        self.result = result
        message = f'the reference value {result["reference"]} lies outside the 1 - (alpha = ' \
            f'{result["alpha"]}) interval [{result["lower"]}, {result["upper"]}]'
        super().__init__(message)


def bootstrap_test(samples: np.ndarray, statistic: typing.Callable, reference: float,
                   statistic_args: typing.Iterable = None, statistic_kwargs: typing.Mapping = None,
                   num_bootstrap_samples: int = 1000, alpha: float = 1e-2,
                   multiple_hypothesis_correction: str = 'bonferroni', rtol: float = 1e-7,
                   atol: float = 0) -> dict:
    """
    Compare a bootstrap sample of a :attr:`statistic` evaluated on i.i.d :attr:`samples` from a
    stochastic process with a :attr:`reference` value.

    The test will fail if the :attr:`reference` lies outside the :code:`1 - alpha` posterior
    interval, i.e. is smaller than the empirical :code:`alpha / 2` quantile or larger than the
    :code:`1 - alpha / 2` quantile. The relative :attr:`rtol` and absolute tolerance :attr:`atol`
    are added together to obtain an overall tolerance :code:`atol + rtol * abs(reference)` for the
    interval test (see :func:`numpy.isclose` for further details).

    Args:
        samples: I.i.d. samples from a stochastic process on which to evaluate the
            :attr:`statistic`.
        statistic: Function to evaluate a statistic on a bootstrapped sample.
        reference: Reference value to compare with the bootstrap sample of the :attr:`statistic`.
        statistic_args: Positional arguments forwarded to the :attr:`statistic`.
        statistic_kwargs: Keyword arguments forwarded to the :attr:`statistic`.
        num_bootstrap_samples: Number of bootstrap samples.
        alpha: Significance level to use for testing agreement between the bootstrapped distribution
            of the :attr:`statistic` and the :attr:`reference` value. :attr:`alpha` roughly
            corresponds to the probability that the test will fail even if the :attr:`reference`
            value is correct. This value should be small for the test to pass with high probability.
        multiple_hypothesis_correction: Method used to correct for multiple hypotheses being tested
            if the statistic is vector-valued. :code:`False` disables multiple hypothesis
            correction.
        rtol: Relative tolerance.
        atol: Absolute tolerance.

    Returns:
        result: Dictionary of test information, comprising

            - :attr:`alpha_corrected` -- Significance level after multiple hypothesis correction.
              Equal to :attr:`alpha` if the statistic is a scalar or no multiple hypothesis
              correction is applied.
            - :attr:`lower` -- Lower limit of the :code:`1 - alpha` bootstrapped interval, i.e. the
              :code:`alpha / 2` quantile.
            - :attr:`upper` -- Upper limit of the :code:`1 - alpha` bootstrapped interval, i.e. the
              :code:`1 - alpha / 2` quantile.
            - :attr:`iqr` -- Interquartile range of the bootstrapped :attr:`statistic`.
            - :attr:`median` -- Median of the bootstrapped :attr:`statistic`.
            - :attr:`z_score` -- Z-score of the :attr:`reference` value under the bootstrapped
              distribution, i.e. :code:`(reference - mean(s)) / std(s)`, where :attr:`s` is the
              vector of bootstrapped :attr:`statistic`.

    """
    statistic_args = statistic_args or ()
    statistic_kwargs = statistic_kwargs or {}

    # Evaluate the bootstrapped statistics.
    samples = np.asarray(samples)
    statistics = []
    for _ in range(num_bootstrap_samples):
        idx = np.random.choice(samples.shape[0], samples.shape[0])
        bootstrap_sample = samples[idx]
        statistics.append(statistic(bootstrap_sample, *statistic_args, **statistic_kwargs))
    statistics = np.asarray(statistics)

    # Sanity check for the dimensionality of the statistic and apply multiple hypothesis correction.
    alpha_corrected = alpha
    if statistics.ndim > 2:
        raise ValueError('only scalar and vector statistics are supported, not statistics with '
                         f'{statistics.ndim - 1} dimensions')
    elif statistics.ndim == 2:
        if multiple_hypothesis_correction == 'bonferroni':
            alpha_corrected = alpha / statistics.shape[1]
        elif multiple_hypothesis_correction:
            raise NotImplementedError('multiple hypothesis correction '
                                      f'`{multiple_hypothesis_correction} is not supported')

    if alpha_corrected < 1 / num_bootstrap_samples:
        warnings.warn('cannot estimate tail probabilities smaller than `1 / (num_bootstrap_samples '
                      f'= {num_bootstrap_samples})', UserWarning)

    # Evaluate the interval.
    quantiles = [100 * alpha_corrected / 2, 100 * (1 - alpha_corrected / 2)]
    lower, upper = np.percentile(statistics, quantiles, axis=0)

    # Collect summary information.
    tol = atol + rtol * np.abs(reference)
    result = {
        'alpha': alpha,
        'alpha_corrected': alpha,
        'reference': reference,
        'lower': lower,
        'upper': upper,
        'z_score': (reference - np.mean(statistics)) / np.std(statistics),
        'median': np.median(statistics),
        'iqr': np.diff(np.percentile(statistics, [25, 75])).squeeze(),
        'tol': tol,
    }

    # Fail the test if the reference value lies outside the interval.
    if np.any(reference < lower - tol) or np.any(reference > upper + tol):
        raise BootstrapTestError(result)
    result['statistics'] = statistics
    return result
