#GROUPBY WITH MULTIPLE AGGREGATIONS 

df = pd.DataFrame(np.random.rand(4,4), columns=list('abcd'))
df['group'] = [0, 0, 1, 1]
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
    return pd.Series(d, index=['a_max', 'a_min', 'a_max-a_min', 'a_sum', 'b_mean', 'c_d_prodsum'])

df.groupby('group').apply(lambda x: groupby_cols(x))
# or df.groupby('group').apply(groupby_cols)


'''
OUTPUT
         a_sum     a_max    b_mean  c_d_prodsum
group                                           
0      0.864569  0.446069  0.466054     0.173711
1      1.478872  0.843026  0.687672     0.630494
'''
