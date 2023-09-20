<div align="center">

![banner]

</div>

# Rinha de compilers

Repositório com a solução desenvolvida em Python para o desafio da [rinha-de-compiler](https://github.com/aripiprazole/rinha-de-compiler)

## Para executar

Construa a imagem:

```bash
docker build -t rinha-compilers .
```

E rode-a:

```bash
docker run --rm rinha-compilers
```

ou setando um novo arquivo de entrada:

```bash
docker run --rm -v $(pwd)/files/fib.json:/var/rinha/source.rinha.json rinha-compilers         
```

[banner]: ./img/banner.png
