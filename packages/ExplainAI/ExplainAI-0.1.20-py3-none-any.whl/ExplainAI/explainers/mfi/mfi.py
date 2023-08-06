
import pandas as pd
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")

def mse_feature_importance(model,data,target,preserve=True):

    standar=["<class 'sklearn.ensemble.forest.RandomForestRegressor'>",
             "<class 'sklearn.ensemble._forest.RandomForestRegressor'>"]
    str_type=str(type(model))
    # print(str_type)

    if str_type in standar:
        # check the model whether randomforest
        data=data.drop(target,axis=1)
        df=pd.DataFrame({"feature":data.columns[1:],
                     "MFI":model.feature_importances_[:-1]}) 
        if preserve:
            df.to_csv("mfi.csv")
        return df
    else:
        print("The model used is not tree-based, the MFI can not be estimated.")
        return None






def mse_feature_importance_plot(df,top=20):

    df_sort=df.sort_values(by="MFI",ascending=False)
    if len(df_sort)<top:
        df_top=df_sort
    else:
        df_top=df_sort[0:top]

    plt.figure()
    plt.barh(df_top["feature"],df_top["MFI"])
    plt.title('MSE-based feature importance')
    plt.show()


