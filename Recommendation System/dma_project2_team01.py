# -*- coding: utf-8 -*-
"""Dma_project2_team01

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1rkprxhW8iLEYIdW_3OeJlNPhk_1t9FJR
"""

# TODO: CHANGE THIS FILE NAME TO DMA_project2_team##.py
# EX. TEAM 1 --> DMA_project2_team01.py

# TODO: IMPORT LIBRARIES NEEDED FOR PROJECT 2
import mysql.connector
import os
import surprise
from surprise import Dataset
from surprise import Reader
from collections import defaultdict
import numpy as np
import pandas as pd
from sklearn import tree
import graphviz
from mlxtend.frequent_patterns import association_rules, apriori


np.random.seed(0)

# TODO: CHANGE GRAPHVIZ DIRECTORY
os.environ["PATH"] += os.pathsep + 'C:/Program Files/Graphviz 2.44.1/bin/'

# TODO: CHANGE MYSQL INFORMATION, team number 
HOST = 'localhost'
USER = 'root'
PASSWORD = '827anfrhk@'
SCHEMA = 'DMA_team01'
team = 1
# PART 1: Decision tree 
def part1():
    cnx = mysql.connector.connect(host=HOST, user=USER, password=PASSWORD)
    cursor = cnx.cursor()
    cursor.execute('SET GLOBAL innodb_buffer_pool_size=2*1024*1024*1024;')
    cursor.execute('USE %s;' % SCHEMA)
    print('1-1 start')
    # TODO: Requirement 1-1. MAKE app_prize column
    cursor.execute('''SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_NAME=\'APP\' 
    AND COLUMN_NAME=\'APP_PRIZE\';''')
    
    exist=bool(cursor.fetchall())
    
    if not exist:
        print('app_prize를 추가합니다.')
        cursor.execute('ALTER TABLE APP ADD APP_PRIZE TINYINT(1) DEFAULT 0;')
    else:
        print('app_prize 가 이미 있습니다.')
        
    
    app_prize_list=pd.read_csv('C:/Users/Sunny.LAPTOP-L010FOP1/Desktop/DMA_project2/DMA_project2/app_prize_list.txt',header=None )
    cursor.execute('''
    SELECT ID FROM app
       ''')
    rows=cursor.fetchall()
    rows=[id[0] for id in rows]
    for i in rows:
        if i in list(app_prize_list[0]):
            cursor.execute('UPDATE app SET app_prize=%d WHERE ID=\'%s\';'%(1,i))
    cnx.commit()


    print('1-2 start')
    # TODO: Requirement 1-2. WRITE MYSQL QUERY AND EXECUTE. SAVE to .csv file
    cursor.execute('''
    SELECT id, app.app_prize, description,
    IF(isnull(pricing_hint),0,1) AS have_pricing_hint,
    
    (SELECT COUNT(*) FROM app_category WHERE app_id=id) AS num_of_categories,
    (SELECT COUNT(*) FROM pricing_plan WHERE app_id=app.id) AS num_of_pricing_plans,
    (SELECT COUNT(*) FROM review WHERE app_id=app.id) AS num_of_reviews,
    (SELECT AVG(rating) FROM review WHERE app_id=app.id) AS avg_of_ratings,
    (SELECT COUNT(*) FROM reply WHERE developer_id=app.developer_id) AS num_of_replies   
    
    FROM app;
    ''')    
    
    result=cursor.fetchall()
    result=pd.DataFrame(result)
    result.columns=['id','app_prize','description','have_pricing_hint',
                                   'num_of_categories','num_of_pricing_plans','num_of_reviews',
                                   'avg_of_ratings','num_of_replies']
    result=result.fillna(0)
    result.to_csv('DMA_project2_team01_part1.csv',index=False)

    print('1-3 start')
    # TODO: Requirement 1-3. MAKE AND SAVE DECISION TREE
    # gini file name: DMA_project2_team##_part1_gini.pdf
    # entropy file name: DMA_project2_team##_part1_entropy.pdf
    data=pd.read_csv('DMA_project2_team01_part1.csv')
    y=np.array(data['app_prize'])
    X=np.array(data.drop(['id','app_prize'],axis=1))
    clf_gini=tree.DecisionTreeClassifier(random_state=0,criterion='gini',min_samples_leaf=10, max_depth=5)
    clf_gini.fit(X,y)
    gini_graph = tree.export_graphviz(clf_gini, out_file=None, feature_names=data.columns[2:], class_names=['normal','PRIZE'])
    gini_graph = graphviz.Source(gini_graph)
    gini_graph.render('DMA_project2_team01_part1_gini', view=True)

    clf_entropy=tree.DecisionTreeClassifier(random_state=0,criterion='entropy',min_samples_leaf=10, max_depth=5)
    clf_entropy.fit(X,y)
    entropy_graph = tree.export_graphviz(clf_entropy, out_file=None, feature_names=data.columns[2:], class_names=['normal','PRIZE'])
    entropy_graph = graphviz.Source(entropy_graph)
    entropy_graph.render('DMA_project2_team01_part1_entropy', view=True)
    
    print('1-4 start')
    # TODO: Requirement 1-4. Don't need to append code for 1-4

    cursor.close()
    


# PART 2: Association analysis
def part2():
    cnx = mysql.connector.connect(host=HOST, user=USER, password=PASSWORD)
    cursor = cnx.cursor()
    cursor.execute('SET GLOBAL innodb_buffer_pool_size=2*1024*1024*1024;')
    cursor.execute('USE %s;' % SCHEMA)
    print('2-1 start')
    # TODO: Requirement 2-1. CREATE VIEW AND SAVE to .csv file
    cursor.execute('''
    CREATE OR REPLACE VIEW category_score AS
    SELECT *, num_developer+num_user+num_app AS score
    FROM(SELECT 
        category.id AS category_id,
        category.title AS category_title,
        (SELECT COUNT(*) FROM category_developer WHERE category_id=category.id) AS num_developer,
        (SELECT COUNT(*) FROM category_user WHERE category_id=category.id) AS num_user,
        (SELECT COUNT(*) FROM app_category WHERE category_id=category.id) AS num_app
        FROM category) AS ic
    ORDER BY score DESC
    LIMIT 30;
    ''')

    cursor.execute('SELECT * FROM category_score;')
    a=cursor.fetchall()
    result=pd.DataFrame(a)
    result.columns=['category_id', 'category_title', 'num_developer', 'num_user', 'num_app','score']
    result.to_csv('DMA_project2_team01_part2_category.csv')

    print('2-2 start')
    # TODO: Requirement 2-2. CREATE 2 VIEWS AND SAVE partial one to .csv file
   
    fopen = open('DMA_project2_team%02d_part2_UIR.csv' % team, 'w', encoding='utf-8')

    fopen.close()
    
    
    cursor.execute('''
    CREATE OR REPLACE VIEW user_item_rating AS
    SELECT total_rel.user_id AS user,cat_score.category_title as category, sum(total_rel.like_rating)+sum(if (total_rel.count_rating<5,total_rel.count_rating,5)) as rating FROM 

    (
    (SELECT count_app.user_id as user_id, count_app.category_id as category_id ,0 AS like_rating ,count_app.count_rating as count_rating FROM 
    (SELECT user_app.user_id as user_id, a.category_id as category_id, count(a.app_id) as count_rating 
        FROM
        (SELECT category_id,app_id FROM app_category) a
        JOIN
        (SELECT developer_id as user_id, id as app_id FROM app
        UNION ALL
        SELECT user_id, app_id FROM review) user_app 
        on a.app_id=user_app.app_id   
        GROUP BY a.category_id , user_app.user_id) count_app

    UNION ALL

    SELECT user_cat.user_id as user_id, user_cat.category_id as category_id,user_cat.like_rating as like_rating,0 as count_rating FROM
    (SELECT category_id,user_id,5 as like_rating FROM category_user
        UNION ALL
        SELECT category_id,developer_id as user_id ,5 as like_rating FROM category_developer) user_cat) total_rel

    JOIN
    
    (SELECT category_id,category_title FROM category_score) cat_score
    on total_rel.category_id=cat_score.category_id)
    GROUP BY total_rel.user_id, total_rel.category_id;
    ''')
    
    cursor.execute('''
    CREATE OR REPLACE VIEW partial_user_item_rating AS
    SELECT * 
    FROM USER_ITEM_RATING
    WHERE user in 
    (SELECT user FROM user_item_rating 
    GROUP BY user HAVING COUNT(user)>=12) ;
    ''')
    
    cursor.execute('SELECT * FROM partial_user_item_rating;')
    b=cursor.fetchall()
    result=pd.DataFrame(b)
    
    result.columns=(['user','category','rating'])
    
    result.to_csv('DMA_project2_team01_part2_UIR.csv',index=False)


    print('2-3 start')
    # TODO: Requirement 2-3. MAKE HORIZONTAL VIEW
    # file name: DMA_project2_team##_part2_horizontal.pkl
    uir_data=pd.read_csv('DMA_project2_team01_part2_UIR.csv')
    uir=uir_data.set_index(['user','category']).unstack()
    uir=uir.notnull().astype('int')
    uir.to_pickle('DMA_project2_team01_part2_horizontal.pkl')
    
    import surprise
    
    print('2-4 start')
    # TODO: Requirement 2-4. ASSOCIATION ANALYSIS
    # filename: DMA_project2_team##_part2_association.pkl (pandas dataframe)

    from mlxtend.frequent_patterns import association_rules, apriori

    frequent_itemsets = apriori(uir, min_support=0.05, use_colnames=True)
    rules =association_rules(frequent_itemsets,metric='lift',min_threshold=2)
    rules.to_pickle('DMA_project2_team01_part2_association.pkl')

    cursor.close()



# TODO: Requirement 3-1. WRITE get_top_n
def get_top_n(algo, testset, id_list, n=10, user_based=True):
    results = defaultdict(list)
    if user_based:
        # TODO: testset의 데이터 중에 user id가 id_list 안에 있는 데이터만 따로 testset_id로 저장
        # Hint: testset은 (user_id, item_id, default_rating)의 tuple을 요소로 갖는 list
        testset_id = []
        for test in testset:
            if test[0] in id_list:
                testset_id.append(test)
                
        predictions = algo.test(testset_id)
        for uid, iid, true_r, est, _ in predictions:
            results[uid]=results[uid]+[(iid,est)]
            
    else:
        # TODO: testset의 데이터 중 item id가 id_list 안에 있는 데이터만 따로 testset_id라는 list로 저장
        # Hint: testset은 (user_id, item_id, default_rating)의 tuple을 요소로 갖는 list
        testset_id = []
        for test in testset:
            if test[1] in id_list:
                testset_id.append(test)
                
        predictions = algo.test(testset_id)
        for uid, iid, true_r, est, _ in predictions:
            results[iid]=results[iid]+[(uid,est)]
            
            # TODO: results는 item_id를 key로, [(user_id, estimated_rating)의 tuple이 모인 list]를 value로 갖는 dictionary
            pass
    
    for id_, ratings in results.items():
        new_ratings=sorted(ratings, key = lambda item: item[1], reverse=True) 
        results[id_]=new_ratings[:n]
        
    return results

# PART 3. Requirement 3-2, 3-3, 3-4
def part3():
    
    file_path = 'DMA_project2_team%02d_part2_UIR.csv' % team
    reader = Reader(line_format='user item rating', sep=',', rating_scale=(1, 10), skip_lines=1)
    data = Dataset.load_from_file(file_path, reader=reader)
    trainset = data.build_full_trainset()
    testset = trainset.build_anti_testset()
    print('3-2 start')
    # TODO: Requirement 3-2. User-based Recommendation
    uid_list = ['583814', '1036252', '33000424']
    # TODO: set algorithm for 3-2-1
    options = {'name':'cosine', 'user_based':True}
    algo = surprise.KNNBasic(sim_options = options)
    algo.fit(trainset)
    results = get_top_n(algo, testset, uid_list, n=10, user_based=True)
    with open('3-2-1.txt', 'w') as f:
        for uid, ratings in sorted(results.items(), key=lambda x: x[0]):
            f.write('User ID %s top-10 results\n' % uid)
            for iid, score in ratings:
                f.write('Item ID %s\tscore %s\n' % (iid, str(score)))
            f.write('\n')

    # TODO: set algorithm for 3-2-2
    options = {'name':'pearson', 'user_based':True}
    algo = surprise.KNNWithMeans(sim_options = options)
    algo.fit(trainset)
    results = get_top_n(algo, testset, uid_list, n=10, user_based=True)
    with open('3-2-2.txt', 'w') as f:
        for uid, ratings in sorted(results.items(), key=lambda x: x[0]):
            f.write('User ID %s top-10 results\n' % uid)
            for iid, score in ratings:
                f.write('Item ID %s\tscore %s\n' % (iid, str(score)))
            f.write('\n')

    # TODO: 3-2-3. Best Model
    # 3-2-3 Best Model을 구하는 과정
    # for algorithm in [surprise.KNNBasic,surprise.KNNWithMeans,surprise.KNNWithZScore,surprise.KNNBaseline]:
    #     for func in ['cosine', 'pearson','pearson_baseline','msd']:
    #             options={'name': func}
    #             algo=algorithm(sim_options=options)
    #             result=surprise.model_selection.cross_validate(algo, data, measures=['RMSE'], cv=kfold, verbose=False)
    #             print(str(algorithm)+" with function "+str(func)+" RMSE Score: "+str(result['test_rmse'].mean()))
    best_algo_ub = algo_baseline_pearson_baseline=surprise.KNNBaseline(sim_options={'name':'pearson_baseline'})

    # TODO: Requirement 3-3. Item-based Recommendation
    print('3-3 start')
    iid_list = ['Dropshipping', 'Store design', 'Finances', 'Productivity', 'Marketing']
    # TODO - set algorithm for 3-3-1
    options = {'name':'cosine', 'user_based':False}
    algo = surprise.KNNBasic(sim_options = options)
    algo.fit(trainset)
    results = get_top_n(algo, testset, iid_list, n=10, user_based=False)
    with open('3-3-1.txt', 'w') as f:
        for iid, ratings in sorted(results.items(), key=lambda x: x[0]):
            f.write('Item ID %s top-10 results\n' % iid)
            for uid, score in ratings:
                f.write('User ID %s\tscore %s\n' % (uid, str(score)))
            f.write('\n')

    # TODO: set algorithm for 3-3-2
    options = {'name':'pearson', 'user_based':False}
    algo = surprise.KNNWithMeans(sim_options = options)
    algo.fit(trainset)
    results = get_top_n(algo, testset, iid_list, n=10, user_based=False)
    with open('3-3-2.txt', 'w') as f:
        for iid, ratings in sorted(results.items(), key=lambda x: x[0]):
            f.write('Item ID %s top-10 results\n' % iid)
            for uid, score in ratings:
                f.write('User ID %s\tscore %s\n' % (uid, str(score)))
            f.write('\n')

    # TODO: 3-3-3. Best Model
    # Best Model 구하는 과정
    # from surprise.model_selection import KFold
    # from surprise import KNNBasic, KNNWithMeans, KNNBaseline    
    # score=1000
    # best_algo=None
    # results=[]
    # for algorithm in [KNNBasic, KNNWithMeans, KNNBaseline]:
    #     for func in ['cosine', 'pearson','pearson_baseline','msd']:
    #         options={'name': func,'user_based': False}
    #         algo=algorithm(sim_options=options)
    #         kfold=KFold(n_splits=5,random_state=0)
    #         result=surprise.model_selection.cross_validate(algo, data, measures=['RMSE'], cv=kfold, verbose=False)
    #         print(str(algorithm)+" with function "+str(func)+" RMSE Score: "+str(result['test_rmse'].mean()))
    #         results.append(str(algorithm)+" with function "+str(func)+" RMSE Score: "+str(result['test_rmse'].mean()))
    #         if result['test_rmse'].mean()<score:
    #             score=result['test_rmse'].mean()
    #             best_algo=str(algorithm)+' with function '+str(func)
    # best_algo_ib = best_algo
    # best_score_ib=score
    # print(best_algo_ib)
    best_algo_ib =surprise.KNNBaseline(sim_options={'name':'msd','user_based':False})


    # TODO: Requirement 3-4. Matrix-factorization Recommendation
    # TODO: set algorithm for 3-4-1
    print('3-4 start')
    algo = surprise.SVD(n_factors=100, n_epochs=50, biased=False) 
    algo.fit(trainset)
    results = get_top_n(algo, testset, uid_list, n=10, user_based=True)
    with open('3-4-1.txt', 'w') as f:
        for uid, ratings in sorted(results.items(), key=lambda x: x[0]):
            f.write('User ID %s top-10 results\n' % uid)
            for iid, score in ratings:
                f.write('Item ID %s\tscore %s\n' % (iid, str(score)))
            f.write('\n')

    # TODO: set algorithm for 3-4-2
    algo = surprise.SVD(n_factors=200, n_epochs=100, biased=True)
    algo.fit(trainset)
    results = get_top_n(algo, testset, uid_list, n=10, user_based=True)
    with open('3-4-2.txt', 'w') as f:
        for uid, ratings in sorted(results.items(), key=lambda x: x[0]):
            f.write('User ID %s top-10 results\n' % uid)
            for iid, score in ratings:
                f.write('Item ID %s\tscore %s\n' % (iid, str(score)))
            f.write('\n')

    # TODO: set algorithm for 3-4-3
    algo = surprise.SVDpp(n_factors=100, n_epochs=50)
    algo.fit(trainset)
    results = get_top_n(algo, testset, uid_list, n=10, user_based=True)
    with open('3-4-3.txt', 'w') as f:
        for uid, ratings in sorted(results.items(), key=lambda x: x[0]):
            f.write('User ID %s top-10 results\n' % uid)
            for iid, score in ratings:
                f.write('Item ID %s\tscore %s\n' % (iid, str(score)))
            f.write('\n')

    # TODO: set algorithm for 3-4-4
    algo = surprise.SVDpp(n_factors=100, n_epochs=100) 
    algo.fit(trainset)
    results = get_top_n(algo, testset, uid_list, n=10, user_based=True)
    with open('3-4-4.txt', 'w') as f:
        for uid, ratings in sorted(results.items(), key=lambda x: x[0]):
            f.write('User ID %s top-10 results\n' % uid)
            for iid, score in ratings:
                f.write('Item ID %s\tscore %s\n' % (iid, str(score)))
            f.write('\n')

    # TODO: 3-4-5. Best Model
    # Best Model 구하는 과정.
#    from surprise.model_selection import KFold

#    score=1000
#    best_algo=None
#    n_factors_set=[50,100,200]
#    n_epochs_set=[10,20,50,100]
#    biased_set=[False, True]
#    algorithm=surprise.SVD
#    results=[]
#    for n_factors in n_factors_set:
#        for n_epochs in n_epochs_set:
#            for biased in biased_set:
#                algo=algorithm(n_factors=n_factors,n_epochs=n_epochs,biased=biased)
#                kfold=KFold(n_splits=5,random_state=0)
#                result=surprise.model_selection.cross_validate(algo, data, measures=['RMSE'],cv=kfold,verbose=False)
#                print(str(algorithm)+' with '+' n_factors: '+str(n_factors)+' n_epochs: '+str(n_epochs)+' biased: '+str(biased)+
#                    " RMSE score : "+str(result['test_rmse'].mean()))
#                results.append(str(algorithm)+' with '+' n_factors: '+str(n_factors)+' n_epochs: '+str(n_epochs)+' biased: '+str(biased)+
#                    " RMSE score : "+str(result['test_rmse'].mean()))
#                if result['test_rmse'].mean()<score:
#                    score=result['test_rmse'].mean()
#                    best_algo=str(algorithm)+' with '+' n_factors: '+str(n_factors)+' n_epochs: '+str(n_epochs)+' biased: '+str(biased)
#        best_algo_mf = surprise.SVDpp(n_factors=50, n_epochs=10) 
#
#    algorithm=surprise.SVDpp
#    for n_factors in n_factors_set:
#        for n_epochs in n_epochs_set:
#            algo=algorithm(n_factors=n_factors,n_epochs=n_epochs)
#            kfold=KFold(n_splits=5,random_state=0)
#            result=surprise.model_selection.cross_validate(algo, data, measures=['RMSE'],cv=kfold,verbose=False)
#            print(str(algorithm)+' with '+' n_factors: '+str(n_factors)+' n_epochs: '+str(n_epochs)+
#                    " RMSE score : "+str(result['test_rmse'].mean()))
#            results.append(str(algorithm)+' with '+' n_factors: '+str(n_factors)+' n_epochs: '+str(n_epochs)+
#                    " RMSE score : "+str(result['test_rmse'].mean()))
#            if result['test_rmse'].mean()<score:
#                score=result['test_rmse'].mean()
#                best_algo=str(algorithm)+' with '+' n_factors: '+str(n_factors)+' n_epochs: '+str(n_epochs)
#    best_algo_mf = best_algo
#    best_score_mf=score
#    print(best_algo_mf)    
     best_algo_mf = surprise.SVDpp(n_factors = 50, n_epochs=10) 

if __name__ == '__main__':
    part1()
    part2()
    part3()