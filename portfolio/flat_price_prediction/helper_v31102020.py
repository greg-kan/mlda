import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import auc, roc_auc_score, accuracy_score, precision_score, recall_score
from sklearn.metrics import f1_score, balanced_accuracy_score 
from sklearn.metrics import precision_recall_curve, roc_curve
from sklearn.metrics import confusion_matrix

def analyse_numeric(df, column, bns=30):
    '''Визуализирует распределения числовых переменных.
       Принимает параметром строковое название столбца
       Печатает различные статистические показатели и строит гистограмму'''
    count = df[column].count()
    mean = df[column].mean()
    std = df[column].std()
    median = df[column].median()
    perc25 = df[column].quantile(0.25)
    perc75 = df[column].quantile(0.75)
    IQR = perc75 - perc25
    range_min = df[column].min()
    range_max = df[column].max()
    margin = (range_max - range_min)/10
    range_start = range_min - margin
    range_stop = range_max + margin
    range_ = (range_start, range_stop)
    outliers = df[column].loc[(df[column] < perc25 - 1.5*IQR) | (df[column] > perc75 + 1.5*IQR)]

    print('Количество: {}, Среднее: {:.3f}, Стандартное отклонение: {:.3f}.'.format(count, mean, std))
    print('Минимум: {}, 25-й перцентиль: {}, Медиана: {}, 75-й перцентиль: {}, Максимум: {}, IQR: {}.'
          .format(range_min, perc25, median, perc75, range_max, IQR))
    print('Количество пропусков в столбце: ', pd.isnull(df[column]).sum())
    print('Границы выбросов: [{f}, {l}].'.format(f=perc25 - 1.5*IQR, l=perc75 + 1.5*IQR)
          , 'Количество выбросов: ', len(outliers))

    plt.figure()
    df[column].loc[df[column].between(perc25 - 1.5*IQR, perc75 + 1.5*IQR)] \
                    .hist(bins = bns, range = range_, label = 'В границах выбросов')
    outliers.hist(bins = bns, range = range_, label = 'Выбросы')
    
    plt.legend()

def print_classification_metrics(d_y_true, d_y_pred, d_y_pred_proba):
    '''Печатает метрики качества классификации.
       Параметры:
       - d_y_true - истинный значения
       - d_y_pred - предсказанные значения
       - d_y_pred_proba - предсказанные вероятности'''
    temp_dict = {}
    temp = accuracy_score(d_y_true, d_y_pred)
    temp_dict['accuracy'] = [temp, '(TP+TN)/(P+N)']

    temp = balanced_accuracy_score(d_y_true, d_y_pred)
    temp_dict['balanced accuracy'] = [temp, 'сбалансированная accuracy']
    
    temp = precision_score(d_y_true, d_y_pred)
    temp_dict['precision'] = [temp, 'точность = TP/(TP+FP)']
    
    temp = recall_score(d_y_true, d_y_pred)
    temp_dict['recall'] = [temp, 'полнота = TP/P']
    
    temp = f1_score(d_y_true, d_y_pred)
    temp_dict['f1_score'] = [temp, 'среднее гармоническое точности и полноты']
    
    temp = roc_auc_score(d_y_true, d_y_pred_proba)
    temp_dict['roc_auc'] = [temp, 'Area Under Curve - Receiver Operating Characteristic']    
    
    temp_df = pd.DataFrame.from_dict(temp_dict, orient='index', columns=['Значение','Описание'])
    display(temp_df)

    return

def get_boxplot(df, column, target):
    '''Строит boxplot - график для визуализации влияния признака column
       на целевую переменную target.
       Параметры:
       - df - датафрейм
       - column - столбец датафрейма (влияющий признак)
       - target - целевая переменная'''
    fig, ax = plt.subplots(figsize = (10, 3))
    sns.boxplot(x=column, y=target, 
                data=df[[column, target]],
                ax=ax)
    plt.xticks(rotation=45)
    ax.set_title('Boxplot for ' + column)
    plt.show() 

def display_roc_auc(d_y_true, d_y_pred_proba, d_font_scale):

    plt.style.use('seaborn-paper')
    sns.set(font_scale=d_font_scale)
    color_text = plt.get_cmap('PuBu')(0.85)

    '''Строит ROC - кривую
       Параметры:
       - d_y_true - истинный значения
       - d_y_pred_proba - предсказанные вероятности'''
    fpr, tpr, threshold = roc_curve(d_y_true, d_y_pred_proba)
    roc_auc = roc_auc_score(d_y_true, d_y_pred_proba)

    plt.figure()
    plt.plot([0, 1], label='Baseline', linestyle='--')
    plt.plot(fpr, tpr, label = 'Regression')
    plt.title('Logistic Regression ROC AUC = %0.3f' % roc_auc)
    plt.ylabel('True Positive Rate')
    plt.xlabel('False Positive Rate')
    plt.legend(loc = 'lower right')
    plt.show()  

def print_confusion_matrix(d_y_true, d_y_pred):
    '''Печатает confusion_matrix
       Параметры:
       - d_y_true - истинный значения
       - d_y_pred - предсказанные значения'''    
    conf_mat = confusion_matrix(d_y_true, d_y_pred)
    conf_mat[0,0], conf_mat[1,1] = conf_mat[1,1], conf_mat[0,0]
    print('Confusion matrix:\n{}'.format(conf_mat))  
    print('Размер тестовой выборки:', conf_mat[0,0]+conf_mat[0,1]+conf_mat[1,0]+conf_mat[1,1])   

def display_confusion_matrix(d_y_true, d_y_pred):
    '''Отображает confusion_matrix
       Параметры:
       - d_y_true - истинный значения
       - d_y_pred - предсказанные значения'''    
    conf_mat = confusion_matrix(d_y_true, d_y_pred)
    conf_mat[0,0], conf_mat[1,1] = conf_mat[1,1], conf_mat[0,0]
    class_names = ['Defaulted', 'Not Defaulted']
    df_cm = pd.DataFrame(conf_mat, index=class_names, columns=class_names)
    plt.figure(figsize = (7,5))
    sns.heatmap(df_cm, annot=True, fmt="d");    

def display_PR_curve(d_y_true, d_y_pred_proba, d_font_scale):
    '''Строит PRC - кривую
       Параметры:
       - d_y_true - истинный значения
       - d_y_pred_proba - предсказанные вероятности
       - d_font_scale - размер шрифта'''    

    plt.style.use('seaborn-paper')
    sns.set(font_scale=d_font_scale)
    # sns.set_color_codes("muted")

    plt.figure(figsize=(8, 6))
    precision, recall, thresholds = precision_recall_curve(d_y_true, d_y_pred_proba, pos_label=1)
    prc_auc_score_f = auc(recall, precision)
    plt.plot(recall, precision, lw=3, label='Площадь под PR кривой = %0.3f)' % prc_auc_score_f)
    
    plt.xlim([-.05, 1.05])
    plt.ylim([-.05, 1.0])
    plt.xlabel('Полнота \n Recall = TP/P')    
    plt.ylabel('Точность \n Precision = TP/(TP+FP)')
    
    plt.title('Precision-Recall кривая')
    plt.legend(loc="upper right")
    plt.show()
    return

def cross_val_score_visualize(d_name_metric, d_vec, d_value_metric, d_font_scale):
    '''Визуализирует кросс-валидацию
       Параметры:
       - d_name_metric- наименование метрики
       - d_vec - словарь - результат отработки функции cross_validate
       - d_value_metric - значение метрики без кросс-валидации для сравнения
       - d_font_scale - размер шрифта'''    
    num_folds = len(d_vec['train_score'])
    avg_metric_train, std_metric_train = d_vec['train_score'].mean(), d_vec['train_score'].std()
    avg_metric_test, std_metric_test = d_vec['test_score'].mean(), d_vec['test_score'].std()

    plt.style.use('seaborn-paper')
    sns.set(font_scale=d_font_scale)
    color_text = plt.get_cmap('PuBu')(0.85)

    plt.figure(figsize=(12, 6))
    plt.plot(d_vec['train_score'], label='тренировочные значения', marker='.', color= 'darkblue')
    plt.plot([0,num_folds-1], [avg_metric_train, avg_metric_train], color='blue', label='среднее трен. значений ', marker='.', lw=2, ls = '--')

    plt.plot(d_vec['test_score'], label='тестовые значения', marker='.', color= 'red')
    plt.plot([0,num_folds-1], [avg_metric_test, avg_metric_test], color='lightcoral', label='среднее тест. значений ', marker='.', lw=2, ls = '--')

    plt.plot([0,num_folds-1], [d_value_metric, d_value_metric], color='grey', label='значение метрики до CV', marker='.', lw=3)

    # plt.xlim([1, num_folds])
    y_max = max(avg_metric_train,avg_metric_test) + 1.5*max(std_metric_train,std_metric_test)
    y_min = min(avg_metric_train,avg_metric_test) - 3*max(std_metric_train,std_metric_test)
    plt.ylim([y_min, y_max])
    plt.xlabel('Номер фолда', fontsize=15, color = color_text)
    plt.ylabel(d_name_metric, fontsize=15, color = color_text)
    plt.title(f'Кросс-валидация по метрике {d_name_metric} на {num_folds} фолдах', color = color_text, fontsize=17)
    plt.legend(loc="lower right", fontsize=11)
    y_min_text = y_min +0.5*max(std_metric_train,std_metric_test)
    plt.text(0, y_min_text, f'{d_name_metric} на трейне = {round(avg_metric_train,3)} +/- {round(std_metric_train,3)} \n{d_name_metric} на тесте    = {round(avg_metric_test,3)} +/- {round(std_metric_test,3)} \n{d_name_metric} до CV        = {round(d_value_metric,3)}', fontsize = 15)
    plt.show()
    return  

def model_coef(d_columns, d_model_coef_0):
    '''Печатает коэффициенты при признаках в логистической регрессии
       Параметры:
       - d_columns - столбцы
       - d_model_coef_0 - коэффициенты'''
    temp_dict = {}
    temp_dict['имя признака'] = d_columns
    temp_dict['коэффициент модели'] = d_model_coef_0
    temp_dict['модуль коэф'] = abs(temp_dict['коэффициент модели'])
    temp_df = pd.DataFrame.from_dict(temp_dict, orient='columns')
    temp_df = temp_df.sort_values(by='модуль коэф', ascending=False)
    temp_df.reset_index(drop=True,inplace=True)
    
    return temp_df.loc[:,['имя признака','коэффициент модели']]


if __name__ == "__main__":
    print('This is the Main program')