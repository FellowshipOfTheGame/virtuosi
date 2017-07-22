Virtuosi
========
Seja um virtuoso tocando músicas eruditas em seu violino.

Para jogar
----------
Execute uma das releases correspondentes ao seu sistema operacional, disponíveis em https://github.com/FellowshipOfTheGame/virtuosi/releases

OU

- Instale python versão 2.7 OU mais recente (http://www.python.org/getit/)
- Instale pygame, com versão correspondente à sua versão do python
  (http://www.pygame.org/download.shtml, ou pelo comando `pip install pygame`)
- Execute: `python main.py`

Para gerar releases
-------------------
`python setup.py build`

Notas
-----
- Em Windows, pygame só funciona usando python2 x86, mesmo em máquinas x86-64
- Em Linux e MacOSX pode ser necessario executar como administrador
- No Linux, instale o timidity++ e algum SoundFont, como Freepats
  (http://freepats.zenvoid.org/) ou Fluidr3 para sair som.
