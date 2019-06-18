package com.hft.spark.hBaseCore

import org.apache.hadoop.conf.Configuration
import org.apache.hadoop.hbase.HBaseConfiguration
import org.apache.hadoop.hbase.mapreduce.TableInputFormat
import org.apache.hadoop.hbase.util.Bytes
import org.apache.spark.{SparkConf, SparkContext}

/**
  *
  * @author : kai.wu
  */
object HBaseReadScala {
  def main(args: Array[String]): Unit = {
    val tableName = "usmile:order"
    val sparkConf = new SparkConf()

      .setMaster("local")
      .setAppName("HBaseRead")
    val sc = new SparkContext(sparkConf)

    val conf = HBaseConfiguration.create()
    conf.set("hbase.zookeeper.property.clientPort", "2181")
    conf.set("hbase.zookeeper.quorum", "master01")
    conf.set(TableInputFormat.INPUT_TABLE, tableName)
    conf.set(TableInputFormat.SCAN_ROW_STOP, "1101")

    val hBaseRDD = sc.newAPIHadoopRDD(conf, classOf[TableInputFormat],
      classOf[org.apache.hadoop.hbase.io.ImmutableBytesWritable],
      classOf[org.apache.hadoop.hbase.client.Result])

    hBaseRDD.map(tuple => tuple._1).map(item => Bytes.toString(item.get())).foreach(println)
    val resultRDD = hBaseRDD.map(tuple => tuple._2)

    val keyValueRDD = resultRDD.map(result => (Bytes.toString(result.getRow), Bytes.toString(result.value())))
    keyValueRDD.foreach(x => println(x._1 + ":" + x._2))
//    hBaseRDD.map(tuple => tuple._2).map(Result => Result.getColumnCells(Bytes.toBytes("data"), Bytes.toBytes("data"))).foreach(println)

    resultRDD.map(result => {
      (Bytes.toString(result.getRow), result.getColumnCells(Bytes.toBytes("data"), Bytes.toBytes("rst")))
    }).foreach(println)

    print(1234567)
    keyValueRDD.groupByKey().mapValues(println)


//    val connection = ConnectionFactory.createConnection(conf)
//
//    val scan = new Scan()
//    scan.setStopRow(Bytes.toBytes("0001_15556788217221000399"))


    sc.stop()
  }
}

