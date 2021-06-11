import subprocess,os

def copyToHdfs(fileName,hdfsDir,hdfsName):
    """ копирует файл в HDFS "таблицу" или удаляет директорию, перенаправляет протоколы, проверяет результат """
    stdErr = open('hdfs_stderr.txt','w')
    stdOut = open('hdfs_stdout.txt','w')
    if hdfsName: # если имя файла есть - копируем
        print("Copying", fileName, "into HDFS...")
        res = subprocess.run(["hdfs","dfs","-mkdir","-p",hdfsDir],stderr=stdErr,stdout=stdOut) 
    else: # иначе - удаляем директорию
        print("Deleting", hdfsDir, "from HDFS...")
        res = subprocess.run(["hdfs","dfs","-rm","-r","-f","-skipTrash",hdfsDir],stderr=stdErr,stdout=stdOut) 
    stdOut.close()
    stdErr.close()
    if res.returncode!=0:
        raise(subprocess.SubprocessError("There were errors while working with dir, check hdfs_stderr.txt"))
    if not hdfsName: # для удаления директории - все сделали, возвращаемся
        print("Done")
        return
    stdErr = open('hdfs_stderr.txt','w')
    stdOut = open('hdfs_stdout.txt','w')
    res = subprocess.run(["hdfs","dfs","-put","-f",fileName,hdfsDir+"/"+hdfsName],stderr=stdErr,stdout=stdOut) 
    stdOut.close()
    stdErr.close()
    if res.returncode!=0:
        raise(subprocess.SubprocessError("There were errors while copying, check hdfs_stderr.txt"))
    print("Done")

fileName = "/home/deng/Data/names.txt"
tabName = "names"
dbName = "mk_test"
hiveTab = dbName + "." + tabName

copyToHdfs(fileName,"/tmp/"+tabName,"data.txt")
execHiveCmd("create external table " +
    hiveTab + " ( id int, name string ) row format delimited fields terminated by ';' location '/tmp/" + tabName + "'")
execHiveCmd("create table "+hiveTab+"_orc stored as ORC as select * from "+hiveTab)
execHiveCmd("drop table " + hiveTab + " purge")
copyToHdfs(fileName,"/tmp/"+tabName,None)
