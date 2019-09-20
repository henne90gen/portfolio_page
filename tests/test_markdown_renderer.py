from typing import List

from flask import Flask

from portfolio_page.markdown_renderer import render_markdown


def test_can_render_images(app: Flask):
    line = "![My Text](http://test.com/image.png)"
    with app.app_context():
        result = render_markdown([line])
        assert result == "<img src=\"http://test.com/image.png\" title=\"My Text\"/>"


def test_can_render_multiple_images_per_line(app: Flask):
    line = "![My Text 1](http://test.com/image1.png) ![My Text 2](http://test.com/image2.png)"
    with app.app_context():
        result = render_markdown([line])
        assert result == "<img src=\"http://test.com/image1.png\" title=\"My Text 1\"/> <img src=\"http://test.com/image2.png\" title=\"My Text 2\"/>"


def test_can_render_links(app: Flask):
    line = "[My Link](http://test.com/link)"
    with app.app_context():
        result = render_markdown([line])
        assert result == "<a href=\"http://test.com/link\">My Link</a>"


def test_can_render_multiple_links_per_line(app: Flask):
    line = "[My Link 1](http://test.com/link1) [My Link 2](http://test.com/link2)"
    with app.app_context():
        result = render_markdown([line])
        assert result == "<a href=\"http://test.com/link1\">My Link 1</a> <a href=\"http://test.com/link2\">My Link 2</a>"


def test_can_render_image_and_links(app: Flask):
    line = "[My Link](http://test.com/link) ![My Text](http://test.com/image.png)"
    with app.app_context():
        result = render_markdown([line])
        assert result == "<a href=\"http://test.com/link\">My Link</a> <img src=\"http://test.com/image.png\" title=\"My Text\"/>"


def test_can_render_headings(app: Flask):
    for index in range(1, 6):
        line = ("#" * index) + " Title"
        with app.app_context():
            result = render_markdown([line])
            assert result == f"<h{index} id=\"title\">Title<a class=\"headerlink\" href=\"#title\" title=\"Permalink to this headline\">¶</a></h{index}>"

def test_can_render_headings_with_spaces(app: Flask):
    for index in range(1, 6):
        line = ("#" * index) + " Title with Spaces"
        with app.app_context():
            result = render_markdown([line])
            assert result == f"<h{index} id=\"title-with-spaces\">Title with Spaces<a class=\"headerlink\" href=\"#title-with-spaces\" title=\"Permalink to this headline\">¶</a></h{index}>"
