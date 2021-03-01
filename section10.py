exec(open("/home/jere/Dropbox/University/Tesina/src/section9.py").read())
#### EXPLORE THE EFFECT THAT DIFFERENT HYPERPARAMETERS HAVE ON SVM-RBF

results_folder_imbalance= "/home/jere/Desktop/section10/"
 
def explore_rbf_potential(train="b278",test="b234",kernel="rbf"):
  
    X,y=get_feature_selected_tile(train,kernel,train,"full")   
    Xt,yt=get_feature_selected_tile(test,kernel,train,"full")  
    fig, ax = plt.subplots(figsize=(20,10))
    scores = {}
    
    for c in np.logspace(-5, 12, 18):
        for gamma in np.logspace(-15, 4,20):
            clf = Pipeline([("discretizer",KBinsDiscretizer(n_bins=get_optimal_parameters_fs("svmk")["n_bins"], encode='ordinal', strategy='quantile')),
                    ("scaler",StandardScaler()),
                    ("feature_map", Nystroem(gamma=gamma, n_components=300)),
                    ("svm", LinearSVC(dual=False,max_iter=100000,C=c))])

            clf.fit(X,y)
            decs  = clf.decision_function(Xt)
            
            s = stats.describe(decs)
            if ( abs(s.minmax[0] - s.minmax[1]) < 0.1 ):
                scores[(c,gamma)] = -1
                continue
            
            p,r,t = metrics.precision_recall_curve(yt,decs)

            precision_fold, recall_fold, thresh = p[::-1], r[::-1], t[::-1]
            recall_interpolated    = np.linspace(min_recall_global, 1, n_samples_prc)
            precision_interpolated = np.interp(recall_interpolated, recall_fold, precision_fold)
            scores[(c,gamma)] = auc(recall_interpolated, precision_interpolated)

    with open(results_folder_imbalance+ "_svmk_train="+train+"test="+test+"_scores.pkl", 'wb') as s_file:
        pickle.dump(scores,s_file)
    return scores  


def explore_rbf_potentialRESPALDO(train="b278",test="b234"):
    
    save_folder = "/home/jere/Desktop/section9/"

    X,y=retrieve_tile(train)
    Xt,yt=retrieve_tile(test)   
    fig, ax = plt.subplots(figsize=(20,10))
    scores = {}
    
    for c in np.logspace(-5, 12, 18):
        for gamma in np.logspace(-15, 4,20):
            clf = Pipeline([("discretizer",KBinsDiscretizer(n_bins=100, encode='ordinal', strategy='quantile')),
                    ("scaler",StandardScaler()),
                    ("feature_map", Nystroem(gamma=gamma, n_components=300)),
                    ("svm", LinearSVC(dual=False,max_iter=100000,C=c))])

            clf.fit(X,y)
            decs  = clf.decision_function(Xt)
            
            s = stats.describe(decs)
            if ( abs(s.minmax[0] - s.minmax[1]) < 0.1 ):
                scores[(c,gamma)] = -1
                continue
            
            p,r,t = metrics.precision_recall_curve(yt,decs)

            precision_fold, recall_fold, thresh = p[::-1], r[::-1], t[::-1]
            recall_interpolated    = np.linspace(min_recall_global, 1, n_samples_prc)
            precision_interpolated = np.interp(recall_interpolated, recall_fold, precision_fold)
            scores[(c,gamma)] = (p,r,auc(recall_interpolated, precision_interpolated))

    with open(save_folder+ "_svmk_train="+train+"test="+test+"_scores.pkl", 'wb') as s_file:
        pickle.dump(scores,s_file)
    return scores  

def calculate_all_potential_rbf():
    scores1= explore_rbf_potential(train="b278",test="b234")
    scores2= explore_rbf_potential(train="b278",test="b261")
    scores3= explore_rbf_potential(train="b234",test="b261")
    scores4= explore_rbf_potential(train="b234",test="b360")
    scores5= explore_rbf_potential(train="b261",test="b360")
    scores6= explore_rbf_potential(train="b261",test="b278")
    scores7= explore_rbf_potential(train="b360",test="b278")
    scores8= explore_rbf_potential(train="b360",test="b234")     

def plot_rbf_potential(train="b278",test="b234",legacy=False):

    if (legacy):
        prefix = "legacy/"
    else:
        prefix = ""
    
    with open(results_folder_imbalance+prefix+ "_svmk_train="+train+"test="+test+"_scores.pkl", 'rb') as s_file:
        scores = pickle.load(s_file)

    c_values = np.logspace(-5, 12, 18)
    g_values = np.logspace(-15, 4,20)
    perf = np.zeros((18,20))

    for i in range(0,len(c_values)-1):
        c = c_values[i]
        for j in range(0,len(g_values)-1):
            gamma = g_values[j]
            if scores[(c,gamma)]!=-1
                perf[i,j] = scores[(c,gamma)]
            else
                perf[i,j] = 0
            
    fig, ax = plt.subplots(figsize=(11, 9))
    sb.heatmap(df_m,square=True,vmin= min_s, vmax=max_s, cmap="magma", linewidth=.3, linecolor='w')

    xlabels = [ "{:.0e}".format(x) for x in c_values ]
    ylabels = g_values

    plt.xticks(np.arange(len(svm_param_grid_hist[0]['discretizer__n_bins']))+.5, labels=ylabels,rotation=60)
    plt.yticks(np.arange(len(svm_param_grid_hist[0]['clf__C']))+.5, labels=xlabels, rotation=45)


    plt.xlabel('gamma')
    plt.ylabel('C')
    plt.colorbar()
    plt.xticks(np.arange(len(g_values)), g_values, rotation=45)
    plt.yticks(np.arange(len(c_values)), c_values, rotation=0)
    plt.title('Average validation  Robust AUCPRC')
    plt.savefig(results_folder_imbalance+"_svmk_train="+train+"test="+test+"_grid.png")


        df_m = scores_l   
        fig, ax = plt.subplots(figsize=(11, 9))
        sb.heatmap(df_m,square=True,vmin= min_s, vmax=max_s, cmap=cmap, center=center, linewidth=.3, linecolor='w')

        xlabels = [ "{:.0e}".format(x) for x in svm_param_grid_hist[0]['clf__C'] ]
        ylabels = svm_param_grid_hist[0]['discretizer__n_bins']

        plt.xticks(np.arange(len(svm_param_grid_hist[0]['discretizer__n_bins']))+.5, labels=ylabels,rotation=60)
        plt.yticks(np.arange(len(svm_param_grid_hist[0]['clf__C']))+.5, labels=xlabels, rotation=45)

        # axis labels
        plt.ylabel('C')
        plt.xlabel('nbins')
        # title
        title = 'Average Robust AUCPRC'.upper()
        plt.title(title, loc='left')

        if cmap==None:
            plt.savefig(results_folder_preproces+"heatmapl"+"NONE.png")
        else:
            plt.savefig(results_folder_preproces+"heatmapl"+cmap+".png")
            
        
def calculate_all_grids():
    scores1= plot_rbf_potential(train="b278",test="b234")
    scores2= plot_rbf_potential(train="b278",test="b261")
    scores3= plot_rbf_potential(train="b234",test="b261")
    scores4= plot_rbf_potential(train="b234",test="b360")
    scores5= plot_rbf_potential(train="b261",test="b360")
    scores6= plot_rbf_potential(train="b261",test="b278")
    scores7= plot_rbf_potential(train="b360",test="b278")
    scores8= plot_rbf_potential(train="b360",test="b234")    





#######################################################################################
################# DEBUGGING RBF: WHY DOES IT WORK SO POORLY?? #########################

#### Analisis 0: El C elegido generaliza muy mal

# Number of kernel approximate components
def effect_of_C_svm_rbf(train="b278",test="b234"):

    X,y = retrieve_tile(train,"full")
    Xt,yt=retrieve_tile(test) 
    fig, ax = plt.subplots()

    for val_c in np.logspace(-5, 15, 21):
    
        clf = Pipeline( 
            [("discretizer",KBinsDiscretizer(n_bins=100, encode='ordinal', strategy='quantile')),
             ("scaler",StandardScaler()), 
             ("feature_map", Nystroem(gamma=0.0001,n_components=300)), 
             ("svm", LinearSVC(dual=False,max_iter=100000,C=val_c))])

        clf.fit(X,y)
        decs  = clf.decision_function(Xt)
        p,r,t = metrics.precision_recall_curve(yt,decs)
        ax.plot(r,p,label="C="+str(val_c))  

    leg = ax.legend(ncol=3)
    plt.xlabel('recall')
    plt.ylabel('precision')
    plt.title('100Bins+StandardScaler+NystroemKernelAprox+SVM-Linear. Effect of C' + str(train) + ' testing in '+str(test))
    plt.show()  
    
#### Analysis 1: Is the approximator to blame? #####

# Number of kernel approximate components
def number_of_approximate_components_svmk(train="b278",test="b234"):

    clf = Pipeline( 
        [("discretizer",KBinsDiscretizer(n_bins=100, encode='ordinal', strategy='quantile')),
         ("scaler",StandardScaler()), 
         ("feature_map", Nystroem(gamma=0.0001)), 
         ("svm", LinearSVC(dual=False,max_iter=100000,C=1000000000000.0))])


    X,y = retrieve_tile(train,"full")
    Xt,yt=retrieve_tile(test) 

    fig, ax = plt.subplots()
        
    grid = 30 * np.arange(1, 13)
            
    for d in grid[:len(grid)//2]:
        clf.set_params(feature_map__n_components=d)
        clf.fit(X,y)
        decs  = clf.decision_function(Xt)
        p,r,t = metrics.precision_recall_curve(yt,decs)
        ax.plot(r,p,label=str(d)+" features")  
        
    for d in grid[len(grid)//2+1:]:
        clf.set_params(feature_map__n_components=d)
        clf.fit(X,y)
        decs  = clf.decision_function(Xt)
        p,r,t = metrics.precision_recall_curve(yt,decs)
        ax.plot(r,p,linestyle="dashed",label=str(d)+" features")  
        
    leg = ax.legend(ncol=3)
    plt.xlabel('recall')
    plt.ylabel('precision')
    plt.title('100Bins+StandardScaler+NystroemKernelAprox+SVM-Linear. Effect of # components in Nystroem ' + str(train) + ' testing in '+str(test))

    plt.show()  

def number_of_approximate_components_svmk_old_hyp(train="b278",test="b234"):

    clf = Pipeline( 
        [("discretizer",KBinsDiscretizer(n_bins=100, encode='ordinal', strategy='quantile')),
         ("scaler",StandardScaler()), 
         ("feature_map", Nystroem(gamma=0.0001)), 
         ("svm", LinearSVC(dual=False,max_iter=100000,C=10000.0))])


    X,y = retrieve_tile(train,"full")
    Xt,yt=retrieve_tile(test) 

    fig, ax = plt.subplots()
        
    grid = 30 * np.arange(1, 13)
            
    for d in grid[:len(grid)//2]:
        clf.set_params(feature_map__n_components=d)
        clf.fit(X,y)
        decs  = clf.decision_function(Xt)
        p,r,t = metrics.precision_recall_curve(yt,decs)
        ax.plot(r,p,label=str(d)+" features")  
        
    for d in grid[len(grid)//2+1:]:
        clf.set_params(feature_map__n_components=d)
        clf.fit(X,y)
        decs  = clf.decision_function(Xt)
        p,r,t = metrics.precision_recall_curve(yt,decs)
        ax.plot(r,p,linestyle="dashed",label=str(d)+" features")  
        
    leg = ax.legend(ncol=3)
    plt.xlabel('recall')
    plt.ylabel('precision')
    plt.title('100Bins+StandardScaler+NystroemKernelAprox+SVM-Linear. Effect of # components in Nystroem ' + str(train) + ' testing in '+str(test))

    plt.show()  
    
def number_of_approximate_components_svmk_no_bins(train="b278",test="b234"):

    clf = Pipeline( 
        [("scaler",StandardScaler()), 
         ("feature_map", Nystroem(gamma=0.0001)), 
         ("svm", LinearSVC(dual=False,max_iter=100000,C=1000000000000.0))])


    X,y = retrieve_tile(train,"full")
    Xt,yt=retrieve_tile(test) 

    fig, ax = plt.subplots()
        
    grid = 30 * np.arange(1, 13)
            
    for d in grid[:len(grid)//2]:
        clf.set_params(feature_map__n_components=d)
        clf.fit(X,y)
        decs  = clf.decision_function(Xt)
        p,r,t = metrics.precision_recall_curve(yt,decs)
        ax.plot(r,p,label=str(d)+" features")  
        
    for d in grid[len(grid)//2+1:]:
        clf.set_params(feature_map__n_components=d)
        clf.fit(X,y)
        decs  = clf.decision_function(Xt)
        p,r,t = metrics.precision_recall_curve(yt,decs)
        ax.plot(r,p,linestyle="dashed",label=str(d)+" features")  
        
    leg = ax.legend(ncol=3)
    plt.xlabel('recall')
    plt.ylabel('precision')
    plt.title('100Bins+StandardScaler+NystroemKernelAprox+SVM-Linear. Effect of # components in Nystroem ' + str(train) + ' testing in '+str(test))

    plt.show()      
    
# Looks like... the more componentes, the more performance, as expected. With a notable exception when training with b234
# Let's compare with the real RBF
    
# Svm-kernel real vs svm-kernel aprox with optimal parameters
def svmkreal_vs_aproximado_bins(train="b278",test="b234"):
    
    fig, ax = plt.subplots()

    rate = "1:100"
    X,y = retrieve_tile(train,rate)
    Xt,yt=retrieve_tile(test)   
    
    clf = Pipeline(
        [("discretizer",KBinsDiscretizer(n_bins=100, encode='ordinal', strategy='quantile')),
         ("scaler",StandardScaler()), 
         ("svm", SVC(kernel="rbf",max_iter=100000,C=1000000000000,gamma=0.0001))])
    clf.fit(X,y)
    decs  = clf.decision_function(Xt)
    p,r,t = metrics.precision_recall_curve(yt,decs)
    ax.plot(r,p,label="100bins+Scaler+ svm rbf exacto rate 1:100") 

    print("Finished real SVM")
    
    X,y = retrieve_tile(train,"full")

    clf = Pipeline( 
        [("discretizer",KBinsDiscretizer(n_bins=100, encode='ordinal', strategy='quantile')),
         ("scaler",StandardScaler()), 
         ("feature_map", Nystroem(gamma=0.0001, n_components=150)), 
         ("svm", LinearSVC(dual=False,max_iter=100000,C=1000000000000.0))])

    clf.fit(X,y)
    decs  = clf.decision_function(Xt)
    p,r,t = metrics.precision_recall_curve(yt,decs)
    ax.plot(r,p,label="100bins+Scaler+ svm aproximado Nystroem 150 componentes") 

    clf = Pipeline( 
        [("discretizer",KBinsDiscretizer(n_bins=100, encode='ordinal', strategy='quantile')),
         ("scaler",StandardScaler()), 
         ("feature_map", Nystroem(gamma=0.0001, n_components=300)), 
         ("svm", LinearSVC(dual=False,max_iter=100000,C=1000000000000.0))])

    clf.fit(X,y)
    decs  = clf.decision_function(Xt)
    p,r,t = metrics.precision_recall_curve(yt,decs)
    ax.plot(r,p,label="100bins+Scaler+ svm aproximado Nystroem 300 componentes") 

    X,y = retrieve_tile(train,rate)
    Xt,yt=retrieve_tile(test)   

    clf = Pipeline( 
        [("discretizer",KBinsDiscretizer(n_bins=100, encode='ordinal', strategy='quantile')),
         ("scaler",StandardScaler()), 
         ("feature_map", Nystroem(gamma=0.0001, n_components=150)), 
         ("svm", LinearSVC(dual=False,max_iter=100000,C=1000000000000.0))])

    clf.fit(X,y)
    decs  = clf.decision_function(Xt)
    p,r,t = metrics.precision_recall_curve(yt,decs)
    ax.plot(r,p,label="100bins+Scaler+ svm aproximado Nystroem 150 componentes 1:100") 

    clf = Pipeline( 
        [("discretizer",KBinsDiscretizer(n_bins=100, encode='ordinal', strategy='quantile')),
         ("scaler",StandardScaler()), 
         ("feature_map", Nystroem(gamma=0.0001, n_components=300)), 
         ("svm", LinearSVC(dual=False,max_iter=100000,C=1000000000000.0))])

    clf.fit(X,y)
    decs  = clf.decision_function(Xt)
    p,r,t = metrics.precision_recall_curve(yt,decs)
    ax.plot(r,p,label="100bins+Scaler+ svm aproximado Nystroem 300 componentes 1:100") 
    
    leg = ax.legend()
    plt.xlabel('recall')
    plt.ylabel('precision')
    plt.title('Nystroem rbf approximator vs SVC-rbf exacto' + str(train) + ' testing in '+str(test))
    
    plt.show()  

# Svm-kernel real vs svm-kernel aprox with sub-optimal parameters and higher rate
def svmkreal_vs_aproximado_bins_subopt(train="b278",test="b234"):
    
    Xt,yt=retrieve_tile(test)   
    fig, ax = plt.subplots()
    
    rate = "1:500"
    X,y = retrieve_tile(train,rate)
    clf = Pipeline(
        [("discretizer",KBinsDiscretizer(n_bins=100, encode='ordinal', strategy='quantile')),
         ("scaler",StandardScaler()), 
         ("svm", SVC(kernel="rbf",max_iter=100000,C=10000,gamma=0.0001))])
    clf.fit(X,y)
    decs  = clf.decision_function(Xt)
    p,r,t = metrics.precision_recall_curve(yt,decs)
    ax.plot(r,p,label="100bins+Scaler+ svm rbf exacto rate 1:500") 
    leg = ax.legend()
    plt.xlabel('recall')
    plt.ylabel('precision')
    plt.title('Nystroem rbf approximator vs SVC-rbf exacto' + str(train) + ' testing in '+str(test))
    
    print("Finished real SVM")
    
    X,y = retrieve_tile(train,"full")



    clf = Pipeline( 
        [("discretizer",KBinsDiscretizer(n_bins=100, encode='ordinal', strategy='quantile')),
         ("scaler",StandardScaler()), 
         ("feature_map", Nystroem(gamma=0.0001, n_components=150)), 
         ("svm", LinearSVC(dual=False,max_iter=100000,C=10000.0))])

    clf.fit(X,y)
    decs  = clf.decision_function(Xt)
    p,r,t = metrics.precision_recall_curve(yt,decs)
    ax.plot(r,p,label="100bins+Scaler+ svm aproximado Nystroem 150 componentes") 

    clf = Pipeline( 
        [("discretizer",KBinsDiscretizer(n_bins=100, encode='ordinal', strategy='quantile')),
         ("scaler",StandardScaler()), 
         ("feature_map", Nystroem(gamma=0.0001, n_components=300)), 
         ("svm", LinearSVC(dual=False,max_iter=100000,C=10000.0))])

    clf.fit(X,y)
    decs  = clf.decision_function(Xt)
    p,r,t = metrics.precision_recall_curve(yt,decs)
    ax.plot(r,p,label="100bins+Scaler+ svm aproximado Nystroem 300 componentes") 

    X,y = retrieve_tile(train,rate)
    Xt,yt=retrieve_tile(test)   
    fig, ax = plt.subplots()


    clf = Pipeline( 
        [("discretizer",KBinsDiscretizer(n_bins=100, encode='ordinal', strategy='quantile')),
         ("scaler",StandardScaler()), 
         ("feature_map", Nystroem(gamma=0.0001, n_components=150)), 
         ("svm", LinearSVC(dual=False,max_iter=100000,C=10000.0))])

    clf.fit(X,y)
    decs  = clf.decision_function(Xt)
    p,r,t = metrics.precision_recall_curve(yt,decs)
    ax.plot(r,p,label="100bins+Scaler+ svm aproximado Nystroem 150 componentes 1:500") 

    clf = Pipeline( 
        [("discretizer",KBinsDiscretizer(n_bins=100, encode='ordinal', strategy='quantile')),
         ("scaler",StandardScaler()), 
         ("feature_map", Nystroem(gamma=0.0001, n_components=300)), 
         ("svm", LinearSVC(dual=False,max_iter=100000,C=10000.0))])

    clf.fit(X,y)
    decs  = clf.decision_function(Xt)
    p,r,t = metrics.precision_recall_curve(yt,decs)
    ax.plot(r,p,label="100bins+Scaler+ svm aproximado Nystroem 300 componentes 1:500") 
    

    plt.show()  
    
    
def svmkreal_vs_aproximado_nobins(train="b278",test="b234"):
    X,y = retrieve_tile(train,"full")
    Xt,yt=retrieve_tile(test)   
    fig, ax = plt.subplots()

    clf = Pipeline(
        [("scaler",StandardScaler()), 
         ("feature_map", Nystroem(n_components=300,gamma=0.00017782794100389227)), 
         ("svm", LinearSVC(dual=False,max_iter=100000,C=10000))])
         
    clf.fit(X,y)
    decs  = clf.decision_function(Xt)
    p,r,t = metrics.precision_recall_curve(yt,decs)
    ax.plot(r,p,label="100bins+Scaler+ svm aproximado Nystroem 300 componentes") 

    X,y = retrieve_tile(train,"1:100")
    clf = Pipeline(
        [("scaler",StandardScaler()), 
         ("svm", SVC(kernel="rbf",max_iter=100000,C=10000,gamma=0.00017782794100389227))])
    clf.fit(X,y)
    decs  = clf.decision_function(Xt)
    p,r,t = metrics.precision_recall_curve(yt,decs)
    ax.plot(r,p,label="100bins+Scaler+ svm rbf exacto rate 1:100") 
    leg = ax.legend()
    plt.xlabel('recall')
    plt.ylabel('precision')
    plt.title('Nystroem rbf approximator vs SVC-rbf exacto' + str(train) + ' testing in '+str(test))

    plt.show()  
    
    
    


#######################################################################################
############################### RULING OUT ERRORS ##################################### 

#  decisionfunc vs predict_proba
def probabilities_svm():
    X,y = retrieve_tile("b278","full") 
    Xt,yt=retrieve_tile(test)
    fig, ax = plt.subplots()

    clf = make_pipeline(StandardScaler(),LinearSVC(C=0.01,verbose=3,dual=False, max_iter=100000))
    clf.fit(X, y)
    decs  = clf.decision_function(Xt)
    p,r,t = metrics.precision_recall_curve(yt,decs)
    ax.plot(r,p,label="decision_func")

    clf2 = make_pipeline(StandardScaler(),LinearSVC(C=0.01,verbose=3,dual=False, max_iter=100000))
    clf = CalibratedClassifierCV(clf2) 
    clf.fit(X, y)
    y_proba = clf.predict_proba(Xt)
    p,r,t = metrics.precision_recall_curve(yt, y_proba[:,1])
    ax.plot(r,p,label="predict_proba")  

    leg = ax.legend();
    plt.xlabel('recall')
    plt.ylabel('precision')
    plt.show()

#tolerance parameter in svm
def tol_experiment():
    
    X,y = retrieve_tile("b278","full") 
    Xt,yt=retrieve_tile("b234")  
    fig, ax = plt.subplots()

    clf = make_pipeline(StandardScaler(),LinearSVC(C=0.1,verbose=3,dual=False, max_iter=100000,tol=1e-12))
    clf.fit(X, y)
    decs  = clf.decision_function(Xt)
    p,r,t = metrics.precision_recall_curve(yt,decs)
    ax.plot(r,p,label="tol=1e-12")


    clf = make_pipeline(StandardScaler(),LinearSVC(C=0.1,verbose=3,dual=False, max_iter=100000,tol=1e-4))
    clf.fit(X, y)
    decs  = clf.decision_function(Xt)
    p,r,t = metrics.precision_recall_curve(yt,decs)
    ax.plot(r,p,label="tol=1e-4")

    clf = make_pipeline(StandardScaler(),LinearSVC(C=0.1,verbose=3,dual=True, max_iter=100000,tol=1e-12))
    clf.fit(X, y)
    decs  = clf.decision_function(Xt)
    p,r,t = metrics.precision_recall_curve(yt,decs)
    ax.plot(r,p,label="tol=1e-12 noD")


    clf = make_pipeline(StandardScaler(),LinearSVC(C=0.1,verbose=3,dual=True, max_iter=100000,tol=1e-4))
    clf.fit(X, y)
    decs  = clf.decision_function(Xt)
    p,r,t = metrics.precision_recall_curve(yt,decs)
    ax.plot(r,p,label="tol=1e-4 NoD")

    clf = make_pipeline(StandardScaler(),LinearSVC(C=10,verbose=3,dual=False, max_iter=100000,tol=1e-12))
    clf.fit(X, y)
    decs  = clf.decision_function(Xt)
    p,r,t = metrics.precision_recall_curve(yt,decs)
    ax.plot(r,p,label="tol=1e-12 10")


    clf = make_pipeline(StandardScaler(),LinearSVC(C=10,verbose=3,dual=False, max_iter=100000,tol=1e-4))
    clf.fit(X, y)
    decs  = clf.decision_function(Xt)
    p,r,t = metrics.precision_recall_curve(yt,decs)
    ax.plot(r,p,label="tol=1e-4 10")

    clf = make_pipeline(StandardScaler(),LinearSVC(C=10,verbose=3,dual=True, max_iter=100000,tol=1e-12))
    clf.fit(X, y)
    decs  = clf.decision_function(Xt)
    p,r,t = metrics.precision_recall_curve(yt,decs)
    ax.plot(r,p,label="tol=1e-12 noD 10")


    clf = make_pipeline(StandardScaler(),LinearSVC(C=10,verbose=3,dual=True, max_iter=100000,tol=1e-4))
    clf.fit(X, y)
    decs  = clf.decision_function(Xt)
    p,r,t = metrics.precision_recall_curve(yt,decs)
    ax.plot(r,p,label="tol=1e-4 NoD 10")

    leg = ax.legend()
    plt.xlabel('recall')
    plt.ylabel('precision')
    plt.show()
    
