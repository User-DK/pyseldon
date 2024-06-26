import os
import pytest
import pyseldon as pd
import shutil

def test_run_simulation(capsys):
    # Set up the paths
    base_dir = os.getcwd()
    config_file = os.path.join(base_dir, "tests/config/conf.toml")
    network_file = os.path.join(base_dir, "tests/network/network.txt")
    invalid_config_file = os.path.join(base_dir, "tests/config/inconf.toml")
    output_dir1 = os.path.join(base_dir, "tests/outputs/outputfile")
    output_dir2 = os.path.join(base_dir, "tests/outputs/opwithnetwork")
    output_dir = os.path.join(base_dir, "output")
    
    if os.path.exists(output_dir1):
        shutil.rmtree(output_dir1)
    if os.path.exists(output_dir2):
        shutil.rmtree(output_dir2)

    # Test with output directory and config
    with capsys.disabled():
        pd.seldoncore.run_simulation(config_file, None, None, output_dir1)
    assert os.path.exists(output_dir1)
    assert os.listdir(output_dir1)

    # Test with network file
    with capsys.disabled():
        pd.seldoncore.run_simulation(config_file, None, network_file, output_dir2)
    assert os.path.exists(output_dir2)
    assert os.listdir(output_dir2)

    # Test with non-existent network file
    invalid_network_file = os.path.join(base_dir, "tests/network/net.txt")
    with pytest.raises(RuntimeError):
        with capsys.disabled():
            pd.seldoncore.run_simulation(config_file, None, invalid_network_file, None)

    # Test with invalid config file
    with pytest.raises(RuntimeError):
        with capsys.disabled():
            pd.seldoncore.run_simulation(invalid_config_file, None, None, None)

    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)

if __name__ == "__main__":
    pytest.main([__file__])
