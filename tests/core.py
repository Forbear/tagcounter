from tagcounter import TagCounter


def test_counter_command():
    c = TagCounter(['sc_list'])
    assert c.arguments.command == 'sc_list'


def test_counter_command_args():
    c = TagCounter(['synthetic', 'arg1', 'arg2', 'arg3', 'arg4'])
    assert c.arguments.command_args == ['arg1', 'arg2', 'arg3', 'arg4']


def test_counter_website():
    c = TagCounter(['synthetic', '-website', 'test.example'])
    assert c.website == 'test.example'


def test_counter_url():
    c = TagCounter(['synthetic', '-website', 'test.example', '-uri', '/test/'])
    assert c.url == 'https://test.example/test/'
