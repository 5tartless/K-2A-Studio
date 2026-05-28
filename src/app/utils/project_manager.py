import requests, platform, shutil, subprocess, zipfile, io
from app.utils.exit_code import EXIT_CODES
from app.utils import file_manager as fm

fm.os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = "--disable-gpu"
fm.os.environ["QT_QPA_PLATFORM"] = "xcb"

APP_DEFAULT_SETTINGS = {
    "projects": [
        #{}, {}
    ],
    "rpid": -1,
}
PROJECT_DEFAULT_SETTINGS = {
    "path": None,
    "name": None,
    "pid": None,
    "ai-context-path": None,
    "github-url": None
}

app_config_folder = None
app_config_file = None
app_cache_folder = None

def setup():
    global app_cache_folder
    read_app_config()
    app_cache_folder = fm.os.path.join(get_cache_dir(), "k2a")
    if not fm.path_exists(app_cache_folder):
        fm.os.mkdir(app_cache_folder)

def read_app_config() -> object:
    global app_config_folder, app_config_file
    if not app_config_folder: app_config_folder = get_app_config_folder()
    if not app_config_file:   app_config_file = fm.os.path.join(app_config_folder, "config.json")

    if fm.path_exists(app_config_folder):
        try:
            return fm.read(app_config_file, True)
        except fm.json.decoder.JSONDecodeError:
            print("WARNING: File was corrupt, recreating app config.")
    else: #app settings is non existent
        fm.os.mkdir(app_config_folder)

    write_app_config(APP_DEFAULT_SETTINGS)
    return read_app_config()
def write_app_config(new):
    fm.write(app_config_file, new, indent=4)
def list_projects() -> list[dict]:
    app_config = read_app_config()
    return app_config["projects"]

def generate_project_id() -> int:
    app_config = read_app_config()
    return app_config["rpid"] + 1
def get_cache_dir() -> str:
    current_os = platform.system()

    if current_os == "Windows":
        return fm.Path(fm.os.environ.get('LOCALAPPDATA', fm.Path.home() /  'AppData/Local'))
    elif current_os == "Darwin":  # macOS
        return fm.Path.home() / 'Library/Caches'
    else:  # Linux and others
        return fm.Path(fm.os.environ.get('XDG_CACHE_HOME', fm.Path.home() / '.cache'))

def get_app_config_folder() -> str:
    current_os = platform.system()
    config_directory = ""
    if current_os == "Windows":
        config_directory = fm.Path(fm.os.environ.get('APPDATA'), fm.Path.home() / 'AppData/Roaming')
    elif current_os == "Darwin":
        config_directory = fm.Path.home() / 'Library/Application/Support'
    else:
        config_directory = fm.Path(fm.os.environ.get('XDG_CONFIG_HOME', fm.Path.home() / '.config'))
    return fm.os.path.join(config_directory, "k2a")

def repo_exists(url: str) -> bool:
    if "github.com" in url:
        if shutil.which("git") != None:
            return repo_exists_git(url)
        return repo_exists_api(url)
    return False

def repo_exists_git(url: str) -> bool: #git ls-remote
    env = fm.os.environ.copy()
    env["GIT_TERMINAL_PROMPT"] = "0"
    try:
        result = subprocess.run(
            ["git", "ls-remote", url],
            stdout=subprocess.DEVNULL,
            stdin=subprocess.DEVNULL,
            env=env,
            timeout=10
        )
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        return False

def repo_exists_api(url: str) -> bool:
    try:
        repo = url.rstrip("/").split("github.com/")[-1]
        api_url = f"https://api.github.com/repos/{repo}"
        response = requests.get(api_url, timeout=10)
        return response.status_code == 200
    except requests.RequestException:
        return False

def download_repo(url: str, destination: str):
    zip_endswith = "-main"
    zip_url = f"{url}/archive/refs/heads/main.zip"
    result = {
        "message": "",
        "path": None #if None then bad result
    }

    print(f"Downloading {zip_url}")
    try:
        response = requests.get(zip_url, timeout=30)
    
        if response.status_code != 200:
            zip_endswith = "-master"
            zip_url = f"{url}/archive/refs/heads/master.zip"
            response = requests.get(zip_url, timeout=30)
        elif response.status_code != 200:
            result["message"] = "Repo not found or branch not detected."
        else:        
            with zipfile.ZipFile(io.BytesIO(response.content)) as z:
                z.extractall(destination)
            
            result["path"] = fm.os.path.join(destination, url.split("/")[-1]+zip_endswith)
            result["message"] = "Repo successfully cloned."
            print(f"Extracted at {result['path']}")
    
    except requests.RequestException:
        result["message"] = "Check your internet conexion."
    
    return result

def get_parent_recursive(obj: object, recursions: int) -> object:
    for i in range(recursions):
        obj = obj.parent()
        if i == recursions:
            break
    return obj

def create_project(data: dict):
    file_content = read_app_config()
    data["pid"] = generate_project_id()
    file_content["rpid"] += 1
    file_content["projects"].append(data)
    write_app_config(file_content)

def is_project(path: str) -> bool:
    file_content = read_app_config()
    for project in file_content["projects"]:
        if project["path"] == path or project["github-url"] == path:
            return True
    return False

def import_local_project(path) -> str | None:
    if fm.path_exists(path):
        if is_project(path): #1 case: project is already registered.
            return "Project is already registered."
        else:                #2 case: project is not registered on config.json
            project: dict = PROJECT_DEFAULT_SETTINGS.copy()
            project["path"] = path
            project["name"] = "Untitled"
            create_project(project)
    else:
        return "Path is non-existent."

def import_github_project(url: str) -> str | None:
    message = ""
    if not is_project(url):
        if repo_exists(url):
            result = download_repo(url, app_cache_folder)
            message = result["message"]

            if result["path"]:
                project = PROJECT_DEFAULT_SETTINGS.copy()
                project_name = url.split("/")[-1]
                
                project["path"] = result["path"]
                project["name"] = project_name
                project["github-url"] = url
                create_project(project)
        else: 
            message = "Couldn't find GitHub repository."
    else:
        message = "The repo you are trying to clone is already in your projects."
    
    return message
