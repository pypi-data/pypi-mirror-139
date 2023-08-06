"""Top-level package for relionai."""

__author__ = """Mo Messidi"""
__email__ = 'messidi.mo@gmail.com'
__version__ = '0.1.0'


from relionai.tabular_classification.evaluation import (  # NOQA
    run_all_tests,
)

from relionai.tabular_classification.monitoring import (  # NOQA
    MonitoringSession,
)

from relionai.timeseries_regression.evaluation import (  # NOQA
    timeseries_initialize,
    timeseries_evaluate,
)

from relionai.timeseries_regression.monitoring import (  # NOQA
    MonitoringSession,
)

