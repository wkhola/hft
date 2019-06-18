package com.hft.spark.hBaseCore;

import org.apache.spark.SparkContext;
import org.apache.spark.sql.SparkSession;
import org.slf4j.Logger;

/**
 * @author : kai.wu
 * @date : 2019/5/7
 */
public class HBaseRead {
    public static void main(String[] args) {
        SparkSession sparkSession = SparkSession
                .builder()
                .master("local")
                .appName("hive")
                .config("spark.driver.memory","2147480000")
                .enableHiveSupport()
                .getOrCreate();
        Logger log = sparkSession.log();

        log.info("print local");
        System.out.println(123);
    }
}
