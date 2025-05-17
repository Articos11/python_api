import subprocess 

# Instala as dependências necessárias do projeto. 
# Como há o arquivo requirements, todos os requirementos serão puxados do arquivo txt. 
def dependencies():
    subprocess.run(['pip', 'install', '-r', 'requirements.txt'])
dependencies()