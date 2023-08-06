import itertools
import math

import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
import plotly
from dash.dependencies import ALL
from dash.exceptions import PreventUpdate
from dash_extensions.enrich import Dash, Trigger, Output, Input, State
from dash_extensions.snippets import get_triggered
from pandas import DataFrame
import plotly.graph_objects as go
from plotly.graph_objs import Scattermapbox

from vizer.graph import Scatter, Hist, AGGREGATIONS, HistCum, Table, Heatmap, Map, Hist2D, Line
from vizer.utils import create_row, full_width_input

X_DROPDOWN_ID = "x-dropdown-id"
Y_DROPDOWN_ID = "y-dropdown-id"
Z_DROPDOWN_ID = "z-dropdown-id"
X_GRP_DROPDOWN_ID = "x-grp-dropdown-id"
Y_GRP_DROPDOWN_ID = "y-grp-dropdown-id"
Z_GRP_DROPDOWN_ID = "z-grp-dropdown-id"
GROUP_DROPDOWN_ID = "group-dropdown-id"
GROUPS_DROPDOWN_ID = "groups-dropdown-id"
AGG_DROPDOWN_ID = "agg-dropdown-id"
QUERY_INPUT_ID = "query-input-id"
ROOT_QUERY_INPUT_ID = "root-query-input-id"
OK_BUTTON_ID = "ok-button-id"
GRAPH_ID = "graph-id"
TYPE_DROPDOWN_ID = "type-dropdown-id"
CHARTS_BUTTONS_ID = "charts-buttons-id"
SELECTED_CHART_STORE_ID = "selected-chart-store-id"

CHARTS_STORE_ID = "charts-store-id"
GENERAL_STORE_ID = "general-store-id"
URL_ID = "url-id"
ADD_CHART_ID = "add-chart-id"
DELETE_CHART_ID = "delete-chart-id"
SELECT_CHECKBOX_ID = "select-checkbox-id"

PLOT_INDEX_INPUT_ID = "plot-index-input-id"
COL_INPUT_ID = "col-input-id"
PLOT_LAYOUT_STORE_ID = "plot-layout-store-id"

STORAGE_TYPE = 'session'


def create_layout(df: DataFrame):
    non_numeric = df.select_dtypes('object').columns
    return html.Div([
        dcc.Store(id=CHARTS_STORE_ID, data={'Chart1': {}}, storage_type=STORAGE_TYPE),
        dcc.Store(id=SELECTED_CHART_STORE_ID, data='Chart1', storage_type=STORAGE_TYPE),
        dcc.Store(id=GENERAL_STORE_ID, data={}, storage_type=STORAGE_TYPE),
        dcc.Store(id=PLOT_LAYOUT_STORE_ID, data=['hist']*9, storage_type=STORAGE_TYPE),
        dcc.Location(id=URL_ID),
        dbc.Card([
            dbc.CardHeader([
                dbc.Row([
                    dbc.Col([
                        html.Div(id=CHARTS_BUTTONS_ID)
                    ], width=5),
                    dbc.Col([
                        dbc.Button(html.I(className="fa fa-trash"), id=DELETE_CHART_ID, color="danger", className="mr-1 float-right"),
                        dbc.Button(html.I(className="fa fa-plus"), id=ADD_CHART_ID, color="success", className="mr-1 float-right")
                    ], width=1),
                    dbc.Col([
                        create_row("Root query", full_width_input(id=ROOT_QUERY_INPUT_ID, type="text"), 2)
                    ], width=6),
                ])
            ]),
            dbc.CardBody([
                dbc.Row([
                    dbc.Col([
                        create_row("Plot Index",
                                   full_width_input(id=PLOT_INDEX_INPUT_ID, type="number", value=1, min=1, max=9), 6)
                    ], width=2),
                    dbc.Col([
                        create_row("X", dcc.Dropdown(id=X_DROPDOWN_ID,
                                                     options=[{'value': x, 'label': x} for x in df.columns]))
                    ], width=2),
                    dbc.Col([
                        create_row("Y", dcc.Dropdown(id=Y_DROPDOWN_ID,
                                                     options=[{'value': x, 'label': x} for x in df.columns]))
                    ], width=2),
                    dbc.Col([
                        create_row("Z", dcc.Dropdown(id=Z_DROPDOWN_ID,
                                                     options=[{'value': x, 'label': x} for x in df.columns]))
                    ], width=2)
                ]),
                dbc.Row([
                    dbc.Col([
                        create_row("Group by", dcc.Dropdown(id=GROUP_DROPDOWN_ID,
                                                            options=[{'value': x, 'label': x} for x in df.columns if
                                                                     str(x) in non_numeric]))
                    ], width=2),
                    dbc.Col([
                        create_row("X group", dcc.Dropdown(id=X_GRP_DROPDOWN_ID,
                                                          options=[{'value': x, 'label': x} for x in df.columns]))
                    ], width=2),
                    dbc.Col([
                        create_row("Y group", dcc.Dropdown(id=Y_GRP_DROPDOWN_ID,
                                                          options=[{'value': x, 'label': x} for x in df.columns]))
                    ], width=2),
                    dbc.Col([
                        create_row("Z group", dcc.Dropdown(id=Z_GRP_DROPDOWN_ID,
                                                          options=[{'value': x, 'label': x} for x in df.columns]))
                    ], width=2),
                    dbc.Col([
                        create_row("Groups", dcc.Dropdown(id=GROUPS_DROPDOWN_ID, multi=True,
                                                          options=[{'value': x, 'label': x} for x in df.columns]), 2)
                    ], width=4)
                ]),
                dbc.Row([
                    dbc.Col([
                        create_row("Aggregation", dcc.Dropdown(id=AGG_DROPDOWN_ID,
                                                               options=[{'value': x, 'label': x} for x in
                                                                        AGGREGATIONS.keys()], disabled=True))
                    ], width=2),
                    dbc.Col([
                        create_row("Chart query", full_width_input(id=QUERY_INPUT_ID, type="text"), 2)
                    ], width=6),
                    dbc.Col([
                        dcc.Checklist(
                            id=SELECT_CHECKBOX_ID,
                            options=[
                                {'label': 'Select', 'value': 'select'}
                            ],
                            value=[]
                        )
                    ], width=4)
                ])
            ])
        ], className="m-1"),
        html.Div([
            html.Div(id=GRAPH_ID, style={"height": "100%"})
        ], className="flex-grow-1 m-1")

    ], style={"height": "100%", "width": "100%", "background-color": "#D3D3D3"}, className="d-flex h-100 flex-column")


def create_callbacks(app: Dash, df: DataFrame):

    @app.callback(
        Trigger(dict(type="chart-selector", chart=ALL), "n_clicks"),
        Output(SELECTED_CHART_STORE_ID, 'data')
    )
    def on_selection():
        t = get_triggered()
        if t.n_clicks is None:
            raise PreventUpdate()
        return t.id["chart"]

    @app.callback(
        [Trigger(URL_ID, 'pathname'), Trigger(ADD_CHART_ID, 'n_clicks'), Trigger(DELETE_CHART_ID, 'n_clicks'),
         Input(SELECTED_CHART_STORE_ID, 'data'), Input(CHARTS_STORE_ID, 'data')],
        [Output(CHARTS_BUTTONS_ID, "children")]
    )
    def update_charts_buttons(selected, charts):

        def color(c):
            if c == selected:
                return "primary"
            else:
                return "secondary"

        k = [dbc.Button(x, color=color(x), id=dict(type="chart-selector", chart=x), className="mr-2") for x in charts.keys()]

        return k

    @app.callback(
        [Trigger(URL_ID, 'pathname'), Trigger(ADD_CHART_ID, 'n_clicks'), Trigger(DELETE_CHART_ID, 'n_clicks')],
        [Output(CHARTS_STORE_ID, 'data'), Output(ROOT_QUERY_INPUT_ID, 'value')],
        [State(CHARTS_STORE_ID, 'data'), State(GENERAL_STORE_ID, 'data'), State(SELECTED_CHART_STORE_ID, 'data')], group="charts"
    )
    def update_or_add_charts_dropdown(charts, general, current):

        trig = get_triggered()

        if trig.id == ADD_CHART_ID:
            last = sorted(charts.keys())[-1]
            value = f"Chart{int(last.lstrip('Chart')) + 1}"
            charts[value] = charts[last].copy()
            if "index" in charts[value]:
                charts[value]["index"] += 1
        elif trig.id == DELETE_CHART_ID:
            del charts[current]

        if not charts:
            charts = {'Chart1': {}}

        return charts, general.get("root_query")

    @app.callback(
        [Trigger(URL_ID, 'pathname'), Input(SELECTED_CHART_STORE_ID, 'data'), Input(GROUP_DROPDOWN_ID, 'value')],
        [Output(X_DROPDOWN_ID, 'value'), Output(Y_DROPDOWN_ID, 'value'), Output(Z_DROPDOWN_ID, 'value'),
         Output(GROUP_DROPDOWN_ID, 'value'), Output(GROUPS_DROPDOWN_ID, 'value'), Output(QUERY_INPUT_ID, 'value'), Output(AGG_DROPDOWN_ID, 'value'),
         Output(GROUPS_DROPDOWN_ID, 'options'), Output(PLOT_INDEX_INPUT_ID, 'value'),
         Output(X_GRP_DROPDOWN_ID, 'options'), Output(Y_GRP_DROPDOWN_ID, 'options'), Output(Z_GRP_DROPDOWN_ID, 'options'),
         Output(X_GRP_DROPDOWN_ID, 'value'), Output(Y_GRP_DROPDOWN_ID, 'value'), Output(Z_GRP_DROPDOWN_ID, 'value')],
        State(CHARTS_STORE_ID, 'data'), group="inputs"
    )
    def update_chart_on_selection(selected_chart, group, charts):

        d = charts[selected_chart]
        kwargs = charts[selected_chart].get("args", {})

        if get_triggered().id == GROUP_DROPDOWN_ID:
            _group = group
            _selected_groups = df[group].unique()[:10]
        else:
            _group = kwargs.get("group_by")
            _selected_groups = kwargs.get("groups")

        groups_options = [{'value': x, 'label': x} for x in df[_group].unique()] if _group is not None else []
        return kwargs.get("x"), kwargs.get("y"), kwargs.get("z"), _group, \
               _selected_groups, kwargs.get("query"), kwargs.get("aggregation"), groups_options, d.get('index', 1), \
                groups_options, groups_options, groups_options, kwargs.get("x_grp"), kwargs.get("y_grp"), kwargs.get("z_grp")

    @app.callback(
        Input(dict(type=TYPE_DROPDOWN_ID, index=ALL), 'value'),
        Output(PLOT_LAYOUT_STORE_ID, 'data'),
        State(PLOT_LAYOUT_STORE_ID, 'data')
    )
    def on_plot_type_change(new_type, layouts):
        idx = get_triggered().id['index'] - 1
        layouts[idx] = new_type[idx]
        return layouts

    @app.callback(
        Input(ROOT_QUERY_INPUT_ID, 'value'),
        Output(GENERAL_STORE_ID, 'data'),
        State(GENERAL_STORE_ID, 'data')
    )
    def on_general_query(val, general):
        general["root_query"] = val
        return general

    @app.callback(
        [Output("query-modal", "is_open"), Output("modal-content", "children")],
        [Input(dict(type="modal-open", idx=ALL), "n_clicks"), Input("close", "n_clicks")],
        [State("query-modal", "is_open"), State(CHARTS_STORE_ID, 'data')],
    )
    def toggle_modal(n1, n2, is_open, charts):
        t = get_triggered()
        cnt = []
        if isinstance(t.id, dict):
            plot_idx = t.id['idx']

            for name, val in charts.items():
                if val['index'] == plot_idx:
                    cnt.append(dbc.Row(f"{name}: {val['args']['query']}"))

        if n1 or n2:
            return not is_open, cnt
        return is_open, cnt

    @app.callback(
        [Input(CHARTS_STORE_ID, 'data'), Input(PLOT_LAYOUT_STORE_ID, 'data'), Input(GENERAL_STORE_ID, 'data')],
        Output(GRAPH_ID, 'children')
    )
    def do_plot(charts, plot_types, general):
        try:
            figures = [go.Figure(layout=dict(margin=dict(t=5, l=10, r=10, b=10))) for _ in range(9)]
            graphs = [html.Div() for _ in range(9)]
            annotations = [[] for _ in range(9)]

            for chart_name, chart_data in charts.items():
                if not chart_data:
                    continue
                _p_index = chart_data.get('index', 0)

                plot_type = plot_types[_p_index - 1]

                kwargs = chart_data.get("args", {}).copy()
                kwargs["prefix"] = chart_name

                queries = []
                if general.get("root_query"):
                    queries.append(general.get("root_query"))
                if kwargs.get("query"):
                    queries.append(kwargs.get("query"))

                if general.get("root_query"):
                    kwargs["query"] = ' & '.join([f'({x})' for x in queries])

                fig = figures[_p_index - 1]

                if plot_type == "cumhist":
                    p = HistCum()
                    title = kwargs['y']
                    x_title = kwargs['y']
                    y_title = "Counts"
                elif plot_type == "hist":
                    p = Hist()
                    title = kwargs['y']
                    x_title = kwargs['y']
                    y_title = "Counts"
                    fig.update_layout(barmode='overlay')
                    fig.update_traces(opacity=0.50)
                elif plot_type == "hist2d":
                    p = Hist2D()
                    title = kwargs['y']
                    x_title = kwargs['x']
                    y_title = kwargs['y']
                elif plot_type == "table":
                    p = Table()
                    title = kwargs['y']
                    x_title = kwargs['x']
                    y_title = kwargs['y']
                elif plot_type == "heatmap":
                    p = Heatmap()
                    title = kwargs['z']
                    x_title = kwargs['x']
                    y_title = kwargs['y']
                elif plot_type == "map":
                    p = Map()
                    title = kwargs['z']
                    x_title = kwargs['x']
                    y_title = kwargs['y']
                    fig.update_layout(mapbox_style="open-street-map")
                elif plot_type == "line":
                    p = Line()
                    title = f"{kwargs['x']} vs. {kwargs['y']}"
                    x_title = kwargs['x']
                    y_title = kwargs['y']
                else:
                    p = Scatter()
                    title = f"{kwargs['x']} vs. {kwargs['y']}"
                    x_title = kwargs['x']
                    y_title = kwargs['y']

                figs, _annotations = p.generate_figure(df.copy(), **kwargs)

                for k in figs:
                    fig.add_trace(k)

                for y in _annotations:
                    if y:
                        annotations[_p_index - 1].append('<br>'.join([kwargs['y']] + y))

                fig.update_layout(dict(uirevision="JOHN"))
                fig.update_layout(dict(xaxis=dict(title=x_title)))
                fig.update_layout(dict(yaxis=dict(title=y_title)))
                fig.update_layout(legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="left",
                    x=0
                ))

                graphs[_p_index - 1] = html.Div([
                    dbc.Card([
                        dbc.CardHeader([
                            dbc.Row([
                                dbc.Col([
                                    html.Div([f'{title}']),

                                    dbc.Modal(
                                        [
                                            dbc.ModalHeader("Queries"),
                                            dbc.ModalBody("This is the content of the modal", id='modal-content'),
                                            dbc.ModalFooter(
                                                dbc.Button("Close", id="close", className="ml-auto")
                                            ),
                                        ],
                                        id="query-modal",
                                    )],
                                    width=6
                                ),
                                dbc.Col(
                                    dbc.Button(
                                        "Query", id=dict(type="modal-open", idx=_p_index), color="primary"
                                    ) if chart_data["args"]["query"] else None,
                                    width=2
                                ),
                                dcc.Dropdown(
                                    id=dict(type=TYPE_DROPDOWN_ID, index=_p_index),
                                    options=[
                                        {'value': 'hist', 'label': 'Histogram'},
                                        {'value': 'hist2d', 'label': 'Histogram2D'},
                                        {'value': 'cumhist', 'label': 'CumHistogram'},
                                        {'value': 'scat', 'label': 'Scatter'},
                                        {'value': 'line', 'label': 'Line'},
                                        {'value': 'table', 'label': 'Table'},
                                        {'value': 'map', 'label': 'Map'},
                                        {'value': 'heatmap', 'label': 'Heatmap'}
                                    ],
                                    value=plot_type,
                                    clearable=False,
                                    style={"width": "200px"}
                                ),
                            ], justify="between"),
                        ]),
                        dbc.CardBody(
                            dcc.Graph(figure=fig, style={"height": f"100%"}, id=dict(type="graph", index=_p_index))
                        )
                    ], style={"height": f"100%"})
                ], className="m-1")

            for fig, a in zip(figures, annotations):
                if fig.data and isinstance(fig.data[0], Scattermapbox):
                    try:
                        lat = [list(x.lat) for x in fig.data]
                        lon = [list(x.lon) for x in fig.data]

                        lat = list(itertools.chain(*lat))
                        lon = list(itertools.chain(*lon))

                        diff_lat = (max(lat) - min(lat))
                        diff_lon = (max(lon) - min(lon))

                        center_lat = diff_lat / 2.0 + min(lat)
                        center_lon = diff_lon / 2.0 + min(lon)

                        fig.update_layout(mapbox=dict(
                            center=go.layout.mapbox.Center(
                                lat=center_lat,
                                lon=center_lon
                            ),
                            zoom=5.5 - len(fig.data)
                        ))
                    except:
                        pass

                if any(a):
                    i = 0
                    offset = 0
                    for label in a:

                        fig.add_annotation(
                            x=0 + offset,
                            y=1.0,
                            xref="paper",
                            yref="paper",
                            text=label,
                            showarrow=False,
                            font=dict(
                                family="Courier New, monospace",
                                size=12,
                                color="black"
                            ),
                            align="right",
                            bgcolor=plotly.colors.qualitative.Plotly[i],
                            opacity=0.8
                        )
                        i += 1

                        offset += 0.2

            graphs = [g for g, f in zip(graphs, figures) if len(f.data)]

            rows = math.ceil(len(graphs) / 3)
            cols = min(len(graphs), 3)

            columns = " ".join([f"{100 / cols}%"] * cols) if cols else "100%"
            rows = " ".join([f"{100 / rows}%"] * rows) if rows else "100%"

            return html.Div(graphs, style={"height": "99%", "display": "grid", "grid-template-columns": columns, "grid-template-rows": rows}),

        except Exception as e:
            # import traceback
            # traceback.print_exc()
            raise PreventUpdate()

    @app.callback(
        Input(dict(type="graph", index=ALL), 'selectedData'),
        Output(QUERY_INPUT_ID, 'value'),
        [State(dict(type="graph", index=ALL), 'figure'), State(SELECTED_CHART_STORE_ID, 'data')], group="inputs"
    )
    def on_box_select(d, layout, do_select):

        if not do_select:
            raise PreventUpdate()

        t = get_triggered()
        idx = t.id['index'] - 1

        x_label = layout[idx]['layout']['xaxis']['title']['text']
        y_label = layout[idx]['layout']['yaxis']['title']['text']

        try:
            x_range = d[0]["range"]['x']
            y_range = d[0]["range"]['y']

            sub_queries = []
            sub_queries.append(f"{x_range[0]:0.4f} < {x_label}")
            sub_queries.append(f"{x_label} < {x_range[1]:0.4f}")

            sub_queries.append(f"{y_range[0]:0.4f} < {y_label}")
            sub_queries.append(f"{y_label} < {y_range[1]:0.4f}")

            query = ' & '.join(sub_queries)
            return query

        except (KeyError, TypeError):
            raise PreventUpdate()

    @app.callback(
        Input(dict(type="graph", index=ALL), 'relayoutData'),
        [Output(QUERY_INPUT_ID, 'value')],
        [State(SELECTED_CHART_STORE_ID, 'data'), State(CHARTS_STORE_ID, 'data'),
         State(dict(type="graph", index=ALL), 'figure'), State(SELECT_CHECKBOX_ID, 'value')], group="inputs"
    )
    def doo(d, current, charts, layout, do_select):
        if not do_select:
            raise PreventUpdate()

        try:
            t = get_triggered()
            idx = t.id['index'] - 1

            x_label = layout[idx]['layout']['xaxis']['title']['text']
            y_label = layout[idx]['layout']['yaxis']['title']['text']
            g = d[idx]
            sub_queries = []

            query = charts[current]['args']['query']

            if 'xaxis.range[0]' in d or 'yaxis.range[0]' in g:
                if x_label in df.columns:
                    try:
                        sub_queries.append(f"{g['xaxis.range[0]']:0.4f} < {x_label}")
                        sub_queries.append(f"{x_label} < {g['xaxis.range[1]']:0.4f}")
                    except (StopIteration, KeyError):
                        pass

                if y_label in df.columns:
                    try:
                        sub_queries.append(f"{g['yaxis.range[0]']:0.4f} < {y_label}")
                        sub_queries.append(f"{y_label} < {g['yaxis.range[1]']:0.4f}")
                    except (StopIteration, KeyError):
                        pass

                query = ' & '.join(sub_queries)
            elif g == {'xaxis.autorange': True, 'yaxis.autorange': True}:
                query = ''
            return query
        except Exception as e:
            import traceback
            traceback.print_exc()
            raise PreventUpdate()

    @app.callback(
        [Input(X_DROPDOWN_ID, 'value'),
         Input(Y_DROPDOWN_ID, 'value'), Input(Z_DROPDOWN_ID, 'value'), Input(GROUP_DROPDOWN_ID, 'value'), Input(GROUPS_DROPDOWN_ID, 'value'),
         Input(QUERY_INPUT_ID, 'value'), Input(AGG_DROPDOWN_ID, 'value'), Input(SELECTED_CHART_STORE_ID, 'data'),
         Input(PLOT_INDEX_INPUT_ID, 'value'),
         Input(X_GRP_DROPDOWN_ID, 'value'), Input(Y_GRP_DROPDOWN_ID, 'value'), Input(Z_GRP_DROPDOWN_ID, 'value')],
        [Output(CHARTS_STORE_ID, 'data')],
        [State(CHARTS_STORE_ID, 'data')], group="charts"
    )
    def ok(x, y, z, group, groups, query, agg, selected_chart, plot_index, x_grp, y_grp, z_grp, charts):
        kwargs = dict(x=x, y=y, z=z, group_by=group, groups=groups, query=query, aggregation=agg,
                      x_grp=x_grp, y_grp=y_grp, z_grp=z_grp)
        charts[selected_chart] = {"args": kwargs, "index": plot_index}
        return charts

