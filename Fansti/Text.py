import zipfile
file_name="E:\\A.txt"
file_name2="E:\\b.txt"
f = zipfile.ZipFile('E:\\test.zip','w',zipfile.ZIP_STORED)
f.write(file_name)
f.write(file_name2)
f.close()
