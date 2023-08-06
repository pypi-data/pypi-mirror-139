
import numpy as np
import pandas as pd
import math

from scipy.stats import norm
from numpy.linalg import inv



def PM_Boost(X,Y,ite,thres,correct_X,correct_Y,pr,lr,matrix):
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
            scalar=np.dot(x[i],beta)
            cdf=norm.cdf(scalar)
            exp=math.exp((scalar**2)*(-0.5))
            pi=math.pi
            common=x[i]*((2*pi)**(-0.5))*exp
            cal=common*(y[i]/cdf+(y[i]-1)/(1-cdf))
            sigma=sigma+ cal 
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
    
# x_revised  (x revised)------------------------------------------------------------------------------
    def x_revised(df):
        
        y=df[['y']]
        x=np.array(df.drop(['y'],axis=1))
    
        
        mean=x.mean(0)
        covariance=np.cov(x.T)
        inverse=inv(covariance)
        
        data=pd.DataFrame({})
        for i in range(n):
            x_new_list=mean+np.dot((covariance-matrix),np.dot(inverse,(x[i]-mean)))
            x_new_list=pd.DataFrame(x_new_list).T
            data=pd.concat([data,x_new_list],axis=0)
        
        
        data=data.set_axis(range(n), axis=0)
        data=data.set_axis(range(1,p+1), axis=1)
        data=pd.concat([data,y],axis=1)
        
        return data
#-----------------------------------------------------------------------------------------------
      
    
    df2_star=df    
    df3_star=new_data2(df2_star)
    df3_star_star=x_revised(df3_star)
    df2_star_star=x_revised(df2_star)
    y_error=df2_star['y']

   
    if correct_X==1 and correct_Y==1:
        data=df3_star_star
    elif correct_X==1 and correct_Y==0:
        data=df2_star_star
    elif correct_X==0 and correct_Y==1:
        data=df3_star
    else:
        data=df2_star
        
    result=threeboost(data,ite,thres)
    y_new=data['y']
    x=np.array(data.drop(['y'],axis=1))
    result=np.array(result) 
    number=[]
    for i in range(len(result)):
        if result[i]!=0:
            number.append(i+1)
    number_set=set(number)


        
    return print('estimated coefficients:{}'.format(result)+'\n'+
                  'predictors:{}'.format(number)+'\n'+
                 'number of predictors:{}'.format(len(number)))
        

       




