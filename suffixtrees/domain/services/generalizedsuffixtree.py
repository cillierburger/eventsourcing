from suffixtrees.domain.model.generalizedsuffixtree import SuffixTreeNode, STRING_ID_END


def get_string_ids(node_id, node_repo, length_until_end=0, edge_length=0, limit=None, hop_count=0, hop_max=None):
    """Generator that performs a depth first search on the suffix tree
    from the given node, yielding leaf node string IDs as they are discovered.
    """
    if hop_max is not None and hop_count >= hop_max:
        raise StopIteration
    hop_count += 1

    stack = list()

    stack.append((node_id, edge_length, None))
    unique_string_ids = set()
    cum_lengths_until_end = {None: length_until_end}
    while stack:

        (node_id, edge_length, parent_node_id) = stack.pop()

        length_until_end = cum_lengths_until_end[parent_node_id] + edge_length
        cum_lengths_until_end[node_id] = length_until_end

        node = node_repo[node_id]
        assert isinstance(node, SuffixTreeNode)

        # If a node doesn't have any children, then it's a leaf node.
        child_node_ids = node._child_node_ids
        if child_node_ids:

            # Since the node has children, then it's not
            # a leaf node, so put child IDs on the stack.
            for (child_node_id, edge_length) in child_node_ids.items():
                stack.append((child_node_id, edge_length, node.id))

        else:
            # If a string has been removed, leaf nodes will have None as the value of string_id.
            string_id = node.string_id
            if string_id is None:
                continue

            # Deduplicate string IDs (the substring might match more than one suffix in any given string).
            if string_id in unique_string_ids:
                continue

            # Check the match doesn't encroach upon the string's extension.
            extension_length = len(string_id) + len(STRING_ID_END)
            if length_until_end < extension_length:
                continue

            # Remember the string ID, we only want one node per string ID.
            unique_string_ids.add(string_id)

            # Yield the string ID.
            yield string_id

            # Check if the limit has been reached.
            if limit is not None and len(unique_string_ids) >= limit:
                raise StopIteration
