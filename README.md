# Projeto-BD
Cadeira de projetos de Banco de Dados

Diagrama Sequencial

    participant U as Usuário
    participant I as Interface (DOM)
    participant A as Aplicação
    participant H as HashIndex
    participant B as Bucket
    participant P as Página
    
    Note over U,P: Inicialização
    U->>I: Carrega a página
    I->>A: Evento DOMContentLoaded
    A->>A: Inicializar()
    A->>A: carregarDadosExemplo()
    A->>I: adicionarLog("Sistema inicializado")

    Note over U,P: Configuração do Índice
    alt Carregar Arquivo
        U->>I: Clica em "Carregar Arquivo"
        I->>A: Evento click
        A->>I: arquivoInput.click()
        U->>I: Seleciona arquivo
        I->>A: Evento change
        A->>A: carregarArquivo(e)
        A->>I: adicionarLog("Arquivo carregado")
    end

    U->>I: Ajusta parâmetros (tamanho da página, etc.)
    U->>I: Clica em "Construir Índice"
    I->>A: Evento click
    A->>A: construirIndice()
    A->>A: Validar configuração
    A->>A: Calcular parâmetros (NB, FR, etc.)
    A->>H: new HashIndex(NB, FR)
    loop Para cada página
        A->>P: new Pagina(numero, registros)
        loop Para cada palavra na página
            A->>H: inserir(palavra, paginaNum, posição)
            H->>H: funcao_hash(chave)
            H->>B: inserir(chave, pagina, posicao)
            alt Bucket cheio
                B->>B: new Bucket(tamanho) para overflow
                H->>H: colisoes++
                H->>H: overflows++
            end
        end
    end
    A->>A: atualizarEstatisticas()
    A->>I: Atualizar interface com estatísticas
    A->>I: Habilitar botões de busca
    A->>I: adicionarLog("Índice construído")

    Note over U,P: Busca por Hash
    U->>I: Insere chave de busca
    U->>I: Clica em "Buscar por Hash"
    I->>A: Evento click
    A->>A: buscar()
    A->>I: adicionarLog("Buscando por hash")
    A->>H: buscar(chave)
    H->>H: funcao_hash(chave)
    H->>B: buscar(chave)
    alt Chave encontrada
        B-->>H: Retorna {pagina, posicao}
        H-->>A: Retorna {resultado, bucketIndex}
        A->>I: Atualizar resultado de busca
        A->>A: mostrarPagina(pagina)
        A->>I: Exibir detalhes do registro e página
        A->>I: adicionarLog("Registro encontrado")
    else Chave não encontrada
        B-->>H: Retorna null
        H-->>A: Retorna {resultado: null, bucketIndex}
        A->>I: Atualizar resultado (não encontrado)
        A->>I: adicionarLog("Chave não encontrada")
    end

    Note over U,P: Table Scan
    U->>I: Insere chave de busca
    U->>I: Clica em "Table Scan"
    I->>A: Evento click
    A->>A: tableScan()
    A->>I: adicionarLog("Realizando table scan")
    loop Para cada página
        A->>P: Verifica se a chave existe na página
        alt Chave encontrada
            P-->>A: Retorna {pagina, posicao}
            A->>I: Atualizar resultado de busca
            A->>A: mostrarPagina(paginaEncontrada)
            A->>I: Exibir detalhes do registro e página
            A->>I: adicionarLog("Registro encontrado por table scan")
            break
        end
    end
    alt Nenhuma chave encontrada
        A->>I: Atualizar resultado (não encontrado)
        A->>I: adicionarLog("Table scan: Chave não encontrada")
    end

    Note over U,P: Navegação entre Páginas
    alt Próxima Página
        U->>I: Clica em "Próxima >"
        I->>A: Evento click
        A->>A: mostrarProximaPagina()
        A->>A: mostrarPagina(paginaAtualIdx + 1)
        A->>I: Atualizar visualização da página
    else Página Anterior
        U->>I: Clica em "< Anterior"
        I->>A: Evento click
        A->>A: mostrarPaginaAnterior()
        A->>A: mostrarPagina(paginaAtualIdx - 1)
        A->>I: Atualizar visualização da página
    end
