import shutil

from freezegun import freeze_time
from pathlib import Path

from nb_prep.nb_convert_strip import convert_notebook
from nb_prep.files import working_directory


@freeze_time("2012-01-14")
def test_convert_notebook(tmp_path, capsys):

    shutil.copyfile(
        "tests/data/example.ipynb",
        str(tmp_path / "example.ipynb"),
    )
    with working_directory(str(tmp_path)):
        convert_notebook(str(tmp_path / "example.ipynb"))
        assert Path("20120114_example_NBCONVERT_RENAME_COMMITHASH_PLACEHOLDER.html").exists()

        # Make sure output is stripped
        nb = tmp_path / "example.ipynb"
        txt = nb.read_text()
        assert "Hello, World!" not in txt

        # No date prefix
        convert_notebook(str(tmp_path / "example.ipynb"), date_format="")
        assert Path("example_NBCONVERT_RENAME_COMMITHASH_PLACEHOLDER.html").exists()

        # Warn if file is not overwritten
        assert "already exists, not overwriting." not in capsys.readouterr().out
        convert_notebook(str(tmp_path / "example.ipynb"), date_format="")
        assert "already exists, not overwriting." in capsys.readouterr().out
