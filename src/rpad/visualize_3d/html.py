import os
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Tuple, Union

import dominate as dom
import dominate.tags as dt
import plotly.graph_objects as go
from dominate.util import raw


class PlotlyWebsiteBuilder:
    def __init__(self, title: str):
        self.title = title
        self.cats: Dict[str, List[Tuple[str, go.Figure]]] = defaultdict(list)
        self.videos: Dict[str, List[Tuple[str, Union[str, Path]]]] = defaultdict(list)

    def add_plot(self, category: str, id: str, plot: go.Figure):
        plot.update_layout(margin=dict(l=5, r=5, t=40, b=5))
        self.cats[category].append((id, plot))

    def add_video(self, category: str, id: str, video_path: Union[str, Path]):
        self.videos[category].append((id, video_path))

    def write_site(self, site_dir: Union[str, Path]):
        os.makedirs(site_dir, exist_ok=True)

        # Group all the IDs by category, and then by ID.
        parsed_ids: Dict[str, Dict[str, List]] = {}
        parsed_videos: Dict[str, Dict[str, List]] = {}
        for cat, plot_list in self.cats.items():
            parsed_ids[cat] = defaultdict(list)
            for id, plot in plot_list:
                obj_id = id.split("_")[0]
                parsed_ids[cat][obj_id].append((id, plot))

        for cat, video_list in self.videos.items():
            parsed_videos[cat] = defaultdict(list)
            for id, video in video_list:
                obj_id = id.split("_")[0]
                parsed_videos[cat][obj_id].append((id, video))

        # Create a page for each object, and put all of its articulations on that page.
        for cat, obj_dict in parsed_ids.items():
            video_dict = parsed_videos[cat]
            for obj_id, plot_list in obj_dict.items():
                video_list = video_dict[obj_id]
                sub_doc = dom.document(title=f"{obj_id}: {self.title}")

                with sub_doc.head:
                    dt.script(src="https://cdn.plot.ly/plotly-2.25.0.min.js")

                with sub_doc:
                    with dt.div(id=cat):
                        dt.h1(f"{obj_id} - {cat}")
                        with dt.table():
                            for i, ((pid, plot), (vid, video)) in enumerate(
                                zip(plot_list, video_list)
                            ):
                                assert (
                                    pid == vid
                                ), f"Video {vid} and image {pid} are from different sample."
                                id = pid
                                if i % 3 == 0:
                                    tr = dt.tr()

                                with tr:
                                    with dt.td(style="min-width:400px;max-width:400px"):
                                        dt.h2(id)
                                        with dt.div(id=id):
                                            raw(
                                                plot.to_html(
                                                    include_plotlyjs=False,
                                                    full_html=False,
                                                    auto_play=False,
                                                )
                                            )
                                        # Add a video section
                                        video_src = video
                                        with dt.div():
                                            dt.video(
                                                src=video_src,
                                                width="640",
                                                height="360",
                                                controls=True,
                                            )
                with open(os.path.join(site_dir, f"{obj_id}.html"), "w") as f:
                    f.write(str(sub_doc))

        # Create the index.
        doc = dom.document(title=self.title)
        with doc:
            for cat, obj_dict in parsed_ids.items():
                dt.h1(f"{cat}")

                for obj_id, plot_list in obj_dict.items():
                    dt.a(obj_id, href=f"./{obj_id}.html")
        with open(os.path.join(site_dir, "index.html"), "w") as f:
            f.write(str(doc))
