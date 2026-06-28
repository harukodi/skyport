import secrets, string, os, shutil
from vars import domain_name, xray_path
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from .DataStore import DataStore

BASE_DIR = Path(__file__).parent.parent.resolve()
CADDYFILE_TEMPLATE = BASE_DIR / "templates" / "caddyfile_template.j2"
OUTPUT_CADDYFILE = BASE_DIR / "caddy_config" / "Caddyfile"

S3_FACADE_CADDY_TEMPLATE = BASE_DIR / "templates" / "s3_facade_template.caddy.j2"
OUTPUT_S3_FACADE_CADDY = BASE_DIR / "caddy_config" / "s3_facade.caddy"
S3_RESPONSES_SRC_DIR = BASE_DIR / "templates" / "s3_responses"
S3_RESPONSES_DST_DIR = BASE_DIR / "caddy_config" / "s3_responses"

PATH_WORDS = [
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

class CaddyConfig:
    def __init__(self):
        self.env = Environment(
            loader=FileSystemLoader(BASE_DIR / "templates"), 
            trim_blocks=True, 
            lstrip_blocks=True
        )
        self.data_store = DataStore()
        self.frontend_path = self._generate_frontend_path()
        self.enable_skyport_ui = os.environ.get("SKYPORT_UI", "false").lower() == "true"

    def _generate_frontend_path(self):
        def _generate_salt(length: int):
            ascii_table = string.ascii_letters + string.digits
            salt = ''.join(secrets.choice(ascii_table) for i in range(length))
            return salt.lower()

        words = secrets.choice(PATH_WORDS)
        verb = secrets.choice(PATH_VERBS)
        adjective = secrets.choice(PATH_ADJECTIVES)
        frontend_path = f"{adjective}-{words}-{verb}-{_generate_salt(8)}"
        self.data_store.insert("frontend_path", frontend_path)

        return frontend_path

    def _copy_s3_facade_responses(self):
        shutil.copytree(S3_RESPONSES_SRC_DIR, S3_RESPONSES_DST_DIR, dirs_exist_ok=True)

    def _render_s3_facade_template(self):
        template = self.env.get_template(S3_FACADE_CADDY_TEMPLATE.name)
        result = template.render(
            s3_responses_dir=S3_RESPONSES_DST_DIR
        )
        with open(OUTPUT_S3_FACADE_CADDY, "w") as file:
            file.write(result)

    def _render_caddyfile_template(self):
        template = self.env.get_template(CADDYFILE_TEMPLATE.name)
        result = template.render(
            domain_name=domain_name, 
            xray_path=xray_path,
            frontend_path=self.data_store.get("frontend_path"),
            enable_skyport_ui=self.enable_skyport_ui,
            s3_facade_config=OUTPUT_S3_FACADE_CADDY
        )
        
        with open(OUTPUT_CADDYFILE, "w") as file:
            file.write(result)

    def generate_caddy_configs(self):
        self._copy_s3_facade_responses()
        self._render_s3_facade_template()
        self._render_caddyfile_template()