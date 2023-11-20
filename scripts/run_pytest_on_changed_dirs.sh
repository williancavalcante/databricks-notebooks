#!/bin/bash

# Tenta obter a lista de diretórios modificados, fallback para todos os diretórios se falhar
dirs=$(git diff --name-only HEAD HEAD~ | grep '\.py$' | xargs -n 1 dirname | sort -u) || dirs=$(find . -type f -name "*.py" | xargs -n 1 dirname | sort -u)

# Executar pytest em cada diretório identificado
for dir in $dirs; do
    if [[ -d $dir ]]; then
        # Substituir '/' por '-' para criar um nome de arquivo válido
        filename=$(echo $dir | sed 's/\//-/g')

        # Gerar um arquivo XML único para cada diretório
        pytest --junitxml="unit-testresults-${filename}.xml" $dir
    fi
done
