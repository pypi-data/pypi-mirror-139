def html_escape(text):
    html_escape_table = {
        "&": "&amp;",
        '"': "&quot;",
        "'": "&apos;",
        ">": "&gt;",
        "<": "&lt;",
    }
    return "".join(html_escape_table.get(c, c) for c in text)


def get_label(node):
    return (
        f' class="{node["data"]["label"]}"'
        if "data" in node and "label" in node.get("data")
        else ""
    )


def standard_tag_serializer(tag):
    return lambda node, children: f"<{tag}{get_label(node)}>{''.join(children)}</{tag}>"


def preformatted_serializer(node, children=None):
    return f"<pre{get_label(node)}>{html_escape(node.get('text'))}</pre>"


def serialize_embed(node, children=None):
    oembed = node.get("oembed", {})
    return f"""<div data-oembed="{oembed.get('embed_url')}" data-oembed-type="{oembed.get('type')}" data-oembed-provider="{oembed.get('provider_name')}"{get_label(node)}>{oembed.get('html')}</div>"""


def serialize_hyperlink(node, children=[]):
    node_data = node.get("data", {})
    if node_data.get("link_type") == "Web":
        return f"""<a href="{html_escape(node_data.get('url'))}" target="{node_data.get('target', 'undefined')}" rel="noopener noreferrer"{get_label(node)}>{''.join(children)}</a>"""
    if node_data.get("link_type") == "Media":
        return f"""<a href="{html_escape(node_data.get('url'))}"{get_label(node)}>{''.join(children)}</a>"""
    # TODO: handle link_type == "Document" with link resolver...
    return ""


def serialize_image(node, children=None):
    image_tag = f"""<img src="{node.get('url')}" alt="{html_escape(node.get('alt'))}"{f' copyright="{html_escape(node.get("copyright"))}"' if node.get('copyright') else ""} />"""

    if node.get("linkTo"):
        image_tag = serialize_hyperlink(
            {
                "type": "hyperlink",
                "data": node.get("linkTo"),
                "start": 0,
                "end": 0,
            },
            children=[image_tag],
        )

    return f"""<p class="block-img">{image_tag}</p>"""


def serialize_span(node, children=None):
    return (
        html_escape(node.get("text")).replace("/\n/g", "<br />")
        if node.get("text")
        else ""
    )


def serialize_tree_nodes(nodes, serializer):
    return [
        serializer(
            node.get("node"),
            serialize_tree_nodes(node.get("children", []), serializer),
        )
        for node in nodes
    ]


def prepare_nodes(rich_text_list):
    """Extract list items and wrap them as items inside a list type node"""
    prepared_nodes = rich_text_list[:]
    i = 0
    for node in prepared_nodes:
        _type = node.get("type")
        if _type == "list-item" or _type == "o-list-item":
            items = [node]
            try:
                while prepared_nodes[i + 1].get("type") == _type:
                    items.append(prepared_nodes[i + 1])
                    prepared_nodes.remove(prepared_nodes[i + 1])
            except IndexError:
                pass

            if _type == "list-item":
                prepared_nodes[i] = {"type": "list", "items": items}
            else:
                prepared_nodes[i] = {"type": "o-list", "items": items}
        i += 1
    return prepared_nodes


def as_tree(rich_text_list):
    nodes = prepare_nodes(rich_text_list)

    return {"children": [node_to_tree_node(node) for node in nodes]}


def node_to_tree_node(node):
    if "text" in node.keys():
        return create_tree_node(
            node, node_spans_to_tree_node_children(node.get("spans"), node)
        )

    if "items" in node.keys():
        children = [node_to_tree_node(item) for item in node.get("items")]
        return create_tree_node(node, children)

    return create_tree_node(node, [])


def create_tree_node(node, children):
    return {
        "type": node.get("type"),
        "text": node.get("text"),
        "node": node,
        "children": children,
    }


def create_text_tree_node(text):
    return create_tree_node({"type": "span", "text": text, "spans": []}, [])


def node_spans_to_tree_node_children(spans, node, parent_span=None):
    if len(spans) == 0:
        return [create_text_tree_node(node.get("text"))]

    spans_copy = spans[:]
    spans_copy.sort(key=lambda a: (a.get("start"), -a.get("end")))
    children = []

    for i, span in enumerate(spans_copy):
        parent_start = parent_span and parent_span.get("start") or 0
        span_start = span.get("start") - parent_start
        span_end = span.get("end") - parent_start

        child_spans = []
        for j in range(i, len(spans_copy) - 1):
            removed_siblings = 0
            sibling_span = spans_copy[j - removed_siblings]

            if (
                sibling_span != span
                and sibling_span.get("start") >= span.get("start")
                and sibling_span.get("end") <= span.get("end")
            ):
                child_spans.append(sibling_span)
                spans_copy.remove(sibling_span)
                removed_siblings += 1

        if i == 0 and span_start > 0:
            children.append(create_text_tree_node(node.get("text", "")[:span_start]))

        children.append(
            create_tree_node(
                span,
                node_spans_to_tree_node_children(
                    child_spans,
                    {**node, "text": node.get("text", "")[span_start:span_end]},
                    span,
                ),
            )
        )

        if span_end < len(node.get("text")):
            slice_end = (
                spans_copy[i + 1].get("start") if len(spans_copy) > i + 1 else None
            )
            children.append(
                create_text_tree_node(node.get("text", "")[span_end:slice_end])
            )

    return children


def default_serializer(node, children):
    serializers = {
        "heading1": standard_tag_serializer("h1"),
        "heading2": standard_tag_serializer("h2"),
        "heading3": standard_tag_serializer("h3"),
        "heading4": standard_tag_serializer("h4"),
        "heading5": standard_tag_serializer("h5"),
        "heading6": standard_tag_serializer("h6"),
        "paragraph": standard_tag_serializer("p"),
        "preformatted": preformatted_serializer,
        "strong": standard_tag_serializer("strong"),
        "em": standard_tag_serializer("em"),
        "list-item": standard_tag_serializer("li"),
        "o-list-item": standard_tag_serializer("li"),
        "list": standard_tag_serializer("ul"),
        "o-list": standard_tag_serializer("ol"),
        "label": standard_tag_serializer("span"),
        "image": serialize_image,
        "embed": serialize_embed,
        "hyperlink": serialize_hyperlink,
        "span": serialize_span,
    }

    return serializers.get(node.get("type"), serialize_span)(node, children)


def as_html(rich_text_list):
    _as_tree = as_tree(rich_text_list)
    # print(_as_tree.get("children"))
    serialized_nodes = serialize_tree_nodes(
        _as_tree.get("children"), default_serializer
    )
    return "".join(serialized_nodes)
