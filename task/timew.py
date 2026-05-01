# task/timew.py
import subprocess

def start(category, subcategory=None):
    tag = category.lower()
    if subcategory:
        tag += f"+{subcategory.lower().replace(' ', '_')}"
    subprocess.run(["timew", "start", tag])

def stop():
    subprocess.run(["timew", "stop"])