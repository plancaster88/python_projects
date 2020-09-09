import pandas as pd 

df = pd.DataFrame(np.random.rand(4,4), columns=list('abcd'))
df['group'] = [0, 0, 1, 1]
df['group2'] = ['x','x','x','y']
df

'''
OUTPUT
          a         b         c         d  group
0  0.418500  0.030955  0.874869  0.145641      0
1  0.446069  0.901153  0.095052  0.487040      0
2  0.843026  0.936169  0.926090  0.041722      1
3  0.635846  0.439175  0.828787  0.714123      1
'''



df.groupby('group').agg({'a':['sum', 'max'], 
                         'b':'mean', 
                         'c':'sum', 
                         'd': lambda x: x.max() - x.min()})

'''
OUTPUT
              a                   b         c         d
            sum       max      mean       sum  <lambda>
group                                                  
0      0.864569  0.446069  0.466054  0.969921  0.341399
1      1.478872  0.843026  0.687672  1.754877  0.672401
'''


def groupby_cols(x):
    d = {}
    d['a_sum'] = x['a'].sum()
    d['a_max'] = x['a'].max()
    d['a_min'] = x['a'].min()   
    d['a_max-a_min'] = x['a'].max() - x['a'].min()
    d['b_mean'] = x['b'].mean()
    d['c_d_prodsum'] = (x['c'] * x['d']).sum()
    return pd.Series(d)

df2 = df.groupby(['group', 'group2']).apply(lambda x: groupby_cols(x))
# or df.groupby('group').apply(groupby_cols)


df2.reset_index(inplace = True)


df2



'''
OUTPUT
   group group2     a_sum  ...  a_max-a_min    b_mean  c_d_prodsum
0      0      x  0.487293  ...     0.028344  0.121449     0.520219
1      1      x  0.956389  ...     0.000000  0.893746     0.040867
2      1      y  0.605411  ...     0.000000  0.141057     0.100948
'''
