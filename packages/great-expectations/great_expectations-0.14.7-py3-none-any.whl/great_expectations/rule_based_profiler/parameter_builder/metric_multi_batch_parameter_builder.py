from typing import Any, Dict, List, Optional, Union

import numpy as np

import great_expectations.exceptions as ge_exceptions
from great_expectations.core.batch import BatchRequest, RuntimeBatchRequest
from great_expectations.rule_based_profiler.parameter_builder.parameter_builder import (
    MetricComputationDetails,
    MetricComputationResult,
    ParameterBuilder,
)
from great_expectations.rule_based_profiler.types import (
    Domain,
    ParameterContainer,
    build_parameter_container,
)
from great_expectations.rule_based_profiler.util import (
    get_parameter_value_and_validate_return_type,
)
from great_expectations.validator.validator import Validator


class MetricMultiBatchParameterBuilder(ParameterBuilder):
    """
    A Single/Multi-Batch implementation for obtaining a resolved (evaluated) metric, using domain_kwargs, value_kwargs,
    and metric_name as arguments.
    """

    def __init__(
        self,
        name: str,
        metric_name: str,
        metric_domain_kwargs: Optional[Union[str, dict]] = None,
        metric_value_kwargs: Optional[Union[str, dict]] = None,
        enforce_numeric_metric: Union[str, bool] = False,
        replace_nan_with_zero: Union[str, bool] = False,
        reduce_scalar_metric: Union[str, bool] = True,
        data_context: Optional["DataContext"] = None,  # noqa: F821
        batch_request: Optional[Union[BatchRequest, RuntimeBatchRequest, dict]] = None,
    ):
        """
        Args:
            name: the name of this parameter -- this is user-specified parameter name (from configuration);
            it is not the fully-qualified parameter name; a fully-qualified parameter name must start with "$parameter."
            and may contain one or more subsequent parts (e.g., "$parameter.<my_param_from_config>.<metric_name>").
            metric_name: the name of a metric used in MetricConfiguration (must be a supported and registered metric)
            metric_domain_kwargs: used in MetricConfiguration
            metric_value_kwargs: used in MetricConfiguration
            enforce_numeric_metric: used in MetricConfiguration to insure that metric computations return numeric values
            replace_nan_with_zero: if False (default), then if the computed metric gives NaN, then exception is raised;
            otherwise, if True, then if the computed metric gives NaN, then it is converted to the 0.0 (float) value.
            reduce_scalar_metric: if True (default), then reduces computation of 1-dimensional metric to scalar value.
            data_context: DataContext
            batch_request: specified in ParameterBuilder configuration to get Batch objects for parameter computation.
        """
        super().__init__(
            name=name,
            data_context=data_context,
            batch_request=batch_request,
        )

        self._metric_name = metric_name
        self._metric_domain_kwargs = metric_domain_kwargs
        self._metric_value_kwargs = metric_value_kwargs

        self._enforce_numeric_metric = enforce_numeric_metric
        self._replace_nan_with_zero = replace_nan_with_zero

        self._reduce_scalar_metric = reduce_scalar_metric

    @property
    def metric_name(self) -> str:
        return self._metric_name

    @property
    def metric_domain_kwargs(self) -> Optional[Union[str, dict]]:
        return self._metric_domain_kwargs

    @property
    def metric_value_kwargs(self) -> Optional[Union[str, dict]]:
        return self._metric_value_kwargs

    @property
    def enforce_numeric_metric(self) -> Union[str, bool]:
        return self._enforce_numeric_metric

    @property
    def replace_nan_with_zero(self) -> Union[str, bool]:
        return self._replace_nan_with_zero

    @property
    def reduce_scalar_metric(self) -> Union[str, bool]:
        return self._reduce_scalar_metric

    def _build_parameters(
        self,
        parameter_container: ParameterContainer,
        domain: Domain,
        variables: Optional[ParameterContainer] = None,
        parameters: Optional[Dict[str, ParameterContainer]] = None,
    ):
        """
        Builds ParameterContainer object that holds ParameterNode objects with attribute name-value pairs and optional
        details.

        :return: ParameterContainer object that holds ParameterNode objects with attribute name-value pairs and
        ptional details
        """
        validator: Validator = self.get_validator(
            domain=domain,
            variables=variables,
            parameters=parameters,
        )

        batch_ids: Optional[List[str]] = self.get_batch_ids(
            domain=domain,
            variables=variables,
            parameters=parameters,
        )
        if not batch_ids:
            raise ge_exceptions.ProfilerExecutionError(
                message=f"Utilizing a {self.__class__.__name__} requires a non-empty list of batch identifiers."
            )

        metric_computation_result: MetricComputationResult = self.get_metrics(
            batch_ids=batch_ids,
            validator=validator,
            metric_name=self._metric_name,
            metric_domain_kwargs=self._metric_domain_kwargs,
            metric_value_kwargs=self._metric_value_kwargs,
            enforce_numeric_metric=self._enforce_numeric_metric,
            replace_nan_with_zero=self._replace_nan_with_zero,
            domain=domain,
            variables=variables,
            parameters=parameters,
        )
        metric_values: np.ndarray = metric_computation_result.metric_values
        details: MetricComputationDetails = metric_computation_result.details

        # Obtain reduce_scalar_metric from "rule state" (i.e., variables and parameters); from instance variable otherwise.
        reduce_scalar_metric: bool = get_parameter_value_and_validate_return_type(
            domain=domain,
            parameter_reference=self._reduce_scalar_metric,
            expected_return_type=bool,
            variables=variables,
            parameters=parameters,
        )

        if reduce_scalar_metric and metric_values.shape[0] == 1:
            metric_values = metric_values[:, 0]

        parameter_values: Dict[str, Any] = {
            f"$parameter.{self.name}": {
                "value": metric_values,
                "details": details,
            },
        }

        build_parameter_container(
            parameter_container=parameter_container, parameter_values=parameter_values
        )
