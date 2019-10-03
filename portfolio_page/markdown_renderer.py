from dataclasses import dataclass, field
from typing import List, Optional

from flask import render_template_string, Markup


@dataclass
class Node:
    content: List[str] = field(default_factory=list)
    children: List["Node"] = field(default_factory=list)
    parent: "Node" = None


def add_css_class(tag: str, cls: str):
    def inner(line: str):
        tag_start = line.find(f"<{tag}")
        if tag_start == -1:
            return line
        tag_end = tag_start + 1 + len(tag)

        if len(line) > tag_end + 1 and (line[tag_end + 1] != " " or line[tag_end + 1] != ">"):
            return line

        if len(line) > tag_end + 2 and line[tag_end + 1] == "/" and line[tag_end + 2] == ">":
            return line

        result = line[:tag_end] + f" class=\"{cls}\"" + line[tag_end:]
        return result

    return inner


def render_short_description(content: List[str], path_prefix: str):
    result = render_tree_content(content, path_prefix, 0)
    result = list(map(add_css_class("p", "card-content"), result))
    return Markup("\n".join(result))


def create_relative_url(url: str, path_prefix: str):
    if url.startswith("http"):
        return url

    if url[0] == "/":
        url = path_prefix + url
    else:
        url = path_prefix + "/" + url
    return url


def render_relative_images(path_prefix: str):
    def render_images(line: str):
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
    def render_links(line: str):
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


def render_heading(line: str):
    if not line.startswith('#'):
        return line

    heading_num = line.find(" ")
    heading_text = line[heading_num + 1:]
    heading_id = heading_text.replace(" ", "-").lower()
    heading_link = f"<a class=\"headerlink\" href=\"#{heading_id}\" title=\"Permalink to this headline\">¶</a>"
    return f"<h{heading_num} id=\"{heading_id}\">{heading_text}{heading_link}</h{heading_num}>"


def render_tables(lines: List[str]):
    return lines


def build_tree(lines: List[str]) -> Optional[Node]:
    root = Node()
    current_parent = root
    current_level = 0
    for line in lines:
        if not line.strip():
            continue

        if line.startswith('#'):
            level = line.find(" ")
            if level > current_level:
                new_node = Node([line], [], current_parent)
                new_node.children.append(Node([], [], new_node))
                current_parent.children.append(new_node)
                current_parent = new_node
                current_level += 1
            elif level < current_level:
                while level <= current_level:
                    current_parent = current_parent.parent
                    current_level -= 1
                new_node = Node([line], [], current_parent)
                new_node.children.append(Node([], [], new_node))
                current_parent.children.append(new_node)
            else:
                new_node = Node([line], [], current_parent.parent)
                new_node.children.append(Node([], [], new_node))
                current_parent.parent.children.append(new_node)
                current_parent = new_node
        else:
            if not current_parent.children:
                current_parent.children.append(Node())
            current_parent.children[0].content.append(line)

    return root


def render_tree_content(content: List[str], path_prefix: str, level: int) -> List[str]:
    if content and content[0].startswith('#'):
        return ["  " * level + render_heading(content[0])]

    def indent_and_line_break(line: str):
        indentation = "  " * (level + 1)
        return f"{indentation}{line}<br/>"

    lines: List[str] = content
    lines = filter(lambda l: l.strip() != "", lines)
    lines = map(render_relative_images(path_prefix), lines)
    lines = map(render_relative_links(path_prefix), lines)
    lines = map(indent_and_line_break, lines)
    lines: List[str] = list(lines)

    lines = render_tables(lines)
    result = []
    if lines:
        result.append("  " * level + "<p>")
        result += lines
        result.append("  " * level + "</p>")

    return result


def render_tree(root: Node, path_prefix: str = "", level: int = 0) -> [str]:
    result = render_tree_content(root.content, path_prefix, level)

    if root.children:
        cls = " class=\"markdown-document\"" if level == 0 else ""
        result.append("  " * level + f"<div{cls}>")
        for child in root.children:
            result += render_tree(child, path_prefix, level + 1)
        result.append("  " * level + "</div>")

    return result


def render_markdown(lines: List[str], path_prefix: str = "") -> Markup:
    root = build_tree(lines)
    return Markup("\n".join(render_tree(root, path_prefix)))
