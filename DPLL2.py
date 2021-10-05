def unitPropagate(S, I):
        Sx = S
        print(u"Realizando Unit Propagation a:", Sx)
        unit = False
        novoid = True
        ind = 0
        for i in range(len(S)):
                if len(S[i]) == 0:
                        novoid = False
                        break
                if len(S[i]) == 1: 
                        unit = True
                        ind = i

        if(unit and novoid):
                current = S[ind][0]
                if '-' in current:
                        dictmp={current[1:]:False}
                        I.update(dictmp)
                        Sx = [x for x in S if current not in x]
                        for i in range(len(Sx)):
                                Sx[i] = [x for x in Sx[i] if current[1:] != x]
                else:
                        dictmp={current:True}
                        I.update(dictmp)
                        Sx = [x for x in S if current not in x]
                        for i in range(len(Sx)):
                                Sx[i] = [x for x in Sx[i] if '-' + current != x]
                return unitPropagate(Sx, I)

        else:
                print(u"Fin de Unit Propagate:", Sx)
                return Sx, I

def DPLL(S, I):
        Sx, Ix = unitPropagate(S, I)
        if len(Sx) == 0: 
                return "Satisfacible", Ix
        for i in range(len(Sx)):
                if len(Sx[i]) == 0:
                        return "Insatisfacible", {}
        current = Sx[0][0]
        if '-' in current:
                dictmp={current[1:]:False}
                Ix.update(dictmp)
                Sy = [x for x in Sx if current not in x]
                for i in range(len(Sy)):
                        Sy[i] = [x for x in Sy[i] if current[1:] != x]
        else:
                dictmp={current:True}
                Ix.update(dictmp)
                Sy = [x for x in Sx if current not in x]
                for i in range(len(Sy)):
                        Sy[i] = [x for x in Sy[i] if '-' + current != x]
        one, two = DPLL(Sy, Ix)
        if one == "Satisfacible":
                return DPLL(Sy, Ix)
        if '-' in current:
                current = current[1:]
                dictmp={current:True}
                Ix.update(dictmp)
                Sy = [x for x in Sx if current not in x]
                for i in range(len(Sy)):
                        Sy[i] = [x for x in Sy[i] if '-' + current != x]
        else:
                current = '-' + current
                dictmp={current[1:]:False}
                Ix.update(dictmp)
                Sy = [x for x in Sx if current not in x]
                for i in range(len(Sy)):
                        Sy[i] = [x for x in Sy[i] if current[1:] != x]
        
        return DPLL(Sy, Ix)
        
        
        
                
