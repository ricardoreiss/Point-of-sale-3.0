from cx_Freeze import setup, Executable

executables = [Executable("index.py", base="Win32GUI", icon="logo.ico")]

setup(
    name="AutoMecNotas",
    version="1.0",
    description="AutoMecNotas1.0",
    executables=executables,
    options={
        "build_exe": {
            "include_files": ["AUTOMEC.png", "logo.ico"]
        }
    }
)
