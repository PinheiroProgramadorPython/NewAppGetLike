from cryptography.fernet import Fernet
from pathlib import Path



def key_generator(caminho=r"./secrets/secret.key"):
    p = Path(caminho)
    if not p.parent.exists():
        p.parent.mkdir(parents=True, exist_ok=True)
    if not p.exists():
        key = Fernet.generate_key()
        p.write_bytes(key)
        print(f"Chave GERADA em: {p.resolve()}")
    else:
        print(f"Chave já existe em: {p.resolve()}")
        
        

def carregar_fernet(caminho=r"./secrets/secret.key") -> Fernet:
    if not Path(caminho).exists():
        key_generator(caminho)
    key = Path(caminho).read_bytes()
    return Fernet(key)





