from make_mozilla.pages import utils
from mock import Mock


def _get_children_mock(depth, parent, total=2):
    children_mock = Mock()
    children = []
    new_depth = depth - 1
    if depth > 0:
        for i in range(total):
            children.append(_get_mock_page(path=str(i), depth=new_depth,
                                           parent=parent))
    children_mock.all.return_value = children
    return children_mock


def _get_mock_page(path='mock', depth=0, parent=None):
    mock_page = Mock()
    mock_page.path = path
    mock_page.save.return_value = True
    mock_page.parent = parent
    mock_page.children = _get_children_mock(depth, parent=mock_page)
    return mock_page


def test_single_item_is_saved():
    mock_page = _get_mock_page()
    utils.update_children(mock_page)
    assert mock_page.save.called
    assert mock_page.children.all() == []
    assert mock_page.real_path == 'mock'


def test_single_item_is_updated():
    mock_page = _get_mock_page()
    utils.update_children(mock_page)
    mock_page.path = 'updated'
    utils.update_children(mock_page)
    assert mock_page.real_path == 'updated'


def test_one_level_children_are_prefixed():
    mock_page = _get_mock_page(depth=1)
    utils.update_children(mock_page)
    child_0, child_1 = mock_page.children.all()
    assert child_0.real_path == 'mock/0'
    assert child_1.real_path == 'mock/1'


def test_one_level_children_are_saved():
    mock_page = _get_mock_page(depth=1)
    utils.update_children(mock_page)
    child_0, child_1 = mock_page.children.all()
    assert child_0.save.called
    assert child_1.save.called


def test_one_level_children_have_no_descendents():
    mock_page = _get_mock_page(depth=1)
    utils.update_children(mock_page)
    child_0, child_1 = mock_page.children.all()
    child_0.children.all() == []
    child_1.children.all() == []


def test_one_level_children_are_updated_when_parent_changes():
    mock_page = _get_mock_page(depth=1)
    utils.update_children(mock_page)
    mock_page.path = 'updated'
    utils.update_children(mock_page)
    child_0, child_1 = mock_page.children.all()
    assert child_0.real_path == 'updated/0'
    assert child_1.real_path == 'updated/1'


def test_two_level_children_are_prefixed():
    mock_page = _get_mock_page(depth=2)
    utils.update_children(mock_page)
    child_0 = mock_page.children.all()[0]
    grand_child_0, grand_child_1 = child_0.children.all()
    assert grand_child_0.real_path == 'mock/0/0'
    assert grand_child_1.real_path == 'mock/0/1'


def test_two_level_children_are_saved():
    mock_page = _get_mock_page(depth=2)
    utils.update_children(mock_page)
    child_0 = mock_page.children.all()[0]
    grand_child_0, grand_child_1 = child_0.children.all()
    assert grand_child_0.save.called
    assert grand_child_1.save.called


def test_two_level_children_have_no_descendents():
    mock_page = _get_mock_page(depth=2)
    utils.update_children(mock_page)
    child_0 = mock_page.children.all()[0]
    grand_child_0, grand_child_1 = child_0.children.all()
    assert grand_child_0.children.all() == []
    assert grand_child_1.children.all() == []


def test_two_level_children_are_updated_when_parent_changes():
    mock_page = _get_mock_page(depth=2)
    utils.update_children(mock_page)
    mock_page.path = 'updated'
    utils.update_children(mock_page)
    child_0 = mock_page.children.all()[0]
    grand_child_0, grand_child_1 = child_0.children.all()
    assert grand_child_0.real_path == 'updated/0/0'
    assert grand_child_1.real_path == 'updated/0/1'


def test_single_item_root():
    mock_page = _get_mock_page()
    root_page = utils.get_page_root(mock_page)
    assert mock_page == root_page


def test_one_level_depth_root():
    mock_page = _get_mock_page(depth=1)
    child = mock_page.children.all()[0]
    root_page = utils.get_page_root(child)
    assert mock_page == root_page


def test_two_level_children_root():
    mock_page = _get_mock_page(depth=2)
    child = mock_page.children.all()[0]
    grand_child = child.children.all()[0]
    root_page = utils.get_page_root(grand_child)
    assert mock_page == root_page


def test_page_descendants_single_item():
    mock_page = _get_mock_page()
    descendants = utils.get_page_descendants(mock_page)
    assert descendants == []


def test_page_descendants_one_level_depth():
    mock_page = _get_mock_page(depth=1)
    children = mock_page.children.all()
    descendants = utils.get_page_descendants(mock_page)
    assert descendants == children


def test_page_descendants_two_level_depth():
    mock_page = _get_mock_page(depth=2)
    # Prepare the list of children to comprare.
    children_list = []
    children = mock_page.children.all()
    children_list += children
    for child in children:
        children_list += child.children.all()
    descendants = utils.get_page_descendants(mock_page)
    # Sort items to perform comparison
    descendants.sort()
    children_list.sort()
    assert descendants == children_list
