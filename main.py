import probability 
import json
class MDProblem :
    def __init__ ( self , fh ) :
    # Place here your code to load problem from opened file object fh
    # and use probability . BayesNet () to create the Bayesian network.
        self.load(fh)
        self.diseases_in_common()
        self.make_bayes_net()
        self.bayes_net = probability.BayesNet(self.bayes_graph)

    def solve ( self ) :
    # Place here your code to determine the maximum likelihood
    # solution returning the solution disease name and likelihood .
    # Use probability . elimination_ask () to perform probabilistic
    # inference .
        self.dise_likelihood = {}
        max_likelihood = -1000.0
        T = len(self.measurements)
        final_dicti = self.create_dict_tests()
        for disease in self.diseases:
            prob = probability.elimination_ask(f'{disease}_{T}',final_dicti,self.bayes_net)
            # prob = float((prob.split(',')[1]).split(':')[1])
            prob = float(prob[True])
            #store
            self.dise_likelihood[f'{disease}_{T}'] = prob
            if(prob >= max_likelihood):
                max_likelihood = prob
                max_disease = disease
        return ( max_disease , max_likelihood )
            
    
    # Dictionary that has all the tests
    def create_dict_tests(self):
        final_dic = {}
        for t in range(1,len(self.measurements)+1,1):
            for exam in self.measurements[t-1].keys():
                final_dic[f'{exam}_{t}'] = self.measurements[t-1][exam]
        return final_dic
            

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
                            self.exam[l[1]] = {'D': l[2],'TPR': float(l[3]),'FPR': float(l[4])}
                        except:
                            print("Wrong format -> ", line)
                            exit()
                        
                    # measurements
                    elif(l[0] == "M"):
                        try:
                            dic = {}
                            for i in range(1, len(l), 2):
                                dic[l[i]] = True if(l[i+1]=='T') else False

                            self.measurements.append(dic)
                        except:
                            print("Wrong format -> ", line)
                            exit()
                        

                    # propagation probability
                    elif(l[0] == "P"):
                        try:
                            self.prop_prob = float(l[1])
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
        for d in self.diseases:
            list_of_dise = []
            if 0 == len(self.disea_sympt[d]):
                self.disease_com[d] = [d]
                continue
            for sympt in self.disea_sympt[d]:
                for disease in self.sympt_disea[sympt]:
                    if not(disease in list_of_dise):
                        list_of_dise.append(disease)
            self.disease_com[d] = list_of_dise

    
    def make_bayes_net(self):
        self.bayes_graph = []
        T, F = True, False
        for t in  range(1,len(self.measurements)+1,1):#iterate over time
            if(t == 1):
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
                exam_table[T] = self.exam[measurement]['TPR']
                exam_table[F] = self.exam[measurement]['FPR']
                lista.append(exam_table)
                self.bayes_graph.append(tuple(lista))
                
                    
        
        
                    
                    
    def truth_table(self,disease):
        table = {}
        nr_bits = len(self.disease_com[disease])
        
        # T, F = True, False
        for i in range(2**nr_bits):
            line = []
            truth_table_line = list(bin(i)[2:].zfill(nr_bits))
            for place in truth_table_line:
                line.append(bool(int(place)))
            
            line = tuple(line)
            
            
            table[line] = self.write_probability(line,disease,nr_bits)
        return table
                    
    def write_probability(self,line,disease,nr_bits):
        if (disease == 'd3'):
            print('cheguei')
        index_disease = self.disease_com[disease].index(disease)
        if(line[index_disease] == False):
            return 0
        elif(line[index_disease] == True and line.count(True) > 1):
            return self.prop_prob
        else:
            return 1
            

        
    
problema = MDProblem(open("tests_project_nr2/tests/PUB1.txt","r"))


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
