import probability 
class MDProblem :
    def __init__ ( self , fh ) :
    # Place here your code to load problem from opened file object fh
    # and use probability . BayesNet () to create the Bayesian network.
        self.load(fh)

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
    
    
problema = MDProblem(open("tests_project_nr2/tests/PUB2.txt","r"))