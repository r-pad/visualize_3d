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

    def add_plot(self, category: str, id: str, plot: go.Figure):
        plot.update_layout(margin=dict(l=5, r=5, t=40, b=5))
        self.cats[category].append((id, plot))

    def write_site(self, site_dir: Union[str, Path]):
        os.makedirs(site_dir, exist_ok=True)

        # Group all the IDs by category, and then by ID.
        parsed_ids: Dict[str, Dict[str, List]] = {}
        for cat, plot_list in self.cats.items():
            parsed_ids[cat] = defaultdict(list)
            for id, plot in plot_list:
                obj_id = id.split("_")[0]
                parsed_ids[cat][obj_id].append((id, plot))

        # Create a page for each object, and put all of its articulations on that page.
        for cat, obj_dict in parsed_ids.items():
            for obj_id, plot_list in obj_dict.items():
                sub_doc = dom.document(title=f"{obj_id}: {self.title}")

                with sub_doc.head:
                    dt.script(src="https://cdn.plot.ly/plotly-2.25.0.min.js")

                with sub_doc:
                    with dt.div(id=cat):
                        dt.h1(f"{id} - {cat}")
                        with dt.table():
                            for i, (id, plot) in enumerate(plot_list):
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
