from typing import List, Optional

from flask import render_template, render_template_string, Markup


def create_relative_url(url: str, path_prefix: str):
    if url.startswith("http"):
        return url

    if url[0] == "/":
        url = path_prefix + url
    else:
        url = path_prefix + "/" + url
    return url


def render_relative_images(path_prefix: str):
    def render_images(line):
        result = ""
        while "![" in line:
            start_index = line.find("![")
            before = line[:start_index]
            line = line[start_index + 2:]

            name_end = line.find(']')
            title = line[:name_end]
            line = line[name_end + 2:]

            url_end = line.find(")")
            url = create_relative_url(line[:url_end], path_prefix)
            line = line[url_end + 1:]

            image = render_template_string(
                "<img src=\"{{ url }}\" title=\"{{ title }}\"/>", url=url, title=title)
            result += before + image

        result += line
        return result
    return render_images


def render_relative_links(path_prefix: str):
    def render_links(line):
        result = ""
        while "[" in line:
            start_index = line.find("[")
            before = line[:start_index]
            line = line[start_index + 1:]

            content_end = line.find('](')
            content = Markup(line[:content_end])
            line = line[content_end + 2:]

            url_end = line.find(')')
            url: str = create_relative_url(line[:url_end], path_prefix)
            line = line[url_end + 1:]

            link = render_template_string(
                "<a href=\"{{ url }}\">{{ content }}</a>", url=url, content=content)
            result += before + link
        result += line
        return result
    return render_links


def render_headings(line: str):
    if not line.startswith('#'):
        return line

    heading_num = line.find(" ")
    heading_text = line[heading_num + 1:]
    heading_id = heading_text.replace(" ", "-").lower()
    heading_link = f"<a class=\"headerlink\" href=\"#{heading_id}\" title=\"Permalink to this headline\">¶</a>"
    return f"<h{heading_num} id=\"{heading_id}\">{heading_text}{heading_link}</h{heading_num}>"


def render_tables(lines: List[str]):
    return lines


def render_markdown(lines: List[str], path_prefix: str = "") -> Markup:
    result = list(
        map(render_headings,
            map(render_relative_links(path_prefix),
                map(render_relative_images(path_prefix),
                    lines))))

    result = render_tables(result)

    return Markup("<br>\n".join(result))
