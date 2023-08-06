# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Configurator(Component):
    """A Configurator component.
The configurator component helps to define plot definitions based on the
metadata of a dataframe.

The metadata is used to compute the available parameters after data 
transformations for the most common plot types.
@hideconstructor

@example
import dash_express_components as dxc
import plotly.express as px

meta = dxc.get_meta(px.data.gapminder())

 dxc.Configurator(
          id="plotConfig",
          meta=meta,
 )
@public

Keyword arguments:

- id (optional):
    The ID used to identify this component in Dash callbacks. @type
    {string}.

- config (optional):
    Prop The resulting configuration of the plot. @type {Object}.

- meta (optional):
    The metadata the plotter selection is based on. @type {Object}.

- setProps (optional):
    Dash-assigned callback that should be called to report property
    changes to Dash, to make them available for callbacks. @private.

- showFilter (default True):
    Prop to define the visibility of the Filter panel @type {boolean}.

- showMetadata (default False):
    Prop to define the visibility of the Metadata panel @type
    {boolean}.

- showParameterization (default False):
    Prop to define the visibility of the Parameterization panel @type
    {boolean}.

- showPlotter (default True):
    Prop to define the visibility of the Plot panel @type {boolean}.

- showStore (default False):
    Prop to define the visibility of the Store panel @type {boolean}.

- showTransform (default True):
    Prop to define the visibility of the Transform panel @type
    {boolean}.

- showUpdate (default True):
    Prop to define the visibility of the update plot button @type
    {boolean}."""
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, meta=Component.UNDEFINED, config=Component.UNDEFINED, showFilter=Component.UNDEFINED, showTransform=Component.UNDEFINED, showPlotter=Component.UNDEFINED, showMetadata=Component.UNDEFINED, showParameterization=Component.UNDEFINED, showStore=Component.UNDEFINED, showUpdate=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'config', 'meta', 'setProps', 'showFilter', 'showMetadata', 'showParameterization', 'showPlotter', 'showStore', 'showTransform', 'showUpdate']
        self._type = 'Configurator'
        self._namespace = 'dash_express_components'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'config', 'meta', 'setProps', 'showFilter', 'showMetadata', 'showParameterization', 'showPlotter', 'showStore', 'showTransform', 'showUpdate']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}
        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(Configurator, self).__init__(**args)
