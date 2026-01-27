import os
import sys
import shutil

def get_file_size(file_path: str) -> int:
    """Retorna o tamanho do arquivo em bytes."""
    if os.path.exists(file_path):
        return os.path.getsize(file_path)
    return 0

def add_junk_data_to_exactly(file_path, desired_size_bytes, use_random=False):
    """Calcula a diferença e preenche o arquivo até atingir o tamanho exato em bytes."""
    current_size = get_file_size(file_path)
    if current_size >= desired_size_bytes:
        print(f"O arquivo já possui {current_size} bytes (Alvo: {desired_size_bytes}).")
        return
    bytes_to_add = desired_size_bytes - current_size
    print(f"Tamanho atual: {current_size} bytes. Faltam: {bytes_to_add} bytes.")
    # Chamamos a função de preenchimento passando a diferença exata
    add_junk_data(file_path, bytes_to_add, use_random)

def add_junk_data(file_path, bytes_to_add, use_random=False):
    """Adiciona uma quantidade específica de bytes ao final do arquivo."""
    chunk_size = 1024 * 1024  # 1MB por pedaço para eficiência
    print(f"Adicionando {bytes_to_add} bytes ao arquivo...")
    try:
        with open(file_path, "ab") as f:
            written_bytes = 0
            while written_bytes < bytes_to_add:
                remaining = bytes_to_add - written_bytes
                # Garante que não escreva mais do que o necessário no último pedaço
                actual_chunk = min(remaining, chunk_size)
                if use_random:
                    data = os.urandom(actual_chunk)
                else:
                    data = b'\x00' * actual_chunk
                f.write(data)
                written_bytes += actual_chunk
                # Progresso em porcentagem
                percent = int((written_bytes / bytes_to_add) * 100)
                print(f"Progresso: {percent}% ({written_bytes}/{bytes_to_add} bytes)", end='\r')
        print(f"\nSucesso! Arquivo finalizado com {get_file_size(file_path)} bytes.")
        
    except PermissionError:
        print("\nErro: Permissão negada ao tentar escrever no arquivo.")
    except Exception as e:
        print(f"\nErro inesperado: {e}")

if __name__ == "__main__":

    while True:
        print()
        original_path = input("Digite o path do arquivo original: ").strip('"') # Remove aspas se o user arrastar o arquivo
        if not os.path.exists(original_path):
            print(f"Erro: Arquivo '{original_path}' não encontrado.")
            continue
            
        copy_path = "modificado_" + os.path.basename(original_path)
        try:
            shutil.copy(original_path, copy_path)
            print(f"Cópia criada como: {copy_path}")
            break
        except Exception as e:
            print(f"Erro ao copiar: {e}")

    while True:
        print("\nEscolha uma das opções:")
        print("(1) - Adicionar X bytes ao final")
        print("(2) - Aumentar ATÉ atingir X bytes no total")
        try:
            option = int(input("Resposta (1 ou 2): "))
            if option in [1, 2]: break
            print("Opção inválida.")
        except ValueError:
            print("Por favor, digite um número inteiro.")

    while True:
        try:
            amount_bytes = int(input("\nQuantos Bytes? "))
            if amount_bytes > 0: break
            print("O valor deve ser maior que zero.")
        except ValueError:
            print("Por favor, digite um número inteiro.")

    # Correção da lógica booleana
    print("\nRandomizar Bytes? (S/N)")
    randomize_input = input("Resposta: ").strip().lower()
    randomize = randomize_input in ['s', 'sim', '1', 'y', 'yes']
    
    if option == 1:
        add_junk_data(copy_path, amount_bytes, randomize)
    elif option == 2:
        add_junk_data_to_exactly(copy_path, amount_bytes, randomize)