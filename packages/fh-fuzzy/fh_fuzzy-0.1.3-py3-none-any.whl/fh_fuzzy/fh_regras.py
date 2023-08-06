# -*- coding: utf-8 -*-
"""
Created on Thu Nov 18 18:19:56 2021

@author: Héber
"""

import matplotlib.pyplot as plt
import numpy as np 

from fh_fuzzy.fh_funcao_pertinencia import funcao_pertinencia

class regras:
    PASSO = 101
    REGRA_E  = 'E'
    REGRA_OU = 'OU'
    E_MIN  = 0
    E_PROD = 1
    OU_MAX = 2
    SEMANTICA_MIN = 0
    SEMANTICA_PROD = 1
    DEFUZIFICACAO_CENTROID = 7
    DEFUZIFICACAO_MOM  = 8
    PLOT_DEFUZZY = True
    MAMDANI = True
    SUGENO = False
    
    #Configurações default
    E  = E_MIN
    OU = OU_MAX    
    DEFUZIFICACAO = DEFUZIFICACAO_CENTROID
    SEMANTICA = SEMANTICA_MIN
    REGRA = MAMDANI

    
    def __init__(self, antecedentes, consequentes):
        self.antecedentes = antecedentes 
        self.consequentes = consequentes 
        self.funcao_pertinencia = funcao_pertinencia()
        self.regras = []
        self.valores = []
        self.v_pertinencias = []
        self.pertinencias_regra = []
        self.indices = []
        self.consequentes_valores = []
        self.inferencia_sugeno = 0
        
    
    def inserir_regra_e(self, antecedente, consequente):
        self.regras.append([self.REGRA_E,antecedente, consequente])

    def inserir_regra_ou(self, antecedente, consequente):
        self.regras.append([self.REGRA_OU, antecedente, consequente])
        
    def defuzzyficacao(self):
        self.v_pertinencias = []
        self.pertinencias_regra = []
        self.indices = []
        self.consequentes_valores = []
        
        self.agregacao_antecedentes()
        
        resultado = 0
        
        if self.REGRA == self.MAMDANI:
            self.agregacao_regras()
            
            if self.DEFUZIFICACAO == self.DEFUZIFICACAO_CENTROID:
                resultado = self.centroid()
            elif self.DEFUZIFICACAO == self.DEFUZIFICACAO_MOM:
                resultado = self.mom()
                
            if self.PLOT_DEFUZZY:
                plt.fill_between(self.indices, self.pertinencias_regra)
                plt.ylim(0, 1)
                plt.plot((resultado, resultado), (0, 1), 'r',linewidth=7)
                plt.show()
            return resultado
        elif self.REGRA == self.SUGENO:
            if self.PLOT_DEFUZZY:
                plt.ylim(0,1)
                plt.plot((self.inferencia_sugeno, self.inferencia_sugeno), (0, 1), 'r',linewidth=7)
                for i in range(len(self.indices)):
                    plt.plot((self.indices[i], self.indices[i]), (0, self.v_pertinencias[i]), 'b', linewidth=7)
                plt.show()
            return self.inferencia_sugeno
        
    
    def centroid(self):
        #print('centroid')
        a = 0
        b = 0
        for i in range(len(self.indices)):
            a = a + self.indices[i]*self.pertinencias_regra[i]
            b = b + self.pertinencias_regra[i]
        if b == 0:
            return 0
        else:
            inferencia = a/b
        #print('inferência: ',inferencia)
        return inferencia
    
    def mom(self):
        inferencia = 0
        maior = max(self.pertinencias_regra)
        qtde = 0
        soma = 0
        #iss = []
        for i in range(len(self.indices)):
            if self.pertinencias_regra[i] == maior:
                qtde += 1
                soma += self.indices[i]
                #iss.append(self.indices[i])
        
        #inferencia = iss[int(len(iss)/2)]
        inferencia = soma/qtde
        
        return inferencia
    
    def agregacao_regras(self):
        self.pertinencias_regra = []
        for j in range(len(self.v_pertinencias[0])):
            m = []
            for i in range(len(self.v_pertinencias)):
                  m.append(self.v_pertinencias[i][j]) 
            self.pertinencias_regra.append(max(m))
    
    def semantica_regras(self,C,maxi):
        minimo = []
        maximo = []
        for m in self.consequentes_valores:
            minimo.append(min(m[0]))
            maximo.append(max(m[0]))
        
        t_min = min(minimo)
        t_max = max(maximo)

        t_min = self.consequentes[0].intervalo_total[0]
        t_max = self.consequentes[0].intervalo_total[1]
        

        intervalo = np.linspace(t_min, t_max, self.PASSO)
        self.indices = intervalo
        vals = []
        #print('min = {}  max = {}'.format(t_min+00.1, t_max))
        for i in intervalo:
            if self.SEMANTICA == self.SEMANTICA_MIN:
                vv = self.funcao_pertinencia.pertinencia_max(C,i,maxi)
            elif self.SEMANTICA == self.SEMANTICA_PROD:
                vv = self.funcao_pertinencia.pertinencia_max_prod(C,i,maxi)
            
            vals.append(vv)
        self.v_pertinencias.append(vals)
        
    def agregacao_antecedentes(self):
        a = 0
        b = 0
        for r in self.regras:
            v = []
            pertinencia = 0
            #print(r[0])
            for i in range(len(r[1])):
                var = r[1][i]
                valor = self.valores[i]
                v.append(self.antecedentes[i].pertinencia(var,valor))
                #print(r[1][i],' = ',self.antecedentes[i].pertinencia(var,valor))                
            if r[0] == self.REGRA_E:
                if self.E == self.E_MIN:
                    #print('minimo (e) : ',min(v))
                    pertinencia = min(v)
                elif self.E == self.E_PROD:
                    prod = 1
                    for i in range(len(v)):
                        prod = prod * v[i]
                    #print('produto (e) : ',prod)
                    pertinencia = prod
            else:
                #print('máximo (ou): ',max(v))
                pertinencia = max(v)
            
            if self.REGRA == self.MAMDANI:
                for i in range(len(r[2])):
                    #print('Consequente: ',r[2][i])
                    #print('Intervalo..: ',self.consequentes[i].var(r[2][i]).intervalo)
                    self.consequentes_valores.append([self.consequentes[i].var(r[2][i]).intervalo, pertinencia])
                    self.semantica_regras(self.consequentes[i].var(r[2][i]).intervalo,pertinencia)
            elif self.REGRA == self.SUGENO:
                a = a + (pertinencia * r[2])
                b = b + pertinencia
                self.v_pertinencias.append(pertinencia)
                self.indices.append(r[2])
        if self.REGRA == self.SUGENO:
            if b == 0:
                self.inferencia_sugeno = 0
            else:
                self.inferencia_sugeno = a/b


    def superficie_regras(self):
        aux = self.PLOT_DEFUZZY
        self.PLOT_DEFUZZY = False
        q_ant = len(self.antecedentes)
        iA = self.antecedentes[0].intervalo_total
        iB = self.antecedentes[1].intervalo_total
        #print(iA)
        #print(iB)
        
        intervaloA = np.linspace(iA[0], iA[1], 15)       
        intervaloB = np.linspace(iB[0], iB[1], 15)       

        matriz_juncao = np.zeros([len(intervaloA),len(intervaloB)])   

        for i in range(len(intervaloA)):
            for j in range(len(intervaloB)):
                self.valores = [intervaloA[i], intervaloB[j]]
                matriz_juncao[j][i] = self.defuzzyficacao()
        
        intervaloA, intervaloB = np.meshgrid(intervaloA, intervaloB)
    
        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')
        
        ax.plot_surface(intervaloA, intervaloB, matriz_juncao,cmap='viridis')
        plt.title('Superfície de Regras')
                      
        ax.set_xlabel(self.antecedentes[0].nome)
        ax.set_ylabel(self.antecedentes[1].nome)
        ax.set_zlabel(self.consequentes[0].nome)
        ax.view_init(30, 240)        
        plt.show()   
        self.PLOT_DEFUZZY = aux
