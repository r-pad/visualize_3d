# visualize_3d

Some sick visualization tools that r-pad has accumulated over the years.

## Usage

### html.py

This is a simple utility for building a website containing Plotly visualizations.

```python
from visualize_3d import html
from plotly import graph_objects as go

# Create the builder.
doc = html.PlotlyWebsiteBuilder("Evaluation Visualizations")

# Create a figure, and add it to the plot.
fig = go.Figure()
doc.add_plot("Sample Category", "Sample ID", fig)

# Write the site to disk.
doc.write_site("./path/to/desired/output/directory")
```

This will create a nice website with headings for each category, and a set of pages for each ID.

To serve the site locally, you can very easily run a simple Python HTML server from the output directory:

```
python -m http.server 9000
```
