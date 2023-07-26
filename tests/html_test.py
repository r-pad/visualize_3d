import os
import tempfile

import plotly.express as px

from rpad.visualize_3d.html import PlotlyWebsiteBuilder


def test_html():
    doc = PlotlyWebsiteBuilder("test_doc")

    with tempfile.TemporaryDirectory() as tmpdir:
        for i in range(10):
            fig = px.line(x=["a", "b", "c"], y=[i + 1, i + 3, i + 2], title=f"Plot {i}")
            doc.add_plot("Show", str(i), fig)
        doc.write_site(os.path.join(tmpdir, "test"))

        # Check that the files were created.
        assert os.path.exists(os.path.join(tmpdir, "test/index.html"))
        for i in range(10):
            assert os.path.exists(os.path.join(tmpdir, f"test/{i}.html"))
