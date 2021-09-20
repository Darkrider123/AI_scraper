from sklearn import preprocessing

def normalize_data(train_data,  validation_data, type=None):
    scaler = None
    if type == 'standard':
        scaler = preprocessing.StandardScaler()

    elif type == 'min_max':
        scaler = preprocessing.MinMaxScaler()

    elif type == 'l1':
        scaler = preprocessing.Normalizer(norm='l1')

    elif type == 'l2':
        scaler = preprocessing.Normalizer(norm='l2')

    if scaler is not None:
        scaler.fit(train_data)
        scaled_train_data = scaler.transform(train_data)
        scaled_validation_data = scaler.transform(validation_data) 
        return (scaled_train_data, scaled_validation_data)
    else:
        print("No scaling was performed. Raw data is returned.")
        return (train_data, validation_data)