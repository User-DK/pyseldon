import pyseldon.seldoncore as pd
import pathlib as ptlb

def test_initial_network_settings_readwrite():
  network_settings = pd.InitialNetworkSettings()

  # default values
  assert network_settings.file is None
  assert network_settings.number_of_agents == 200
  assert network_settings.connections_per_agent == 10

  # set values
  base_dir = ptlb.Path(__file__).parent.resolve()
  file = str(base_dir / "res/network.txt")
  network_settings.file = file
  network_settings.number_of_agents = 100
  network_settings.connections_per_agent = 5

  # check values
  assert network_settings.file == file
  assert network_settings.number_of_agents == 100
  assert network_settings.connections_per_agent == 5