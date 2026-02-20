"""Tests for __main__ entry point."""



def test_main_module_imports():
    """Test that __main__ can be imported."""
    from marty_cli import __main__
    assert hasattr(__main__, "main")
