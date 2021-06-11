import subprocess,os

def sqoopImport(tabName,dbName='default'):
    """ запускает sqoop, перенаправляет протоколы, проверяет результат """
    print("Importing", tabName, "table into database", dbName, "with sqoop import...")
    stdErr = open('sqoop_stderr.txt','w')
    stdOut = open('sqoop_stdout.txt','w')
    subprocess.run(["hdfs","dfs","-rm","-r","-f","-skipTrash",tabName],stderr=stdErr,stdout=stdOut) 
    os.environ['JAVA_HOME'] = "/usr"
    args = [
        '/usr/lib/sqoop/bin/sqoop',
        'import',
        '--connect', 'jdbc:mysql://10.93.1.9/skillfactory',
        '--username', 'mysql',
        '--password', 'arenadata',
        '--hive-import',
        '-m', '1',
        '--table', tabName,
        '--hive-table', dbName+"."+tabName
    ]
    res = subprocess.run(args,stderr=stdErr,stdout=stdOut)
    stdOut.close()
    stdErr.close()
    if res.returncode!=0:
        raise(subprocess.SubprocessError("There were errors while sqooping, check sqoop_stderr.txt"))
    print("Done")

def execHiveCmd(sql):
    """ выполянет команду Hive, перенаправляет вывод, проверяет результат """
    print("Executing Hive QL command:", sql, "...")
    cmdFile = open("/tmp/sql.txt","w")
    cmdFile.write("!connect  jdbc:hive2://10.93.1.9:10000 hive eee;\n")
    cmdFile.write(sql + ";")
    cmdFile.close()
    args = [
        'beeline',
        '-f',
        '/tmp/sql.txt'
    ]
    stdErr = open('hive_stderr.txt','w')
    stdOut = open('hive_stdout.txt','w')
    res = subprocess.run(args,stderr=stdErr,stdout=stdOut)
    stdOut.close()
    stdErr.close()
    if res.returncode!=0:
        raise(subprocess.SubprocessError("There were errors while hive-ing, check hive_stderr.txt"))
    print("Done")

tabName = "phones"
dbName = "mk_test"
hiveTab = dbName + "." + tabName

sqoopImport(tabName,dbName)
execHiveCmd("drop table if exists "+hiveTab+"_orc purge")
execHiveCmd("create table "+hiveTab+"_orc stored as ORC as select * from "+hiveTab)
execHiveCmd("drop table " + hiveTab + " purge")

