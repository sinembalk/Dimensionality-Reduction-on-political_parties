### How to run the package

To get excel files and images run run__model.py

# Dimensionality Reduction in CHES data


Simply put, a `dimensionality reduction` is a technique to reduce the number of random variables to consider. The technique is widely used by empirical political scientist because it enables better understanding of the nature of the politics which can be conceived as contestation in an infinite-issue space. It is crucial to constrain the number of dimensions for voters or researchers who face the limits of cognition or capacity to process high dimensional information (Hinich and Munger, 1996).

Stoll (2011) suggests that the way researchers conceptualize dimensionality matters in understanding the ideology of political parties. In political literature, many empirical studies discuss on conceptualizing the dimensions and/or on the defining the number of dimensions. 

As Bakker, Jolly and Pork (2012) states, the CHES survey is designed to uncover three potentially distinct dimensions of political contestation: social left/right,  economic left/right and the pro-/anti-European integration dimension. This study roughly follows the idea to conceptualize the dimensions as socical left/right and economic left/right dimensions, with additional attempt to incorporate EU integration dimension into social left/right dimension so that the data can be projected into 2D with best approximation to the distribution  of economic left/right and social left/right dimensions across parties.

Among dimensionality reduction techniques, Principal Component Analysis (PCA) is being utilized in this study. The technique combines  input features advanced linear algebra so that the “least important” features is discarded while still retaining the most valuable parts of all of the variables. Thus, the high dimensional data is projected into components (a.k.a factors) which explain the maximum amount of variance.

A widely used dimensionality reduction technique, Factor Analysis, would best suits if the aim of this study were to map features to latent constructs (or factors), under a testing theory on better fit of dimensions on the data. However, since the scope of the study is to represent the CHES data on 2D and generate insights from the visualizations, PCA fits well our purpose with following previous studies on conceptualizing the dimensions.

Another widely used technique, t-SNE is not leveraged in this study due to preserving global structure of the data to generate insights for the comparison of political parties scoped in the CHES data. 

To validate the reason to leverage PCA, FA and t-SNE techniques are also experimented. The distribution of the parties in 2D is barely changed, therefore PCA is kept being used. 


### Data cleaning and preprocessing

2019 Chapel Hill expert survey aims to position 277 political parties across Europe according to ideology from EU integration, social and economic perspective. The data has 55 columns in total. Some columns are conceptual such as the country of the political party, and the rests are average of the input by experts regarding the political positioning of the parties.
 

#### Missing value treatment

The political parties from Turkey, Iceland, Norway and Switzerland are discarded due to lack of data on a certain extend of EU integration ideology. For the remaining 247 political parties, the null treatment is exercised as follows:

Since the value of the features maps left/right positioning, the null values of the features with the range from 1 to 7 are filled with 4 meaning that it has centrist stance. Following similar logic, the features with the range from 0 to 10 are undergone filling with 6. 

The other suitable null treatment exercises would be knn-imputer in which sample’s missing values are imputed using the mean value from n_neighbors nearest neighbors found in the data. However, since the data has very few missing values by features, the study leaves out conducting the analysis of the best fit on null imputation technique.   

The percentage of the null values by features are as follows:
"""
eu_position: 0.0%            multiculturalism: 0.0%
eu_position_sd: 0.0%         multicult_salience: 0.4%
eu_salience: 0.0%            multicult_dissent: 0.4%
eu_dissent: 0.8%             redistribution: 0.4%
eu_blur: 0.4%                redist_salience: 0.0%
eu_cohesion: 0.0%            environment: 0.0%
eu_foreign: 0.4%             enviro_salience: 0.0%
eu_intmark: 0.0%             spendvtax: 0.4%
eu_budgets: 0.4%             deregulation: 0.0%
eu_asylum: 0.4%              econ_interven: 0.0%
lrgen: 0.0%                  civlib_laworder: 0.4%
lrecon: 0.0%                 sociallifestyle: 0.0%
lrecon_sd: 0.0%              religious_principles: 0.0%
lrecon_salience: 0.0%        ethnic_minorities: 0.4%
lrecon_dissent: 0.8%         nationalism: 0.4%
lrecon_blur: 1.2%            urban_rural: 0.0%
galtan: 0.0%                 protectionism: 0.4%
galtan_sd: 0.0%              regions: 1.6%
galtan_salience: 0.0%        russian_interference: 0.0%
galtan_dissent: 3.2%         anti_islam_rhetoric: 0.4%
galtan_blur: 0.8%            people_vs_elite: 0.0%
immigrate_policy: 0.0%       antielite_salience: 0.0%
immigrate_salience: 0.0%     corrupt_salience: 0.0%
immigrate_dissent: 0.4%      members_vs_leadership: 0.4%
"""

#### Standardization

Since PCA gives more emphasis to those variables having higher variances than to those variables with very low variances while identifying the right principle component and the variance can be varied by scale, standardization of the data is needed.

Even though PCA is prone to outliers, the outliers are left as they are under the assumption that the political parties may lay on the extreme left or right wing given an ideology rather than the outliers may address the data quality issues so that the possible information loss is prevented.In addition, since PCA does not make use of any label by its design, train-test split is not applied.


### Visualization of CHES data in 2D by political parties

As stated PCA technique is leveraged for reducing the high dimensional CHES data to 2D in a way that first dimension represents the economic left/right position while the second dimension represents the social left/right position plus EU integration stance. 

The features are categorized as follows:

`
**Economic left/right**
lrecon
lrecon_sd
lrecon_salience
lrecon_dissent
lrecon_blur
econ_interven
spendvtax
deregulation
redistribution
redist_salience

**Social left/right and EU integration**
eu_position        people_vs_elite
eu_position_sd     ethnic_minorities
eu_salience        civlib_laworder
eu_dissent         religious_principles
eu_blur            galtan_blur
eu_cohesion        nationalism
eu_foreign         immigrate_policy
eu_intmark         multicult_salience
eu_budgets         urban_rural
eu_asylum          anti_islam_rhetoric
sociallifestyle    regions
multiculturalism   galtan
corrupt_salience   enviro_salience
multicult_dissent  galtan_dissent
protectionism      members_vs_leadership
antielite_salience immigrate_salience
environment        immigrate_dissent
lrgen              galtan_sd
galtan_salience    russian_interference
`

Note that `eu_econ_require, eu_political_require, eu_googov_require` features are dropped as they are only specific to Turkey which is discarded from the scope of the study.

PCA with a single component is applied for each feature group separately, thus giving us the 2D from the data.

The figure saved in images folder shows that for political parties in Europe having a specific economic position on left or right wing, does not necessarily mean that having specific EU integration and social position. For example, Italian party LN's economic stance is considered as left while its social and EU integration stance is on the right wing. On the other hand, Belgian party, PS has just the opposite stance on two dimensions. 
The insight generated from this study is in line with the results from the study of Bakker, Jolly and Pork (2012) that leverages Confirmatory Factor Analysis on CHES data. 

Additional analysis on the results would be examining the distribution of the political parties by country. Bakker, Jolly and Pork (2012) suggest that the relationship between economic and social left/right varies across countries. For example, Spain has positive and statistically significant relationship while Hungary has negative and significant relationship. As for Slovakia, there is no discernable pattern between those two dimensions.


### The distribution of the 2D points

To illustrate the distribution of the 2D points, kernel density estimation is leveraged. It is a non-parametric method used primarily to estimate the probability density function of a collection of discrete data points. If (x1,x2,⋯,xn), (y1,y2,⋯,yn) represent an independent and identically distributed sample drawn from an unknown distribution, then the kernel density estimator estimates the shape of the density function from the unknown distributions.

The figure saved in images folder shows that the majority of the parties are roughly centrist in terms of both stances.


### The feature values  from the high-dimensional space


PCA follows the steps:
- calculating covariance matrix by all possible combinations of columns, 
- then calculating the eigenvectors of the matrix which is simply the special direction of the data points, 
- then getting the dot product of eigenvector and column value by each row so that it produces a projection of the high dimensional data with the most of the variance retained.

"""Scikit-learn""" library's PCA class has a attributes that gives the weights of the component, i.e. the eigen vectors.

For randomly selected 10 parties, feature values and the projection of them by each dimensions are given in the sample_data.xlxs file. In addition, the weights of the components associated with the feature set is given in weights.xlxs file.

The equation is as follows:
`
principal_component1= x1*w1 + ... xn*wn
principal_component2= y1*w1 + ... yn*wm
`


### The bounds mapped into the 2D space

Since the data is standardized, the boundaries are shrinked accordingly. However, there is still some values on axes that exceed the standardized boundaries because sum of the weights is not equal to 1. To prevent this, the weights can be normalised, ranging from 0 to 1.



















