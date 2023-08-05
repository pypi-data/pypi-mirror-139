# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Utilities for testing."""


import logging

import dataclasses
import jax
from jax import jit
from jax import vmap
from jax.lib import xla_bridge
import jax.numpy as np
import jax.test_util as jtu
import numpy as onp


def _jit_vmap(f):
  return jit(vmap(f))


def update_test_tolerance(f32_tol=5e-3, f64_tol=1e-5):
  jtu._default_tolerance[onp.dtype(onp.float32)] = f32_tol
  jtu._default_tolerance[onp.dtype(onp.float64)] = f64_tol
  def default_tolerance():
    if jtu.device_under_test() != 'tpu':
      return jtu._default_tolerance
    tol = jtu._default_tolerance.copy()
    tol[onp.dtype(onp.float32)] = 5e-2
    return tol
  # TODO(schsam): don't use JAX test_utils.
  jax._src.test_util.default_tolerance = default_tolerance
  jtu.default_tolerance = default_tolerance


def stub_out_pmap(batch, count):
  # If we are using GPU or CPU stub out pmap with vmap to simulate multi-core.
  if count > 0:

    class xla_bridge_stub(object):

      def device_count(self):
        return count

    platform = xla_bridge.get_backend().platform
    if platform == 'gpu' or platform == 'cpu':
      batch.pmap = _jit_vmap
      batch.xla_bridge = xla_bridge_stub()


def _log(relative_error, absolute_error, expected, actual, did_pass):
  msg = 'PASSED' if did_pass else 'FAILED'
  logging.info(f'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX\n'
               f'\n{msg} with {relative_error} relative error \n'
               f'and {absolute_error} absolute error: \n'
               f'---------------------------------------------\n'
               f'EXPECTED: \n'
               f'{expected}\n'
               f'---------------------------------------------\n'
               f'ACTUAL: \n'
               f'{actual}\n'
               f'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX\n'
               )


def assert_close_matrices(self, expected, actual, rtol, atol=0.1):
  def assert_close(expected, actual):
    self.assertEqual(expected.shape, actual.shape)
    relative_error = (
        np.linalg.norm(actual - expected) /
        np.maximum(np.linalg.norm(expected), 1e-12))

    absolute_error = np.mean(np.abs(actual - expected))

    if np.isnan(relative_error) or relative_error > rtol or absolute_error > atol:
      _log(relative_error, absolute_error, expected, actual, False)
      self.fail(self.failureException('Relative ERROR: ',
                                      float(relative_error),
                                      'EXPECTED:' + ' ' * 50,
                                      expected,
                                      'ACTUAL:' + ' ' * 50,
                                      actual,
                                      ' ' * 50,
                                      'Absolute ERROR: ',
                                      float(absolute_error)))
    else:
      _log(relative_error, absolute_error, expected, actual, True)

  jax.tree_map(assert_close, expected, actual)


class NeuralTangentsTestCase(jtu.JaxTestCase):

  def assertAllClose(
      self,
      x,
      y,
      *,
      check_dtypes=True,
      atol=None,
      rtol=None,
      canonicalize_dtypes=True,
      err_msg='',
  ):
    def is_finite(x):
      self.assertTrue(np.all(np.isfinite(x)))

    jax.tree_map(is_finite, x)
    jax.tree_map(is_finite, y)

    def assert_close(x, y):
      super(NeuralTangentsTestCase, self).assertAllClose(
          x, y,
          check_dtypes=check_dtypes,
          atol=atol,
          rtol=rtol,
          canonicalize_dtypes=canonicalize_dtypes,
          err_msg=err_msg,
      )

    if dataclasses.is_dataclass(x):
      self.assertIs(type(y), type(x))
      for field in dataclasses.fields(x):
        key = field.name
        x_value, y_value = getattr(x, key), getattr(y, key)
        is_pytree_node = field.metadata.get('pytree_node', True)
        if is_pytree_node:
          assert_close(x_value, y_value)
        else:
          self.assertEqual(x_value, y_value, key)
    else:
      assert_close(x, y)
