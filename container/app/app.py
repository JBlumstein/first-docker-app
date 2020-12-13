import os
import io
import random
import numpy as np
import pandas as pd
import boto3
import pickle
import implicit
import scipy.sparse as sparse
from scipy.sparse.linalg import spsolve

print(f'testing buildtime args')
aws_key = os.environ['AWS_KEY']
aws_secret = os.environ['AWS_SECRET']
BUCKET_PATH = os.environ['BUCKET_PATH']
KEY_NAME = os.environ['KEY_NAME']
print(f'key: {aws_key}')
print(f'secret: {aws_secret}')

print('setting up client')
client = boto3.client('s3', aws_access_key_id=aws_key, aws_secret_access_key=aws_secret)

print('reading in data')
csv_obj = client.get_object(Bucket=BUCKET_PATH, Key=KEY_NAME)
body = csv_obj['Body']
csv_string = body.read().decode('utf-8')
books = pd.read_csv(io.StringIO(csv_string))

print('processing data')
books['read'] = 1
num_readers = books.groupby(['book_id'])['user_id'].count().reset_index().rename(columns={'user_id':'num_readers'})
pop_book_cutoff = num_readers['num_readers'].describe(percentiles=[.95])['95%']
pop_book_ids = sorted(list(num_readers[num_readers['num_readers']>=pop_book_cutoff]['book_id']))
books = books[books['book_id'].isin(pop_book_ids)]

print('test / train split')
users = list(books['user_id'].unique())
test_sub = .9
train_sub = 1 - test_sub
train_users = random.sample(users, int(np.floor(len(users)*train_sub)))
books_train = books[books['user_id'].isin(train_users)]
# books_test = books[~books['user_id'].isin(train_users)]

print('readjust book ids')
books_train_book_ids = sorted(list(books_train['book_id'].unique()))
books_train_book_ids_df = pd.DataFrame(list(zip(books_train_book_ids, range(len(books_train_book_ids)))), columns=['book_id','adj_book_id'])
books_train = books_train.merge(books_train_book_ids_df)
# books_test = books_test.merge(books_train_book_ids_df)

print('creating csr')
sparse_user_item = sparse.csr_matrix((books_train['read'], (books_train['user_id'], books_train['adj_book_id'])))
sparse_item_user = sparse.csr_matrix((books_train['read'], (books_train['adj_book_id'], books_train['user_id'])))

print('fitting model')
# Initialize the als model and fit it using the sparse item-user matrix
model = implicit.als.AlternatingLeastSquares(factors=20, regularization=0.1, iterations=3)
# Calculate the confidence by multiplying it by our alpha value.
alpha_val = 15
data_conf = (sparse_item_user * alpha_val).astype('double')
# Fit the model
model.fit(data_conf)

print('saving user factors model to s3')
user_factors_data = io.BytesIO()
pickle.dump(model.user_factors, user_factors_data)
user_factors_data.seek(0)
client.upload_fileobj(user_factors_data, BUCKET_PATH, 'model/user_factors.pkl')

print('saving item factors model to s3')
item_factors_data = io.BytesIO()
pickle.dump(model.item_factors, item_factors_data)
item_factors_data.seek(0)
client.upload_fileobj(item_factors_data, BUCKET_PATH, 'model/item_factors.pkl')

print('success')