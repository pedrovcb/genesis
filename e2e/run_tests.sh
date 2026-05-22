#!/bin/bash
# Script para rodar testes E2E

set -e

echo "ARCA Gênesis - Testes E2E"
echo ""

echo "1. Verificando serviços..."
sleep 2

if ! curl -s http://localhost:3000 > /dev/null; then
    echo "ERRO: Frontend não está rodando em http://localhost:3000"
    echo "Execute: docker compose -f docker-compose.yml -f docker-compose.dev.yml up -d"
    exit 1
fi

if ! curl -s http://localhost:8000 > /dev/null; then
    echo "ERRO: Backend não está rodando em http://localhost:8000"
    echo "Execute: docker compose -f docker-compose.yml -f docker-compose.dev.yml up -d"
    exit 1
fi

echo "OK: Serviços online"
echo ""

echo "2. Rodando testes..."
echo ""

pytest tests/ -v --html=report.html --self-contained-html "$@"

echo ""
echo "SUCESSO: Testes completos"
echo "Relatorio: ./report.html"
