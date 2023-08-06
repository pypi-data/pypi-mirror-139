Provides basic postgres functions for databases request.

**select**:
 ```python
def get_my_data():
    def _(cursor):
        cursor.execute(f"select data from database")
        return cursor.fetchone()

    result = select(_)

    return result.get('data') if result else None
 ```

**insert**:

 ```python
def insert_my_data():
    data = {
        'data_1': data_1,
        'data_2': data_2
    }

    insert(TABLE_NAME, data)
 ```

**update**:
the primary key can be a string for array who have only one primary key but if it's a tuple, 
you can put a table of string : ['first_primay_key', 'second_primay_key']
 ```python
def update_my_data():
    data = {
        'data_1': data_1,
        'data_2': data_2
    }

    update(TABLE_NAME, 'my_primary_key', data)
 ```

**upsert**:
Upsert is a function who insert if the data doesn't exist. And update if the data can be updated.
the primary key can be a string for array who have only one primary key but if it's a tuple, 
you can put a table of string : ['first_primay_key', 'second_primay_key']
 ```python
def upsert_my_data():
    data = {
        'data_1': data_1,
        'data_2': data_2
    }

    upsert(TABLE_NAME, 'my_primary_key', data)
 ```

**delete**:

 ```python
def delete_my_data():
    delete(TABLE_NAME, primary_key, data_id)
 ```