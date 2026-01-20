import os
from pathlib import Path
from shutil import rmtree



pasta_project = Path.cwd()
caminho_profiles = Path(pasta_project/"perfil_chrome")

def executar_limpeza(caminho_profiles: str = caminho_profiles):
    #caminho_profiles = Path(r"C:\Users\Pinheiro PC\Desktop\Programing\Automações GetLike\aplicativo\perfil_chrome")
    pastas_profiles = caminho_profiles.iterdir()
    for pasta in pastas_profiles:
        sub_pastas = Path(pasta).iterdir()
        for sub_pasta in sub_pastas:
            if sub_pasta.name == "Default":
                profile = Path(sub_pasta)
                arquivos_profile = profile.iterdir()
                for arquivo in arquivos_profile:
                    if arquivo.name == "Cache":
                        cache = Path(arquivo).iterdir()
                        for cache_data in cache:
                            if cache_data.name == "Cache_Data":
                                try:
                                    rmtree(cache_data)
                                    print(f"Deletei a pasta: {cache_data} do Profile {profile}")
                                except Exception as erro:
                                    print(f"Não foi possivel Excluir! Erro: {erro}")
                    if arquivo.name == "Code Cache":
                        code_cache = Path(arquivo).iterdir()
                        for pasta in code_cache:
                            try:
                                rmtree(pasta)
                                print(f"Deletei pasta: {pasta} dentro da pasta Code Cache")
                            except Exception as erro:
                                print(f"Não foi possivel excluir a pasta: {pasta} , erro: {erro}")
                                

def tamanho_pasta(caminho_profiles: str = caminho_profiles) -> int:
    total = 0
    for dirpath, dirnames, filenames in os.walk(caminho_profiles):
        for f in filenames:
            fp = Path(dirpath) / f
            try:
                total += fp.stat().st_size
            except FileNotFoundError:
                pass
    tamanho = total / (1024 ** 3)
    return tamanho
