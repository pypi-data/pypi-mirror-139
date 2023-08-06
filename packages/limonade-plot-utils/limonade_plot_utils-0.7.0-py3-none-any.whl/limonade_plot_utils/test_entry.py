from importlib.resources import files
import json

def test_entry():
    try:
        path_to_conf = (files('limonade_plot_utils')/'data/local_cfg.json')[0]
    except TypeError:
        path_to_conf = (files('limonade_plot_utils')/'data/local_cfg.json')
        
    with path_to_conf.open('r') as fil:
        local_cfg = json.load(fil)
        print(local_cfg)
    local_cfg['cfg_dir'] = 'C:/Users/03130100/Work Folders/tih/config'
    with path_to_conf.open('w') as fil:
        json.dump(local_cfg, fil)
    

if __name__ == '__main__':

    test_entry()
