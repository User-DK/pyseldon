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

````{py:property} get_direction
:canonical: src.Network.get_direction

```{autodoc2-docstring} src.Network.get_direction
```

````

````{py:property} strongly_connected_components
:canonical: src.Network.strongly_connected_components

```{autodoc2-docstring} src.Network.strongly_connected_components
```

````

````{py:method} get_neighbours(index)
:canonical: src.Network.get_neighbours

```{autodoc2-docstring} src.Network.get_neighbours
```

````

````{py:method} get_weights(index)
:canonical: src.Network.get_weights

```{autodoc2-docstring} src.Network.get_weights
```

````

````{py:method} set_weights(agent_idx, weights)
:canonical: src.Network.set_weights

```{autodoc2-docstring} src.Network.set_weights
```

````

````{py:method} set_neighbours_and_weights(agent_idx, buffer_neighbours, buffer_weights)
:canonical: src.Network.set_neighbours_and_weights

```{autodoc2-docstring} src.Network.set_neighbours_and_weights
```

````

````{py:method} push_back_neighbour_and_weight(agent_idx_i, agent_idx_j, weight)
:canonical: src.Network.push_back_neighbour_and_weight

```{autodoc2-docstring} src.Network.push_back_neighbour_and_weight
```

````

````{py:method} transpose()
:canonical: src.Network.transpose

```{autodoc2-docstring} src.Network.transpose
```

````

````{py:method} toggle_incoming_outgoing()
:canonical: src.Network.toggle_incoming_outgoing

```{autodoc2-docstring} src.Network.toggle_incoming_outgoing
```

````

````{py:method} switch_direction_flag()
:canonical: src.Network.switch_direction_flag

```{autodoc2-docstring} src.Network.switch_direction_flag
```

````

````{py:method} remove_double_counting()
:canonical: src.Network.remove_double_counting

```{autodoc2-docstring} src.Network.remove_double_counting
```

````

````{py:method} clear()
:canonical: src.Network.clear

```{autodoc2-docstring} src.Network.clear
```

````

````{py:method} get_agents_data(index=None)
:canonical: src.Network.get_agents_data

```{autodoc2-docstring} src.Network.get_agents_data
```

````

````{py:method} set_agents_data(index, opinion, activity=None, reluctance=None, velocity=None)
:canonical: src.Network.set_agents_data

```{autodoc2-docstring} src.Network.set_agents_data
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
