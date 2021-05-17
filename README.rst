quic_stego
=======

|rtd| |pypi-v| |pypi-pyversions| |pypi-l| |tests| |codecov| |black|

.. |rtd| image:: https://readthedocs.org/projects/aioquic/badge/?version=latest
    :target: https://aioquic.readthedocs.io/

.. |pypi-v| image:: https://img.shields.io/pypi/v/aioquic.svg
    :target: https://pypi.python.org/pypi/aioquic

.. |pypi-pyversions| image:: https://img.shields.io/pypi/pyversions/aioquic.svg
    :target: https://pypi.python.org/pypi/aioquic

.. |pypi-l| image:: https://img.shields.io/pypi/l/aioquic.svg
    :target: https://pypi.python.org/pypi/aioquic

.. |tests| image:: https://github.com/aiortc/aioquic/workflows/tests/badge.svg
    :target: https://github.com/aiortc/aioquic/actions

.. |codecov| image:: https://img.shields.io/codecov/c/github/aiortc/aioquic.svg
    :target: https://codecov.io/gh/aiortc/aioquic

.. |black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/python/black


A stegnographic tool PoC based on QUIC and HTTP/3. This tool hide a message into a image and send it by QUIC protocol.
The tool has two parts:

* Stego part: where the tool hide the message into the image

* QUIC part: send that secret image

What is aioquic?
--------------------

``aioquic`` is a library for the QUIC network protocol in Python. It features
a minimal TLS 1.3 implementation, a QUIC stack and an HTTP/3 stack.

QUIC standardisation is not finalised yet, but ``aioquic`` closely tracks the
specification drafts and is regularly tested for interoperability against other
`QUIC implementations`_.

To learn more about ``aioquic`` please `read the documentation`_.


Stegnographic tool implementation execution.
----------------------------------------------

There are specifically two modules that are introduced as a part of this two:

1. The stegnographic module that hides a secret string into an image.
2. The Network module based on HTTP/3 and QUIC.


To actually run the whole pipeline, we have introduced a bash script that encoded the string into the image and send the image to the client and does the communication.


To hide the file.txt into template.png and invoke the server to upload the secret image (or icon.png):

.. code-block:: console

   $ bash quic_stego.sh -i resources/template.png -s resources/file.txt

To invoke the client and download the icon.png. Extract the secret message from icon.png. The result would be in the path result_resources/secretXX.txt:

.. code-block:: console

   $ sh quic_stego.sh -E


You could invoke each part individually to test different properties offered by them:

To invoke the network modules client and server, you could do:

The client:

.. code-block:: console

    $ python examples/http3_client.py --ca-certs tests/pycacert.pem https://localhost:4433/secret --output-dir=result_resources/

The server:

.. code-block:: console

   $ python examples/http3_server.py --certificate tests/ssl_cert.pem --private-key tests/ssl_key.pem -v

Inorder to invoke the stegnographic module:

To encrypt the text in the file:

.. code-block:: console

   $ python3 Stego.py -i resources/template.png -s resources/file.txt

To decrypt the image with the secret text attached:

.. code-block:: console

   $ python3 Stego.py -E -i result_resources/secretimage.png


