with open('data/config.ini') as cfg:
    cfg_lines = cfg.readlines()
    cfg_data: dict = {
        'api_id': int(cfg_lines[0].split(' = ')[1].rstrip()),
        'api_hash': cfg_lines[1].split(' = ')[1].rstrip(),
        'username': cfg_lines[2].split(' = ')[1].rstrip(),
        'bot_token': cfg_lines[3].split(' = ')[1].rstrip(),
        'buffer_group_id': int(cfg_lines[4].split(' = ')[1].rstrip()),
        'admin_id': int(cfg_lines[5].split(' = ')[1].rstrip())
    }
