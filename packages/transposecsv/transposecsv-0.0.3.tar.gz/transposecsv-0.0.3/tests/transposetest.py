import chunk
import numpy as np 
import pandas as pd 
import pathlib 
import os 

from transposecsv import Transpose 

here = pathlib.Path(__file__).parent.resolve()
print(f'Here in transposetest.py file is {here =}')
print('Generating test DataFrame')
rand = np.ones([500, 1000])
rand = pd.DataFrame(rand)

rand.to_csv(os.path.join(here, 'test.csv'), index=False)

rand = rand.T.reset_index(drop=True)

print('Running transpose')
trans = Transpose(
    file=os.path.join(here, 'test.csv'),
    outfile=os.path.join(here, 'test_T.csv'),
    chunksize=10,
    save_chunks=True,
    quiet=True,
)

trans.compute()
print('Reading in transpose')
transpose = pd.read_csv(os.path.join(here, 'test_T.csv'))

# print(f'Transpose is')
# print(transpose)

# print('And original is')
# print(rand)

transpose.columns = pd.RangeIndex(0, len(transpose.columns))

print('Shapes are', transpose.shape, rand.shape)

print(f'Transposed == direct transpose: {transpose.equals(rand)}')
