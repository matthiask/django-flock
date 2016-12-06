==========
Change log
==========

`Next version`_
~~~~~~~~~~~~~~~

- Added this CHANGELOG.
- Allow overriding the project on the donation amount page by appending
  ``?project=42``.


`0.3`_ (2016-11-11)
~~~~~~~~~~~~~~~~~~~

- django-mooch_'s ``post_charge`` signals' senders are instances now, not
  classes.


`0.2`_ (2016-11-09)
~~~~~~~~~~~~~~~~~~~

- Do not send mails if moochers belonging to other projects are charged.


`0.1`_ (2016-10-05)
~~~~~~~~~~~~~~~~~~~

- Initial release.


.. _0.1: https://github.com/matthiask/django-flock/commit/08e172dfb658
.. _0.2: https://github.com/matthiask/django-flock/compare/0.1...0.2
.. _Next version: https://github.com/matthiask/django-flock/compare/0.2...master

.. _django-mooch: https://github.com/matthiask/django-mooch/
