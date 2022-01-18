# Databricks notebook source
dbutils.widgets.get("myparam")
p = getArgument("myparam")
print ("Param -\'myparam':")
print (p)

dbutils.widgets.get("input")
i = getArgument("input")
print ("Param -\'input':")
print (i)

dbutils.widgets.get("output")
o = getArgument("output")
print ("Param -\'output':")
print (o)

n = i + "/testdata.txt"
df = spark.read.csv(n)

display (df)

data = [('value1', 'value2')]
df2 = spark.createDataFrame(data)

z = o + "/output.txt"
df2.write.csv(z)
