import probability 
class MDProblem :
    def __init__ ( self , fh ) :
    # Place here your code to load problem from opened file object fh
    # and use probability . BayesNet () to create the Bayesian network.
        self.load(fh)
        self.diseases_in_common()
        self.make_bayes_net()

   # def solve ( self ) :
    # Place here your code to determine the maximum likelihood
    # solution returning the solution disease name and likelihood .
    # Use probability . elimination_ask () to perform probabilistic
    # inference .
    #    return ( disease , likelihood )
    

    def load(self, fh):
        
        self.disea_sympt = {}
        self.diseases = []
        self.sympt_disea = {}
        self.exam = {}
        self.measurements = []
        

        for line in fh:
                if line.strip(): # skips blank lines
                    l = line.split() 
                    
                    # diseases
                    if(l[0] == "D"):
                        try:
                            for d in l[1:]:
                                self.diseases.append(d)
                        except:
                            print("Wrong format -> ", line)
                            exit()

                    # symptoms
                    elif(l[0] == "S"):
                        try:
                            self.sympt_disea[l[1]] = l[2:]
                        except:
                            print("Wrong format -> ", line)
                            exit()
                        
                    # exams
                    elif(l[0] == "E"):
                        try:
                            self.exam[l[1]] = {'D': l[2],'TPR': l[3],'FPR': l[4]}
                        except:
                            print("Wrong format -> ", line)
                            exit()
                        
                    # measurements
                    elif(l[0] == "M"):
                        try:
                            dic = {}
                            for i in range(1, len(l), 2):
                                dic[l[i]] = l[i+1]

                            self.measurements.append(dic)
                        except:
                            print("Wrong format -> ", line)
                            exit()
                        

                    # propagation probability
                    elif(l[0] == "P"):
                        try:
                            self.prop_prob = l[1]
                        except:
                            print("Wrong format -> ", line)
                            exit()

                    else:
                        print("Wrong format -> ", line)
                        exit()
        
        
        print("Doenças = ",self.diseases)
        print("Sintomas = ",self.sympt_disea)
        print("Exames = ",self.exam)
        print("Medicoes = ",self.measurements)
        

        for disease in self.diseases:
            dic = []
            for sympt in self.sympt_disea.keys():
                if disease in self.sympt_disea[sympt]:
                    dic.append(sympt)
            self.disea_sympt[disease] = dic
        return
    
    # Produces a dictionary of diseases in common
    def diseases_in_common(self):
        self.disease_com = {}
        for d in self.disea_sympt.keys():
            list_of_dise = []
            for sympt in self.disea_sympt[d]:
                for disease in self.sympt_disea[sympt]:
                    if not(disease in list_of_dise):# and not(d==disease):
                        list_of_dise.append(disease)
            self.disease_com[d] = list_of_dise

    
    def make_bayes_net(self):
        self.bayes_graph = []
        
        for t in  range(len(self.measurements)+1):#iterate over time
            if(t == 0):
                for d in  self.diseases:
                    node = (f'{d}_{t}','',0.5)
                    self.bayes_graph.append(node)
            else:
                for d in self.diseases:
                    
                    ## Create node of the disease d
                    lista = []
                    lista.append(f'{d}_{t}') # Name of the disease in t
                    diseas_common = []
                    for prev_d in self.disease_com[d]: # Parents of disease d in t-1
                        diseas_common.append(f'{prev_d}_{t-1}')
                    lista.append(' '.join(diseas_common))
                    lista.append(self.truth_table(d))
                    self.bayes_graph.append(tuple(lista))
                    
                ## Create node of the measurement
                for measurement in self.measurements[t-1].keys():
                    lista = []
                    lista.append(f'{measurement}_{t}')
                    aux = self.exam[measurement]['D']
                    lista.append(f'{aux}_{t}')
                    exam_table = {}
                    exam_table['T'] = self.exam[measurement]['TPR']
                    exam_table['F'] = self.exam[measurement]['FPR']
                    lista.append(exam_table)
                    self.bayes_graph.append(tuple(lista))
                    
                    
        
        
                    
                    
    def truth_table(self,disease):
        table = {}
        nr_bits = len(self.disease_com[disease])
        for i in range(2**nr_bits):
            truth_table_line = bin(i)[2:].zfill(nr_bits)
            truth_table_line = truth_table_line.replace('0','T')
            truth_table_line = truth_table_line.replace('1','F')
            line = tuple(list(truth_table_line))
            
            
            table[line] = self.write_probability(line,disease,nr_bits)
        return table
                    
    def write_probability(self,line,disease,nr_bits):
        index_disease = self.disease_com[disease].index(disease)
        if(line[index_disease] == 'F'):
            return 0
        else:
            return 1
            
        # print(line)
                
        
        
        
     # def parent_diseases(self,t,d):#time t of the disease d      
     #     for
        
        
    
problema = MDProblem(open("tests_project_nr2/tests/PUB2.txt","r"))


#%% Exemplo manual PUB2


T, F = True, False

# D covid common_cold flu asthma
# S fever covid flu
# S nose_clogged common_cold flu
# S shortness_of_breath covid asthma
# S fatigue covid common_cold asthma
# E pcr covid 0.6893 0.3426 
# E chest_xray common_cold 0.9893 0.0526
# E feno asthma 0.8932 0.1213
# E ridt flu 0.8321 0.2423
# M pcr F
# M pcr F chest_xray T
# P 0.25


    

# pub2 = probability.BayesNet(bayes_graph)
# probability.enumeration_ask('common_cold_2', dict(pcr_1=F, pcr_2=F,chest_xray_2=T), pub2).show_approx()
