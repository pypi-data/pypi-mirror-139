#  Copyright 2020 Rikai Authors
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

"""Rikai Feature Store
"""
from rikai.conf import *
from rikai.spark.sql.codegen import mlflow_logger as mlflow

from .__version__ import version

__all__ = [
    "get_option",
    "mlflow",
    "options",
    "option_context",
    "reset_option",
    "set_option",
    "version",
]
