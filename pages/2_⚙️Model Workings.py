import streamlit as st

# Display the mathematical model using LaTeX
# st.title("Mean-Variance Optimization Model")

st.write("""### 🧠Mathematical Model """)
st.latex(r'''
\text{Minimize:} \quad \frac{1}{2} \sum_{i=1}^{n} \sum_{j=1}^{n} w_i w_j \sigma_{ij}
''')
st.latex(r'''
\text{Subject to:} \quad \sum_{i=1}^{n} w_i \bar{r}_i = \bar{r}
''')

st.latex(r'''
\quad \sum_{i=1}^{n} w_i = 1
''')

st.latex(r'''
\quad \bar{r}_i = \text{mean rates of returns of selected stocks,} \quad \sigma_{ij} = \text{covariances of selected stocks,} \quad w_i = \text{weights of stocks}
''')

st.write("""
### 🧠 Approach 
   - Markowitz Model is an optimization problem that leads to minimum varinace problem.
   - To find minimum varinace portfolio,we fix some mean value at some arbitary value r̄ (which we enter as a portfolio return we want).
   - Then we find feasible portfolio with minimum variance that has this mean.
          
""")
