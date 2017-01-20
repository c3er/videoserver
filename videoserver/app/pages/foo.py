#!/usr/bin/env python
# -*- coding: utf-8 -*-


import flask

import app


template = '''\
{% extends "layout.html" %}

{% block content %}

<h1>{{ message }}</h1>

{% endblock %}
'''


@app.servicehandler(app.services.foo)
def func():
    return flask.render_template_string(
        template,
        title="Foo bar",
        message = "Hello world!"
    )
