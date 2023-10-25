name := "MyScalaClass"

version := "2.0"

scalaVersion := "2.12.11"

libraryDependencies += "org.apache.spark" % "spark-core_2.12" % "3.1.1"
libraryDependencies += "org.apache.spark" % "spark-sql_2.12" % "3.1.1"
// for debugging sbt problems
logLevel := Level.Debug

scalacOptions += "-deprecation"
