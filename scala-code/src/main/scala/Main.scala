package simple
import org.apache.spark.rdd.RDD
import org.apache.spark.sql.functions.{col, explode, max, when, concat, lit}
import org.apache.spark.sql.types._
import org.apache.spark.sql.{DataFrame, Row, SQLContext, SparkSession}
import org.apache.spark.sql.expressions.UserDefinedFunction
import org.apache.spark.sql.functions.udf


class MyScalaClass(sqlContext: SQLContext, df: DataFrame) {
  import sqlContext.implicits._
  import org.apache.spark.sql.functions._

  def myScalaFunction(column: String): DataFrame = {
    df.withColumn(column, concat(col(column), lit(" was processed by Scala function.")))
  }
}

object MyScalaObject {
  def myScalaUDF(): UserDefinedFunction = {
    udf((value: Double) => {
      value * 2
    })
  }
}