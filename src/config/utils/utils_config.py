import yaml
UTILS_CONFIGS_PATH = 'src/config/utils/utils.yml'


class UtilsConfig:
    INPUT_USERNAME_PROMPT = None
    INPUT_PASSWORD_PROMPT = None
    EMPTY_UNAME_FOUND = None
    EMPTY_PASSWORD_FOUND = None
    INPUT_ROUND_PROMPT = None
    VALID_INPUT = None
    YOUR_CHOICE = None
    SAFE_PASSWORD_PROMPT = None

    @classmethod
    def load(cls):
        with open(UTILS_CONFIGS_PATH, 'r') as f:
            data = yaml.safe_load(f)
            cls.INPUT_USERNAME_PROMPT = data['INPUT_USERNAME_PROMPT']
            cls.INPUT_PASSWORD_PROMPT = data['INPUT_PASSWORD_PROMPT']
            cls.EMPTY_UNAME_FOUND = data['EMPTY_UNAME_FOUND']
            cls.EMPTY_PASSWORD_FOUND = data['EMPTY_PASSWORD_FOUND']
            cls.INPUT_ROUND_PROMPT = data['INPUT_ROUND_PROMPT']
            cls.VALID_INPUT = data['VALID_INPUT']
            cls.YOUR_CHOICE = data['YOUR_CHOICE']
            cls.SAFE_PASSWORD_PROMPT = data['SAFE_PASSWORD_PROMPT']

