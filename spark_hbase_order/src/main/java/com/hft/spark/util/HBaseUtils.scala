package com.hft.spark.util
//import org.apache.hadoop.conf.Configuration
//
//import org.apache.hadoop.hbase.client.BufferedMutator.ExceptionListener
//
//import org.apache.hadoop.hbase.client._
//
//import org.apache.hadoop.hbase.io.ImmutableBytesWritable
//
//import org.apache.hadoop.hbase.protobuf.ProtobufUtil
//
//import org.apache.hadoop.hbase.util.{Base64, Bytes}
//
//import org.apache.hadoop.hbase.{HBaseConfiguration, HColumnDescriptor, HTableDescriptor, TableName}
//
//import org.apache.hadoop.mapred.JobConf
//
//import org.apache.hadoop.mapreduce.Job
//
//import org.apache.spark.SparkContext
//
//import org.slf4j.LoggerFactory

/**
  *
  * @author : kai.wu
  */
object HBaseUtils {

//  private val LOGGER = LoggerFactory.getLogger(this.getClass)
//
//  private var connection:Connection = _
//
//  private var conf:Configuration = _
//
//
//
//  def init(): Unit = {
//
//    conf = HBaseConfiguration.create()
//
//    conf.set("hbase.zookeeper.quorum", "lee")
//
//    connection = ConnectionFactory.createConnection(conf)
//
//  }
//
//
//
//  def getJobConf(tableName:String): JobConf = {
//
//    val conf = HBaseConfiguration.create()
//
//    val jobConf = new JobConf(conf)
//
//    jobConf.set("hbase.zookeeper.quorum", "lee")
//
//    jobConf.set("hbase.zookeeper.property.clientPort", "2181")
//
//    jobConf.set(org.apache.hadoop.hbase.mapred.TableOutputFormat.OUTPUT_TABLE,tableName)
//
//    jobConf.setOutputFormat(classOf[org.apache.hadoop.hbase.mapred.TableOutputFormat])
//
//    jobConf
//
//  }
//
//
//
//  def getNewConf(tableName:String): Configuration = {
//
//    conf = HBaseConfiguration.create()
//
//    conf.set("hbase.zookeeper.quorum", "master01")
//
//    conf.set("hbase.zookeeper.property.clientPort", "2181")
//
//    conf.set(org.apache.hadoop.hbase.mapreduce.TableInputFormat.INPUT_TABLE,tableName)
//
//    val scan = new Scan()
//
//    conf.set(org.apache.hadoop.hbase.mapreduce.TableInputFormat.SCAN,Base64.encodeBytes(ProtobufUtil.toScan(scan).toByteArray))
//
//    conf
//
//  }
//
//
//
//  private def getNewJobConf(tableName:String) = {
//
//    val conf = HBaseConfiguration.create()
//    conf.set("hbase.zookeeper.quorum", "master01")
//    conf.set("hbase.zookeeper.property.clientPort", "2181")
//    conf.set("hbase.defaults.for.version.skip", "true")
//    conf.set(org.apache.hadoop.hbase.mapreduce.TableOutputFormat.OUTPUT_TABLE, tableName)
//    conf.setClass("mapreduce.job.outputformat.class", classOf[org.apache.hadoop.hbase.mapreduce.TableOutputFormat[String]],
//      classOf[org.apache.hadoop.mapreduce.OutputFormat[String, Mutation]])
//    new JobConf(conf)
//  }
//
//
//
//  def closeConnection(): Unit = {
//
//    connection.close()
//
//  }
//
//  def getGetAction(rowKey: String):Get = {
//
//    val getAction = new Get(Bytes.toBytes(rowKey))
//
//    getAction.setCacheBlocks(false)
//
//    getAction
//
//  }
//
//
//
//  def getPutAction(rowKey: String, familyName:String, column: Array[String], value: Array[String]):Put = {
//
//    val put: Put = new Put(Bytes.toBytes(rowKey))
//
//    for (i <- column.indices) {
//      put.addColumn(Bytes.toBytes(familyName), Bytes.toBytes(column(i)), Bytes.toBytes(value(i)))
//    }
//
//    put
//
//  }
//
//
//
//  private def insertData(tableName:String, put: Put): Unit = {
//
//    val name = TableName.valueOf(tableName)
//
//    val table = connection.getTable(name)
//
//    table.put(put)
//
//  }
//
//
//
//  def addDataBatchEx(tableName:String, puts:java.util.List[Put]): Unit = {
//
//    val name = TableName.valueOf(tableName)
//
//    val table = connection.getTable(name)
//
//    val listener = new ExceptionListener {
//
//      override def onException(e: RetriesExhaustedWithDetailsException, bufferedMutator: BufferedMutator): Unit = {
//
//        for(i <-0 until e.getNumExceptions){
//
//          LOGGER.info("写入put失败:" + e.getRow(i))
//
//        }
//
//      }
//
//    }
//
//    val params = new BufferedMutatorParams(name)
//
//      .listener(listener)
//
//      .writeBufferSize(4*1024*1024)
//
//    try{
//
//      val mutator = connection.getBufferedMutator(params)
//
//      mutator.mutate(puts)
//
//      mutator.close()
//
//    }catch {
//
//      case e:Throwable => e.printStackTrace()
//
//    }
//
//  }

}
