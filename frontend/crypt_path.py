import secrets, string

PATH_WORDS = [
    "fox", "wolf", "hawk", "bear", "crow", "lynx", "vole", "mink",
    "otter", "crane", "finch", "bison", "moose", "heron", "stoat",
    "kitty", "swift", "rook", "kite", "quail", "badger", "beaver",
    "ferret", "gecko", "iguana", "jaguar", "koala", "lemur", "llama",
    "marten", "newt", "panda", "quokka", "robin", "sable", "tapir",
    "viper", "walrus", "xerus", "yak", "zebu", "alpaca", "cow",
    "condor", "dingo", "egret", "falcon", "gibbon", "hyena", "impala",
    "jackal", "kakapo", "lark", "meerkat", "numbat", "ocelot", "puffin",
    "quetzal", "razorbill", "serval", "toucan", "uakari", "vulture",
    "wombat", "xeme", "yellowjacket", "zorilla", "aardvark", "booby",
    "capybara", "dugong", "echidna",
    "alice", "bella", "clara", "daisy", "ellie", "flora", "grace",
    "hazel", "iris", "julia", "kira", "luna", "mia", "nora", "olivia",
    "penny", "quinn", "rose", "stella", "tilda", "ursula", "violet",
    "willow", "xena", "yara", "zoe", "amber", "bonnie", "chloe",
    "diana", "eva", "fiona", "greta", "hannah", "isla", "jade",
    "karen", "lily", "maya", "nina", "ora", "petra", "rita", "sara",
    "tara", "uma", "vera", "wendy", "ximena", "yvette", "zelda",
    "aria", "brooke", "cora", "della", "eden", "freya", "gemma",
    "holly", "imogen", "juno", "kate", "lena", "mabel", "nell",
    "opal", "piper", "yon", "sonya", "moma", "jay", "milya", "molly",
]

def generate_path() -> str:
    def _generate_salt(length: int, only_letters: bool = False, only_numbers: bool = False):
        if only_letters:
            ascii_table = string.ascii_letters
        elif only_numbers:
            ascii_table = string.digits
        else:
            ascii_table = string.ascii_letters + string.digits

        salt = ''.join(secrets.choice(ascii_table) for i in range(length)).lower()
        return salt
    words = "-".join(secrets.choice(PATH_WORDS) for _ in range(3))
    return f"{words}-{_generate_salt(4, only_letters=True)}-{_generate_salt(4, only_numbers=True)}"

print(generate_path())