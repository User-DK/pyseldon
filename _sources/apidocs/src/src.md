# {py:mod}`src`

```{py:module} src
```

```{autodoc2-docstring} src
:allowtitles:
```

## Submodules

```{toctree}
:titlesonly:
:maxdepth: 1

src.network
src.simulation
```

## Package Contents

### Classes

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`Network <src.Network>`
  - ```{autodoc2-docstring} src.Network
    :summary:
    ```
* - {py:obj}`Simulation <src.Simulation>`
  - ```{autodoc2-docstring} src.Simulation
    :summary:
    ```
````

### Functions

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`run_simulation_from_config_file <src.run_simulation_from_config_file>`
  - ```{autodoc2-docstring} src.run_simulation_from_config_file
    :summary:
    ```
* - {py:obj}`run_simulation_from_options <src.run_simulation_from_options>`
  - ```{autodoc2-docstring} src.run_simulation_from_options
    :summary:
    ```
````

### Data

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`__all__ <src.__all__>`
  - ```{autodoc2-docstring} src.__all__
    :summary:
    ```
````

### API

````{py:data} __all__
:canonical: src.__all__
:value: >
   ['run_simulation_from_config_file', 'run_simulation_from_options']

```{autodoc2-docstring} src.__all__
```

````

````{py:function} run_simulation_from_config_file(config_file_path: str, agent_file_path: typing.Optional[str] = None, network_file_path: typing.Optional[str] = None, output_dir_path: typing.Optional[str] = None)
:canonical: src.run_simulation_from_config_file

```{autodoc2-docstring} src.run_simulation_from_config_file
```
````

````{py:function} run_simulation_from_options(options, agent_file_path=None, network_file_path=None, output_dir_path=None)
:canonical: src.run_simulation_from_options

```{autodoc2-docstring} src.run_simulation_from_options
```
````

`````{py:class} Network(model_string=None, n_agents=None, agents=None, neighbour_list=None, weight_list=None, direction=None)
:canonical: src.Network

```{autodoc2-docstring} src.Network
```

```{rubric} Initialization
```

```{autodoc2-docstring} src.Network.__init__
```

````{py:property} n_agents
:canonical: src.Network.n_agents

```{autodoc2-docstring} src.Network.n_agents
```

````

````{py:property} n_edges
:canonical: src.Network.n_edges

```{autodoc2-docstring} src.Network.n_edges
```

````

`````

````{py:class} Simulation(model_string='DeGroot', agent_file_path=None, network_file_path=None)
:canonical: src.Simulation

```{autodoc2-docstring} src.Simulation
```

```{rubric} Initialization
```

```{autodoc2-docstring} src.Simulation.__init__
```

````
