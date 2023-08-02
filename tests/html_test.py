import os
import tempfile

import plotly.express as px

from rpad.visualize_3d.html import PlotlyWebsiteBuilder


def test_html():
    doc = PlotlyWebsiteBuilder("test_doc")

    with tempfile.TemporaryDirectory() as tmpdir:
        # Make a test video.
        video_fn = os.path.join(tmpdir, "test", "test.mp4")

        for i in range(10):
            fig = px.line(x=["a", "b", "c"], y=[i + 1, i + 3, i + 2], title=f"Plot {i}")
            doc.add_plot("Show", str(i), fig)

            # Add a video.
            doc.add_video("Show", str(i), "./test.mp4")
        doc.write_site(os.path.join(tmpdir, "test"))

        os.system(f"ffmpeg -f lavfi -i testsrc=size=640x300:rate=30 -t 5 {video_fn}")

        # Check that the files were created.
        assert os.path.exists(os.path.join(tmpdir, "test/index.html"))
        for i in range(10):
            assert os.path.exists(os.path.join(tmpdir, f"test/{i}.html"))
