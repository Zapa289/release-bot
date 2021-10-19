class BuildNotification:
    DIVIDER = {'type': 'divider'}

    def __init__(self, build_info):
        self.branch = build_info.get('branch')
        self.platforms = build_info.get('platform')
        self.new_rom_version = build_info.get('new_rom_version')
        self.parent_version = build_info.get('parent_rom_version')
        self.rom_type = build_info.get('rom_type')
        self.user_email = build_info.get('user_email')
        self.release = build_info.get('release_build_enabled')
        self.sub_id = build_info.get('submission_id')

        self.raw_json = build_info
        
        self.timestamp = ''
        self.is_prereleased = False

    def get_build_message(self):
        return { 
            'ts': self.timestamp,
            'blocks' : [
                #self.START_TEXT,
                self.DIVIDER,
                self._get_build_info(),
                self.DIVIDER,
                self._get_MAT_Status(),
                self.DIVIDER
            ] 
        }

    def _get_MAT_Status(self):
        checkmark = ':x:'
        if self.is_prereleased:
            checkmark = ':white_check_mark:'

        text = f'*Pre-released to Morpheus* {checkmark} '
        return {
            'type': 'section',
            'text': {
                'type' : 'mrkdwn',
                'text': text
            }
        }
    
    def _get_build_info(self):
        if len(self.platforms) > 1:
            text = '*'
            for platform in self.platforms:
                if self.platforms.index(platform) != 0:
                    text += ', '
                text += f'{platform}'
            text += ' builds complete*\n'
        else: 
            text =  f'*{self.platforms[0]} build complete*\n'
        text = text + f'Build version: {self.new_rom_version}'
        return {
            'type': 'section',
            'text': {
                'type' : 'mrkdwn',
                'text'  : text
            }
        }

class BuildMessage:
    def __init__(self, build_message):
        pass

    def _store_build_message(self):
        pass

    def _get_build_message(self, platform, rom_version):
        pass