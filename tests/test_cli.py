from click.testing import CliRunner

from callicog.cli import run
from callicog.cli import resume


def test_run():
  runner = CliRunner()
  result = runner.invoke(run, ['--help'])
  assert result.exit_code == 0
  assert "Usage: run [OPTIONS] HOST ANIMAL TEMPLATE" in result.output