import pytest
from main import check_balance


@pytest.mark.parametrize(
    "seq, balance",
    [
        ("(((([{}]))))", True),
        ('[([])((([[[]]])))]{()}', True),
        ('{{[()]}}', True),
        ('}{}', False),
        ('{{[(])]}}', False),
        ('[[{())}]', False)
    ]
)
def test_check_balance(seq, balance):
    result = check_balance(seq)
    assert result == balance
