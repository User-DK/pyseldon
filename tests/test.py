import pathlib as ptlb
# import os
import pytest
import pyseldon as pd
import shutil

def test_run_simulation(capsys):
    # Set up the paths
    base_dir = ptlb.Path(__file__).parent.resolve()
    config_file = str(base_dir / "config/conf.toml")
    network_file = str(base_dir / "network/network.txt")
    invalid_config_file = str(base_dir / "config/inconf.txt")
    output_dir1 = str(base_dir / "outputs/outputfile")
    output_dir2 = str(base_dir / "outputs/opwithnetwork")
    output_dir = str(base_dir / "outputs/output")
    
    if ptlb.Path(output_dir1).exists():
        shutil.rmtree(output_dir1)
    if ptlb.Path(output_dir2).exists():
        shutil.rmtree(output_dir2)

    # Test with output directory and config
    with capsys.disabled():
        pd.seldoncore.run_simulation(config_file,None, None, None, output_dir1)
    assert ptlb.Path(output_dir1).exists()
    assert ptlb.Path(output_dir1).is_dir()

    # Test with network file
    with capsys.disabled():
        pd.seldoncore.run_simulation(config_file,None, None, network_file, output_dir2)
    assert ptlb.Path(output_dir2).exists()
    assert ptlb.Path(output_dir2).is_dir()

    # Test with non-existent network file
    invalid_network_file = str(ptlb.Path(base_dir, "tests/network/net.txt"))
    with pytest.raises(RuntimeError):
        with capsys.disabled():
            pd.seldoncore.run_simulation(config_file,None, None, invalid_network_file, None)

    # Test with invalid config file
    with pytest.raises(RuntimeError):
        with capsys.disabled():
            pd.seldoncore.run_simulation(invalid_config_file,None, None, None, None)

    if ptlb.Path(output_dir).exists():
        shutil.rmtree(output_dir)

def test_settings():
    degroot_settings = pd.seldoncore.DeGrootSettings()
    output_settings = pd.seldoncore.OutputSettings()
    deffuant_settings = pd.seldoncore.DeffuantSettings()
    activitydriven_settings = pd.seldoncore.ActivityDrivenSettings()
    activitydriveninertial_settings = pd.seldoncore.ActivityDrivenInertialSettings()
    initial_network_settings = pd.seldoncore.InitialNetworkSettings()

    assert degroot_settings is not None
    assert output_settings is not None
    assert deffuant_settings is not None
    assert activitydriven_settings is not None
    assert activitydriveninertial_settings is not None
    assert initial_network_settings is not None
    assert activitydriveninertial_settings.covariance_factor == 0.0

# def test_network():
#     degroot_network = pd.seldoncore.DeGrootNetwork()
#     deffuant_network = pd.seldoncore.DeffuantNetwork()
#     activitydriven_network = pd.seldoncore.ActivityDrivenNetwork()
#     activitydriveninertial_network = pd.seldoncore.InertialNetwork()
    
#     assert degroot_network is not None
#     assert deffuant_network is not None
#     assert activitydriven_network is not None
#     assert activitydriveninertial_network is not None

def test_simulation_with_simulationOptions():
    degroot_settings = pd.seldoncore.DeGrootSettings()
    output_settings = pd.seldoncore.OutputSettings()
    initial_network_settings = pd.seldoncore.InitialNetworkSettings()
    simulation_options = pd.seldoncore.SimulationOptions()
    simulation_options.model_string = "DeGroot"
    simulation_options.rng_seed = 1
    simulation_options.output_settings = output_settings
    simulation_options.model_settings = degroot_settings
    simulation_options.network_settings = initial_network_settings

    base_dir = ptlb.Path(__file__).parent.resolve()
    output_dir = str(base_dir / "outputs/output")

    pd.seldoncore.run_simulation(None, simulation_options, None, None, output_dir)
    assert ptlb.Path(output_dir).exists()
    # shutil.rmtree(output_dir)

if __name__ == "__main__":
    pytest.main([__file__])