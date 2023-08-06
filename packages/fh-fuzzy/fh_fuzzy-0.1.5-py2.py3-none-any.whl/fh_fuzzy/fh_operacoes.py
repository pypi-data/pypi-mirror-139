# -*- coding: utf-8 -*-
"""
Created on Mon Nov  1 11:02:08 2021

@author: Héber
"""

import matplotlib.pyplot as plt
import numpy as np 

from fh_fuzzy.fh_funcao_pertinencia import funcao_pertinencia

class operacoes:
    
    UNIAO = 1
    INTERSECAO = 0
    corte = 0
    
    funcao_pertinencia = funcao_pertinencia()
    
    
    def uniao(self, cA, cB, concentracaoA, concentracaoB):
        self.operacao_generica(cA.intervalo, 
                               cB.intervalo, 
                               self.UNIAO, 
                               True, 
                               True, 
                               concentracaoA, 
                               concentracaoB, 
                               'r',
                               'UNIÃO ({} e {})'.format(cA.nome, cB.nome))

    def uniao_not_A(self, cA, cB, concentracaoA, concentracaoB):
        self.operacao_generica(cA.intervalo, 
                               cB.intervalo, 
                               self.UNIAO, 
                               False, 
                               True, 
                               concentracaoA, 
                               concentracaoB, 
                               'r',
                               'UNIÃO ({} e {})'.format(cA.nome, cB.nome))

    def uniao_not_B(self, cA, cB, concentracaoA, concentracaoB):
        self.operacao_generica(cA.intervalo, 
                               cB.intervalo,
                               self.UNIAO, 
                               True, 
                               False, 
                               concentracaoA, 
                               concentracaoB, 
                               'r',
                               'UNIÃO ({} e {})'.format(cA.nome, cB.nome))
        
    def uniao_not_AB(self, cA, cB, concentracaoA, concentracaoB):
        self.operacao_generica(cA.intervalo, 
                               cB.intervalo, 
                               self.UNIAO, 
                               False, 
                               False, 
                               concentracaoA, 
                               concentracaoB, 
                               'r',
                               'UNIÃO ({} e {})'.format(cA.nome, cB.nome))

    def inter(self, cA, cB, concentracaoA, concentracaoB):
        self.operacao_generica(cA.intervalo, 
                               cB.intervalo, 
                               self.INTERSECAO, 
                               True, 
                               True, 
                               concentracaoA, 
                               concentracaoB, 
                               'r',
                               'INTERSECAO ({} e {})'.format(cA.nome, cB.nome))
    
    def inter_not_A(self, cA, cB, concentracaoA, concentracaoB):
        self.operacao_generica(cA.intervalo, 
                               cB.intervalo,
                               self.INTERSECAO, 
                               False, 
                               True, 
                               concentracaoA, 
                               concentracaoB, 
                               'r',
                               'INTERSECAO ({} e {})'.format(cA.nome, cB.nome))
    
    def inter_not_B(self, cA, cB, concentracaoA, concentracaoB):
        self.operacao_generica(cA.intervalo, 
                               cB.intervalo, 
                               self.INTERSECAO, 
                               True, 
                               False, 
                               concentracaoA, 
                               concentracaoB, 
                               'r',
                               'INTERSECAO ({} e {})'.format(cA.nome, cB.nome))
        
    def inter_not_AB(self, cA, cB, concentracaoA, concentracaoB):
        self.operacao_generica(cA.intervalo, 
                               cB.intervalo, 
                               self.INTERSECAO, 
                               False, 
                               False, 
                               concentracaoA, 
                               concentracaoB, 
                               'r',
                               'INTERSECAO ({} e {})'.format(cA.nome, cB.nome))
        
    

    
    def operacao_generica(self, cA, cB, uniao, notA, notB, concentA, concentB, style,titulo):

        passo = 99
        count = 0
        valor = []
        indic = []
        count = 0
        valor = []
        indic = []
        maior = self.funcao_pertinencia.maior(cA, cB)
        menor = self.funcao_pertinencia.menor(cA, cB)
        
        i = menor
        intervalo = np.linspace(menor, maior, passo)
        for i in intervalo:
        
            count += 1
            perA = 0
            perB = 0
            if len(cA)==3:
                perA = self.funcao_pertinencia.pertinenciaTri(cA, i)
            elif len(cA)==4:
                perA = self.funcao_pertinencia.pertinenciaTrap(cA, i)
            if len(cB)==3:
                perB = self.funcao_pertinencia.pertinenciaTri(cB, i)
            elif len(cB)==4:
                perB = self.funcao_pertinencia.pertinenciaTrap(cB, i)
            
            perA = self.concentracao(perA,concentA)
            perB = self.concentracao(perB,concentB)
            val = 0
            if uniao == 1:
                if perA >= perB:
                    val = perA if notA else 1 - perA
                else:
                    val = perB if notB else 1 - perB
            else:
                if perA <= perB:
                    val = perA if notA else 1 - perA
                else:
                    val = perB if notB else 1 - perB

            valor.append(val)
            indic.append(i)
        plt.title(titulo)    
        plt.plot(indic, valor, style)
        plt.show()


    LARSEN = 4
    MANDANI = 9
    MAX = 19
    INTERCESSAO = 0
    LUKASIEWICZ = 17
    GODEL = 20
    GAMES = 21
    MI = 22
    KLEENE = 16
    CILINDRICA = 23
   
    def implicacao_kleene(self, cA, cB):
        self.operacao_generica2(cA.intervalo, 
                                cB.intervalo, 
                                self.UNIAO, 
                                True, 
                                True, 
                                1, 
                                1, 
                                self.KLEENE,
                                'IMPLICAÇÃO ({} e {}) KLEENE'.format(cA.nome, cB.nome))

    
    def implicacao_godel(self, cA, cB):
        self.operacao_generica2(cA.intervalo, 
                                cB.intervalo, 
                                self.UNIAO, 
                                True, 
                                True, 
                                1, 
                                1, 
                                self.GODEL,
                                'IMPLICAÇÃO ({} e {}) GODEL'.format(cA.nome, cB.nome))

    def implicacao_games(self, cA, cB):
        self.operacao_generica2(cA.intervalo, 
                                cB.intervalo, 
                                self.UNIAO, 
                                True, 
                                True, 
                                1, 
                                1, 
                                self.GAMES,
                                'IMPLICAÇÃO ({} e {}) GAMES'.format(cA.nome, cB.nome))

    def implicacao_mi(self, cA, cB):
        self.operacao_generica2(cA.intervalo, 
                                cB.intervalo, 
                                self.UNIAO, 
                                True, 
                                True, 
                                1, 
                                1, 
                                self.MI,
                                'IMPLICAÇÃO ({} e {}) MI'.format(cA.nome, cB.nome))

    def implicacao_lukasiewicz(self, cA, cB):
        self.operacao_generica2(cA.intervalo, 
                                cB.intervalo, 
                                self.UNIAO, 
                                True, 
                                True, 
                                1, 
                                1, 
                                self.LUKASIEWICZ,
                                'IMPLICAÇÃO ({} e {}) LUKASIEWICZ'.format(cA.nome, cB.nome))

    def uniao_mandani(self, cA, cB):
        return self.operacao_generica2(cA.intervalo, 
                                cB.intervalo, 
                                self.UNIAO, 
                                True, 
                                True, 
                                1, 
                                1, 
                                self.MANDANI,
                                'UNIÃO ({} e {}) MANDANI'.format(cA.nome, cB.nome))
        
    def uniao_larsen(self, cA, cB):
        self.operacao_generica2(cA.intervalo, 
                                cB.intervalo, 
                                self.UNIAO, 
                                True, 
                                True, 
                                1, 
                                1, 
                                self.LARSEN,
                                'UNIÃO ({} e {}) LARSEN'.format(cA.nome, cB.nome))
    
    MUITO = 2
    MAIS = 1.5
    MENOS = 0.75
    MAIS_OU_MENOS = 0.5
    LEVEMENTE = -1
    NORMAL = 1
    
    def uniao_larsen_ling(self, cA, cB,conA, conB):
        self.operacao_generica2(cA.intervalo, 
                                cB.intervalo, 
                                self.UNIAO, 
                                True, 
                                True, 
                                conA, 
                                conB, 
                                self.LARSEN,
                                'UNIÃO ({} e {}) LARSEN'.format(cA.nome, cB.nome))   
        
    def disjuncao(self, cA, cB):
        self.operacao_generica2(cA.intervalo, 
                                cB.intervalo, 
                                self.UNIAO, 
                                True, 
                                True, 
                                1, 
                                1, 
                                self.MAX,
                                'DISJUNÇÃO ({} e {})'.format(cA.nome, cB.nome))


    def extencao_cilindrica(self, c, concentracao, universo):
        passo = 99
        cA = c.intervalo
        nome = c.nome
        maiorA = universo[1]
        menorA = universo[0]
        maiorB = universo[1]
        menorB = universo[0]
       
        pertA = []
        
        valA = []
        
        rangeA = np.linspace(maiorA, menorA, passo)
        for i in rangeA:
            valA.append(i)
            perA = 0
            if len(cA)==3:
                perA = self.funcao_pertinencia.pertinenciaTri(cA, i)
            elif len(cA)==4:
                perA = self.funcao_pertinencia.pertinenciaTrap(cA, i)   
            elif len(cA)==2:
                perA = self.funcao_pertinencia.pertinenciaGaussiana(cA, i)
            perA = self.concentracao(perA,concentracao)
        
            pertA.append(perA)
            
            
        matriz_juncao = []
        for a in pertA:
            matriz = []
            for b in pertA:
                val = a 
                matriz.append(val)
            matriz_juncao.append(matriz)
            
            
        matriz_juncao = np.array(matriz_juncao)    
        pertA, pertB = np.meshgrid(pertA, pertA)
        valA, valB = np.meshgrid(valA, valA)
    
        
        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')
        ax.plot_surface(valA, valB, matriz_juncao,cmap='viridis')
        plt.title('EXTENÇÃO CILINDRICA DO CONJUNTO {}'.format(nome))
        plt.show()   
        return matriz_juncao
       

    def concentracao(self, v, c):
        if c > 0:
            return v**c
        elif c == -1:

            return min((v/2), 1-(v**2))
        elif c == -2:
            if v <= 0.5:
                return 0
            else:
                return 0

    def operacao_generica2(self, cA, cB, uniao, notA, notB, concentA, concentB, norma,titulo):
        passo = 99
        
        maiorA = 0
        menorA = 0
        maiorB = 0
        menorB = 0
        
        corte_gauss = 2.3        
        if(len(cA)==2):
            maiorA = cA[0] + (cA[1] * corte_gauss)
            menorA = cA[0] - (cA[1] * corte_gauss)
        else:            
            maiorA = self.funcao_pertinencia.maior(cA, cA)
            menorA = self.funcao_pertinencia.menor(cA, cA)
        
        
        if(len(cB)==2):
            maiorB = cB[0] + (cB[1] * corte_gauss)
            menorB = cB[0] - (cB[1] * corte_gauss)
        else: 
            maiorB = self.funcao_pertinencia.maior(cB, cB)
            menorB = self.funcao_pertinencia.menor(cB, cB)
        
            
        
        pertA = []
        pertB = []
        
        valA = []
        valB = []
        
        rangeA = np.linspace(maiorA, menorA, passo)
        rangeB = np.linspace(maiorB, menorB, passo)
    
        for i in rangeA:
            valA.append(i)
            perA = 0
            if len(cA)==3:
                perA = self.funcao_pertinencia.pertinenciaTri(cA, i)
            elif len(cA)==4:
                perA = self.funcao_pertinencia.pertinenciaTrap(cA, i)   
            elif len(cA)==2:
                perA = self.funcao_pertinencia.pertinenciaGaussiana(cA, i)
            perA = self.concentracao(perA,concentA)
        
            pertA.append(perA)
            
            
        for i in rangeB:
            valB.append(i)
            perB = 0
            if len(cB)==3:
                perB = self.funcao_pertinencia.pertinenciaTri(cB, i)
            elif len(cB)==4:
                perB = self.funcao_pertinencia.pertinenciaTrap(cB, i) 
            elif len(cB)==2:
                perB = self.funcao_pertinencia.pertinenciaGaussiana(cB, i)
            perB = self.concentracao(perB,concentB)

        
            pertB.append(perB)
            
            
        matriz_juncao = []
        for a in pertA:
            matriz = []
            for b in pertB:
                val = 0
                if uniao == 1:
                    if a >= b:
                        val = a if not a else 1 - a
                    else:
                        val = b if not b else 1 - b
                else:
                    if a <= b:
                        val = a if not a else 1 - a
                    else:
                        val = b if not b else 1 - b
                        
                        
                if norma == 14:
                    val = a + b - (a*b)
                    
                if norma == 18:
                    if b == 0:
                        val = a
                    elif a == 0:
                        val = b
                    else:
                        val = 1      
                        
                if norma == self.GODEL:
                    if b >= a:
                        val = 1
                    else:
                        val = b
                
                if norma == self.GAMES:
                    if b >= a:
                        val = 1
                    else:
                        val = 0
                        
                if norma == self.MI:
                    if b >= a:
                        val = 1
                    else:
                        val = b/a
                        
                if norma == self.KLEENE:
                    val = max(1-a, b)

                if norma == self.LUKASIEWICZ:
                    val = min(1, 1-(a*b))
                    
                if norma == self.MAX:
                    val = max(a,b)
                                                            
                if norma == self.LARSEN:
                    val = a * b
                    
                if norma == self.MANDANI:
                    val = min(a,b)
                    
                if norma == 8:
                    if b == 1:
                        val = a
                    elif a == 1:
                        val = b
                    else:
                        val = 0
    
                if self.corte > 0:
                    if val >= self.corte:
                        val = 1
                    else:
                        val = 0
                    
                matriz.append(val)
            matriz_juncao.append(matriz)
            
            
        matriz_juncao = np.array(matriz_juncao)    
        pertA, pertB = np.meshgrid(pertA, pertB)
        valA, valB = np.meshgrid(valA, valB)
    
        
        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')
        ax.plot_surface(valB, valA, matriz_juncao,cmap='viridis')
        plt.title(titulo)
        plt.show()   
        
        
    def intersesco_regra(self, cA, cB, cC, c, universo):
        return self.operacao_generica_regra(cA.intervalo, 
                                     cB.intervalo, 
                                     cC, 
                                     self.UNIAO, 
                                     True, 
                                     True, 
                                     1, 
                                     1,
                                     c,
                                     self.LARSEN,
                                     universo,
                                     'INTESEÇÃO {} -> {} = {} '.format(cA.nome, cB.nome, cC.nome))

    def intersesco_regra_ling(self, cA, cB, cC, concentA, concentB, concentC, universo):
        return self.operacao_generica_regra(cA.intervalo, 
                                     cB.intervalo, 
                                     cC, 
                                     self.UNIAO, 
                                     True, 
                                     True, 
                                     concentA, 
                                     concentB,
                                     concentC,
                                     self.LARSEN,
                                     universo,
                                     'INTESEÇÃO {} -> {} = {} '.format(cA.nome, cB.nome, cC.nome))
    

        
    def operacao_generica_regra(self, cA, cB, cC, uniao, notA, notB, concentA, concentB, concentC, norma, universo, titulo):
        passo = 99
        
        maiorA = 0
        menorA = 0
        maiorB = 0
        menorB = 0
                
        corte_gauss = 2.3        
        if(len(cA)==2):
            maiorA = cA[0] + (cA[1] * corte_gauss)
            menorA = cA[0] - (cA[1] * corte_gauss)
        else:            
            maiorA = self.funcao_pertinencia.maior(cA, cA)
            menorA = self.funcao_pertinencia.menor(cA, cA)
  
        if(len(cB)==2):
            maiorB = cB[0] + (cB[1] * corte_gauss)
            menorB = cB[0] - (cB[1] * corte_gauss)
        else: 
            maiorB = self.funcao_pertinencia.maior(cB, cB)
            menorB = self.funcao_pertinencia.menor(cB, cB)
        
        
        pertA = []
        pertB = []
        
        valA = []
        valB = []
        
        
        rangeA = np.linspace(maiorA, menorA, passo)
        rangeB = np.linspace(maiorB, menorB, passo)
    
        for i in rangeA:
            valA.append(i)
            perA = 0
            if len(cA)==3:
                perA = self.funcao_pertinencia.pertinenciaTri(cA, i)
            elif len(cA)==4:
                perA = self.funcao_pertinencia.pertinenciaTrap(cA, i)   
            elif len(cA)==2:
                perA = self.funcao_pertinencia.pertinenciaGaussiana(cA, i)
            perA = self.concentracao(perA,concentA)
        
            pertA.append(perA)
            
            
        for i in rangeB:
            valB.append(i)
            perB = 0
            if len(cB)==3:
                perB = self.funcao_pertinencia.pertinenciaTri(cB, i)
            elif len(cB)==4:
                perB = self.funcao_pertinencia.pertinenciaTrap(cB, i) 
            elif len(cB)==2:
                perB = self.funcao_pertinencia.pertinenciaGaussiana(cB, i)
            perB = self.concentracao(perB,concentB)
        
            pertB.append(perB)
            
        matriz_juncao = []
        for a in pertA:
            matriz = []
            for b in pertB:
                val = 0
                if uniao == 1:
                    if a >= b:
                        val = a if not a else 1 - a
                    else:
                        val = b if not b else 1 - b
                else:
                    if a <= b:
                        val = a if not a else 1 - a
                    else:
                        val = b if not b else 1 - b
                        
                        
                if norma == 14:
                    val = a + b - (a*b)
                    
                if norma == 18:
                    if b == 0:
                        val = a
                    elif a == 0:
                        val = b
                    else:
                        val = 1      
                        
                if norma == self.GODEL:
                    if b >= a:
                        val = 1
                    else:
                        val = b
                
                if norma == self.GAMES:
                    if b >= a:
                        val = 1
                    else:
                        val = 0
                        
                if norma == self.MI:
                    if b >= a:
                        val = 1
                    else:
                        val = b/a
                        
                if norma == self.KLEENE:
                    val = max(1-a, b)
        
                if norma == self.LUKASIEWICZ:
                    val = min(1, 1-(a*b))
                    
                if norma == self.MAX:
                    val = max(a,b)
                                                            
                if norma == self.LARSEN:
                    val = a * b
                    
                if norma == self.MANDANI:
                    val = min(a,b)
                    
                if norma == self.CILINDRICA:
                    val = a
        
                if norma == 8:
                    if b == 1:
                        val = a
                    elif a == 1:
                        val = b
                    else:
                        val = 0
        
                if self.corte > 0:
                    if val >= self.corte:
                        val = 1
                    else:
                        val = 0
                    
                matriz.append(val)
            matriz_juncao.append(matriz)
            

        matriz_juncao = np.array(matriz_juncao)    
        pertA, pertB = np.meshgrid(pertA, pertB)
        valA, valB = np.meshgrid(valA, valB)
        
        matriz2 = self.extencao_cilindrica(cC,concentC,universo)
        
        
        for i in range(len(matriz2)):
            for j in range(len(matriz2[i])):
                matriz_juncao[i][j]  = min(matriz2[i][j],matriz_juncao[i][j])

 
        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')
        ax.plot_surface(valB, valA, matriz_juncao,cmap='viridis')
        plt.title(titulo+' com a EC')
        plt.show()   
        
        return matriz_juncao
  
    def regras_superficie(self, regras):
        
        rangeX = np.linspace(1, 100, 99)
        rangeY = np.linspace(1, 2, 99)
    
        rangeX, rangeY = np.meshgrid(rangeX, rangeY)

        m = np.zeros((len(regras[0]),len(regras[0])))
        t = len(regras[0])
        cont = 0
        for l in range(t):
            for c in range(t):
                valores = []
                for r in range(len(regras)):
                    valores.append(regras[r][l][c])
                m[l][c] = max(valores)

        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')
        ax.plot_surface(rangeX, rangeY, m,cmap='viridis')
        plt.title('Superfície de Regras')
        plt.show()   
        