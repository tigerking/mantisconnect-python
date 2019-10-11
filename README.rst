1. Update to support mantisbt 2.x version
2. support more features ,eg add issue etc


mantisconnect-python2
=======================

Python client for Mantis Connect SOAP API

 - It is good to request issue data on a filter basis.
 - You can use extended fields as well as custom fields.
 - Offers simple interface.

Usage
-----------------------
See sample/sample.py

::

    mc = MantisSoapConnector("url")
    mc.set_user_passwd("username", "password")
    mc.connect()

    p = SimpleProject(mc, "your project name")
    filter_name = "your filter name"
    issue_list = p.request_filter_all_issues(filter_name)


Install
-----------------------
Requirement
 - python > 3.5
 - zeep

::

    $ pip3 install mantisconnect


Test version
 - mantis 1.2.11
