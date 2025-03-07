import tkinter as tk
from tkinter import filedialog, messagebox
import hashlib
import time

class Pagina:
    def __init__(self, numero, registros):
        self.numero = numero
        self.registros = registros

class Bucket:
    def __init__(self, tamanho):
        self.registros = []
        self.tamanho = tamanho
        self.OVERFLOW: Bucket = None
    
    def inserir(self, chave, pagina):
        if len(self.registros) < self.tamanho:
            self.registros.append((chave, pagina))
            return True
        return False

class HashIndex:
    def __init__(self, num_buckets, fr):
        self.num_buckets = num_buckets
        self.buckets = [Bucket(fr) for _ in range(num_buckets)]
        self.colisoes = 0
        self.overflows = 0
    
    def funcao_hash(self, chave):
        return int(hashlib.md5(chave.encode()).hexdigest(), 16) % self.num_buckets
    
    def inserir(self, chave, pagina):
        idx = self.funcao_hash(chave)
        if not self.buckets[idx].inserir(chave, pagina):
            self.colisoes += 1
            self.overflows += 1  # Implementação de overflow pode ser melhorada
    
    def buscar(self, chave):
        idx = self.funcao_hash(chave)
        for k, p in self.buckets[idx].registros:
            if k == chave:
                return p
        return None

class Aplicacao:
    def __init__(self, root):
        self.root = root
        self.root.title("Índice Hash Estático")
        
        self.label = tk.Label(root, text="Insira a chave para busca:")
        self.label.pack()
        
        self.entrada_chave = tk.Entry(root)
        self.entrada_chave.pack()
        
        self.botao_busca = tk.Button(root, text="Buscar", command=self.buscar)
        self.botao_busca.pack()
        
        self.resultado = tk.Label(root, text="")
        self.resultado.pack()
        
        self.botao_table_scan = tk.Button(root, text="Table Scan", command=self.table_scan, state=tk.DISABLED)
        self.botao_table_scan.pack()
        
        self.index = HashIndex(1000, 5)
        self.paginas = []
        self.carregar_dados()
    
    def carregar_dados(self):
        with open("words.txt", "r") as f:
            palavras = f.read().splitlines()
        
        tam_pagina = 100  # Definido por usuário
        for i in range(0, len(palavras), tam_pagina):
            pagina = Pagina(i // tam_pagina, palavras[i:i+tam_pagina])
            self.paginas.append(pagina)
            for palavra in pagina.registros:
                self.index.inserir(palavra, pagina.numero)
    
    def buscar(self):
        chave = self.entrada_chave.get()
        if not chave:
            messagebox.showwarning("Erro", "Digite uma chave!")
            return
        
        inicio = time.time()
        resultado = self.index.buscar(chave)
        tempo_busca = time.time() - inicio
        
        if resultado is not None:
            self.resultado.config(text=f"Encontrado na página {resultado} em {tempo_busca:.6f}s")
        else:
            self.resultado.config(text="Chave não encontrada")
        
        self.botao_table_scan.config(state=tk.NORMAL)
    
    def table_scan(self):
        chave = self.entrada_chave.get()
        inicio = time.time()
        for pagina in self.paginas:
            if chave in pagina.registros:
                tempo_scan = time.time() - inicio
                self.resultado.config(text=f"Table Scan: Encontrado na página {pagina.numero} em {tempo_scan:.6f}s")
                return
        self.resultado.config(text="Table Scan: Chave não encontrada")

if __name__ == "__main__":
    root = tk.Tk()
    app = Aplicacao(root)
    root.mainloop()

