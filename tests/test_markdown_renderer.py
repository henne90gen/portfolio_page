import pytest
from flask import Flask

import portfolio_page
from portfolio_page.markdown_renderer import render_relative_images, render_relative_links, render_heading, render_tree, \
    build_tree, Node, add_css_class, render_short_description, render_code


def render_simple_heading(line: str) -> str:
    if not line.startswith('#'):
        return line

    heading_num = line.find(" ")
    heading_text = line[heading_num + 1:]
    return f"<h{heading_num}>{heading_text}</h{heading_num}>"


def test_add_css_class():
    lines = ["<p>", "</p>", "<project>"]
    expected = ["<p class=\"my-class\">", "</p>", "<project>"]
    actual = list(map(add_css_class("p", "my-class"), lines))
    assert len(actual) == len(expected)
    for actual_line, expected_line in zip(actual, expected):
        assert actual_line == expected_line


def test_can_render_short_description(app: Flask):
    lines = [
        "[![Build Status](https://travis-ci.org/henne90gen/pixel_sorting.svg?branch=master)](https://travis-ci.org/henne90gen/pixel_sorting)",
        "[![Coverage Status](https://coveralls.io/repos/github/henne90gen/pixel_sorting/badge.svg?branch=master)](https://coveralls.io/github/henne90gen/pixel_sorting?branch=master)"
    ]
    expected = """<div class="card-content">
  <a href="https://travis-ci.org/henne90gen/pixel_sorting"><img src="https://travis-ci.org/henne90gen/pixel_sorting.svg?branch=master" title="Build Status"/></a><br/>
  <a href="https://coveralls.io/github/henne90gen/pixel_sorting?branch=master"><img src="https://coveralls.io/repos/github/henne90gen/pixel_sorting/badge.svg?branch=master" title="Coverage Status"/></a><br/>
</div>"""

    with app.app_context():
        actual = str(render_short_description(lines, ""))
    assert actual == expected


def test_can_render_short_description_with_code(app: Flask):
    lines = [
        "```bash",
        "make install",
        "```"
    ]
    expected = """<div class="card-content">
  <div class="code-block">
  make install<br/>
  </div>
</div>"""

    with app.app_context():
        actual = str(render_short_description(lines, ""))
    assert actual == expected


def test_can_render_images(app: Flask):
    line = "![My Text](http://test.com/image.png)"
    with app.app_context():
        result = render_relative_images("project")(line)
        assert result == "<img src=\"http://test.com/image.png\" title=\"My Text\"/>"


def test_can_render_multiple_images_per_line(app: Flask):
    line = "![My Text 1](http://test.com/image1.png) ![My Text 2](http://test.com/image2.png)"
    with app.app_context():
        result = render_relative_images("project")(line)
        assert result == "<img src=\"http://test.com/image1.png\" title=\"My Text 1\"/> <img src=\"http://test.com/image2.png\" title=\"My Text 2\"/>"


def test_can_render_links(app: Flask):
    line = "[My Link](http://test.com/link)"
    with app.app_context():
        result = render_relative_links("project")(line)
        assert result == "<a href=\"http://test.com/link\">My Link</a>"


def test_can_render_multiple_links_per_line(app: Flask):
    line = "[My Link 1](http://test.com/link1) [My Link 2](http://test.com/link2)"
    with app.app_context():
        result = render_relative_links("project")(line)
        assert result == "<a href=\"http://test.com/link1\">My Link 1</a> <a href=\"http://test.com/link2\">My Link 2</a>"


def test_can_render_image_and_links(app: Flask):
    line = "[My Link](http://test.com/link) ![My Text](http://test.com/image.png)"
    with app.app_context():
        result = render_relative_images("project")(line)
        result = render_relative_links("project")(result)
        assert result == "<a href=\"http://test.com/link\">My Link</a> <img src=\"http://test.com/image.png\" title=\"My Text\"/>"

        pytest.skip("images and links cannot be rendered in arbitrary order yet")
        result = render_relative_links("project")(line)
        result = render_relative_images("project")(result)
        assert result == "<a href=\"http://test.com/link\">My Link</a> <img src=\"http://test.com/image.png\" title=\"My Text\"/>"


def test_can_render_headings(app: Flask):
    for index in range(1, 6):
        line = ("#" * index) + " Title"
        result = render_heading(line)
        assert result == f"<h{index} id=\"title\">Title<a class=\"headerlink\" href=\"#title\" title=\"Permalink to this headline\">¶</a></h{index}>"


def test_can_render_headings_with_spaces():
    for index in range(1, 6):
        line = ("#" * index) + " Title with Spaces"
        result = render_heading(line)
        assert result == f"<h{index} id=\"title-with-spaces\">Title with Spaces<a class=\"headerlink\" href=\"#title-with-spaces\" title=\"Permalink to this headline\">¶</a></h{index}>"


def test_can_render_code_blocks():
    lines = ["```bash", "make install", "```"]
    expected = ["<div class=\"code-block\">", "make install<br/>", "</div>"]
    actual = render_code(lines, 0)
    assert len(actual) == len(expected)
    for a, e in zip(actual, expected):
        assert a == e


def compare_trees(expected: Node, actual: Node):
    assert expected.content == actual.content
    assert len(expected.children) == len(actual.children)
    for expected_child, actual_child in zip(expected.children, actual.children):
        compare_trees(expected_child, actual_child)


def test_can_build_simple_tree():
    text = """# Title

## Title 1

### Title 1.1

### Title 1.2

## Title 2

## Title 3
"""
    root = build_tree(text.split('\n'))
    expected_root = Node(
        [], [
            Node(["# Title"], [
                Node(),
                Node(["## Title 1"], [
                    Node(),
                    Node(["### Title 1.1"], [Node()]),
                    Node(["### Title 1.2"], [Node()])
                ]),
                Node(["## Title 2"], [Node()]),
                Node(["## Title 3"], [Node()])
            ])
        ])
    compare_trees(expected_root, root)


def test_can_build_simple_tree_with_content():
    text = """# Title

This is the introduction to the project

## Title 1

This is chapter 1

## Title 2

This is chapter 2

## Title 3

This is chapter 3
"""
    root = build_tree(text.split('\n'))
    expected_root = Node(
        [], [
            Node(["# Title"], [
                Node(["This is the introduction to the project"]),
                Node(["## Title 1"], [Node(["This is chapter 1"])]),
                Node(["## Title 2"], [Node(["This is chapter 2"])]),
                Node(["## Title 3"], [Node(["This is chapter 3"])])
            ])
        ])
    compare_trees(expected_root, root)


def test_can_build_tree_with_links_images_tables_and_code():
    text = """# Title

This is the introduction to the project
![Build Status](https://github.com/user/repo/image.png)

## Title 1

| Header 1 | Header 2 |
| -------- | -------- |
| row 1.1  | row 1.2  |

## Title 2

[My Link](https://google.de)

## Title 3

```bash
make install
```
"""
    root = build_tree(text.split('\n'))
    expected_root = Node(
        [], [
            Node(["# Title"], [
                Node(
                    ["This is the introduction to the project",
                     "![Build Status](https://github.com/user/repo/image.png)"]),
                Node(["## Title 1"], [Node([
                    "| Header 1 | Header 2 |",
                    "| -------- | -------- |",
                    "| row 1.1  | row 1.2  |"
                ])]),
                Node(["## Title 2"], [Node(["[My Link](https://google.de)"])]),
                Node(["## Title 3"], [Node(["```bash", "make install", "```"])])
            ])
        ])
    compare_trees(expected_root, root)


def test_can_render_tree():
    root = Node(
        [], [
            Node(["# Title"], [
                Node(["This is the introduction to the project"]),
                Node(["## Title 1"], [Node(["This is chapter 1"])]),
                Node(["## Title 2"], [Node(["This is chapter 2"])]),
            ])
        ])
    expected_html = [
        "<div class=\"markdown-document\">",
        "  <h1>Title</h1>",
        "  <div>",
        "    <div>",
        "      This is the introduction to the project<br/>",
        "    </div>",
        "    <h2>Title 1</h2>",
        "    <div>",
        "      <div>",
        "        This is chapter 1<br/>",
        "      </div>",
        "    </div>",
        "    <h2>Title 2</h2>",
        "    <div>",
        "      <div>",
        "        This is chapter 2<br/>",
        "      </div>",
        "    </div>",
        "  </div>",
        "</div>"
    ]
    portfolio_page.markdown_renderer.render_heading = render_simple_heading
    result = render_tree(root)
    assert result is not None
    assert len(result) == len(expected_html)
    for expected_line, actual_line in zip(expected_html, result):
        assert actual_line == expected_line


def test_can_render_tree_with_html():
    root = Node(
        [], [
            Node(["# Title"], [
                Node(["<my-tag></my-tag>"]),
            ])
        ])
    expected_html = [
        "<div class=\"markdown-document\">",
        "  <h1>Title</h1>",
        "  <div>",
        "    <div>",
        "      <my-tag></my-tag><br/>",
        "    </div>",
        "  </div>",
        "</div>"
    ]
    portfolio_page.markdown_renderer.render_heading = render_simple_heading
    result = render_tree(root)
    assert result is not None
    assert len(result) == len(expected_html)
    for expected_line, actual_line in zip(expected_html, result):
        assert actual_line == expected_line
