from pathlib import Path

from git_synchronizer.git_synchronizer import parse_config

EXAMPLE_CONFIG = Path(__file__).parent.parent / Path("example_config.tsv")
def test_config_parsing():
    config = parse_config(EXAMPLE_CONFIG)
    assert len(config) == 2
    assert config[0] == ("https://example.com/examples/example.git", ["git@mygit.com:/examples/example.git"])
    assert config[1] == ("https://example.com/examples/example2.git", ["git@mygit.com:/examples/example2.git", "git@myothergit.com/example/example2.git"])