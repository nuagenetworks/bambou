Version 0.0.2
-------------

* Connection provides a read-only attribute `request`.
* `BambouHTTPError` returns connection that contains both the `request` and the `response` objects.
* Expose `BambouConfig` which enable to use `set_should_raise_bambou_http_error`