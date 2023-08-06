
import numpy as np
import pandas as pd
import math





def ME_Generate(n,p,cov):
    def xi(p):
        def cov(p):
            cov=[]
            for i in range(p):
                n=[0]*i
                n.append(1)
                for j in range(i+1,p):
                    n.append(0.5**(j-i))
                cov.append(n)
            cov=np.array(cov)
            cov1=cov.T-np.diag(cov.diagonal())
            return  (cov+cov1)
        
        def mean(p):
            zero=[0]
            return zero*p 
    
        return np.random.multivariate_normal(mean(p),cov(p))
   

    def beta_0(p):
        return[1]*3+[0]*(p-3)
    def data(p,n):
        data=pd.DataFrame({})
        for i in range(n): 
            x=xi(p)
            scalar=np.dot(x,beta_0(p))
            outcome=math.exp(scalar)/(1+math.exp(scalar))
        
            x=list(x)
            x.append(outcome)
            if outcome>=0.5:
                x.append(1)
            else:
                x.append(0)
            
            x=pd.DataFrame(x).T
            data=pd.concat([data,x],axis=0)
        
        data=data.set_axis(range(n), axis=0)
        data=data.set_axis(range(1,p+3), axis=1)
        data=data.rename({p+1: 'prob', p+2:'y'}, axis=1)
                  
        return data
    


# new data1 (y unrevised)--------------------------------------------------------------------


    def new_data1(df):
        p=df.shape[1]-2
        n=len(df)
    
        prob=np.array(df['prob'])
        x=np.array(df.drop(['y','prob'],axis=1))
    
        y_new=[]
        m=[]
    
        for i in range(n):
            m_list=[]
            scalar=math.exp(1+np.dot(x[i],np.array([1.0]*p)))
            matrix=np.array([[1/(1+scalar),scalar/(1+scalar)],[scalar/(1+scalar),1/(1+scalar)]])
            prob_old=np.array([[prob[i]],[1-prob[i]]])
            prob_new=np.dot(matrix,prob_old)
            
            m_list.append(matrix[0][1])
            m_list.append(matrix[1][0])
            m_list=np.array(m_list)
            m.append(m_list)
        
            if prob_new[0]>prob_new[1]:
                y_new.append(1)
            else:
                y_new.append(0)
        y_new_data=pd.DataFrame(np.array(y_new))
    
        y_new_data.columns=['y']
        y_new_data=y_new_data.set_axis(range(n), axis=0)
    
    
        data=pd.concat([df.drop('y',axis=1), y_new_data] ,axis=1)
        m=np.array(m)
        
        return data,m

    
# error (x unrevised)------------------------------------------------------------------
    def x_error(df):
        x=np.array(df.drop(['y','prob'],axis=1))
        p=df.shape[1]-2
        n=len(df)
    
        def mean(p):
            zero=[0]
            return zero*p
    
    
        data=pd.DataFrame({})
        for i in range(n):
            e=np.array(np.random.multivariate_normal(mean(p),cov))
            x=np.array(df.T[i][:p])+e
        
            x=pd.DataFrame(x).T
            data=pd.concat([data,x],axis=0)
        
        data=data.set_axis(range(n), axis=0)
        data=data.set_axis(range(1,p+1), axis=1)
    
        return data
    
# data x_unrevised and y, y*, y**------------------------------------------------------------

    def data_error(df):
        drop=df[['y']]
        data=pd.concat([error,drop],axis=1)
        return data

#-----------------------------------------------------------------------------------------------
      
    
    df1=data(p,n)
    error=x_error(df1)
    y_true=df1['y']
    df2=new_data1(df1)
    df2_star=data_error(df2[0])

    
    return df2[1],df2_star
         

