from typing import List

from flask import Flask

from portfolio_page import github_api
from portfolio_page.generator import create_landing_page, generate_project_pages, correct_relative_links


def test_generate_index(app: Flask, repos: List[github_api.Repository]):
    github_api.get_repositories = lambda: repos
    with app.app_context():
        result = create_landing_page()
        # print(result)
        # assert result is None


def test_can_correct_image_links():
    html = "<img src=\"screenshots/font-demo.png\" alt=\"Font Demo\" style=\"max-width:100%;\">"
    path_prefix = "graphics_playground"
    actual = correct_relative_links(html, path_prefix)
    expected = "<img src=\"graphics_playground/screenshots/font-demo.png\" alt=\"Font Demo\" style=\"max-width:100%;\">"
    assert expected == actual


def test_can_correct_links():
    html = "<a target=\"_blank\" rel=\"noopener noreferrer\" href=\"screenshots/font-demo.png\"></a>"
    path_prefix = "graphics_playground"
    actual = correct_relative_links(html, path_prefix)
    expected = "<a target=\"_blank\" rel=\"noopener noreferrer\" href=\"graphics_playground/screenshots/font-demo.png\"></a>"
    assert expected == actual


def test_does_not_correct_absolute_links():
    html = "<a href=\"https://travis-ci.org/henne90gen/RacingToHell\" rel=\"nofollow\"></a>"
    path_prefix = "RacingToHell"
    actual = correct_relative_links(html, path_prefix)
    expected = "<a href=\"https://travis-ci.org/henne90gen/RacingToHell\" rel=\"nofollow\"></a>"
    assert expected == actual

def test_does_not_correct_internal_page_links():
    html ="<a id=\"user-content-for-loops\" class=\"anchor\" aria-hidden=\"true\" href=\"#for-loops\"></a>"
    path_prefix = "Neon"
    actual = correct_relative_links(html, path_prefix)
    expected = "<a id=\"user-content-for-loops\" class=\"anchor\" aria-hidden=\"true\" href=\"#user-content-for-loops\"></a>"
    assert expected == actual


def test_does_not_correct_absolute_image_links():
    html = "<img src=\"https://camo.githubusercontent.com/bcc1fd87d7747978e5e28f191286887860b79e80/68747470733a2f2f7472617669732d63692e6f72672f68656e6e65393067656e2f526163696e67546f48656c6c2e7376673f6272616e63683d6d6173746572\" alt=\"Build Status\" data-canonical-src=\"https://travis-ci.org/henne90gen/RacingToHell.svg?branch=master\" style=\"max-width:100%;\">"
    path_prefix = "RacingToHell"
    actual = correct_relative_links(html, path_prefix)
    expected = "<img src=\"https://camo.githubusercontent.com/bcc1fd87d7747978e5e28f191286887860b79e80/68747470733a2f2f7472617669732d63692e6f72672f68656e6e65393067656e2f526163696e67546f48656c6c2e7376673f6272616e63683d6d6173746572\" alt=\"Build Status\" data-canonical-src=\"https://travis-ci.org/henne90gen/RacingToHell.svg?branch=master\" style=\"max-width:100%;\">"
    assert expected == actual
