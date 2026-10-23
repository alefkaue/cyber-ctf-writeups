# Write-ups de CTF — Alef Kaue Santos Nunes

Conquistei o **3º lugar geral no CTF da Faculdade SENAI São Caetano do Sul**, conforme informação
fornecida por mim. Os relatórios sustentam as atividades técnicas; não comprovam a classificação.
A competição teve categorias de redes, criptografia, web, OSINT e investigação técnica.

Os dois relatórios foram produzidos em dupla. Aqui estão resumos anonimizados e código didático
reconstruído com assistência de IA, sem atribuir autoria individual de toda a investigação.

- **Star Wars — concluído:** reconhecimento web, investigação de logs e parâmetros, autenticação
  fraca e RSA com módulo reduzido; flag final obtida no cenário acadêmico.
- **Among Us — parcial:** JWT, sessões, logs, esteganografia e assinatura RSA-PSS. A forja JWT
  investigada não funcionou na instância endurecida. O campo `trace_anchor` não foi confirmado;
  não houve obtenção da flag final.

```console
python -m ctf_lab rsa
python -m ctf_lab forensics
python -m ctf_lab jwt
python -m ctf_lab lsb
python -m unittest discover -s tests -v
```

Python 3.11+, sem dependências externas. Tudo funciona offline com exemplos sintéticos.
Não incluímos PDFs confidenciais, cookies, credenciais, endereços originais, chaves ou flags da prova.
As imagens mostram saídas das demonstrações reconstruídas. Veja os write-ups e a política de evidências.
