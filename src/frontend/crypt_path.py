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

PATH_VERBS = [
    "runs", "leaps", "flies", "dives", "hunts", "rests", "hides", "waits",
    "calls", "swims", "climbs", "drifts", "glides", "roams", "stalks",
    "turns", "walks", "peers", "howls", "soars", "sniffs", "pads", "trots",
    "coils", "nests", "perches", "darts", "bolts", "lurks", "prowls",
    "wades", "barks", "chirps", "hoots", "yowls", "growls", "hisses",
    "gnaws", "burrows", "circles", "springs", "sprints", "slinks", "creeps",
    "pounces", "scurries", "gallops", "charges", "grazes", "scratches",
    "shrieks", "whistles", "stomps", "shuffles", "slithers", "scampers",
    "bounds", "swoops", "plunges", "thrashes", "scuttles", "wanders",
    "forages", "lingers",
]

PATH_ADJECTIVES = [
    "swift", "silent", "golden", "silver", "ancient", "hidden", "frozen",
    "wild", "dark", "bright", "hollow", "iron", "noble", "pale", "bold",
    "calm", "deep", "fair", "glad", "high", "keen", "lean", "mild",
    "neat", "pure", "rare", "safe", "tame", "vast", "warm", "wise",
    "cold", "damp", "fine", "hard", "kind", "loud", "nice", "rich",
    "slow", "tall", "wavy", "cozy", "dull", "epic", "flat", "good",
    "hazy", "icy", "jolly", "lush", "misty", "muddy", "rocky", "sandy",
    "shady", "sharp", "sleek", "slim", "sly", "soft", "stout", "stray",
    "sunny", "thick", "thin", "tiny", "tough", "true", "vague", "young",
    "azure", "beige", "blunt", "brash", "brave", "brisk", "broad", "brown",
]


def generate_path() -> str:
    def _generate_salt(length: int):
        ascii_table = string.ascii_letters + string.digits
        salt = ''.join(secrets.choice(ascii_table) for i in range(length))
        return salt.lower()
    
    words = secrets.choice(PATH_WORDS)
    verb = secrets.choice(PATH_VERBS)
    adjective = secrets.choice(PATH_ADJECTIVES)
    return f"{adjective}-{words}-{verb}-{_generate_salt(10)}"

print(generate_path())