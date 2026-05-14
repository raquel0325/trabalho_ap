import subprocess

print("Limpando caches Python...")
print("-" * 40)

try:
    subprocess.run('powershell -Command "Get-ChildItem -Path . -Recurse -Directory -Filter \'__pycache__\' | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue"', shell=True)
    subprocess.run('powershell -Command "Get-ChildItem -Path . -Recurse -File -Filter \'*.pyc\' | Remove-Item -Force -ErrorAction SilentlyContinue"', shell=True)
    print("Limpeza concluída!")
except Exception as e:
    print(f"Erro: {e}")