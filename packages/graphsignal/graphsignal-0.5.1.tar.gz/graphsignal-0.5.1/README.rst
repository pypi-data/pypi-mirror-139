Graphsignal Profiler
====================

|License| |Version| |Downloads| |SaaS Status|

Overview
--------

Graphsignal is a machine learning profiler. It helps data scientists and
ML engineers make model training and inference faster and more
efficient. Learn more at `graphsignal.com <https://graphsignal.com>`__.

Machine Learning Profiling
~~~~~~~~~~~~~~~~~~~~~~~~~~

-  **Training and inference profiling** Graphsignal provides operation
   and kernel level statistics about machine learning runs,
   e.g. training steps or prediction calls, to enable optimization and
   tuning.

-  **Integration and support** Add a few lines of code to automatically
   profile TensorFlow and PyTorch jobs and model serving automatically.

-  **Any environment** The profiler only needs outbound connection to
   Graphsignal. No inbound ports or additional software is required,
   allowing it run everywhere.

-  **Data privacy** No code or data is sent to Graphsignal cloud, only
   run statistics and metadata.

Profile dashboard
~~~~~~~~~~~~~~~~~

|Data Analysis|

Documentation
-------------

See full documentation at
`graphsignal.com/docs <https://graphsignal.com/docs/>`__.

Getting Started
---------------

1. Installation
~~~~~~~~~~~~~~~

Install the profiler by running:

::

   pip install graphsignal

Or clone and install the `GitHub
repository <https://github.com/graphsignal/graphsignal>`__:

::

   git clone https://github.com/graphsignal/graphsignal.git
   python setup.py install

Import the module in your application:

.. code:: python

   import graphsignal

For GPU profiling, make sure the `NVIDIA® CUDA® Profiling Tools
Interface <https://developer.nvidia.com/cupti>`__ (CUPTI) is installed
by running:

.. code:: console

   /sbin/ldconfig -p | grep libcupti

2. Configuration
~~~~~~~~~~~~~~~~

Configure the profiler by specifying your API key.

.. code:: python

   graphsignal.configure(api_key='my_api_key', workload_name='job1')

To get an API key, sign up for a free account at
`graphsignal.com <https://graphsignal.com>`__. The key can then be found
in your account’s `Settings / API
Keys <https://app.graphsignal.com/settings/api_keys>`__ page.

``workload_name`` identifies the job, application or service that is
being profiled.

3. Profiling
~~~~~~~~~~~~

To profile TensorFlow or PyTorch, add the following code around a code
span, e.g. training step/batch or a prediction call. Only some spans
will be profiled; the profiler decides which spans to profile for
optimal statistics and low overhead. To ensure a profile for the current
span, ``ensure_profile=True`` argument can be provided. See `profiling
API reference <https://graphsignal.com/docs/profiler/api-reference/>`__
for full documentation.

Profile TensorFlow:

.. code:: python

   span = graphsignal.profile_span_tf()
       # training step, prediction call, etc.
   span.stop()

Profile TensorFlow using ``with`` context manager:

.. code:: python

   with graphsignal.profile_span_tf() as span:
       # training step, prediction call, etc.

Profile Keras training or inference using a callback:

.. code:: python

   from graphsignal.callbacks.keras import GraphsignalCallback
   ...
   model.fit(..., callbacks=[GraphsignalCallback()])
   # or model.predict(..., callbacks=[GraphsignalCallback()])

Profile PyTorch:

.. code:: python

   span = graphsignal.profile_span_pt()
       # training step, prediction call, etc.
   span.stop()

Profile PyTorch using ``with`` context manager:

.. code:: python

   with graphsignal.profile_span_pt() as span:
       # training step, prediction call, etc.

Profile Hugging Face training using a callback:

.. code:: python

   from graphsignal.callbacks.huggingface import GraphsignalPTCallback
   # or GraphsignalTFCallback for TensorFlow
   ...
   trainer = Trainer(..., callbacks=[GraphsignalPTCallback()])
   # or trainer.add_callback(GraphsignalPTCallback())

Optionally record metadata in the profile:

.. code:: python

   span.add_metadata('key1', 'value1')

4. Dashboards
~~~~~~~~~~~~~

After profiling is setup, `sign
in <https://app.graphsignal.com/signin>`__ to Graphsignal to analyze
recorded profiles.

Examples
--------

Model training
~~~~~~~~~~~~~~

.. code:: python

   import torch

   import graphsignal
   graphsignal.configure(api_key='my_key', workload_name='training_example')

   x = torch.arange(-5, 5, 0.1).view(-1, 1)
   y = -5 * x + 0.1 * torch.randn(x.size())

   model = torch.nn.Linear(1, 1)
   criterion = torch.nn.MSELoss()
   optimizer = torch.optim.SGD(model.parameters(), lr = 0.1)

   for epoch in range(10):
       with graphsignal.profile_span_pt():
           y1 = model(x)
           loss = criterion(y1, y)
           optimizer.zero_grad()
           loss.backward()
           optimizer.step()

Model serving
~~~~~~~~~~~~~

.. code:: python

   from tensorflow import keras
   import json
   from flask import Flask, request

   import graphsignal
   graphsignal.configure(api_key='my_key', workload_name='fraud_detection_prod')

   model = keras.models.load_model('fraud_model.h5')
   app = Flask(__name__)

   @app.route('/predict_fraud', methods = ['POST'])
   def predict_digit():
       input_data = request.get_json()

       with graphsignal.profile_span_tf():
         output_data = model.predict([input_data])

       return json.dumps(output_data.tolist())

   app.run(port=8090)

Overhead
--------

Although profiling may add some overhead to applications, Graphsignal
Profiler only profiles certain spans, e.g. training batches or
prediction calls, automatically limiting the overhead.

Security and Privacy
--------------------

Graphsignal Profiler can only open outbound connections to
``profile-api.graphsignal.com`` and send data, no inbound connections or
commands are possible.

No code or data is sent to Graphsignal cloud, only run statistics and
metadata.

Troubleshooting
---------------

To enable debug logging, add ``debug_mode=True`` to ``configure()``. If
the debug log doesn’t give you any hints on how to fix a problem, please
report it to our support team via your account.

In case of connection issues, please make sure outgoing connections to
``https://profile-api.graphsignal.com`` are allowed.

.. |License| image:: http://img.shields.io/github/license/graphsignal/graphsignal
   :target: https://github.com/graphsignal/graphsignal/blob/main/LICENSE
.. |Version| image:: https://img.shields.io/github/v/tag/graphsignal/graphsignal?label=version
   :target: https://github.com/graphsignal/graphsignal
.. |Downloads| image:: https://pepy.tech/badge/graphsignal
   :target: https://pepy.tech/project/graphsignal
.. |SaaS Status| image:: https://img.shields.io/uptimerobot/status/m787882560-d6b932eb0068e8e4ade7f40c?label=SaaS%20status
   :target: https://stats.uptimerobot.com/gMBNpCqqqJ
.. |Data Analysis| image:: https://graphsignal.com/external/profile-dashboard.png
   :target: https://graphsignal.com
