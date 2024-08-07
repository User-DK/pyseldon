import pyseldon
import pytest


def test_degroot_settings():
    settings = pyseldon.seldoncore.DeGrootSettings()
    assert settings.max_iterations == None
    assert settings.convergence_tol == 1e-6

    # set values
    settings.max_iterations = 100
    settings.convergence_tol = 1e-5

    # check values
    assert settings.max_iterations == 100
    assert settings.convergence_tol == 1e-5
