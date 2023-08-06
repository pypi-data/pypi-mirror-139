# -*- coding: utf-8 -*-
"""
Created on Mon Nov  1 09:36:30 2021

@author: Héber
"""
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator
import numpy as np 

from fh_fuzzy.fh_funcao_pertinencia import funcao_pertinencia

class variavel:
    STYLES = ['r','g','b','y','purple','orange','black','pink','gray','brown']
    
    def __init__(self, nome, intervalo_total):
        self.variaveis = []
        self.nome = nome
        self.funcao_pertinencia = funcao_pertinencia()    
        self.valor = 0
        self.intervalo_total = intervalo_total
        
    def inserirFP(self, intervalo, nome):
        """
        Utilizada para inserir uma função de pertinência à uma variável

        :param intervalo: tupla que define o intervalo da função de pertinência. com 2 valores cria uma função de pertinência gaussiana; com 3 valores cria uma função de pertinência triangular; com 4 valores cria uma função de pertinência trapezoidal;
        :param nome: str armazena o nome da função de pertinêncoa.
        """
        var = funcao_pertinencia.novaFP(intervalo, nome)
        if var != 0:    
            self.variaveis.append(var)
        
    def visualizar_base(self):
        #intervalo = self.menor_maior()
        intervalo = self.intervalo_total
        
        i = 0
        for v in self.variaveis:
            self.funcao_pertinencia.plot(v.intervalo, v.nome, intervalo, self.STYLES[i])
            i += 1
        plt.xlabel(self.nome)
        plt.ylabel('PERTINÊNCIA')
        
    def visualizar(self):
        """
        Utilizada para gerar um gráfico com todas as funções de pertinência
        inseridas na variável.
        """
        if self.variavel_valido():
            self.visualizar_base()
            plt.show()
        else:
            print('Impossível plotar o variavel {}, ele não possui variáveis!'.format(self.nome))
 
 
    def menor_maior(self):
        if self.variavel_valido():
            menor = min(self.variaveis[0].intervalo)
            maior = max(self.variaveis[0].intervalo)
            for v in self.variaveis:
                if min(v.intervalo) < menor:
                    menor = min(v.intervalo)
                if max(v.intervalo) > maior:
                    maior = max(v.intervalo)
            #return menor, maior
            return self.intervalo_total
        
    def variavel_valido(self):
        if len(self.variaveis) == 0:
            return False
        else:
            return True
        
    def var(self, nome):
        if self.variavel_valido():
            c = []
            for v in self.variaveis:
                if v.nome == nome:
                    return v
            if len(c) == 0:
                print('A variável {} não foi encontrada no variavel {}'.format(nome, self.nome))
        else:
            print('O variavel ainda não possui nenhuma variável')
    
    def pertinencia(self, nome, v):
        funcao_pertinencia = self.var(nome)
        return self.funcao_pertinencia.pertinencia(funcao_pertinencia.intervalo, v)

    def pertinencia_todos(self):
        if self.variavel_valido():
            for v in self.variaveis:
                pert = self.funcao_pertinencia.pertinencia(v.intervalo, self.valor)
                v.valor_pertinencia = pert
            self.vizualizar_pertinencia()
            
                
    def vizualizar_pertinencia(self):
        #intervalo = self.menor_maior()
        intervalo = self.intervalo_total
        i = 0
        perts = []
        for v in self.variaveis:
            self.funcao_pertinencia.plot(v.intervalo, v.nome, intervalo, self.STYLES[i])
            p = v.valor_pertinencia
            perts.append(p)
            if p > 0:
                corte_gauss = 2.3
                if len(v.intervalo) == 2:
                    a = v.intervalo[0] + (v.intervalo[1] * corte_gauss)
                    b = v.intervalo[0] - (v.intervalo[1] * corte_gauss)
                    m = v.intervalo[1]
                    n = v.intervalo[1]
                elif len(v.intervalo) == 3:
                    a = v.intervalo[0]
                    b =  v.intervalo[2]
                    m = v.intervalo[1]
                    n = v.intervalo[1]
                elif len(v.intervalo) == 4:
                    a = v.intervalo[0]
                    b = v.intervalo[3]
                    m = v.intervalo[1]
                    n = v.intervalo[2]

                '''                    
                a = v.intervalo[0]
                b = v.intervalo[2] if len(v.intervalo)==3 else v.intervalo[3]
                
                m = v.intervalo[1]
                n = v.intervalo[2] if len(v.intervalo)==4 else v.intervalo[1]
                '''              
                d1 = m-a
                d2 = b-n
                f1 = p*d1
                f2 = p*d2

                plt.fill_between([a,a+f1,b-f2,b], 
                                 [0,p,p,0],
                                 #[0.5],
                                 #where=x2<0.5, 
                                 alpha=0.2,
                                 #step='mid',                
                                 interpolate=True,
                                 facecolor=self.STYLES[i]
                                 )
            #print('Variável {} valor = {}'.format(v.nome, v.valor_pertinencia))
            i += 1
        #print('VALOR MÁXIMO DE PERTINENCIAS = ',max(perts))
        plt.plot((self.valor, self.valor), (0, max(perts)), 'k--')

        plt.xlabel(self.nome)
        plt.ylabel('PERTINÊNCIA')
        plt.show()
        
     
            
            