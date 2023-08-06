
import numpy as np
import pandas as pd
import math

from scipy.stats import norm
from numpy.linalg import inv


def LR_Boost(X,Y,ite,thres,correct_X,correct_Y,pr,lr,matrix):
    y1=pd.DataFrame(Y)
    y1.columns=['y']
    df=pd.concat([X,y1],axis=1)
    
    p=df.shape[1]-1
    n=len(df)
# g function ----------------------------------------------------------------------
    def g(beta,df):
    
        y=np.array(df['y'])
        x=np.array(df.drop(['y'],axis=1))    
        sigma=np.array([0]*p)
        for i in range(n):
            try:
                scalar=(math.exp(np.dot(x[i],beta)))
            except :
                scalar=8.218407461554972e+307
            sigma=sigma+ (-x[i]*scalar/(1+scalar)+y[i]*x[i])  
        return sigma
# delta function ----------------------------------------------------------------------
    def delta_function(beta,df):
    

        y=np.array(df['y'])
        x=np.array(df.drop(['y'],axis=1))
    
    
        sigma=np.array([0]*p)
        for i in range(n):
            scalar1=np.dot(x[i],beta)
            scalar2= y[i]* (np.dot((np.dot(beta,matrix)),beta))
            mul=x[i]+y[i]*(np.dot(beta,matrix))
            scalar=math.exp(scalar1+scalar2)
                              
            sigma=sigma+(-mul*scalar/(1+scalar)+y[i]*mul)
        
        return sigma

# threeboost-----------------------------------------------------------------------
    def threeboost(df,ite,thres):
    
        delta=np.array([0.0]*p)
        for i in range(ite):
            g_function=g(delta,df)
            maxima=max(abs(g_function))
        
            for j in range(len(g_function)):
                if abs(g_function[j])>=(thres*maxima):
                    delta[j]=delta[j]+g_function[j]*lr
                else :
                    delta[j]=delta[j] 
        delta=np.where(abs(delta)>0.01,delta,0)
        return delta  
# threeboost_delta-----------------------------------------------------------------------    
    def threeboost_delta(df,ite,thres):
    
        delta=np.array([0.0]*p)
        for i in range(ite):
            g_function=delta_function(delta,df)
            maxima=max(abs(g_function))
        
            for j in range(len(g_function)):
                if abs(g_function[j])>=(thres*maxima):
                    delta[j]=delta[j]+g_function[j]*lr
                else:
                    delta[j]=delta[j]
                    
        delta=np.where(abs(delta)>0.01,delta,0)
        return delta      

# new data2  (y revised)------------------------------------------------------------------------------
    def new_data2(df):
       
        y_old=np.array(df['y'])
        x=np.array(df.drop(['y'],axis=1))
    
        y_new=[]
    
        for i in range(n):
            p1=pr[i][0]
            p2=pr[i][1]
            y=((y_old[i]-p1)/(1-p1-p2))
            if y>=0.5:
                y_new.append(1)
            else:
                y_new.append(0)
        
        
        
        y_new_data=pd.DataFrame(np.array(y_new))
    
        y_new_data.columns=['y']
        y_new_data=y_new_data.set_axis(range(n), axis=0)
    
    
        data=pd.concat([df.drop('y',axis=1), y_new_data] ,axis=1)
        
        return data



#-----------------------------------------------------------------------------------------------
  
    df2_star=df    
    df3_star=new_data2(df2_star)
    y_error=df2_star['y']
    
    
    if correct_X==1 and correct_Y==1:
        result=threeboost_delta(df3_star,ite,thres)
        y_new=df3_star['y']
        x_new=df3_star.drop(['y'],axis=1)
    elif correct_X==1 and correct_Y==0:
        result=threeboost_delta(df2_star,ite,thres)
        y_new=df2_star['y']
        x_new=df2_star.drop(['y'],axis=1)
    elif correct_X==0 and correct_Y==1:
        result=threeboost(df3_star,ite,thres)
        y_new=df3_star['y']
        x_new=df3_star.drop(['y'],axis=1)
    else:
        result=threeboost(df2_star,ite,thres)
        y_new=df2_star['y']
        x_new=df2_star.drop(['y'],axis=1)
    
    number=[]
    for i in range(len(result)):
        if result[i]!=0:
            number.append(i+1)




        

    return print('estimated coefficient :{}'.format(result)+'\n'+
                  'predictors:{}'.format(number)+'\n'+
                 'number of predictors:{}'.format(len(number)))
                






