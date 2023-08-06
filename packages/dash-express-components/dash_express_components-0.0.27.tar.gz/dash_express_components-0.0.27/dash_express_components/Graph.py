# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Graph(Component):
    """A Graph component.
Graph is based on the original dash Graph and can be used to render any
plotly.js-powered data visualization.

In addition, there is the possibility to add plot parameters as `defParams` and 
the dataframe `meta` data.  
This automatically adds a configurator modal, which can be opened via a button
at the bottom right. 


@hideconstructor

@example
import dash_express_components as dxc
import plotly.express as px

meta = dxc.get_meta(px.data.gapminder())

dxc.Graph(
    id="fig",
    meta=meta,
    defParams={}
)
@public

Keyword arguments:

- id (string; optional):
    The ID of this component, used to identify dash components in
    callbacks. The ID needs to be unique across all of the components
    in an app. @type {string}.

- className (string; optional):
    className of the parent div.

- defParams (dict; optional):
    Metadata to describe the plot features.

- figure (boolean | number | string | dict | list; default {    data: [],    layout: {},    frames: [],}):
    Plotly `figure` object. See schema:
    https://plotly.com/javascript/reference  `config` is set
    separately by the `config` property.

- meta (boolean | number | string | dict | list; optional):
    The metadata the plotter selection is based on.

- style (dict; optional):
    Generic style overrides on the plot div."""
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, defParams=Component.UNDEFINED, meta=Component.UNDEFINED, figure=Component.UNDEFINED, style=Component.UNDEFINED, className=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'className', 'defParams', 'figure', 'meta', 'style']
        self._type = 'Graph'
        self._namespace = 'dash_express_components'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'className', 'defParams', 'figure', 'meta', 'style']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}
        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(Graph, self).__init__(**args)
