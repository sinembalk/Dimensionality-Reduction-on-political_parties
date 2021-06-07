import pandas as pd
import numpy as np
import os
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns


class Model:   
    
    def __init__(self,
                 country_out_scope,
                 conceptual_cols,
                 scale_7,                 
                ):
        self.country_out_scope= country_out_scope
        self.conceptual_cols= conceptual_cols
        self.scale_7= scale_7
                    
    def data_preperation(self):
        """
        Reads the data, drops the redundant columns and trimms the data the countries out of 
        the scop of the study
        """
        df = pd.read_stata(f'data\CHES2019V3.dta')
        
        out_scope= self.country_out_scope
        df= df.query('country!=@out_scope')
        
        drop_cols= [x for x in df.columns if '_require' in x] 
        df.drop(drop_cols, axis=1, inplace=True)
        
        return df
        
    def get_concept_dimensions(self, df_prep):
        """ 
        It groups the features according to the conceptualized laten variables as described in 
        README file       
        """
        
        economic= []
        for category in ['econ', 'tax', 'dereg', 'redist']:
            economic+= [x for x in df_prep.columns if (f'{category}' in x) and (x not in self.conceptual_cols)  ]
        
        eu=[x for x in df_prep.columns if ('eu' in x) and (x not in self.conceptual_cols )]
        social= list(set(df_prep.columns)- set(self.conceptual_cols + economic + eu))
    
        feature_dict= { 'eu': eu,
                       'social': social,
                       'economic': economic 
            
        }
        return feature_dict
        
        
    def null_treatment(self, df):
        """
        Treats the null values of the data according to the different scaled features
        """
        
        null_cols=df.columns[df.isnull().any()] 
        null_features= [ x for x in null_cols if x not in self.conceptual_cols]
        
        df[self.scale_7] = df[self.scale_7].fillna(4)

        scale_10= list(set(null_features) - set(self.scale_7))
        df[scale_10] =  df[scale_10].fillna(6)
        
        return df
    
    def two_d_visual(self, df_treated, feature_dict):
        """
        Generates two images for visualization of 2D data points and for distribution 
        of the data points.
        Also returns the weights of the principal components
        """
        
        from sklearn.preprocessing import StandardScaler
        from sklearn.decomposition import PCA
        
        
        weight_dict= {}
        all_features = feature_dict['social'] + feature_dict['eu'] + feature_dict['economic']
        X= df_treated.set_index('party_id')[all_features]

        scaler = StandardScaler()
        scaler.fit(X)
        X_std= pd.DataFrame(scaler.transform(X))
        X_std.columns= X.columns

        X_pca= pd.DataFrame(index= X.index)
        pca = PCA(n_components=1, random_state=42)
        X_pca['component_economic'] = pca.fit_transform(X_std[feature_dict['economic']])
        
        weight_dict['economic'] = pca.components_[0]

        X_pca['component_social_eu']= pca.fit_transform(X_std[feature_dict['eu']+ feature_dict['social']])
        
        weight_dict['social_eu'] = pca.components_[0]
        
        fig = px.scatter(X_pca.merge(df_treated, on='party_id',how='left'),
                         x="component_economic", 
                         y="component_social_eu",  
                         color= 'country', 
                         text= 'party', 
                         title= "2D representation of CHES data"
        )
        fig.update_layout(width= 1000, height= 750, plot_bgcolor='rgba(0,0,0,0)' )
        fig.update_traces(textposition= 'top center', textfont_size= 9)
        
        if not os.path.exists("images"):
            os.mkdir("images")
        fig.write_image("images/two_dim_representation.png")
        
        fig_dist= sns.jointplot(data=X_pca, 
                      x="component_economic",
                      y="component_social_eu", 
                      kind="kde"
        )
        
        plt.savefig('images/distribution_2d.png')       
        
        return weight_dict 
    
    def feature_value_wieghts(self, df_treated, feature_dict,weight_dict ):
        """
        It creates and saves a sample data with 10 political parties. 
        Also saves the weights obtianed in PCA
        """
        
        random_parties= list(df_treated['party_id'].sample(n=10, random_state=41))
        component_economic= []
        component_social_eu= []

        for i in random_parties:

            a= df_treated[df_treated['party_id'] == i][feature_dict['economic']]
            component_economic.append(np.dot(a,np.transpose(weight_dict['economic']) )[0])

            b= df_treated[df_treated['party_id'] == i][feature_dict['social'] + feature_dict['eu']]
            component_social_eu.append(np.dot(b,np.transpose(weight_dict['social_eu']) )[0])

        all_features= feature_dict['social'] + feature_dict['eu'] + feature_dict['economic']
        sample_data= df_treated.query('party_id ==@ random_parties')[all_features]
        sample_data['comp_economic']= component_economic
        sample_data['comp_socail_eu']= component_social_eu
               
        if not os.path.exists("outputs"):
            os.mkdir("outputs")
        pd.DataFrame.from_dict(weight_dict,  orient='index').to_excel('outputs/weights.xlsx')      
        sample_data.to_excel('outputs/sample_data.xlsx')
